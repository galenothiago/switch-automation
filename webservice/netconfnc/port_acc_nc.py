#!/bin/python
from ncclient import manager
from config.settings import DEVICE_PARAMS


# LinkType: 1 Access, 2 Trunk, 3 Hybrid


def access(ip, user, password, interface, port_link_type, dados_vlan, desc_of_port):


    xml_port_type_acc = '''
                <nc:config xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
                        <top xmlns="http://www.hp.com/netconf/config:1.0">
                            <Ifmgr>
                                <Interfaces>
                                    <Interface>
                                        <IfIndex>{interface}</IfIndex>
                                        <LinkType>{port_link_type}</LinkType>
                                        <PVID>{number_of_vlan}</PVID>
                                        <Description>{desc_of_port}</Description>
                                    </Interface>
                                </Interfaces>
                            </Ifmgr>
                            <VLAN>
                                <AccessInterfaces>
                                    <Interface>
                                        <IfIndex>{interface}</IfIndex>
                                        <PVID>{number_of_vlan}</PVID>
                                    </Interface>
                                </AccessInterfaces>
                            </VLAN>
                        </top>
                </nc:config>
    '''.format(interface=interface, port_link_type=port_link_type, number_of_vlan=dados_vlan[1], desc_of_port=desc_of_port)

    device_kargs = {'port': 830, 'hostkey_verify': False, 'allow_agent': False,
                    'look_for_keys': False, 'device_params': DEVICE_PARAMS}
    device_kargs['host'] = ip
    device_kargs['username'] = user
    device_kargs['password'] = password

    with manager.connect(**device_kargs) as netconf_manager:
        netconf_manager.edit_config(target='running', config=xml_port_type_acc, default_operation='merge')
