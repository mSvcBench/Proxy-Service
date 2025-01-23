#!/bin/bash


if [ "$1" == "apply" ]; then
    echo ":: Deploying the sock-shop application."
    echo ":: kubectl apply -f manifest/sock-shop_namespace.yaml"
    kubectl apply -f manifest/sock-shop_namespace.yaml

    echo ":: kubectl apply -f manifest/base"
    kubectl apply -f manifest/base

    echo ":: kubectl apply -f destination_rule/least_request.yaml ---------> LEAST REQUEST"
    kubectl apply -f destination_rule/least_request.yaml

    echo ""
    echo "When all the deploymets are ready, register the users before load testing sock-shop."
    
elif [ "$1" == "scale" ]; then
    echo ":: Scaling the sock-shop application."
    set -x
    kubectl scale deployment carts --replicas=8
    kubectl scale deployment carts-db --replicas=1
    kubectl scale deployment catalogue --replicas=5
    kubectl scale deployment catalogue-db --replicas=1
    kubectl scale deployment front-end --replicas=30
    kubectl scale deployment orders --replicas=7
    kubectl scale deployment orders-db --replicas=1
    kubectl scale deployment payment --replicas=5
    kubectl scale deployment queue-master --replicas=10
    kubectl scale deployment rabbitmq --replicas=5
    kubectl scale deployment session-db --replicas=1
    kubectl scale deployment shipping --replicas=10
    kubectl scale deployment user --replicas=9
    kubectl scale deployment user-db --replicas=1

elif [ "$1" == "proxy-service" ]; then
    echo ":: Replacing the original services with the proxy-services ones."
    set -x
    kubectl delete svc carts
    kubectl apply -f manifest/proxyservice_overwrite/carts.yaml
    kubectl delete svc catalogue
    kubectl apply -f manifest/proxyservice_overwrite/catalogue.yaml
    kubectl delete svc orders
    kubectl apply -f manifest/proxyservice_overwrite/orders.yaml
    kubectl delete svc payment
    kubectl apply -f manifest/proxyservice_overwrite/payment.yaml
    kubectl delete svc queue-master
    kubectl apply -f manifest/proxyservice_overwrite/queue-master.yaml
    kubectl delete svc shipping
    kubectl apply -f manifest/proxyservice_overwrite/shipping.yaml
    kubectl delete svc user
    kubectl apply -f manifest/proxyservice_overwrite/user.yaml

elif [ "$1" == "ps-delete" ]; then
    echo ":: Deleting the proxy-service replacing it with the original services."
    set -x
    kubectl delete -f manifest/proxyservice_overwrite/carts.yaml
    kubectl apply -f manifest/base_svc/carts.yaml
    kubectl delete -f manifest/proxyservice_overwrite/catalogue.yaml
    kubectl apply -f manifest/base_svc/catalogue.yaml
    kubectl delete -f manifest/proxyservice_overwrite/orders.yaml
    kubectl apply -f manifest/base_svc/orders.yaml
    kubectl delete -f manifest/proxyservice_overwrite/payment.yaml
    kubectl apply -f manifest/base_svc/payment.yaml
    kubectl delete -f manifest/proxyservice_overwrite/queue-master.yaml
    kubectl apply -f manifest/base_svc/queue-master.yaml
    kubectl delete -f manifest/proxyservice_overwrite/shipping.yaml
    kubectl apply -f manifest/base_svc/shipping.yaml
    kubectl delete -f manifest/proxyservice_overwrite/user.yaml
    kubectl apply -f manifest/base_svc/user.yaml

elif [ "$1" == "delete" ]; then
    echo ":: Deleting the sock-shop application and namespace."
    set -x
    kubectl delete -f manifest/base
    kubectl delete -f destination_rule/random.yaml
    kubectl delete -f manifest/proxyservice_overwrite
    kubectl delete -f manifest/sock-shop_namespace.yaml
else
    echo ":: Usage -> 'bash $0 apply|scale|proxy-service|ps-delete|delete'"
fi