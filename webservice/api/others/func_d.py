from flask import Flask, Request, Response, request
import json

def devices():
    dict_device = request.get_data(as_text=True)
    dados_device = json.loads(dict_device)
