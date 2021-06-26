
![Logo of Coinboot](https://raw.githubusercontent.com/frzb/coinboot/master/coinboot.png)

## Plugins for Coinboot

Coinboot is a framework for diskless computing.   
This repository contains plugins for Coinboot which expand Coinboot with further software and functionalities.  
It also contains `coinbootmaker` - a little helper to build your own Coinboot plugins.  
  
For more information how to boot your machines with Coinboot visit: https://coinboot.io

## Coinboot Plugins 

<!-- PLACEHOLDER FOR MARKDOWN PLUGIN TABLE -->

## Requirements

* Coinboot with kernel `5.4.0-58-generic`

### If you want to build plugins on your own: 

* Docker 

* a Debian or Ubuntu build host

* `brctl` which is part of the `bridge-utils` package

## Usage

### Pre-built Plugins

Put the pre-built plugins of your choice that your can download under [releases](https://github.com/frzb/coinboot-plugins/releases)
into the `plugins` directory of your Coinboot setup.

### Coinbootmaker - build the Plugins

To build Coinboot plugins on your own use `coinbootmaker`.

```
Usage: coinbootmaker [-i] [-l] [-h] [-p <plugin name> <path to initramfs>]

-i              Interactive mode - opens a shell in the build environment
-p <file name>  Plugin to build
-l              List plugins available to build
-h              Display this help
```

For example:

```
$ ./coinbootmaker -p ethminer /tmp/coinboot-initramfs-4.15.0-43-generic  
```

`coinbootmaker` takes a path to a Coinboot-Initramfs to create an environment for building the plugins  
by converting the given Initramfs into a Container image and run it.  
The plugin creation script located at `src` is executed in that `coinbootmaker` container and the resulting  
plugin archive is written to the `build` directory.

## License

MIT

Please notice even while the scripts to create Coinboot plugins are licensed with the MIT license the software packaged by this scripts may be licensed by an other license with different terms and conditions.  
You have to agree to the license of the packaged software to use it.

## Author

Gunter Miegel 
gm@coinboot.io

## Contribution

Fork this repo. 
Make a pull request to this repo. 
