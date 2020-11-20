#!/usr/bin/python3
from netmiko import ConnectHandler
from shutil import rmtree
from shutil import move
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
    commands = (r"display current-configuration")

    with ConnectHandler(**device) as net_connect:
        backup_in_file = net_connect.send_command_timing(commands)

    with open('backup.cfg', 'w') as file:
        file.write(backup_in_file)

    if os.path.exists(path):
        rmtree(path, ignore_errors=False, onerror=None)
        os.makedirs(path)
        move('backup.cfg', path)
    else:
        os.makedirs(path)
        move('backup.cfg', path)