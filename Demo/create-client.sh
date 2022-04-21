#!/bin/bash
add_config(){
    echo "Adding To Config [${1}]"
    echo $1 >> /etc/rancher/rke2/config.yaml
}
mkdir -p /etc/rancher/rke2/
RKE2_VERSION=v1.20.15+rke2r2
curl -sfL https://get.rke2.io | INSTALL_RKE2_VERSION=$RKE2_VERSION INSTALL_RKE2_TYPE="agent"  sh -
systemctl enable rke2-agent.service
SERVERIP=https://kubernetes2.lootbot.cloud:9345
add_config "server: ${SERVERIP}"
SERVERTOKEN=K10b4d94bd910e6d57feba6f922f7463f9f2d4d7073ccc0e1102e98869cb2b3668f::server:d794e1da80a3cd9146d690c0d39317bb
add_config "token: ${SERVERTOKEN}"
EXTERNAL=40.83.181.140
add_config "node-external-ip: ${EXTERNAL}"
systemctl start rke2-agent.service

# Follow Logs
journalctl -u rke2-agent -f
