# Coinbootmaker

`coinbootmaker` - a little helper to build your own Coinboot plugins.  

## Requirements

* Docker 

* a Debian or Ubuntu build host

* `brctl` which is part of the `bridge-utils` package

## Usage

```
coinbootmaker [-i] -p <file name> <path to initramfs>                                                          

-i              Interactive mode - opens a shell in the build environment                                             
-p <file name>  Plugin to build
-h              Display this help
```

### Example:

```
$ ./coinbootmaker /tmp/coinboot-initramfs-4.15.0-43-generic -p ethminer 
```

`coinbootmaker` takes a path to a Coinboot-Initramfs to create an environment for building the plugins  
by converting the given Initramfs into a Container image and run it.  
A plugin creation script located at `./src` is executed in that `coinbootmaker` container and the resulting  
plugin archive is written to the `./build` directory.

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
