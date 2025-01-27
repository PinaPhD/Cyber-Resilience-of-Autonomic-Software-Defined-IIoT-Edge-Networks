---
### ONOS SDN Controller

![ONOS SDN Controller](https://upload.wikimedia.org/wikipedia/en/d/d3/Logo_for_the_ONOS_open_source_project.png)

#### Setting up the ONOS SDN Controller Cluster:

```bash
	sudo apt-get -y update && sudo apt-get -y upgrade
	sudo apt install git wget vim
	sudo apt -y install openjdk-8-jdk
```

Append environment variable JAVA_HOME to ~/.bashrc 
```bash
	export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
	export JRE_HOME=$JAVA_HOME/jre
	export CLASSPATH=.:$JAVA_HOME/lib:$JRE_HOME/lib
	export PATH=$JAVA_HOME/bin:$PATH
```

Run this: `source ~/.bashrc`

Installing ONOS Ver2.0.0 (_Loon_)

Download the onos binary file:  `sudo wget -c https://repo1.maven.org/maven2/org/onosproject/onos-releases/2.0.0/onos-2.0.0.tar.gz`

```bash
	tar zxvf onos-2.0.0.tar.gz
	sudo mkdir /opt/onos 
	sudo cp -r onos-2.0.0/* /opt/onos
```

Run onos services 
```bash
	cd /opt/onos/bin
	sudo /opt/onos/bin/onos-service start
```

Open another terminal and add configuration to ~/.ssh/config
```bash
	mkdir ~/.ssh
	touch ~/.ssh/config
	vim ~/.ssh/config
```

Paste this in the `~/.ssh/config` file
```bash
	HostKeyAlgorithms +ssh-rsa
	PubkeyAcceptedKeyTypes +ssh-rsa
```

Connect to onos cli and activate application
```bash
	cd /opt/onos/bin
	/opt/onos/bin/onos -l onos
	password: rocks
```

On the ONOS SDN Controller CLI activate the following applications:
```bash
	onos@root$ app activate org.onosproject.pipelines.basic
	onos@root$ app activate org.onosproject.fwd
	onos@root$ app activate org.onosproject.openflow
```

Login GUI
Open browser and type `http:<localhost>:8181/onos/ui`

username/password: onos/rocks