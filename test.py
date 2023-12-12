from tkinter import ttk, filedialog, scrolledtext
from urllib.parse import urlencode
import http.client, base64, json, sys, os, re, tkinter as tk, pandas as pd, asyncio


async def gerar_token():
    # Alterar a url de homologacao para produção depois de finalizado
    url_homologacao = "webservice-homol.facta.com.br"
    path = "/gera-token"
    # Código do usuário master
    usuario = "93862"
    # Senha gerada pelo operador da api do facta
    senha = "3rpl7ds11psjo3cloae6"
    credenciais = f"{usuario}:{senha}"
    credenciais_base64 = base64.b64encode(credenciais.encode()).decode('utf-8')
    connection = http.client.HTTPSConnection(url_homologacao)
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
        expire = response_json["expira"]
        #JanelaComConsole.adicionar_print(JanelaComConsole, f'Expira em: {expire}')
        print(f'Expira em: {expire}')
        return token
    else:
        #JanelaComConsole.adicionar_print(JanelaComConsole, f"Erro na requisição: {response_json['mensagem']}")
        print(f"Erro na requisição: {response_json['mensagem']}")
        return None


async def obter_cidade(token, uf=str, nome=str):
    # Função para buscar o código da cidade na api
    uf = uf.upper()
    nome = nome.upper()
    nome = nome.replace("Ã", "A").replace("À", "A").replace("Á", "A").replace("Â", "A")
    nome = nome.replace("Õ", "O").replace("Ò", "O").replace("Ó", "O").replace("Ô", "O")
    nome = nome.replace("È", "E").replace("É", "E").replace("Ê", "E")
    nome = nome.replace("Í", "I").replace("Ì", "I").replace("Î", "I")
    nome = nome.replace("Ú", "U").replace("Ù", "U").replace("Û", "U")
    nome = nome.replace("Ç", "C")
    nome = nome.replace(" ", "_").strip()

    url = "webservice-homol.facta.com.br"
    endpoint = f"/proposta-combos/cidade?estado={uf}&nome_cidade={nome}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    conn = http.client.HTTPSConnection(url)
    conn.request("GET", endpoint, headers=headers)

    response = conn.getresponse()
    city = json.loads(response.read().decode("utf-8"))
    conn.close()
    with open("cidade.json", "w") as json_file:
        json.dump(city, json_file, indent=2)
    if city['erro'] == True:
        #JanelaComConsole.adicionar_print(JanelaComConsole, f"Cidade não encontrada")
        print("Cidade não encontrada")
    else:
        cidade = city['cidade']
        chave_cidade = list(cidade.keys())[0]
    return chave_cidade


async def simula_port_refin(token):
    # Essa função passa um dicionário codificado para o request
    url_homologacao = "webservice-homol.facta.com.br"
    path = "/proposta/operacoes-disponiveis"
    produto = "D"
    tipo_operacao = "003500"
    averbador = "3"
    convenio = "3"
    opcao_valor = "2"
    valor_parcela = "320"
    prazo = "84"
    cpf = "00000000000"
    data_nascimento = "12/12/1984"
    prazo_restante = "60"
    saldo_devedor = "11230.00"
    valor_parcela_original = "320"
    prazo_original = "84"
    parametros = {
        "produto": produto,
        "tipo_operacao": tipo_operacao,
        "averbador": averbador,
        "convenio": convenio,
        "opcao_valor": opcao_valor,
        "valor_parcela": valor_parcela,
        "prazo": "84",
        "cpf": cpf,
        "data_nascimento": data_nascimento,
        "prazo_restante": prazo_restante,
        "saldo_devedor": saldo_devedor,
        "valor_parcela_original": valor_parcela_original,
        "prazo_original": prazo_original,
    }

    parametros_codificados = urlencode(parametros)
    connection = http.client.HTTPSConnection(url_homologacao)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": "PHPSESSID=olqno6ge8khacr1g3stplm8tmj",
    }

    connection.request("GET", f"{path}?{parametros_codificados}", headers=headers)
    response = connection.getresponse()
    content = response.read().decode("utf-8")
    response_dict = json.loads(content)
    if response_dict['erro'] == True:
        try:
            print(f"Tabela Port:\n{response_dict['tabelas_portabilidade'][0]['tabela']}")
        except:
            print("Sem tabela disponível para portabilidade")
        try:
            print(f"Tabela Refin:\n{response_dict['tabelas_refin_portabilidade'][0]['tabela']}")
        except:
            print("Sem tabela disponível para refin da port")
    else:
        print("Sucesso na simulação")
    with open("simulacao.json", "w") as json_file:
        json.dump(response_dict, json_file, indent=2)
    connection.close()
    return response_dict


async def main():
    TOKEN = await gerar_token()
    chave_cidade = await obter_cidade(TOKEN, "SE", "ARACAJU")
    id_simulacao = await simula_port_refin(TOKEN)
    print(id_simulacao)

# Chame a função principal usando asyncio.run()
asyncio.run(main())
