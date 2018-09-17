![Logo of Coinboot](coinboot.png)


## Coinboot [![Build Status](https://travis-ci.com/frzb/coinboot.svg?branch=master)](https://travis-ci.com/frzb/coinboot)

Coinboot is a framework for diskless computing. 


Its core features are:

* **Running Diskless**

  With Coinboot there is no need to equip machines with storage media like SSDs, HDDs or USB flash drives.  
  All machines are booting the operating system over network and run completely from memory, in-memory.


* **Leightweight Footprint**

  Coinboot has a lightweight footprint.  
  Driven by the demand to run sufficiently on hundreds of machines with commodity 1 Gbit/s network hardware.


* **Familiar Usabillity**

  No bumpy ride.  
  Coinboot feels just like every other Debian/Ubuntu-based system. 


* **Easy Expandability**

  Need to expand your machines with further configuration, software, libraries, proprietary drivers?  
  By packing them as Coinboot plugin you can use them right after your machines have booted.

## Requirements

Docker

Docker Compose

## Usage

### Preparations

Clone this repository one the host where you want to execute the Coinboot Docker container.

#### RootFS and Kernel

You can **build** your own Coinboot base image using: [coinboot-debirf](https://github.com/frzb/coinboot-debirf).   
Or **download** a pre-build release at: https://coinboot.io/releases.

Put the Coinboot RootFS (`initramfs`) and Kernel (`vmlinuz`) into the directory `./tftpboot`.

#### Plugins

Coinboot plugins should be placed into  the directory `./plugins`

You can create your own plugins (see below) or pick some at: https://coinboot.io/plugins

#### DHCP configuration

Put your own `dnsmasq` DHCP server configuration in `./conf/dnsmasq/` or edit the existing configuration file `./conf/dnsmasq/coinboot.conf`.

#### IP address and network

Take care that your Docker host has assigned an IP address matching to the `dhcp-range` specified at `./conf/dnsmasq/coinboot.conf`. 

For example the Docker host has assigned `192.168.1.2` then a matching DHCP-range configuration is: `dhcp-range=192.168.1.10,192.168.1.100,6h`. 

Also verify that the network adapter you assigned this IP address on your Docker host is connected to the same L2/broadcast domain as the machines you want to boot with Coinboot.

#### Environment variables

You can hand over environment variables to the machines booting with Coinboot.  
Just put these variables in a file in the directoy `./conf/environment/`.

### Start the Coinboot container

Just bring the Coinboot Docker container up with `docker-compose`.

```
$ docker-compose up -d
```

### Boot your machines with Coinboot

Start your machines.  
They are booting over network.  
You can login to your machines over `ssh`.  
Default credentials are:

* login: `ubuntu`
* password: `ubuntu`
  
Please change the password via creating a Coinboot Plugin.

## Test and development environment

There is Vagrant environment for developing purposes.
It consists of two Vagrant machines: One with the the Coinboot Docker container and one acting as client, which boots over PXE.

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

Fork this repo. Use the test- and development enviroment provided.
Make a pull request to this repo. 
