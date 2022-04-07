# Cloudwatch Operator
# watches for changes in the state of the cluster connection and starts the appropriate services if the cluster is connected or disconnected from the cloud and the cluster is not already running in the desired state (i.e. running or stopped) 
from kubernetes import client, config

def main():
    config.load_kube_config()
    config.load_incluster_config()

    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        print("%s\t%s\t%s" %
              (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

if __name__ == '__main__':
    main()