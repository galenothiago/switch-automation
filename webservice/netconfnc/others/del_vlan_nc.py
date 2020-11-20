#!/bin/python
from ncclient import manager
from config.settings import DEVICE_PARAMS


def del_vlan_nc(ip, user, password, number_of_vlan):

    xml_del_vlan = '''
                  <nc:config xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
                     <top xmlns="http://www.hp.com/netconf/config:1.0">
                          <VLAN>
                              <VLANs>
                                <VLANID nc:operation="delete">
                                  <ID>{id}</ID>
                                </VLANID>
                              </VLANs>
                          </VLAN>
                    </top>
                  </nc:config>
                 '''.format(id=number_of_vlan)

    device_kargs = {'port': 830, 'hostkey_verify': False, 'allow_agent': False,
                    'look_for_keys': False, 'device_params': DEVICE_PARAMS}
    device_kargs['host'] = ip
    device_kargs['username'] = user
    device_kargs['password'] = password

    with manager.connect(**device_kargs) as netconf_manager:
        netconf_manager.edit_config(
            target='running', config=xml_del_vlan, default_operation='merge')
