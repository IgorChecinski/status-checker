#!/bin/bash
apt update
apt install -y docker.io docker-compose git


cd /opt
git clone https://github.com/IgorChecinski/status-checker.git
cd devops-monitor

docker-compose up -d
