#!/usr/bin/python3
from netmiko import ConnectHandler
from config.settings import DEVICE_TYPE

def create_vlan(ip, user, password, port_link_type, dados_vlans):

    device_kargs = {'device_type': DEVICE_TYPE, 'use_keys': False, 'allow_agent': False, 'conn_timeout': 30}
    device_kargs['ip'] = ip
    device_kargs['username'] = user
    device_kargs['password'] = password

    if port_link_type == 'access':

        a = 'vlan {number_of_vlan}'.format(number_of_vlan=dados_vlans[1])
        b = 'name {name_of_vlan}'.format(name_of_vlan=dados_vlans[0])
        c = 'description {description_of_vlan}'.format(description_of_vlan=dados_vlans[2])
        config_commands = [a, b, c]

        with ConnectHandler(**device_kargs) as net_connect:
            j = net_connect.send_config_set(config_commands)
            print(j)
            net_connect.save_config()

    elif port_link_type == 'hybrid':

        # CRIA VLAN UNTAGGED
        a = 'vlan {number_of_vlan}'.format(number_of_vlan=dados_vlans[0][1])
        b = 'name {name_of_vlan}'.format(name_of_vlan=dados_vlans[0][0])
        c = 'description {description_of_vlan}'.format(description_of_vlan=dados_vlans[0][2])
        config_commands1 = [a, b, c]

        with ConnectHandler(**device_kargs) as net_connect:
            p = net_connect.send_config_set(config_commands1)
            print(p)
            net_connect.save_config()

        # CRIA VLANS TAGGED

        with ConnectHandler(**device_kargs) as net_connect:
                    
            for tag_vlans in (dados_vlans[1]):

                a = 'vlan {number_of_vlan}'.format(number_of_vlan=tag_vlans['vid'])
                b = 'name {name_of_vlan}'.format(name_of_vlan=tag_vlans['name'])
                c = 'description {description_of_vlan}'.format(description_of_vlan=tag_vlans['description'])
                config_commands2 = [a, b, c]

                net_connect.send_config_set(config_commands2)

            net_connect.save_config()

        
    elif port_link_type == 'trunk':

        a = 'vlan {number_of_vlan}'.format(number_of_vlan=dados_vlans[1])
        b = 'name {name_of_vlan}'.format(name_of_vlan=dados_vlans[0])
        c = 'description {description_of_vlan}'.format(description_of_vlan=dados_vlans[2])
        config_commands = [a, b, c]

        with ConnectHandler(**device_kargs) as net_connect:
            net_connect.send_config_set(config_commands)
            net_connect.save_config()