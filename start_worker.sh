#!/bin/bash

pip install locust
nohup locust -f simple.py --worker --master-host=172.31.46.167 --processes -1 &