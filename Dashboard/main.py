# Developed by William Wright for Senior Project at Capitol Technology University
# Cloudwatch Dashboard API
# Author: William Wright
# Date: 2022-04-17
# Version: 1.0
# Description: This is the main file for the Dashboard API.
# It is responsible for setting up the flask server and handling all requests.

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
    print_info("[INFO] Processing Dashboard...")
    information = {
        "cloud_provider_status": "OK",
    }
    return information


@app.route("/api/v1/cluster/status")
def cluster_status():
    # Get the cluster status
    global v1_api
    global cloud_provider
    global pod_name
    global pod_namespace
    global pod_serviceaccount
    print_info("[INFO] Processing Cluster Status...")
    RED = "FF0000FF"
    GREEN = "01BB00FF"
    INFO = {
        "cluster_health": "HEALTH_OK",
        "cluster_health_color": GREEN,
        "nodes_online": "0 Nodes",
        "nodes_online_color": RED,
        "failover_status": "Failover Ready",
        "failover_status_color": GREEN,
        "cloud_provider_aws": "0/2 Deployed",
        "cloud_provider_aws_color": RED,
        "cloud_provider_other": "0/2 Deployed",
        "cloud_provider_other_color": RED,
        "cloud_provider_azure": "0/2 Deployed",
        "cloud_provider_azure_color": RED,
        "cloudwatch_operator": "0/2 Deployed",
        "cloudwatch_operator_color": RED,
        "cloudwatch_dashboard": "0/2 Deployed",
        "cloudwatch_dashboard_color": RED,
        "cloudwatch_Healthcheck": "0/2 Deployed",
        "cloudwatch_Healthcheck_color": RED
    }
    return INFO


if __name__ == "__main__":
    global pod_name
    global pod_namespace
    global pod_serviceaccount
    global node_name
    global cloud_provider
    global v1_api
    global port
    # Check if the Dashboard is in development mode
    # If it is in development mode, it will use the local kubernetes cluster
    print_info("[INFO] Starting Cloudwatch Dashboard V1.0")
    print("Developed by William Wright for Senior Project at Capitol Technology University")

    if os.environ.get('CLOUDWATCH_OPERATOR_DEVELOPMENT_MODE') == 'true':
        print_warning("[DEV] Running in development mode")
        # Check for mounted kubeconfig file in development mode
        if os.path.exists("./kubeconfig"):
            print_info("[DEV] Loading kubeconfig file from ./kubeconfig")
            config.load_kube_config(config_file="./kubeconfig")
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
    # if not in development mode
    if os.environ.get('CLOUDWATCH_OPERATOR_DEVELOPMENT_MODE') != 'true':
        try:
            pod_serviceaccount = os.environ['POD_SERVICEACCOUNT']
            pod_name = os.environ['POD_NAME']
            pod_namespace = os.environ['POD_NAMESPACE']

            print("-------------------------------------------------------")
            print(f"Pod Name: {pod_name}")
            print(f"Pod Namespace: {pod_namespace}")
            print(f"Pod Service Account: {pod_serviceaccount}")
            print("-------------------------------------------------------")
        except KeyError:
            print_error("[Error] Unable to get Pod information from environment variables")
            print_error("[Error] This is likely due to the Operator not being run as a Pod")
            print_error("[Error] Exiting...")
            exit(1)
    else:
        print("-------------------------------------------------------")
        print("Running in development mode")
        pod_serviceaccount = "Development"
        pod_name = "Development"
        pod_namespace = "cloudwatch"
        print("-------------------------------------------------------")

    port = 28015
    print_info(f"Starting Dashboard on port {port}")
    app.run(host='0.0.0.0', port=port)
