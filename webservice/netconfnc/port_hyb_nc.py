#!/bin/python
from ncclient import manager
from config.settings import DEVICE_PARAMS

def hybrid(ip, user, password, interface, port_link_type, dados_vlans, desc_of_port):


    device_kargs = {'port': 830, 'hostkey_verify': False, 'allow_agent': False, 'look_for_keys': False, 'device_params': DEVICE_PARAMS}
    device_kargs['host'] = ip
    device_kargs['username'] = user
    device_kargs['password'] = password

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

    with manager.connect(**device_kargs) as netconf_manager:
        netconf_manager.edit_config(target='running', config=xml_clean_conf, default_operation='replace')

    vlans_tagged = (','.join(str(tag_vlans['vid']) for tag_vlans in dados_vlans[1]))


    xml_port_type_hyb = '''
                <nc:config xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
                        <top xmlns="http://www.hp.com/netconf/config:1.0">
                            <Ifmgr>
                                <Interfaces>
                                    <Interface>
                                        <IfIndex>{interface}</IfIndex>
                                        <LinkType>{port_link_type}</LinkType>
                                        <PVID>{vlan_untagged}</PVID>
                                        <Description>{desc_of_port}</Description>
                                    </Interface>
                                </Interfaces>
                            </Ifmgr>
                            <VLAN>
                                <HybridInterfaces>
                                    <Interface>
                                        <IfIndex>{interface}</IfIndex>
                                        <UntaggedVlanList>{vlan_untagged}</UntaggedVlanList>
                                        <TaggedVlanList>{vlans_tagged}</TaggedVlanList>
                                    </Interface>
                                </HybridInterfaces>
                            </VLAN>
                        </top>
                </nc:config>
    '''.format(vlan_untagged=dados_vlans[0][1], desc_of_port=desc_of_port, interface=interface, vlans_tagged=vlans_tagged, port_link_type=port_link_type)

    with manager.connect(**device_kargs) as netconf_manager:
        netconf_manager.edit_config(target='running', config=xml_port_type_hyb, default_operation='replace')
