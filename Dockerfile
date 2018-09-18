FROM alpine:3.8

#TODO add syslinux/pxelinux files
RUN apk --no-cache add nginx supervisor dnsmasq alpine-ipxe\
    && echo "conf-dir=/etc/dnsmasq.d" > /etc/dnsmasq.conf

RUN mkdir -p /run/nginx /var/lib/tftpboot/pxelinux.cfg \
     /etc/dnsmasq.d /etc/supervisor /srv/plugins /opt/ipxe \
     && wget http://boot.ipxe.org/ipxe.efi -P /opt/ipxe \
     && wget http://boot.ipxe.org/undionly.kpxe -P /opt/ipxe \
     && ln -vfs /opt/ipxe/ipxe.efi /var/lib/tftpboot/ipxe.efi \
     && ln -vfs /opt/ipxe/undionly.kpxe /var/lib/tftpboot/undionly.kpxe \
