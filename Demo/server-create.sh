#!/bin/bash
add_config(){
    echo "Adding To Config [${1}]"
    echo $1 >> /etc/rancher/rke2/config.yaml
}

mkdir -p /etc/rancher/rke2/
RKE2_VERSION=v1.20.15+rke2r2
FQDN=kubernetes2.lootbot.cloud
add_config "tls-san: ${FQDN}"
NODEEX=54.172.28.154
add_config "node-external-ip: ${NODEEX}"
curl -sfL https://get.rke2.io | INSTALL_RKE2_VERSION=$RKE2_VERSION sh -
systemctl enable rke2-server.service
systemctl start rke2-server.service
export KUBECONFIG=/etc/rancher/rke2/rke2.yaml
export NODETOKEN=/var/lib/rancher/rke2/server/node-token
# echo "KUBECONFIG Stored at [$KUBECONFIG]"
# echo "NODETOKEN Stored at [$NODETOKEN]"


alias kubectl="/var/lib/rancher/rke2/bin/kubectl"
alias helm="/var/lib/rancher/rke2/bin/helm"
# journalctl -u rke2-server -f
echo "NodeToken: "`cat $NODETOKEN`
# cat $KUBECONFIG
# /usr/local/bin/rke2-uninstall.sh
