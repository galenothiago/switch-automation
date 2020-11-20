#!/usr/bin/python3
from netmiko import ConnectHandler
from config.settings import DEVICE_TYPE


def hybrid(ip, user, password, interface, port_link_type, dados_vlans, description_of_port):

    device_kargs = {'device_type': DEVICE_TYPE, 'use_keys': False, 'allow_agent': False, 'conn_timeout': 30}
    device_kargs['ip'] = ip
    device_kargs['username'] = user
    device_kargs['password'] = password

    vlans_tagged = (' '.join(str(tag_vlans['vid']) for tag_vlans in dados_vlans[1]))

    a = 'interface {interface}'.format(interface=interface)
    b = 'undo port link-type'
    c = 'port link-type {port_link_type}'.format(port_link_type=port_link_type)
    d = 'undo port hybrid vlan 1'
    e = 'port {port_link_type} vlan {vlan_untagged} untagged'.format(port_link_type=port_link_type, vlan_untagged=dados_vlans[0][1])
    f = 'port {port_link_type} vlan {vlans_tagged} tagged'.format(port_link_type=port_link_type, vlans_tagged=vlans_tagged)
    g = 'port hybrid pvid vlan {vlan_untagged}'.format(vlan_untagged=dados_vlans[0][1])
    h = 'description {description_of_port}'.format(description_of_port=description_of_port)
    config_commands = [a, b, c, d, e, f, g, h]

    with ConnectHandler() as net_connect:
        net_connect.send_config_set(config_commands)
        net_connect.save_config()
