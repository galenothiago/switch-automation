#!/usr/bin/python3
from netmiko import ConnectHandler
from config.settings import DEVICE_TYPE


def access(ip, user, password, interface, port_link_type, dados_vlans, description_of_port):

    device_kargs = {'device_type': DEVICE_TYPE, 'use_keys': False, 'allow_agent': False}
    device_kargs['ip'] = ip
    device_kargs['username'] = user
    device_kargs['password'] = password

    a = 'interface {interface}'.format(interface=interface)
    b = 'undo port link-type'
    c = 'port link-type {port_link_type}'.format(port_link_type=port_link_type)
    d = 'port {port_link_type} vlan {number_of_vlan}'.format(port_link_type=port_link_type, number_of_vlan=dados_vlans[1])
    e = 'description {description_of_port}'.format(description_of_port=description_of_port)
    config_commands = [a, b, c, d, e]

    with ConnectHandler(**device_kargs) as net_connect:
        net_connect.send_config_set(config_commands)
        net_connect.save_config()

        