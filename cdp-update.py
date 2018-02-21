

import argparse
import ast
import yaml
import re
from netmiko import ConnectHandler


parser = argparse.ArgumentParser(description='Send command to cisco device.')
parser.add_argument('infile', metavar='input file', type=str, nargs=1, help='list of device ip addresses')

args = parser.parse_args()
infile = args.infile[0]

emptyfile = open("cdp_log.txt","w+")
emptyfile.write("---\n")
emptyfile.write("\n")
emptyfile.close()


with open(infile) as f:
    device_list = []
    for device in (yaml.load(f)):
        device_list.append(device)

dev_pattern = re.compile("Device")
intf_pattern = re.compile("interface")


def create_yaml():
    cdp_log = "cdp_log.txt"
    device_dict ={}
    for x in device_list:
        net_connect = ConnectHandler(**x)
        raw_output = net_connect.send_command('show cdp neighbor detail | inc Device|Interface')
        cdp_output = raw_output.splitlines()
        f = open(cdp_log,"a+")
        f.write("- device_type : cisco_ios")
        f.write("\n")
        f.write("  ip : ")
        f.write(x['ip'])
        f.write("\n")
        f.write("  username : cisco")
        f.write("\n")
        f.write("  password : cisco")
        f.write("\n")
        f.write("  interfaces :")
        f.write("\n")
        nbr_list = []
        for line in cdp_output:
            dev = re.match("Device",line)
            intf = re.match("Interface",line)
            if dev:
                device = line.split(":")[1]
                device = device.strip()
                f.write("    - { ")
                f.write("Device : " + '"' + device + '"')
            if intf:
                lport = line.split(",")[0].split(":")[1]
                lport = lport.strip()
                rport = line.split(",")[1].split(":")[1]
                rport = rport.strip()
                f.write(", Lport : " + '"' + lport + '"')
                f.write(", Rport : " + '"' + rport + '"')
                f.write(" }")
                f.write("\n")
    f.close()

create_yaml()

def load_update_list():
    cdp_yaml_file = "cdp_log.txt"
    update_list = []
    with open(cdp_yaml_file) as f:
        for device in (yaml.load(f)):
            update_list.append(device)
    return update_list

for x in load_update_list():
    d = x.copy()
    del d['interfaces']
    net_connect = ConnectHandler(**d)
    interfaces = x['interfaces']
    for interface in interfaces:
        nbr = interface['Device']
        lport = interface['Lport']
        rport = interface['Rport']
        config_cmd = []
        config_cmd.append("interface " + lport)
        config_cmd.append("description "+ '"' + "Connected to " + nbr + "_" + lport + '"')
        print (config_cmd)
        output = net_connect.send_config_set(config_cmd)
        print (output)




