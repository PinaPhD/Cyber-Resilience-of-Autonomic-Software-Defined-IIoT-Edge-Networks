## Analyzing the cyber-resilience of zero-trust software-defined industrial IoT-Edge networks in offshore wind farms


---
![Security Framework]()
---



## Table of Contents

1. [Executive Summary](#summary)
2. [Pre-requisites](#requirements)
3. [Data Plane Design](#data-plane-design)
4. [Control Plane Design](#control-plane-design)
5. [Cyber-Resilience Analysis](#cyber-resilience-analysis)
6. [Reach Us](#reach-us)
7. [References](#references)


## Executive Summary

To be Updated


## Pre-requisites

1. On the Utrecht University SURF HPC Research Cloud Portal, request sufficient CPU-hrs credits for your preferred workspace.
2. Follow this documentation to create a workspace and attach a storage unit using your preferred compute and storage requirements.
	- See the [Installation Guide](https://utrechtuniversity.github.io/vre-docs/docs/first-steps.html)
3. In the workspace, create 3 virtual machines running Ubuntu-GNOME Desktop version. 
	- The default Ubuntu VM comes in xfce4 format. Upgrade it to the GNOME full version using this code snippet [here]()
Alternatively, get a physical server and proceed to step 3.


## Data Plane Design

- On one of the VMs with Mininet Installation run the [network topology](https://github.com/PinaPhD/A-threshold-triggered-DQN-self-healing-framework/blob/main/DataPlane/topology.py) for an offshore wind farm (reduce model with 20 WTGs communicating with one OSS)
- At the Mininet prompt, run xterm on select mininet hosts to initialize traffic generation using the following data sets:
    - [MQTT sensor data traffic](https://github.com/PinaPhD/A-threshold-triggered-DQN-self-healing-framework/tree/main/DataPlane/IIoT_ECP_Socket)
    - [IEC61850 SV/GOOSE docker based data traffic](https://github.com/mz-automation/libiec61850)
    - Ordinary ping tests

- To monitor network performance, use the [iperf3](https://iperf.fr/) tool for active measurements of network latency, throughput, jitter, packet loss (loss of datagrams).



## Control Plane Design

- On one of the VMs, download the [ONOS ver.2.0.0](https://repo1.maven.org/maven2/org/onosproject/onos-releases/2.0.0/onos-2.0.0.tar.gz) SDN Controller.
- Create a cluster using the _"org.onosproject.cluster-ha"_ ONOS SDN controller feature.
- Install the following ONOS features:
    - org.onosproject.pipelines.basic
    - org.onosproject.fwd
    - org.onosproject.openflow
    - org.onosproject.cpman
    - org.onosproject.metrics

- See more information on ONOS installation and design [here](https://wiki.onosproject.org/display/ONOS/ONOS).
- The Knowledge plane interacts with the ONOS SDN Controller [subsystems](https://github.com/PinaPhD/A-threshold-triggered-DQN-self-healing-framework/tree/main/Images/onos-subsystems.png) using RESTFul APIs from the Northbound Interface.


## Cyber Resilience Analysis
To be updated

## Reach Us

- If you need assistance using this tool, kindly log an issue [here](https://github.com/PinaPhD/A-threshold-triggered-DQN-self-healing-framework/issues) and we will respond within 24hrs maximum waiting time.
- Also, feel free to contribute to discussion posts and suggest any points of improvement by logging an issue.


## References

- To be updated.

```{bibliography}
    @article{mwangi2025,
    title="I",
    journal="",
    year="2025",
    volume="",
    issue="",
    }
```

- More studies from us and cite our work: [Reference list](https://github.com/PinaPhD/A-threshold-triggered-DQN-self-healing-framework/blob/main/References.md)
