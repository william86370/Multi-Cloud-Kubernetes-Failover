# Developed by William Wright for Senior Project at Capitol Technology University
# Cloudwatch Operator
# Author: William Wright
# Date: 2022-04-17
# Version: 1.0
# Description:
#  This file contains the Cloudwatch Operator.
#  This operator is responsible for creating and deleting cloudwatch daemon sets and services.
#  It also creates and deletes the cloudwatch dashboard.

# -------
# Imports
# -------
import os
from kubernetes import client, config, utils
import colorama
from colorama import Fore
from colorama import init
import json
from flask import Flask
# Add CORS support
from flask_cors import CORS, cross_origin

# Colored output Messages WARNING, ERROR, INFO
from kubernetes.client import ApiException

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
    return "Welcome to the Cloudwatch Operator"


def main():
    # Cloudwatch Operator
    # Check if the operator is running in a kubernetes cluster
    print("-------------------------------------------------------")
    print("| Cloudwatch Operator V1.0 Developed by William Wright |")
    print("-------------------------------------------------------")

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

    # get the namespace
    namespace = os.environ.get('CLOUDWATCH_OPERATOR_NAMESPACE')

    # Initialize kubernetes client
    v1 = client.CoreV1Api()
    v1_api_apps = client.AppsV1Api()
    print_info("[INFO] KubeAPI Successfully Connected to Cluster")
    # Check if the daemon set exists
    try:
        # Get the daemon set
        daemon_set = v1_api_apps.read_namespaced_daemon_set(name="cloudwatch-healthcheck", namespace=namespace)
        print_info("[INFO] Found existing Healthcheck DaemonSet")
        # check the version of the daemon set
        # TODO - Add version check
    except ApiException as e:
        print_info("[INFO] No existing Healthcheck DaemonSet found")
        print_info("[INFO] Deploying Healthcheck DaemonSet")
        # Deploy the daemon set
        utils.create_from_yaml(v1, '/app/deploy-daemonset.yaml', verbose=True)
        print_info("[INFO] Healthcheck DaemonSet Deployed")
    # Check if the dashboard exists
    print_info("[INFO] Checking for Existing Cloudwatch Dashboard")
    try:
        # Get the dashboard
        dashboard = v1_api_apps.read_namespaced_deployment(name="cloudwatch-dashboard", namespace=namespace)
        print_info("[INFO] Found existing dashboard")
        # TODO - Add version check
    except ApiException as e:
        print_info("[INFO] No existing dashboard found")
        print_info("[INFO] Deploying Cloudwatch Dashboard")
        # Deploy the dashboard
        utils.create_from_yaml(v1, '/app/deploy-dashboard.yaml', verbose=True)
        # TODO - Deploy dashboard
        print_info("[INFO] Cloudwatch Dashboard Deployed")

    # Operator has deployed all resources
    print_info("[INFO] Cloudwatch Operator Startup Complete")
    port = 8080
    print_info(f"Starting Operator on port {port}")
    CORS(app)
    app.run(host='0.0.0.0', port=port)


if __name__ == "__main__":
    main()
