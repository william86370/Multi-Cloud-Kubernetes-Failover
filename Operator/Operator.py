# Cloudwatch Operator watches for changes in the state of the cluster connection and starts the appropriate services
# if the cluster is connected or disconnected from the cloud and the cluster is not already running in the desired
# state (i.e. running or stopped)
import os

from kubernetes import client, config


def main():
    # Check if the Operator is in development mode
    # If it is in development mode, it will use the local kubernetes cluster
    if "DEVELOPMENT" in os.environ:
        config.load_kube_config()
    else:
        config.load_incluster_config()

    # Create a client to the kubernetes API
    v1 = client.CoreV1Api()

    print("Creating a new deployment...")
    # Create a deployment
    create_pod("deployment", "alpine", ["/bin/sh", "-c", "echo Hello World"], "default")
    print("Created deployment")
    ret = v1.list_namespaced_pod(namespace="default")
    for i in ret.items:
        print("%s  %s  %s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
    print("Deleting deployment...")
    # Delete the deployment
    delete_pod("deployment", "default")


def create_pod(name, image, command, namespace):
    # Create a pod with the given name, image, command, and namespace
    v1 = client.CoreV1Api()
    pod = client.V1Pod(
        metadata=client.V1ObjectMeta(name=name),
        spec=client.V1PodSpec(containers=[client.V1Container(name=name, image=image, command=command)]))
    v1.create_namespaced_pod(namespace=namespace, body=pod)
    return pod


def delete_pod(name, namespace):
    # Delete a pod
    v1 = client.CoreV1Api()
    v1.delete_namespaced_pod(name=name, namespace=namespace, body=client.V1DeleteOptions())


class CloudwatchOperator:
    def __init__(self):
        # This function is called when the operator starts up
        print("Cloudwatch Operator starting up...")
        self.v1 = client.CoreV1Api()
        # get the current namespace
        self.namespace = self.v1.list_namespace().items[0].metadata.name

    def check_operator_status(self):
        # This function is called when the operator is checking the cluster status
        print("Performing Operator status check...")
        # get all the pods in the current namespace
        pods = self.v1.list_namespaced_pod(namespace=self.namespace).items
        # get the number of nodes in the cluster
        nodes = self.v1.list_node().items
        # get the number of pods in the cluster
        pod_count = len(pods)
        print("Number of pods in the cluster: " + str(pod_count))
        # get the number of nodes in the cluster
        node_count = len(nodes)
        print("Number of nodes in the cluster: " + str(node_count))
        # get the status of the deamonset
        daemonset_status = self.v1.read_namespaced_daemon_set_status(name="cloudwatch agent", namespace=self.namespace)


if __name__ == '__main__':
    main()
