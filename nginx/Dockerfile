FROM nginxinc/nginx-uprivileged:1-alpine

COPY ./default.conf /etc/nginx/conf.d/default.conf

USER root

RUN mkdir -p /vol/static
RUN chmod 775 /vol/static

USER nginx