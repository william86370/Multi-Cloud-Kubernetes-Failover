# Developed by William Wright for Senior Project at Capitol Technology University
# Cloudwatch Healthcheck INIT configuration
# Author: William Wright
# Date: 2022-04-17
# Version: 1.0
# Description:
# INIT Runs before the main healthcheck container starts.
# This will check the cloud provider and annotate the node with the cloud provider.

import os
import requests
from kubernetes import client, config
import colorama
from colorama import Fore
from colorama import init


def get_cloud_provider():
    # Get the cloud provider from IMDSv2
    # https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-instance-identity-id.html

    # Check if cloud provider is AWS
    path = 'latest/dynamic/instance-identity/document'
    url = f'http://169.254.169.254/{path}'
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        # Check Availability Zone
        availability_zone = response.json()['availabilityZone']
        if availability_zone.startswith('us-east-'):
            return 'aws'
        else:
            return 'azure'
    else:
        return "self-hosted"


def annotate_node(node_name, cloud_provider):
    # Give the node a label with the cloud provider
    # https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.18/#v1-node-spec-template
    # Find the node by name and annotate it with the cloud provider
    v1 = client.CoreV1Api()
    node = v1.read_node(node_name)
    body = {
        "metadata": {
            "labels": {
                "cloudwatch/provider": cloud_provider}
        }
    }

    v1.patch_node(node_name, body)
    print(f'[INFO] Annotated node {node_name} with cloud provider {cloud_provider}')
    print("-------------------------------------------------------")
    print(f'Node: {node.metadata.name}')
    print(f'Cloud Provider: {cloud_provider}')
    print(f'Labels: {node.metadata.labels}')
    print(f'Annotations: {node.metadata.annotations}')
    print(f'Taints: {node.spec.taints}')
    print(f'Unschedulable: {node.spec.unschedulable}')
    print(f'Pod CIDR: {node.spec.pod_cidr}')
    print("-------------------------------------------------------")
    return


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


def main():
    # Check if the Operator is in development mode
    # If it is in development mode, it will use the local kubernetes cluster
    print_info("[INFO] Starting Cloudwatch Healthcheck init V1.0")
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

    # Cluster Should be loaded by now
    print("[INFO] Checking for cloud provider")
    # Get the Current Pod information from environment variables
    pod_name = os.environ['POD_NAME']
    pod_namespace = os.environ['POD_NAMESPACE']
    pod_ip = os.environ['POD_IP']
    pod_serviceaccount = os.environ['POD_SERVICEACCOUNT']
    node_name = os.environ['NODE_NAME']
    print("-------------------------------------------------------")
    print(f"Pod Name: {pod_name}")
    print(f"Pod Namespace: {pod_namespace}")
    print(f"Pod IP: {pod_ip}")
    print(f"Pod Service Account: {pod_serviceaccount}")
    print(f"Node Name: {node_name}")
    print("-------------------------------------------------------")
    # Get the cloud provider
    cloud_provider = get_cloud_provider()
    # Annotate the node with the cloud provider
    print("[INFO] Cloud provider: " + cloud_provider)
    # Annotate the current node with the cloud provider
    annotate_node(node_name, cloud_provider)
    print_info("[INFO] Cloudwatch Healthcheck init complete")


if __name__ == "__main__":
    main()
