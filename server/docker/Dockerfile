FROM alpine:3.8

#TODO add syslinux/pxelinux files
RUN apk --no-cache add nginx supervisor dnsmasq jq curl wget openssl ca-certificates && update-ca-certificates

RUN mkdir -p /run/nginx /var/lib/tftpboot /etc/dnsmasq.d /etc/supervisor /srv/plugins

COPY ./dnsmasq/dnsmasq.conf /etc/dnsmasq.conf
COPY ./nginx /etc/nginx/conf.d
COPY ./supervisor /etc/supervisor
COPY ./coinboot-download-helper /usr/local/bin/coinboot-download-helper
COPY ./graylog-contentpack-helper /usr/local/bin/graylog-contentpack-helper

CMD /usr/bin/supervisord -c /etc/supervisor/coinboot.ini

EXPOSE 67/udp
EXPOSE 67/tcp
EXPOSE 80/tcp
