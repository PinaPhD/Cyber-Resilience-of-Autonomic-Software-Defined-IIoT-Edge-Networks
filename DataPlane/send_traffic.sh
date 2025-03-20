#!/bin/bash
while true; do
    iperf -c 10.0.0.47 -u -b $(( RANDOM % 2000 + 1000 ))M -t 1
    sleep 1
done
