![Logo of Coinboot](coinboot.png)


## Coinboot [![Build Status](https://travis-ci.com/frzb/coinboot.svg?branch=master)](https://travis-ci.com/frzb/coinboot)

Coinboot is a framework for diskless computing. 

Its core features are:

* **Running Diskless**

  With Coinboot there is no need to equip machines with storage media like SSDs, HDDs or USB flash drives.  
  All machines are booting the operating system over network and run completely from memory, in-memory.


* **Lightweight Footprint**

  Coinboot has a lightweight footprint.  
  Driven by the demand to run sufficiently on hundreds of machines with commodity 1 Gbit/s network hardware.


* **Familiar Usability**

  No bumpy ride.  
  Coinboot feels just like every other Debian/Ubuntu-based system. 


* **Easy Expandability**

  Need to expand your machines with further configuration, software, libraries, proprietary drivers?  
  By packing them as Coinboot plugin you can use them right after your machines have booted.

This repository contains the Coinboot Server Docker container.                 
This container includes all services to get Coinboot up and running and boot diskless Coinboot Worker nodes over network.

## Requirements

Docker

Docker Compose

## Usage

### Quickstart

Clone this repository on the host where you want to execute the Coinboot Docker container.

#### IP address and network

Take care that your Docker host has assigned an IP address matching to the `dhcp-range` specified at `./conf/dnsmasq/coinboot.conf`.  
For example the Docker host has assigned `192.168.1.2` then a matching DHCP-range configuration is: `dhcp-range=192.168.1.10,192.168.1.100,6h`.  
Also verify that the network adapter you assigned this IP address on your Docker host is connected to the same L2/broadcast domain as the machines you want to boot with Coinboot.  

#### Environment variables

You can hand over environment variables to the worker nodes booting with Coinboot.  
This way you can keep the configuration of your Coinboot Worker nodes at one point.  
Just put these variables in a file in the directory `./conf/environment/`.  
These variables are added to `/etc/environment` on the worker nodes during boot and are exported and available for login shells on these nodes.  
If these variables are not exported and available, e.g. in Systemd units, just source the file `/etc/environment` to make them available.

#### RootFS and Kernel

The RootFS and Kernel are downloaded autmatically when the Coinboot Server Docker container 4is started based on the `RELEASE`set at `./conf/environment/default.env`.

You can **build** your own Coinboot base image using: [coinboot-debirf](https://github.com/frzb/coinboot-debirf).   
Or **download** a pre-build daily release at: https://github.com/frzb/coinboot-debirf/releases  
These builds are made daily to contain all current packages updates and security fixes.
The RootFS (`*initramfs*`) and Kernel (`*vmlinuz*`) you want to use are to be placed in the directory `./boot`.

#### Plugins

Coinboot plugins should be placed into  the directory `./plugins`

You can create your own plugins (see below) or pick some at: https://coinboot.io/plugins

#### DHCP configuration

Put your own `dnsmasq` DHCP server configuration in `./conf/dnsmasq/` or edit the existing configuration file `./conf/dnsmasq/coinboot.conf`.

In the most  cases you should only need  to configure: 

* DHCP lease range
* DNS server
* Default network gateway


#### IP address and network

Take care that your Docker host has assigned an IP address matching to the `dhcp-range` specified at `./conf/dnsmasq/coinboot.conf`. 

For example the Docker host has assigned `192.168.1.2` then a matching DHCP-range configuration is: `dhcp-range=192.168.1.10,192.168.1.100,6h`. 

Also verify that the network adapter you assigned this IP address on your Docker host is connected to the same L2/broadcast domain as the machines you want to boot with Coinboot.

#### Environment variables

You can hand over environment variables to the machines booting with Coinboot.  
This is the way to keep the configuration for your machines at one point.  
Just put these variables in a file in the directory `./conf/environment/`.
These varibales are added to `/etc/environment` on your machines and are exported  and available for login shells.
If these variables are no exported and available, e.g. in Systemd units, just source the file `/etc/environment` to make them available.

### Start the Coinboot Server Docker container

Just bring the Coinboot Server Docker container up with `docker-compose`.

```
$ docker-compose up -d
```

### Boot your worker nodes with Coinboot

Start your worker nodes.  
After they have booted Coinboot over network you can login to your machines over `ssh`.  
Default credentials are:

* login: `ubuntu`
* password: `ubuntu`
  
Please change the password via creating a Coinboot Plugin.

### Logfiles

To see what's currently going on you can look at the logfiles of the Coinboot Docer container.  
For instance to see the DHCP lease hand-shakes happen or what plugins are delivered.

```
$ docker-compose logs -f
```

## Test and development environment

There is Vagrant environment for developing purposes.
It consists of two Vagrant machines: One with the the Coinboot Server Docker container and one machine acting as worker node, which boots over PXE.

To spin up the Vagrant machines execute:

```
$ vagrant up
```

## Pack your own Coinboot plugins

A Coinboot plugin is the way to go to extend the functionality of machines that boot with Coinboot.

Basically a Coinboot plugin is just set of file system changes that is applied at boot time.


All you need to create your own plugins is:

* Boot the Coinboot base image

* Execute `$ create_plugin start`

* Do your changes to the system - e.g. install packages and edit configuration files.

* When your are done: Execute `$ create_plugin finish <name-of-your-plugin>`

* Place the created plugin archive into `./plugins` on the host where you run the Coinboot Docker container

Up on the next boot the changes your made in your plugin are ready to be used on your Coinboot machines!

Creation of plugins can also be scripted. Just do whatever you want to do between the lines `$ create_plugin start` and `$ create_plugin finish <name-of-your-plugin>`.

## License

GNU GPLv3 

## Author

Gunter Miegel 
gm@coinboot.io

## Contribution

Fork this repo. Use the test- and development environment provided.
Make a pull request to this repo. 
