#!/usr/bin/python3
from netmiko import ConnectHandler

def undo_vlan(ip, user, password, number_of_vlan):
    
    device = dict()
    device['device_type']      = 'hp_comware'
    device['ip']               = str(ip)
    device['username']         = str(user)
    device['password']         = str(password)
    device['blocking_timeout'] = 8
    device['timeout']          = 10
    
    config_command = f'undo vlan {number_of_vlan}'

    with ConnectHandler(**device) as net_connect:
        net_connect.send_config_set(config_command)
        net_connect.save_config()
