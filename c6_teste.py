import http.client, base64, json, sys, os, re, pandas as pd, tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
from urllib.parse import urlencode


def gerar_token():
    username = "01067744509_000873"
    username = username.encode()
    password = "Senha@3030"
    password = password.encode()
    url = f"https://marketplace-proposal-in.hom.core.gondor.infra/auth/token?username={username}&password={password}"
    # credenciais = f"{usuario}:{senha}"
    # credenciais_base64 = base64.b64encode(credenciais.encode()).decode('utf-8')
    connection = http.client.HTTPSConnection(url)
    headers = {
        "Authorization": f"Basic {credenciais_base64}",
        "Content-Type": "application/json",
    }
    connection.request("GET", path, headers=headers)
    response = connection.getresponse()
    content = response.read().decode("utf-8")
    response_json = json.loads(content)
    connection.close()
    if response_json["erro"] is False:
        token = response_json["token"]
        return token
    else:
        print(f"Erro na requisição: {response_json['mensagem']}")
        return None