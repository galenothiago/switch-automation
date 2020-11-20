#!/bin/python
from ncclient import manager
from config.settings import DEVICE_PARAMS



def clean_conf(ip, user, password, interface):


    xml_clean_conf = '''
                <nc:config xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
                        <top xmlns="http://www.hp.com/netconf/config:1.0">
                            <Ifmgr>
                                <Interfaces>
                                    <Interface>
                                        <IfIndex>{interface}</IfIndex>
                                        <LinkType>1</LinkType>
                                        <PVID>1</PVID>
                                        <Description>Porta Limpa</Description>
                                    </Interface>
                                </Interfaces>
                            </Ifmgr>
                        </top>
                </nc:config>
    '''.format(interface=interface)

    device_kargs = {'port': 830, 'hostkey_verify': False, 'allow_agent': False, 'look_for_keys': False, 'device_params': DEVICE_PARAMS}
    device_kargs['host'] = ip
    device_kargs['username'] = user
    device_kargs['password'] = password

    with manager.connect(**device_kargs) as netconf_manager:
        netconf_manager.edit_config(target='running', config=xml_clean_conf, default_operation='merge')
