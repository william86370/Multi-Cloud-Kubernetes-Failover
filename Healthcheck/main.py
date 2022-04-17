# Developed by William Wright for Senior Project at Capitol Technology University
# Cloudwatch Healthcheck Daemon
# Author: William Wright
# Date: 2022-04-17
# Version: 1.0
# Description:
# The Daemon runs on each of the nodes in the cluster and checks the health of the node.
# The Daemon will expose a REST API to the operator to pull the information from the node.
import json

from flask import Flask
import os
from kubernetes import client, config
import colorama
from colorama import Fore
from colorama import init

global pod_name
global pod_namespace
global pod_ip
global pod_serviceaccount
global node_name
global cloud_provider
global v1_api
global port

# Colored output Messages WARNING, ERROR, INFO
init(autoreset=True)


def print_warning(message):
    print(Fore.YELLOW + message)
    return


def print_error(message):
    print(Fore.RED + message)
    return


def print_info(message):
    print(Fore.GREEN + message)
    return


app = Flask(__name__)


@app.route("/")
def default():
    global pod_name
    global pod_namespace
    global pod_serviceaccount
    global node_name
    global cloud_provider
    print_info("[INFO] Processing Healthcheck...")
    information = {
        "pod_name": pod_name,
        "pod_namespace": pod_namespace,
        "pod_serviceaccount": pod_serviceaccount,
        "node_name": node_name,
        "cloud_provider": cloud_provider,
        "cloud_provider_status": "OK",
    }
    return information


def get_cloudprovider_from_node():
    global cloud_provider
    global v1_api
    global node_name
    print_info("[INFO] Getting cloud provider from KubeAPI")
    node = v1_api.read_node(node_name)
    cloud_provider = node.metadata.labels['cloudwatch/provider']
    print_info("Cloud Provider: " + cloud_provider)
    return cloud_provider


def create_service():
    global pod_name
    global pod_namespace
    global pod_serviceaccount
    global node_name
    global cloud_provider
    global v1_api
    global port
    print_info("[INFO] Creating Service")
    print("------------------------------------------------------")
    service_name = "cloudwatch-healthcheck-" + node_name
    body = client.V1Service(
        api_version="v1",
        kind="Service",
        metadata=client.V1ObjectMeta(name=service_name),
        spec=client.V1ServiceSpec(
            type="ClusterIP",
            selector={"cloudwatch.daemon.node": node_name},
            ports=[client.V1ServicePort(
                port=port,
                target_port=port
            )]
        )
    )
    v1_api.create_namespaced_service(namespace=pod_namespace, body=body)
    print_info("[INFO] Service Created")
    print("------------------------------------------------------")
    return


def add_pod_label():
    # Add label to pod
    global pod_name
    global pod_namespace
    global pod_serviceaccount
    global node_name
    global cloud_provider
    global v1_api
    print_info("[INFO] Adding Label to Pod")
    print("------------------------------------------------------")
    body = {
        "metadata": {
            "labels": {
                "cloudwatch.daemon.node": node_name}
        }
    }
    v1_api.patch_namespaced_pod(pod_name, pod_namespace, body)
    print_info("[INFO] Label Added")
    print("------------------------------------------------------")
    return


def remove_prev_service():
    global pod_name
    global pod_namespace
    global pod_serviceaccount
    global node_name
    global cloud_provider
    global v1_api
    # This Function will create a service for the node to be able to communicate with the operator
    print_info("[INFO] Creating Service for Healthcheck on Node " + node_name)
    print("------------------------------------------------------")
    # Check if the service already exists
    print_info("[INFO] Checking if service already exists")
    service_name = "cloudwatch-healthcheck-" + node_name
    services = v1_api.list_namespaced_service(namespace=pod_namespace)
    for service in services.items:
        if service.metadata.name == service_name:
            print_info("[INFO] Service already exists")
            # print_info("[INFO] Deleting Service")
            # v1_api.delete_namespaced_service(name=service_name, namespace=pod_namespace)
            # print_info("[INFO] Service Deleted")
            print("------------------------------------------------------")
            return
    print_info("[INFO] Service does not exist")
    # Create the new service
    create_service()
    print("------------------------------------------------------")
    return


if __name__ == "__main__":
    global pod_name
    global pod_namespace
    global pod_serviceaccount
    global node_name
    global cloud_provider
    global v1_api
    global port
    # Check if the Operator is in development mode
    # If it is in development mode, it will use the local kubernetes cluster
    print_info("[INFO] Starting Cloudwatch Daemonset V1.0")
    print("Developed by William Wright for Senior Project at Capitol Technology University")

    if os.environ.get('CLOUDWATCH_OPERATOR_DEVELOPMENT_MODE') == 'true':
        print_warning("[DEV] Running in development mode")
        # Check for mounted kubeconfig file in development mode
        if os.path.exists("/app/kubeconfig"):
            print_info("[DEV] Loading kubeconfig file from /app/kubeconfig")
            config.load_kube_config(config_file="/app/kubeconfig")
        else:
            print_info("[DEV] Loading kubeconfig file from default location")
            config.load_kube_config()
    else:
        # Production mode
        print_info("[INFO] Production mode detected")
        # Load Kubeconfig from running Cluster
        try:
            config.load_incluster_config()
            # This is a production cluster
            print_info("[INFO] Running in cluster")
        except config.config_exception.ConfigException:
            print_error("[Error] Failed to load kubeconfig from Service Account")
            print_error("[Error] Please ensure the Service Account has the correct permissions")
            print_error("[Error] Exiting...")
            exit(1)

    # Cluster will be loaded by now
    v1_api = client.CoreV1Api()
    print_info("[INFO] KubeAPI Successfully Connected to Cluster")
    # Get the current Pod name and namespace
    try:
        pod_serviceaccount = os.environ['POD_SERVICEACCOUNT']
        pod_name = os.environ['POD_NAME']
        pod_namespace = os.environ['POD_NAMESPACE']
        node_name = os.environ['NODE_NAME']

        print("-------------------------------------------------------")
        print(f"Pod Name: {pod_name}")
        print(f"Pod Namespace: {pod_namespace}")
        print(f"Pod Service Account: {pod_serviceaccount}")
        print(f"Node Name: {node_name}")
        print("-------------------------------------------------------")
    except KeyError:
        print_error("[Error] Unable to get Pod information from environment variables")
        print_error("[Error] This is likely due to the Operator not being run as a Pod")
        print_error("[Error] Exiting...")
        exit(1)
    # Using the Node name, get the Cloud Provider from labels
    get_cloudprovider_from_node()

    port = int(os.getenv("PORT", 8080))
    # Add node to pod as a label
    add_pod_label()
    # Remove the old service
    remove_prev_service()
    # Create the new DaemonSet
    print_info(f"Starting Healthcheck daemon on port {port}")
    app.run(host='0.0.0.0', port=port)
