#!/bin/bash

# Update system
sudo yum update -y

# Install Python and Git
sudo yum install python3 python3-pip git -y

# Create directory for the app
sudo mkdir -p /opt/stratum-proxy
sudo chown ec2-user:ec2-user /opt/stratum-proxy

# Copy files to the application directory
cp proxy_server.py config.py /opt/stratum-proxy/

# Create a systemd service file for the proxy
sudo tee /etc/systemd/system/stratum-proxy.service << EOF
[Unit]
Description=Stratum Proxy Service
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/opt/stratum-proxy
ExecStart=/usr/bin/python3 /opt/stratum-proxy/proxy_server.py
Restart=always
RestartSec=3
StandardOutput=append:/var/log/stratum-proxy.log
StandardError=append:/var/log/stratum-proxy.log

[Install]
WantedBy=multi-user.target
EOF

# Create log file and set permissions
sudo touch /var/log/stratum-proxy.log
sudo chown ec2-user:ec2-user /var/log/stratum-proxy.log

# Reload systemd and start the service
sudo systemctl daemon-reload
sudo systemctl enable stratum-proxy
sudo systemctl start stratum-proxy

# Check the status
sudo systemctl status stratum-proxy

# Show the logs
echo "Showing logs..."
tail -f /var/log/stratum-proxy.log
