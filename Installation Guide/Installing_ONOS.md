---
### ONOS SDN Controller Installation Guide

![ONOS SDN Controller](https://upload.wikimedia.org/wikipedia/en/d/d3/Logo_for_the_ONOS_open_source_project.png)


### Pre-requisites
On an Ubuntu 20.04 LTS-Gen2 Virtual Machine with Gnome Desktop, do the following:

```bash
sudo apt-get -y update && sudo apt-get -y upgrade
sudo apt install default-jdk
sudo apt install apt-transport-https curl gnupg -y
curl -fsSL https://bazel.build/bazel-release.pub.gpg | gpg --dearmor >bazel-archive-keyring.gpg
sudo mv bazel-archive-keyring.gpg /usr/share/keyrings
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/bazel-archive-keyring.gpg] https://storage.googleapis.com/bazel-apt stable jdk1.8" | sudo tee /etc/apt/sources.list.d/bazel.list
sudo apt update && sudo apt install bazel-3.7.2
```

Now install the latest version of ONOS (ver.2.7.0 -- ~Snowy Owl~)

```bash
git clone https://github.com/opennetworkinglab/onos.git
cd onos
git checkout 2.7.0 # or git reset --hard 2.7.0
sudo apt-get install python-is-python3 -y
bazel build onos
```

- If you get any error, run `bazel build onos` again and it will clean them up.

```bash
bazel run onos-local [-- [clean] [debug]]
```

Now you may log onto the ONOS Web App:
- Open browser and type `http:<localhost>:8181/onos/ui`
- username/password: `onos/rocks`

On the ONOS SDN Controller CLI activate the following applications:
```bash
	onos@root$ app activate org.onosproject.pipelines.basic
	onos@root$ app activate org.onosproject.fwd
	onos@root$ app activate org.onosproject.openflow
```

