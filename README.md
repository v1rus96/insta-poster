# Stratum Proxy Setup

## AWS EC2 Deployment Instructions

1. Launch EC2 Instance:
   - Use Amazon Linux 2023
   - Instance type: t2.micro (free tier eligible)
   - Configure Security Group:
     - Allow SSH (port 22)
     - Allow Custom TCP port 8333

2. Connect to your EC2 instance:
```bash
ssh -i your-key.pem ec2-user@your-instance-ip
```

3. Copy files to EC2:
```bash
# From your local machine
scp -i your-key.pem -r /path/to/insta-poster/* ec2-user@your-instance-ip:~/insta-poster/
```

4. Run deployment script:
```bash
cd ~/insta-poster
chmod +x deploy.sh
./deploy.sh
```

5. Check service status:
```bash
sudo systemctl status stratum-proxy
```

## Miner Configuration

Configure your miner with:
```
URL: stratum+tcp://your-ec2-ip:8333
Worker: your-worker-name
Password: your-password
```

## Monitoring Logs

View proxy logs:
```bash
sudo journalctl -u stratum-proxy -f
```

## Troubleshooting

If the proxy isn't working:
1. Check service status:
```bash
sudo systemctl status stratum-proxy
```

2. Check ports:
```bash
sudo netstat -tulpn | grep 8333
```

3. Check security group rules in AWS Console
