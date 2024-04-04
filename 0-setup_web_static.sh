#!/usr/bin/env bash
#Script for setting the server
sudo apt update -y
sudo apt install --allow-downgrades nginx -y
sudo ufw allow 'Nginx HTTP'
sudo mkdir -p /data/web_static/shared /data/web_static/releases/test
echo 'Holberton School' | sudo tee /data/web_static/releases/test/index.html
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data
sudo sed -i '27i\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default
sudo service nginx restart
exit 0
