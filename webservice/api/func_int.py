import json
import requests
from flask import Flask, Request, Response, request
from api import func_aux


def interfaces():

    dict_interfaces = request.get_data(as_text=True)
    dados_int = func_aux.dados_interface(dict_interfaces)
    func_aux.add_del_vlan_port(dados_int[2], dados_int[1], func_aux.get_ip_sw(
        dados_int[2]), dados_int[0], func_aux.get_vlans(dict_interfaces), dados_int[3])