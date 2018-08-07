FROM nginx:1.14.0-alpine

#TODO add syslinux/pxelinux files
RUN apk --no-cache add supervisor dnsmasq syslinux\
    && echo "conf-dir=/etc/dnsmasq.d" > /etc/dnsmasq.conf

RUN mkdir -p /var/lib/tftpboot/pxelinux.cfg /etc/dnsmasq.d /etc/supervisor /srv/plugins \
    && ln -vfs /usr/share/syslinux/lpxelinux.0 /var/lib/tftpboot/lpxelinux.0 \
    && ln -vfs /usr/share/syslinux/ldlinux.c32 /var/lib/tftpboot/ldlinux.c32 \
    && ln -vfs /usr/share/syslinux/efi64/syslinux.efi /var/lib/tftpboot/syslinux.efi \
    && ln -vfs /usr/share/syslinux/efi64/ldlinux.e64 /var/lib/tftpboot/ldlinux.e64

#CMD ["dnsmasq"]
