#!/usr/bin/python3
from netmiko import ConnectHandler


def get_vlans(device_type, ip, user, password):

    device_kargs = {'blocking_timeout': 8, 'timeout': 10, }
    device_kargs['device_type'] = device_type
    device_kargs['ip'] = str(ip)
    device_kargs['username'] = str(user)
    device_kargs['password'] = str(password)

    command = 'dis vlan'

    with ConnectHandler(**device_kargs) as net_connect:
        return net_connect.send_command(command)