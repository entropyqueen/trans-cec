FROM nginx:1.23-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY prepare_nginx_conf.sh /
RUN chmod 755 /prepare_nginx_conf.sh
COPY nginx.conf /etc/nginx/conf.d/nginx.conf.tpl