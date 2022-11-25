#!/usr/bin/env sh

echo "################################## Run nginx"
export DOLLAR='$'
envsubst < /etc/nginx/conf.d/nginx.conf.tpl > /etc/nginx/conf.d/nginx.conf
nginx -g "daemon off;"