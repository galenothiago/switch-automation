from flask import Flask, Request, Response, request
from config.settings import IP_NB,HEADERS
import json
import requests

def ip():
    dict_ip = request.get_data(as_text=True)
    dados_ip = json.loads(dict_ip)
    data = dados_ip['data']
    url_api = data['url']
    res = requests.get('http://{}{}'.format(IP_NB,url_api),headers=HEADERS,timeout=5)
    dados_api = res.json()
    data_api = dados_ip['data']