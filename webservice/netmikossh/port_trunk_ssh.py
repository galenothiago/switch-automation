#!/usr/bin/python3
from netmiko import ConnectHandler
from config.settings import DEVICE_TYPE


def trunk(ip, user, password, interface, port_link_type, dados_vlans, description_of_port):

    device_kargs = {'device_type': DEVICE_TYPE, 'use_keys': False, 'allow_agent': False, 'conn_timeout': 30}
    device_kargs['ip'] = ip
    device_kargs['username'] = user
    device_kargs['password'] = password

    a = 'interface {interface}'.format(interface=interface)
    b = 'undo port link-type'
    c = 'port link-type {port_link_type}'.format(port_link_type=port_link_type)
    d = 'undo port trunk permit vlan 1'
    e = 'port {port_link_type} permit vlan all'.format(port_link_type=port_link_type)
    f = 'description {description_of_port}'.format(description_of_port=description_of_port)
    g = 'port {port_link_type} pvid {vlan_pvid}'.format(port_link_type=port_link_type, vlan_pvid=dados_vlans[1])

    config_commands = [a, b, c, d, e, f]

    with ConnectHandler(**device_kargs) as net_connect:
        net_connect.send_config_set(config_commands)
        net_connect.save_config()
