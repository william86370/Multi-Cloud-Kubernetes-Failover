# Developed by William Wright for Senior Project at Capitol Technology University
# Cloudwatch Dashboard API
# Author: William Wright
# Date: 2022-04-17
# Version: 1.0
# Description: This is the main file for the Dashboard API.
# It is responsible for setting up the flask server and handling all requests.

import json
from flask import Flask, render_template
# Add CORS support
from flask_cors import CORS, cross_origin

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
global v1_api_apps
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


def print_data(message):
    print(Fore.BLUE + message)
    return


RED = "#FF0000FF"
GREEN = "#01BB00FF"
YELLOW = "#FFFF00FF"
ORANGE = "#FF7F00FF"
PURPLE = "#FF00FFFF"
BLUE = "#0000FFFF"
WHITE = "#FFFFFFFF"

app = Flask(__name__)


@app.route("/")
def default():
    return render_template('Home.html')


def get_nodes_online():
    # Get the number of nodes online
    global v1_api
    # Get all of the required information from the kubernetes api using v1_api
    node_list = v1_api.list_node()
    node_count = 0
    node_ready = 0
    node_color = BLUE
    for node in node_list.items:
        node_count += 1
        # Get the node Status
        node_statuss = node.status.conditions
        for node_status in node_statuss:
            if node_status.type == "Ready":
                if node_status.status == "True":
                    node_ready += 1
                    print_info("[INFO] Node " + node.metadata.name + " is online")
                else:
                    print_warning("[WARN] Node " + node.metadata.name + " is offline")
    print_data("[DATA] Nodes Online: " + str(node_count))
    if node_count == node_ready:
        print_info("[INFO] All nodes are online")
        node_color = GREEN
    elif node_ready == 0:
        print_warning("[WARN] No nodes are online")
        node_color = RED
    else:
        print_warning("[WARN] Some nodes are offline")
        node_color = YELLOW
    node_count = str(node_ready) + "/" + str(node_count)
    return node_count, node_color


def get_cloud_providers():
    # Get the number of nodes online
    global v1_api
    # Get all of the required information from the kubernetes api using v1_api
    node_list = v1_api.list_node()
    cloud_provider_count_aws = [0, 0]
    cloud_provider_count_azure = [0, 0]
    cloud_provider_count_other = [0, 0]
    cloud_provider_color_aws = BLUE
    cloud_provider_color_azure = BLUE
    cloud_provider_color_other = BLUE

    for node in node_list.items:
        node_labels = node.metadata.labels
        # Check if the node is AWS
        if node_labels.get("cloudwatch/provider") == "aws":
            cloud_provider_count_aws[0] += 1
            print_info("[INFO] Node " + node.metadata.name + " is AWS")
        if node_labels.get("cloudwatch/provider") == "azure":
            cloud_provider_count_azure[0] += 1
            print_info("[INFO] Node " + node.metadata.name + " is Azure")
        if node_labels.get("cloudwatch/provider") == "self-hosted":
            cloud_provider_count_other[0] += 1
            print_info("[INFO] Node " + node.metadata.name + " is self-hosted")
        # Get the node Status
        node_statuss = node.status.conditions
        for node_status in node_statuss:
            if node_status.type == "Ready":
                if node_status.status == "True":
                    if node_labels.get("cloudwatch/provider") == "aws":
                        cloud_provider_count_aws[1] += 1
                    if node_labels.get("cloudwatch/provider") == "azure":
                        cloud_provider_count_azure[1] += 1
                    if node_labels.get("cloudwatch/provider") == "self-hosted":
                        cloud_provider_count_other[1] += 1

    if cloud_provider_count_aws[1] == 0:
        print_warning("[WARN] No AWS nodes are online")
        cloud_provider_color_aws = RED
    elif cloud_provider_count_aws[0] == cloud_provider_count_aws[1]:
        print_info("[INFO] All AWS nodes are online")
        cloud_provider_color_aws = GREEN
    else:
        print_warning("[WARN] Some AWS nodes are offline")
        cloud_provider_color_aws = YELLOW
    cloud_provider_count_aws = str(cloud_provider_count_aws[1]) + "/" + str(cloud_provider_count_aws[0]) + " Ready"

    if cloud_provider_count_azure[1] == 0:
        print_warning("[WARN] No Azure nodes are online")
        cloud_provider_color_azure = RED
    elif cloud_provider_count_azure[0] == cloud_provider_count_azure[1]:
        print_info("[INFO] All Azure nodes are online")
        cloud_provider_color_azure = GREEN
    else:
        print_warning("[WARN] Some Azure nodes are offline")
        cloud_provider_color_azure = YELLOW
    cloud_provider_count_azure = str(cloud_provider_count_azure[1]) + "/" + str(cloud_provider_count_azure[0]) + " Ready"

    if cloud_provider_count_other[1] == 0:
        print_warning("[WARN] No self-hosted nodes are online")
        cloud_provider_color_other = RED
    elif cloud_provider_count_other[0] == cloud_provider_count_other[1]:
        print_info("[INFO] All self-hosted nodes are online")
        cloud_provider_color_other = GREEN
    else:
        print_warning("[WARN] Some self-hosted nodes are offline")
        cloud_provider_color_other = YELLOW
    cloud_provider_count_other = str(cloud_provider_count_other[1]) + "/" + str(cloud_provider_count_other[0]) + " Ready"

    print_data("[DATA] AWS Nodes Ready: " + str(cloud_provider_count_aws))
    print_data("[DATA] AZURE Nodes Ready: " + str(cloud_provider_count_azure))
    print_data("[DATA] OTHER Nodes Ready: " + str(cloud_provider_count_other))

    return cloud_provider_color_aws, cloud_provider_color_azure, cloud_provider_color_other, cloud_provider_count_aws, cloud_provider_count_azure, cloud_provider_count_other


def get_deployment_status(deployment_name):
    global v1_api
    global pod_namespace
    global v1_api_apps
    deployment_status_color = RED
    deployment_status_count = [0, 0]
    deployments = v1_api_apps.list_namespaced_deployment(namespace=pod_namespace, label_selector="app=" + deployment_name)
    for deployment in deployments.items:
        deployment_status_count[0] += deployment.status.replicas
        deployment_status_count[1] += deployment.status.ready_replicas

    if deployment_status_count[1] == 0:
        print_warning("[WARN] No " + deployment_name + " replicas are ready")
        deployment_status_color = RED
    elif deployment_status_count[0] == deployment_status_count[1]:
        print_info("[INFO] All " + deployment_name + " replicas are ready")
        deployment_status_color = GREEN
    else:
        print_warning("[WARN] Some " + deployment_name + " replicas are not ready")
        deployment_status_color = YELLOW
    deployment_status_count = str(deployment_status_count[1]) + "/" + str(deployment_status_count[0]) + " Ready"
    print_data("[DATA] " + deployment_name + " Replicas Ready: " + str(deployment_status_count))
    return deployment_status_color, deployment_status_count


def get_daemon_status(daemon_name):
    global v1_api
    global pod_namespace
    daemon_status_color = RED
    daemon_status_count = [0, 0]

    daemons = v1_api_apps.list_namespaced_daemon_set(namespace=pod_namespace, label_selector="app=" + daemon_name)
    for daemon in daemons.items:
        daemon_status_count[0] += daemon.status.desired_number_scheduled
        daemon_status_count[1] += daemon.status.number_ready

    if daemon_status_count[0] == 0:
        print_warning("[WARN] No " + daemon_name + " daemons are ready")
        daemon_status_color = RED
    elif daemon_status_count[0] == daemon_status_count[1]:
        print_info("[INFO] All " + daemon_name + " daemons are ready")
        daemon_status_color = GREEN
    else:
        print_warning("[WARN] Some " + daemon_name + " daemons are not ready")
        daemon_status_color = YELLOW
    daemon_status_count = str(daemon_status_count[1]) + "/" + str(daemon_status_count[0]) + " Ready"
    print_data("[DATA] " + daemon_name + " Daemons Ready: " + str(daemon_status_count))
    return daemon_status_color, daemon_status_count


@app.route("/api/v1/cluster/status")
def cluster_status():
    # Get the cluster status
    global v1_api
    global cloud_provider
    global pod_name
    global pod_namespace
    global pod_serviceaccount

    # Get all of the required information from the kubernetes api using v1_api
    print("----------------------------------------------------")
    print_info("[INFO] Processing Cluster Status...")

    INFO = dict(cluster_health="HEALTH_OK", cluster_health_color=GREEN, nodes_online="0 Nodes", nodes_online_color=BLUE,
                failover_status="Failover Ready", failover_status_color=GREEN, cloud_provider_aws="0/2 Deployed",
                cloud_provider_aws_color=RED, cloud_provider_other="0/2 Deployed", cloud_provider_other_color=RED,
                cloud_provider_azure="0/2 Deployed", cloud_provider_azure_color=RED, cloudwatch_operator="0/2 Deployed",
                cloudwatch_operator_color=RED, cloudwatch_dashboard="0/2 Deployed", cloudwatch_dashboard_color=RED,
                cloudwatch_Healthcheck="0/2 Deployed", cloudwatch_Healthcheck_color=RED)

    node_online_infd = get_nodes_online()
    INFO["nodes_online"] = str(node_online_infd[0]) + " Nodes"
    INFO["nodes_online_color"] = node_online_infd[1]

    # Cloud Providers
    cloud_providers = get_cloud_providers()
    INFO["cloud_provider_aws_color"] = cloud_providers[0]
    INFO["cloud_provider_azure_color"] = cloud_providers[1]
    INFO["cloud_provider_other_color"] = cloud_providers[2]
    INFO["cloud_provider_aws"] = cloud_providers[3]
    INFO["cloud_provider_azure"] = cloud_providers[4]
    INFO["cloud_provider_other"] = cloud_providers[5]

    # Cloudwatch
    cloudwatch_operator = get_deployment_status("cloudwatch-operator")
    INFO["cloudwatch_operator_color"] = cloudwatch_operator[0]
    INFO["cloudwatch_operator"] = cloudwatch_operator[1]
    cloudwatch_dashboard = get_deployment_status("cloudwatch-dashboard")
    INFO["cloudwatch_dashboard_color"] = cloudwatch_dashboard[0]
    INFO["cloudwatch_dashboard"] = cloudwatch_dashboard[1]
    cloudwatch_Healthcheck = get_daemon_status("cloudwatch-healthcheck")
    INFO["cloudwatch_Healthcheck_color"] = cloudwatch_Healthcheck[0]
    INFO["cloudwatch_Healthcheck"] = cloudwatch_Healthcheck[1]

    # Figure out the cluster health and failover status
    if INFO["nodes_online_color"] == RED:
        INFO["cluster_health"] = "HEALTH_WARN"
        INFO["cluster_health_color"] = ORANGE
    if INFO["cloud_provider_aws_color"] == RED or INFO["cloud_provider_azure_color"] == RED:
        INFO["cluster_health"] = "HEALTH_WARN"
        INFO["cluster_health_color"] = ORANGE
    if INFO["cloudwatch_operator_color"] == RED or INFO["cloudwatch_Healthcheck_color"] == RED:
        INFO["cluster_health"] = "HEALTH_WARN"
        INFO["cluster_health_color"] = ORANGE
    if INFO["cluster_health_color"] == GREEN:
        INFO["failover_status"] = "Failover Ready"
        INFO["failover_status_color"] = GREEN
    else:
        INFO["failover_status"] = "Failover Not Ready"
        INFO["failover_status_color"] = RED

    print("----------------------------------------------------")
    return INFO


if __name__ == "__main__":
    global pod_name
    global pod_namespace
    global pod_serviceaccount
    global node_name
    global cloud_provider
    global v1_api
    global port
    global v1_api_apps
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
    v1_api_apps = client.AppsV1Api()
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
    CORS(app)
    app.run(host='0.0.0.0', port=port)
