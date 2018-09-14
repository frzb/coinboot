FROM alpine:3.8

#TODO add syslinux/pxelinux files
RUN apk --no-cache add nginx supervisor dnsmasq alpine-ipxe\
    && echo "conf-dir=/etc/dnsmasq.d" > /etc/dnsmasq.conf

RUN mkdir -p /run/nginx /var/lib/tftpboot/pxelinux.cfg /etc/dnsmasq.d /etc/supervisor /srv/plugins \
    #&& ln -vfs /usr/share/alpine-ipxe/undionly.kpxe /var/lib/tftpboot/undionly.kpxe \
   # && ln -vfs /usr/share/alpine-ipxe/ipxe.efi /var/lib/tftpboot/ipxe.efi
     && wget http://boot.ipxe.org/ipxe.efi -P /var/lib/tftpboot \
     && wget http://boot.ipxe.org/undionly.kpxe -P /var/lib/tftpboot
