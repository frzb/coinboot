Change for testing conditional builds #33

![Logo of Coinboot](https://raw.githubusercontent.com/frzb/coinboot/master/img/coinboot.png)

[![Build Status](https://travis-ci.org/frzb/coinboot-debirf.svg?branch=master)](https://travis-ci.org/frzb/coinboot-debirf)

***Building  your own Coinboot image***

Coinboot is a framework for diskless computing.

Coinboot uses a heavy adapted version of [debirf](http://cmrg.fifthhorseman.net/wiki/debirf) to build the Coinboot base image which makes it possible to run machines diskless and completely in-memory.

Coinboot is made to be lightweight. Measuring ~85M for the initramfs and ~7M for the kernel archive.

Coinboot is currently based on Ubuntu 16.04 Xenial.

For more information how to boot your machines with Coinboot visit: https://coinboot.io

## Requirements 

* Vagrant

or 

* Docker and Docker Compose

## Hardware support

All hardware which is supported by a 4.4 `generic` kernel of Debian/Ubuntu should just work out of the box.
The reference hardware setup is build around a Gigabyte GA-H110-D3A mainboard.

* Architecture: AMD64
* Chipset: Intel H110
* CPU: Intel-based with integrated GPU
* NIC: Realtek RTL8111G

Further hardware support can be added by using the Coinboot plugin system e.g. to integrate the proprietary AMDGPU-Pro driver.

We also try to built up an overview with hardware setups known to work.


## Usage

For the build process Vagrant or Docker with Docker Compose can be used.  
To build the Coinboot base image consisting of a initramfs archive (`initramfs`) and kernel archive (`vmlinuz`) run:

```
$ vagrant up
```

or 

```
$ docker-compose up
```

When the build has finished the resulting archives are written to the `./build` directory.

## License

GNU GPLv3 

## Author

Gunter Miegel 
gm@coinboot.io

## Contribution

Fork this repo. 
Make a pull request to this repo. 
