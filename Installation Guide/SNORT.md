---
### SNORT IDS/IPS System Installation Guide

![SNORT ids/ips SYSTEM](https://cyberhub.oss-me-central-1.aliyuncs.com/uploads/V-OFXjGTSHrFZjg_KTxNbo4b2v7GdT)


### PRE-REQUISITES

```bash
sudo apt-get -y update && sudo apt-get -y upgrade
sudo apt remove docker docker-engine docker.io containerd runc
sudo apt install -y ca-certificates curl gnupg lsb-release
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
docker --version
sudo systemctl start docker
sudo systemctl enable docker
```

### SNORT RULE SET DEVELOPER (SNORPY)
```bash

```



### SNORT INSTALLATION AND CONFIGURATION