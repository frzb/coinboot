FROM alpine:3.8

#TODO add syslinux/pxelinux files
RUN apk --no-cache add nginx supervisor dnsmasq cups-client \
    && echo "conf-dir=/etc/dnsmasq.d" > /etc/dnsmasq.conf

RUN mkdir -p /run/nginx /var/lib/tftpboot \
     etc/dnsmasq.d /etc/supervisor /srv/plugins /opt/ipxe \
     && wget http://boot.ipxe.org/ipxe.efi -P /opt/ipxe \
     && wget http://boot.ipxe.org/undionly.kpxe -P /opt/ipxe \
     && ln -vfs /opt/ipxe/ipxe.efi /var/lib/tftpboot/ipxe.efi \
     && ln -vfs /opt/ipxe/undionly.kpxe /var/lib/tftpboot/undionly.kpxe

COPY ./conf/nginx /etc/nginx/conf.d
COPY ./conf/supervisord /etc/supervisor

CMD /usr/bin/supervisord -c /etc/supervisor/coinboot.ini

EXPOSE 67/udp
EXPOSE 67/tcp
EXPOSE 80/tcp
