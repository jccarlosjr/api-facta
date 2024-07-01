import http.client, base64, json, sys, os, re, pandas as pd, tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
from urllib.parse import urlencode
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import requests


URL_PROD = "webservice.facta.com.br"
URL_HOMO = "webservice-homol.facta.com.br"

import requests
import base64
import json

def get_token():
    url = "https://webservice-homol.facta.com.br"  # Substitua pela URL correta
    user = "93862"
    password = "3rpl7ds11psjo3cloae6"
    login_data = f"{user}:{password}"
    login_data_base64 = base64.b64encode(login_data.encode()).decode('utf-8')

    headers = {
        "Authorization": f"Basic {login_data_base64}",
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        response_json = response.json()
        if not response_json["erro"]:
            token = response_json["token"]
            return token
        else:
            print(response_json["mensagem"])
    else:
        print(f"Falha na requisição: {response.status_code}, {response.text}")


# Exemplo de chamada da função
token = get_token()
if token:
    print(f"Token: {token}")


token = get_token()
print(token)