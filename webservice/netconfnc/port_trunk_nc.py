#!/bin/python
from ncclient import manager
from config.settings import DEVICE_PARAMS


def trunk(ip, user, password, interface, port_link_type, dados_vlan, desc_of_port):


    xml_clean_conf = '''
                <nc:config xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
                        <top xmlns="http://www.hp.com/netconf/config:1.0">
                            <Ifmgr>
                                <Interfaces>
                                    <Interface>
                                        <IfIndex>{interface}</IfIndex>
                                        <LinkType>1</LinkType>
                                    </Interface>
                                </Interfaces>
                            </Ifmgr>
                        </top>
                </nc:config>
    '''.format(interface=interface)

    xml_port_type_trunk = '''
                <nc:config xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
                        <top xmlns="http://www.hp.com/netconf/config:1.0">
                            <Ifmgr>
                                <Interfaces>
                                    <Interface>
                                        <IfIndex>{interface}</IfIndex>
                                        <LinkType>{port_link_type}</LinkType>
                                        <Description>{desc_of_port}</Description>
                                        <PVID>{number_of_vlan}</PVID>
                                    </Interface>
                                </Interfaces>
                            </Ifmgr>
                            <VLAN>
                                <TrunkInterfaces>
                                    <Interface>
                                        <IfIndex>{interface}</IfIndex>
                                        <PermitVlanList>1-4094</PermitVlanList>
                                    </Interface>
                                </TrunkInterfaces>
                            </VLAN>
                        </top>
                    </nc:config>
    '''.format(interface=interface, port_link_type=port_link_type, number_of_vlan=dados_vlan[1], desc_of_port=desc_of_port)

    device_kargs = {'port': 830, 'hostkey_verify': False, 'allow_agent': False, 'look_for_keys': False, 'device_params': DEVICE_PARAMS}
    device_kargs['host'] = ip
    device_kargs['username'] = user
    device_kargs['password'] = password

    with manager.connect(**device_kargs) as netconf_manager:
        netconf_manager.edit_config(target='running', config=xml_clean_conf, default_operation='merge')
        netconf_manager.edit_config(target='running', config=xml_port_type_trunk, default_operation='merge')
