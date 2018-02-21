# UPDATE INTERFACE DESCRIPTIONS

This script uses netmiko to connect to a list of devices and update their interface descriptions based on CDP

## How it works

* See the devices.yaml file for example list of devices
* Phase 1: It connects to each device and gathers the cdp info
* It creates a file called cdp_log.txt which is also a yaml with an interface list for each devices 
* Phase 2: It connects to each device and updates CDP

## To Run

First you need netmiko:

```
pip install netmiko
```

Then just this command:

```
python3 cdp-update.py devices.yaml
```

## Future

I need to figure out how to do this in one pass and not have to use the "temporary" cdp_log.txt file
