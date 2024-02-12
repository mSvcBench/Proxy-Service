import kopf
import yaml
import pykube
import logging
import copy
from kubernetes import client, config
from kubernetes.client.rest import ApiException
import istio_definitions


# Create a logger object
logger = logging.getLogger(__name__)
yaml_istio_ingress = "./ingress.yaml"


@kopf.on.create('proxyservices')
def create_fn(body, spec, **kwargs):
    try:
        name = body['metadata']['name']
        k8s_resources = get_yaml(yaml_istio_ingress, body)
        config.load_incluster_config()
        api = pykube.HTTPClient(pykube.KubeConfig.from_env())

        for k8s_resource in k8s_resources:
            kopf.adopt(k8s_resource)
            logger.info(f"Creating {k8s_resource['kind']} for {name}")
            k8s_create(k8s_resource, api)
        
        create_istio_stuff(body, spec)

        api.session.close()
        return {'message': f'Created all proxy-services of {name}'}
    except Exception as err:
        logger.exception(f"Error creating proxy-service resource: {err}")


@kopf.on.delete('proxyservices')
def delete_fn(body, spec, **kwargs):
    try:
        name = body['metadata']['name']
        k8s_resources = get_yaml(yaml_istio_ingress, body)
        api = pykube.HTTPClient(pykube.KubeConfig.from_env())

        for k8s_resource in k8s_resources:
            logger.info(f"Deleting {k8s_resource['kind']} for {name}")
            k8s_delete(k8s_resource, api)

        delete_istio_stuff(body)
        api.session.close()
        return {'message': f'Deleted all proxyservices of {name}'}
    except Exception as err:
        logger.exception(f"Error deleting proxy-service resource: {err}")


def get_yaml(yaml_file, body):
    try: 
        with open(yaml_file, 'r') as file:
            f = file.read()
        
        f = f.replace('{{ my-ingress-name }}', body['metadata']['name'])
        f = f.replace('{{ my-service-name }}', body['spec']['serviceName'])
        f = f.replace('{{ namespace }}', body['metadata']['namespace'])
        f = f.replace('{{ port }}', str(body['spec']['port']))

        k8s_resources = yaml.safe_load_all(f)
    except Exception as err:
        logger.exception(f"Error reading YAML file: {err}")
    return k8s_resources


def k8s_create(k8s_resource, api):
    try: 
        if k8s_resource['kind'] == 'ServiceAccount':
            pykube.ServiceAccount(api, k8s_resource).create()
            logger.info("ServiceAccount created")
        elif k8s_resource['kind'] == 'Role':
            pykube.Role(api, k8s_resource).create()
            logger.info("Role created")
        elif k8s_resource['kind'] == 'RoleBinding':
            pykube.RoleBinding(api, k8s_resource).create()
            logger.info("RoleBinding created")
        elif k8s_resource['kind'] == 'Service':
            pykube.Service(api, k8s_resource).create()
            logger.info("Service created")
        elif k8s_resource['kind'] == 'Deployment':
            pykube.Deployment(api, k8s_resource).create()
            logger.info("Deployment created")
        elif k8s_resource['kind'] == 'HorizontalPodAutoscaler':
            pykube.HorizontalPodAutoscaler(api, k8s_resource).create()
            logger.info(" HorizontalPodAutoscaler")
        else:
            logger.error(f"Unknown kind: {k8s_resource['kind']}")
    except Exception as err:
        logger.exception(f"Error creating Kubernetes object {k8s_resource['kind']}: {err}")    


def k8s_delete(k8s_resource, api):
    try:
        if k8s_resource['kind'] == 'ServiceAccount':
            pykube.ServiceAccount(api, k8s_resource).delete()
            logger.info("ServiceAccount deleted")
        elif k8s_resource['kind'] == 'Role':
            pykube.Role(api, k8s_resource).delete()
            logger.info("Role deleted")
        elif k8s_resource['kind'] == 'RoleBinding':
            pykube.RoleBinding(api, k8s_resource).delete()
            logger.info("RoleBinding deleted")
        elif k8s_resource['kind'] == 'Service':
            pykube.Service(api, k8s_resource).delete()
            logger.info("Service deleted")
        elif k8s_resource['kind'] == 'Deployment':
            pykube.Deployment(api, k8s_resource).delete()
            logger.info("Deployment deleted")
        elif k8s_resource['kind'] == 'HorizontalPodAutoscaler':
            pykube.HorizontalPodAutoscaler(api, k8s_resource).delete()
            logger.info("HorizontalPodAutoscaler deleted")
        else:
            logger.error(f"Unknown kind: {k8s_resource['kind']}")
    except Exception as err:
        logger.exception(f"Error deleting Kubernetes object {k8s_resource['kind']}: {err}")


def create_istio_stuff(body, spec):
    try:
        name = body['metadata']['name']
        namespace = body['metadata']['namespace']
        target = spec.get('target')
        port = spec.get('port')
        if target == None:
            logger.exception("No spec.target specified in YAML")
            return
        if port == None:
            logger.exception("No spec.port specified in YAML")
            return
    
        config.load_incluster_config()
        api_instance = client.CustomObjectsApi()

        gateway = copy.deepcopy(istio_definitions.gateway)
        gateway['metadata']['name'] = f"{name}-gw"
        gateway['metadata']['namespace'] = namespace
        gateway['spec']['selector']['istio'] = name
        gateway['spec']['servers'][0]['hosts'][0] = "*"
        gateway['spec']['servers'][0]['port']['number'] = port

        # Edit custom fields for VirtualService
        virtual_service = copy.deepcopy(istio_definitions.virtual_service)
        virtual_service['metadata']['name'] = f"{name}-vs"
        virtual_service['metadata']['namespace'] = namespace
        virtual_service['spec']['gateways'][0] = f"{name}-gw"
        virtual_service['spec']['http'][0]['name'] = f"{name}-rewrite"
        if spec.get('uri') is not None:
            if spec.get('uri')['matchUriPrefix'] is not None:
                virtual_service['spec']['http'][0]['match'][0]['uri']['prefix'] = spec.get('uri')['matchUriPrefix']
            else:
                logger.exception("No spec.uri.matchUriPrefix specified in YAML")
            if spec.get('uri')['rewriteUri'] != None:
                virtual_service['spec']['http'][0]['rewrite']['uri'] = spec.get('uri')['rewriteUri']
            else:
                logger.exception("No spec.uri.rewriteUri specified in YAML")
        
        virtual_service['spec']['http'][0]['route'][0]['destination']['host'] = f"{target}.{namespace}.svc.cluster.local"
        virtual_service['spec']['http'][0]['route'][0]['destination']['port']['number'] = port
        virtual_service['spec']['http'][1]['name'] = f"{name}-default-route"
        virtual_service['spec']['http'][1]['route'][0]['destination']['host'] = f"{target}.{namespace}.svc.cluster.local"
        virtual_service['spec']['http'][1]['route'][0]['destination']['port']['number'] = port
        virtual_service['spec']['hosts'][0] = "*"
    
        # Edit custom fields for DestinationRule
        destination_rule = copy.deepcopy(istio_definitions.destination_rule)
        destination_rule['metadata']['name'] = f"{name}-dr"
        destination_rule['metadata']['namespace'] = namespace
        destination_rule['spec']['host'] = f"{target}"
        destination_rule['spec']['trafficPolicy']['loadBalancer']['simple'] = spec.get('loadBalancer')

        # Create Gateway
        api_instance.create_namespaced_custom_object(
            group="networking.istio.io",
            version="v1alpha3",
            namespace=namespace,
            plural="gateways",
            body=gateway
        )
        logger.info("Gateway created")

        # Create VirtualService
        api_instance.create_namespaced_custom_object(
            group="networking.istio.io",
            version="v1alpha3",
            namespace=namespace,
            plural="virtualservices",
            body=virtual_service
        )
        logger.info("VirtualService created")

        # Create DestinationRule
        api_instance.create_namespaced_custom_object(
            group="networking.istio.io",
            version="v1alpha3",
            namespace=namespace,
            plural="destinationrules",
            body=destination_rule
        )
        logger.info("DestinationRule created")

    except Exception as err:
        logger.exception(f"Error creating istio component: {err}")


def delete_istio_stuff(body):
    name = body['metadata']['name']
    namespace = body['metadata']['namespace']
    config.load_incluster_config()
    api_instance = client.CustomObjectsApi()

    try:
        # Delete Gateway
        api_instance.delete_namespaced_custom_object(
            group="networking.istio.io",
            version="v1alpha3",
            namespace=namespace,
            plural="gateways",
            name=f"{name}-gw"
        )
        logger.info("Gateway deleted")

        # Delete VirtualService
        api_instance.delete_namespaced_custom_object(
            group="networking.istio.io",
            version="v1alpha3",
            namespace=namespace,
            plural="virtualservices",
            name=f"{name}-vs"
        )
        logger.info("VirtualService deleted")

        # Delete DestinationRule
        api_instance.delete_namespaced_custom_object(
            group="networking.istio.io",
            version="v1alpha3",
            namespace=namespace,
            plural="destinationrules",
            name=f"{name}-dr"
        )
        logger.info("DestinationRule deleted")
    except Exception as err:
        logger.exception(f"Error deleting istio component: {err}")
