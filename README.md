# Multi-Cloud-Kubernetes-Failover
### Description

* This operator provides ability to Monitor and failover Kubernetes applications running on any cluster from one cloud provider to another.
* The Operator Will expose a web based portal to monitor and track the connection status between the running cluster workloads. 
* the operator will utilize a [linkerd](https://linkerd.io/) service mesh to connect the Multi-Cloud Environment Together. 
* Operator is being designed as a Senior Final Project For IAE-458-L01_2022_30.US Senior Design Project II

## Introduction

This [Helm](https://github.com/kubernetes/helm) chart installs [Multi-Cloud-Kubernetes-Failover](https://github.com/william86370/Multi-Cloud-Kubernetes-Failover) in a Kubernetes cluster.

## Prerequisites
- Docker Desktop
- AWS-CLI
- RKE-2
- Azure Services
- Hard-Metal Servers

## Installation


### Create a New Kubernetes Cluster Using RKE-2 on AWS
**Notes** Creating a Cluster for the first time is a complex process and this tutorial is only going to explane the bare basics for creating a functional cluster, there are hundreds of different configuration changes you can make to optimize the cluster to fit your needs. 

# Installing Dependency's

**Note** This example is being run on Ubuntu 20.04 on WSL Windows-10
 ```bash 
# Update The system
# Assume Root
apt-get update && apt-get upgrade -y
# Install The AWS CommandLine Interface 
apt-get install -y awscli 

```
# Login To AWS-Cli
#TODO

# Create a new EC2 Ubuntu VM for Running K8 Node

1.) Open the Amazon EC2 console at [Ec2](https://console.aws.amazon.com/ec2/)
2.) From the console dashboard, choose Launch Instance.
3.) From the AMI Page, Select Ubuntu Linux
4.) From the Choose an Instance Type page, Select the t2.small instance type.
5.) On the Choose an Instance Type page, choose Review and Launch.
6.) On the Review Instance Launch page, under Security Groups, you'll see that the wizard created and selected a security group for you.
7.) On the Review Instance Launch page, choose Launch.
8.) When prompted for a key pair, select Choose an existing key pair.
9.) On the Instances screen, you can view the status of the launch. It takes a short time for an instance to launch. When you launch an instance, its initial state is pending. After the instance starts, its state changes to running and it receives a public DNS name.
10.) It can take a few minutes for the instance to be ready so that you can connect to it.


# Connect to your AWS instance 

1.) Get the public DNS name and user name to connect to your instance
2.) Open a new Terminal Window. 
3.) Using SSH connect to the public IP using the username.
```bash 
ssh -i /path/to/pkey ubuntu@exampleip 
```

# Update the system
```bash
sudo su
apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends --no-install-suggests awscli 
```

## Setup New RKE2 Cluster Using AWS EC2 VM.


# Create Rancher Directory 
```bash 
mkdir -p /etc/rancher/rke2/
```
# Set the RKE2 Version 
``` bash
RKE2_VERSION=v1.21.6+rke2r1
```
# Set the Public Ipv4 DNS FQDN 
```bash
add_config(){
    echo "Adding To Config [${1}]"
    echo $1 >> /etc/rancher/rke2/config.yaml
}
FQDN=example.ipv4dns.ec2.local
add_config "tls-san: ${FQDN}"
```

# Install RKE2 Server
```bash 
curl -sfL https://get.rke2.io | INSTALL_RKE2_VERSION=$RKE2_VERSION sh -
```
# Enable RKE2 Server 
``` bash
systemctl enable rke2-server.service
```

# Start RKE2 Server
```bash 
systemctl start rke2-server.service
```

### Add Helm repository
```bash
helm repo add CloudWatch https://github.com/william86370/Multi-Cloud-Kubernetes-Failover
```


### Add Linkerd Service-Mesh



#### Configure the way how to expose CloudWatch service

- **Ingress**: The ingress controller must be installed in the Kubernetes cluster.
- **ClusterIP**: Exposes the service on a cluster-internal IP. Choosing this value makes the service only reachable from within the cluster.
- **NodePort**: Exposes the service on each Node’s IP at a static port (the NodePort). You’ll be able to contact the NodePort service, from outside the cluster, by requesting `NodeIP:NodePort`.
- **LoadBalancer**: Exposes the service externally using a cloud provider’s load balancer.
