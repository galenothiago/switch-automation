#!/usr/bin/python3
from netmiko import ConnectHandler
from shutil import rmtree
from shutil import move
import shutil
import time
import os

def backup_conf(ip, user, password):

    device = {'session_log': 'my_file.out'}
    device['device_type'] = 'hp_comware'
    device['ip']          = str(ip)
    device['username']    = str(user)
    device['password']    = str(password)
    device['blocking_timeout'] = 8
    device['timeout'] = 10

    path = ip 
    file = 'D:/tcc-codes/{}/backup.cfg'.format(ip)

    if os.path.exists(path):
        shutil.copy()
    
    with ConnectHandler(**device) as net_connect:
        net_connect.send_config_from_file(cfg_file)
        net_connect.save_config()
