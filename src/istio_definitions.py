gateway = {
    "apiVersion": "networking.istio.io/v1alpha3",
    "kind": "Gateway",
    "metadata": {
        "name": "my-gateway",
        "namespace": "default"
    },
    "spec": {
        "selector": {
            "istio": "istio-label"
        },
        "servers": [
            {
                "port": {
                    "number": 80,
                    "name": "http",
                    "protocol": "HTTP"
                },
                "hosts": ["*"]
            }
        ]
    }
}

virtual_service = {
    "apiVersion": "networking.istio.io/v1alpha3",
    "kind": "VirtualService",
    "metadata": {
        "name": "my-virtual-service",
        "namespace": "default"
    },
    "spec": {
        "hosts": ["*"],
        "gateways": ["my-gateway"],
        "http": [
            {
                "name": "my-route",
                "match": [
                    {
                        "uri": {
                            "prefix": "/"
                        }
                    }
                ],
                "rewrite": {
                    "uri": "/"
                },
                "route": [
                    {
                        "destination": {
                            "host": "my-service",
                            "port": {
                                "number": 80
                            }
                        }
                    }
                ]
            },
            {
                "name": "my-default-route",
                "route": [
                    {
                        "destination": {
                            "host": "my-service",
                            "port": {
                                "number": 80
                            }
                        }
                    }
                ]
            }
        ]
    }
}

destination_rule = {
    "apiVersion": "networking.istio.io/v1alpha3",
    "kind": "DestinationRule",
    "metadata": {
        "name": "my-destination-rule",
        "namespace": "default"
    },
    "spec": {
        "host": "my-service",
        "trafficPolicy": {
            "loadBalancer": {
                "simple": "LEAST_REQUEST"
            }
        }
    }
}

