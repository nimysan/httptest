#!/bin/bash

sudo cat hosts >> /etc/hosts
pip install locust
nohup locust -f simple.py --worker --master-host=172.31.46.167 --processes -1 > /tmp/locust.out 2>&1 &