#!/usr/bin/python3
import json
import os.path
import sys
import requests
import time
from netconfnc import create_vlan_nc, port_acc_nc, port_hyb_nc, port_trunk_nc, undo_port_nc
from netmikossh import create_vlan_ssh, port_acc_ssh, port_hyb_ssh, port_trunk_ssh,undo_port_ssh
from config.settings import USER_SW, PASS_SW, HEADERS, IP_NB


def get_proto_gerencia(url_device):
    get_dic_device = requests.get('http://{}{}'.format(IP_NB,url_device),headers=HEADERS,timeout=5)
    dados_device = get_dic_device.json()
    url_device_type = (dados_device['device_type']['url'])
    print(url_device_type)
    get_dic_dt = requests.get(url_device_type, headers=HEADERS, timeout=5)
    dados_dt =  get_dic_dt.json()
    print(dados_dt)
    protocolo_gerencia = (dados_dt['custom_fields']['protocol']['label'])
    return protocolo_gerencia


def get_ip_sw(url_device):
    get_dic_device = requests.get('http://{}{}'.format(IP_NB,url_device),headers=HEADERS,timeout=5)
    dados_device = get_dic_device.json()
    ip_sw = (dados_device['primary_ip']['address'].split('/')[0])
    return ip_sw


def get_vlans(dict_interfaces):

    dados_interface = json.loads(dict_interfaces)
    data_interface = dados_interface['data']
    tagged_vlans = data_interface['tagged_vlans']
    untagged_vlan = data_interface['untagged_vlan']
    
    try: 
        port_type = data_interface['mode']['value']
    except TypeError:
        port_type = 'null'

    if (port_type) == 'access':

        untagged_vlan = data_interface['untagged_vlan']

        url_vlan_untagged = untagged_vlan['url']
        name_vlan_untagged = untagged_vlan['name']
        vid_vlan_untagged = untagged_vlan['vid']
         
        get_dic_vlan_untagged = requests.get('http://{ip}{url}'.format(ip=IP_NB, url=url_vlan_untagged),headers=HEADERS,timeout=5)
        dados_vlan_untagged = get_dic_vlan_untagged.json()
        description_of_vlan_untagged = dados_vlan_untagged['description']

        vlan_untagged = [name_vlan_untagged, vid_vlan_untagged, description_of_vlan_untagged]

        return vlan_untagged

    elif (port_type) == 'tagged':
        
        untagged_vlan = data_interface['untagged_vlan']
     
        url_vlan_untagged = untagged_vlan['url']
        name_vlan_untagged = untagged_vlan['name']
        vid_vlan_untagged = untagged_vlan['vid']
        
        dict_untagged = requests.get('http://{}{}'.format(IP_NB,url_vlan_untagged),headers=HEADERS,timeout=5)
        description_untagged = dict_untagged.json()['description']

        vlan_untagged = [name_vlan_untagged, vid_vlan_untagged, description_untagged]

        tagged_vlans = data_interface['tagged_vlans']
        port_type = data_interface['mode']['value']
        vlans_tagged = []
        
        dados_tagged = [{'name': tag_vlans['name'], 'vid': tag_vlans['vid']} for tag_vlans in tagged_vlans]

        for  desc in tagged_vlans:

            dict_tagged = requests.get('http://{}{}'.format(IP_NB, desc['url']),headers=HEADERS,timeout=5)
            vlans_tagged.append({'vid': desc['vid'], 'description': dict_tagged.json()['description']})
        
        for  i in range(len(tagged_vlans)):
            if vlans_tagged[i]['vid'] == dados_tagged[i]['vid']:
                vlans_tagged[i].update(dados_tagged[i])

        return [vlan_untagged, vlans_tagged]

    elif (port_type) == 'tagged-all':

        untagged_vlan = data_interface['untagged_vlan']

        url_vlan_untagged = untagged_vlan['url']
        name_vlan_untagged = untagged_vlan['name']
        vid_vlan_untagged = untagged_vlan['vid']
         
        get_dic_vlan_untagged = requests.get('http://{}{}'.format(IP_NB,url_vlan_untagged),headers=HEADERS,timeout=5)
        dados_vlan_untagged = get_dic_vlan_untagged.json()
        description_of_vlan_untagged = dados_vlan_untagged['description']

        vlan_untagged = [name_vlan_untagged, vid_vlan_untagged, description_of_vlan_untagged]

        return vlan_untagged

    else:
        pass


def dados_interface(dict_interfaces):

    dados_interface = json.loads(dict_interfaces)
    data_interface = dados_interface['data']
    interface = data_interface['name']
    url_device = data_interface['device']['url']
    desc_interface = data_interface['description']

    try: 
        port_type = data_interface['mode']['value']
    except TypeError:
        port_type = 'null'

    return [interface, port_type, url_device, desc_interface]


def add_del_vlan_port(url_device, port_type, ip_sw, interface, dados_vlan, desc_of_port):
    protocolo_gerencia = get_proto_gerencia(url_device)

    if protocolo_gerencia == 'SSH':
        if (port_type) == 'access':
            port_link_type = 'access'
            create_vlan_ssh.create_vlan(ip_sw, USER_SW, PASS_SW, port_link_type, dados_vlan)
            port_acc_ssh.access(ip_sw, USER_SW, PASS_SW, interface, port_link_type, dados_vlan, desc_of_port)
        
        elif (port_type) == 'tagged':
            port_link_type = 'hybrid'
            create_vlan_ssh.create_vlan(ip_sw, USER_SW, PASS_SW, port_link_type, dados_vlan)
            port_hyb_ssh.hybrid(ip_sw, USER_SW, PASS_SW, interface, port_link_type, dados_vlan, desc_of_port)
        
        elif (port_type) == 'tagged-all':
            port_link_type = 'trunk'
            create_vlan_ssh.create_vlan(ip_sw, USER_SW, PASS_SW, port_link_type, dados_vlan)
            port_trunk_ssh.trunk(ip_sw, USER_SW, PASS_SW, interface, port_link_type, dados_vlan, desc_of_port)
            
        elif (port_type) == 'null':
            undo_port_ssh.clean_conf(ip_sw, USER_SW, PASS_SW, interface)

    elif protocolo_gerencia == 'NETCONF':

        if (port_type) == 'access':
            port_link_type = '1' # access
            create_vlan_nc.create_vlan(ip_sw, USER_SW, PASS_SW, port_link_type, dados_vlan)
            port_acc_nc.access(ip_sw, USER_SW, PASS_SW, interface, port_link_type, dados_vlan, desc_of_port)
        
        elif (port_type) == 'tagged':
            port_link_type = '3' # hybrid
            create_vlan_nc.create_vlan(ip_sw, USER_SW, PASS_SW, port_link_type, dados_vlan)
            port_hyb_nc.hybrid(ip_sw, USER_SW, PASS_SW, interface, port_link_type, dados_vlan, desc_of_port)
        
        elif (port_type) == 'tagged-all':
            port_link_type = '2' # trunk
            create_vlan_nc.create_vlan(ip_sw, USER_SW, PASS_SW, port_link_type, dados_vlan)
            port_trunk_nc.trunk(ip_sw, USER_SW, PASS_SW, interface, port_link_type, dados_vlan, desc_of_port)
                  
        elif (port_type) == 'null':
            undo_port_nc.clean_conf(ip_sw, USER_SW, PASS_SW, interface)

