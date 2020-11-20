from flask import Flask,Request,Response,request
import pynetbox
import json

def vlans():
    dict_vlan = request.get_data(as_text=True)
    dados_vlan = json.loads(dict_vlan)
