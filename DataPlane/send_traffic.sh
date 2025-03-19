#!/bin/bash
while true; do
    iperf -c 10.0.0.47 -u -b $(( RANDOM % 100 + 1 ))M -t 1
    sleep 1
done
