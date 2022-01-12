#!/usr/bin/env bash
#script that sets up your web servers for the deployment of web_static

sudo apt-get update
sudo apt-get install -y nginx

rm -rf "/data/web_static"
mkdir -p "/data/web_static/releases/test/"
mkdir -p "/data/web_static/shared/"

printf %s "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
" > /data/web_static/releases/test/index.html

rm -rf "/data/web_static/current"
ln -fs "/data/web_static/releases/test/" "/data/web_static/current"

chown -R ubuntu:ubuntu "/data/"

printf %s "server {
    listen 80;
    listen [::]:80 default_server;
    root   /etc/nginx/html;
    index  index.html index.htm;
    add_header X-Served-By $hostname;
    location /redirect_me {
        return 301 https://www.youtube.com/watch?v=QH2-TGUlwu4;
    }
    location /hbnb_static {
        alias /data/web_static/current/;
    }
}" > /etc/nginx/sites-available/default



service nginx restart
