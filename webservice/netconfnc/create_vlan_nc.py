#!/bin/python
import json
import requests
from ncclient import manager
from config.settings import DEVICE_PARAMS


def create_vlan(ip, user, password, port_link_type, dados_vlan):

    device_kargs = {'port': 830, 'hostkey_verify': False, 'allow_agent': False,
                    'look_for_keys': False, 'device_params': DEVICE_PARAMS}
    device_kargs['host'] = ip
    device_kargs['username'] = user
    device_kargs['password'] = password

    if (port_link_type) == '1':  # Access

        xml_create_vlan = '''
                    <nc:config xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
                      <top xmlns="http://www.hp.com/netconf/config:1.0">
                            <VLAN>
                                <VLANs>
                                  <VLANID>
                                    <ID>{number_of_vlan}</ID>
                                    <Description>{description_of_vlan}</Description>
                                    <Name>{name_of_vlan}</Name>
                                  </VLANID>
                                </VLANs>
                            </VLAN>
                      </top>
                    </nc:config>
                  '''.format(number_of_vlan=dados_vlan[1], 
                  description_of_vlan=dados_vlan[2], name_of_vlan=dados_vlan[0])

        with manager.connect(**device_kargs) as netconf_manager:
            netconf_manager.edit_config(
                target='running', config=xml_create_vlan, default_operation='merge')

    elif (port_link_type) == '3':  # Tagged

        xml_create_vlan = '''
                    <nc:config xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
                      <top xmlns="http://www.hp.com/netconf/config:1.0">
                            <VLAN>
                                <VLANs>
                                  <VLANID>
                                    <ID>{number_of_vlan}</ID>
                                    <Description>{description_of_vlan}</Description>
                                    <Name>{name_of_vlan}</Name>
                                  </VLANID>
                                </VLANs>
                            </VLAN>
                      </top>
                    </nc:config>
                  '''.format(number_of_vlan=dados_vlan[0][1], description_of_vlan=dados_vlan[0][2], name_of_vlan=dados_vlan[0][0])

        with manager.connect(**device_kargs) as netconf_manager:
            netconf_manager.edit_config(
                target='running', config=xml_create_vlan, default_operation='merge')

        for tag_vlans in (dados_vlan[1]):

            xml_create_vlan = '''
                          <nc:config xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
                            <top xmlns="http://www.hp.com/netconf/config:1.0">
                                  <VLAN>
                                      <VLANs>
                                        <VLANID>
                                          <ID>{number_of_vlan}</ID>
                                          <Description>{description}</Description>
                                          <Name>{name}</Name>
                                        </VLANID>
                                      </VLANs>
                                  </VLAN>
                            </top>
                          </nc:config>
                        '''.format(number_of_vlan=tag_vlans['vid'], name=tag_vlans['name'], description=tag_vlans['description'])

            with manager.connect(**device_kargs) as netconf_manager:
                netconf_manager.edit_config(
                    target='running', config=xml_create_vlan, default_operation='merge')

    elif (port_link_type) == '2':  # Trunk

        xml_create_vlan = '''
                    <nc:config xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
                      <top xmlns="http://www.hp.com/netconf/config:1.0">
                            <VLAN>
                                <VLANs>
                                  <VLANID>
                                    <ID>{number_of_vlan}</ID>
                                    <Description>{description_of_vlan}</Description>
                                    <Name>{name_of_vlan}</Name>
                                  </VLANID>
                                </VLANs>
                            </VLAN>
                      </top>
                    </nc:config>
                  '''.format(number_of_vlan=dados_vlan[1], description_of_vlan=dados_vlan[2], name_of_vlan=dados_vlan[0])

        with manager.connect(**device_kargs) as netconf_manager:
            netconf_manager.edit_config(
                target='running', config=xml_create_vlan, default_operation='merge')
