This is taken from: https://opendev.org/openstack/fuel-main/raw/commit/169f1d1cdc5ef0fb271a8e02fb409f6faa30126d/virtualbox/drivers/README.md

# iPXE - open source boot firmware for VirtualBox

This is a prebuilt binary version of **iPXE** as an **VirtualBox PXE ROM**.

The **iPXE** source code is maintained in a git repository. You can check out a copy of the code using:

```
git clone git://git.ipxe.org/ipxe.git
```

and build it using:

```
cd ipxe/src
make
```

You will need to have at least the following packages installed in order to build **iPXE**:

```
* gcc (version 3 or later)
* binutils (version 2.18 or later)
* make
* perl
* syslinux (for isolinux, only needed for building .iso images)
* liblzma or xz header files
* zlib, binutils and libiberty header files (only needed for EFI builds)
```

to build this **Intel 82540EM Gigabit Ethernet PXE ROM** for VirtualBox use:

```
make CONFIG=vbox bin/8086100e.isarom
```

Max size of a VirtualBox ROM is 56KB (57344 bytes).  
There should be no need to pad the image as long as the binary is smaller or equal to this size.

To use the ROM in VirtualBox you need to enable it using this command:

```
vboxmanage setextradata global VBoxInternal/Devices/pcbios/0/Config/LanBootRom \
  /absolute/path/to/8086100e.isarom
```

NB: If you build the ROM using the .rom prefix then it'll be built as a PCI  
ROM, which won't work properly in VirtualBox.  The error message you'll see  
is "No more network devices", which is somewhat confusing.  If you enter the  
shell and use the "autoboot" command things will work as intended.  Remember  
to always build as a .isarom to avoid this issue.

You can find **iPXE** at the official site of the project: <http://ipxe.org/>.
