# Sock-Shop testbed

This repository contains the testbed for the Sock-Shop microservices demo application.
Use `deploy_sock_shop.sh` for deploying it on a Kubernetes cluster.

```bash
Usage: deploy_sock_shop.sh apply|scale|proxy-service|ps-delete|delete

kubectl apply -f sock-shop_ingress.yaml # deploys istio ingress gateway
bash deploy_sock_shop.sh apply #to deploy sock-shop without the proxy-service
bash deploy_sock_shop.sh scale #to scale the sock-shop
bash deploy_sock_shop.sh proxy-service #to deploy the proxy-service without deleting the entire application, overwriting the existing services
bash deploy_sock_shop.sh ps-delete #to delete the proxy-service and replace it with the original sock-shop services
bash deploy_sock_shop.sh delete #to delete the entire sock-shop application

```
