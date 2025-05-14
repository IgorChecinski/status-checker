#!/bin/bash

set -e


if ! command -v docker &> /dev/null
then
    echo "Docker not found. Installing..."
    sudo apt-get update
    sudo apt-get install -y docker.io
    sudo systemctl start docker
    sudo systemctl enable docker
fi


if ! command -v docker-compose &> /dev/null
then
    echo "Docker Compose not found. Installing..."
    sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi


cd /home
sudo git clone https://github.com/IgorChecinski/status-checker.git
cd status-checker

cat <<EOF > .env
DATABASE_URL=postgresql://postgres:password@db:5432/mydatabase
REDIS_HOST=redis
REDIS_PORT=6379
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=mydatabase
EOF

echo "Cleaning up any old containers..."
sudo docker-compose down || true

sudo docker-compose up -d

echo "Startup script completed successfully!"
