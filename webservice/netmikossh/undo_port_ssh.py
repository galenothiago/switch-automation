#!/usr/bin/python3
from netmiko import ConnectHandler
from config.settings import DEVICE_TYPE

def clean_conf(ip, user, password, interface):
    
    device_kargs = {'device_type': DEVICE_TYPE, 'use_keys': False, 'allow_agent': False, 'conn_timeout': 30}
    device_kargs['ip'] = ip
    device_kargs['username'] = user
    device_kargs['password'] = password

    
    a = 'interface {interface}'.format(interface=interface)
    b = 'undo desc'
    c = 'undo port link-type'
    config_command = [a, b, c]

    with ConnectHandler(** device_kargs) as net_connect:
        net_connect.send_config_set(config_command)
        net_connect.save_config()