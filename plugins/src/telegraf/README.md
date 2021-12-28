# Coinboot Telegraf plugin

As we have to compile the Telegraf binary with an adapted configuration containing only a minimal subset of the available 
Telegraf plugins we keep a local copy of the upstream sources.  
The local copy of the upstream repository is done with `git subtree`.

## Pull upstream Telegraf repository  

$ git subtree pull --prefix plugins/src/telegraf/upstream git@github.com:influxdata/telegraf.git master --squash

## Custom configuration

### Reduced subset of plugins

Telegraf supports a wide range of plugins which create a quite huge binary.  
To minize the Telegraf binary we provide a redcued subset of plugins to be include.  
The custom configuration which plugins are included in our custom Telegraf binary resided inside the `conf` directory and is appliad against the local copy of the upstream source and overwrites the upstream plugin include configuration.

### Shrinked binary size

By striping off symbol tables and debugging information during compilation with `-ldflags="-s -w"` we can reduce the binary size by 25%.

## Build with `coinbootmaker_helper`

```
$ pipenv run ./coinbootmaker_helper create plugin src/telegraf/telegraf.yaml
```
