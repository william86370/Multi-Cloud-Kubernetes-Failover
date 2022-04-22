#1.) 
3 different applications make up the operator
The operator is a container that runs inside the Kubernetes cluster

# Cloudwatch-operator
# cloudwatch-dashboard
# cloudwatch-healthcheck
# cloudwatch-healthcheck-init

Nodes 
https://rancher.lootbot.cloud/dashboard/c/c-m-rh4fgbjl/explorer/node 

aws node 
https://rancher.lootbot.cloud/dashboard/c/c-m-rh4fgbjl/explorer/node/i-0b8e598b59f057de7#pods

azure node 
https://rancher.lootbot.cloud/dashboard/c/c-m-rh4fgbjl/explorer/node/azure-worker#pods

2.) Operator ./Operator/operator.py 
https://rancher.lootbot.cloud/dashboard/c/c-m-rh4fgbjl/explorer/apps.deployment/cloudwatch/cloudwatch-operator#pods 
deploys healthcheck daemon 
deploys dashboard 

Healthcheck daemonset 
https://rancher.lootbot.cloud/dashboard/c/c-m-rh4fgbjl/explorer/apps.daemonset/cloudwatch/cloudwatch-healthcheck#pods

3.) Service Overview 
https://rancher.lootbot.cloud/dashboard/c/c-m-rh4fgbjl/explorer/service

Healthcheck API Endpoints 
exec pod 
kubectl --namespace cloudwatch get pods
export KUBECONFIG=/home/wawright/workspace/Multi-Cloud-Kubernetes-Failover/Demo/kubeconfig
kubectl exec -n cloudwatch --stdin --tty exec-pod -- /bin/bash

# Aws node i-0b8e598b59f057de7
curl http://cloudwatch-healthcheck-i-0b8e598b59f057de7:8080

# aws node 	ip-172-31-22-83
curl http://cloudwatch-healthcheck-ip-172-31-22-83:8080

3.) 
Dashboard Deployment in Cluster 
https://rancher.lootbot.cloud/dashboard/c/c-m-rh4fgbjl/explorer/apps.deployment/cloudwatch/cloudwatch-dashboard#pods
https://demo-cloudwatch.lootbot.cloud/ 

4.) namespace annotations 
 https://demo-cloudwatch.lootbot.cloud/api/v1/cloudwatch/healthcheck
 https://demo-cloudwatch.lootbot.cloud/api/v1/cloudwatch/namespace
 https://demo-cloudwatch.lootbot.cloud/api/v1/cluster/status