#!/bin/bash
add_config(){
    echo "Adding To Config [${1}]"
    echo $1 >> /etc/rancher/rke2/config.yaml
}

#Assume root
apt update
apt upgrade -y

mkdir -p /etc/rancher/rke2/
FQDN=dev-rancher.lootbot.live.local
add_config "tls-san: ${FQDN}"
RKE2_VERSION=v1.21.6+rke2r1
curl -sfL https://get.rke2.io | INSTALL_RKE2_VERSION=$RKE2_VERSION sh -
systemctl enable rke2-server.service
systemctl start rke2-server.service



export KUBECONFIG=/etc/rancher/rke2/rke2.yaml
export NODETOKEN=/var/lib/rancher/rke2/server/node-token
echo "KUBECONFIG Stored at [$KUBECONFIG]"
echo "NODETOKEN Stored at [$NODETOKEN]"
echo "NodeToken: "`cat $NODETOKEN`
alias kubectl="/var/lib/rancher/rke2/bin/kubectl"
alias helm="/var/lib/rancher/rke2/bin/helm"

