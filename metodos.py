import http.client
import json
import base64



def obter_estado_civil(token):
    url = "webservice.facta.com.br"
    endpoint = "/proposta-combos/estado-civil"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    conn = http.client.HTTPSConnection(url)
    conn.request("GET", endpoint, headers=headers)

    response = conn.getresponse()
    estado_civil_data = json.loads(response.read().decode("utf-8"))
    conn.close()
    #retorna um dicionário com  outro dicionário dentro chamado estado_civil
    #para acessar o valor de solteiro = id_estado_civil['estado_civil']['4']
    # {'erro': False, 'estado_civil': 
    # {'3': 'CASADO', 
    # '7': 'DESQUITADO', 
    # '2': 'DIVORCIADO', 
    # '8': 'NAO CADASTRADO', 
    # '9999': 'NAO DEFINIDO', 
    # '6': 'OUTROS', 
    # '1': 'SEPARADO', 
    # '4': 'SOLTEIRO', 
    # '9': 'UNIÃO ESTÁVEL', 
    # '5': 'VIUVO'}}
    return estado_civil_data


def obter_estado(token):
    url = "webservice.facta.com.br"
    endpoint = "/proposta-combos/estado"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    conn = http.client.HTTPSConnection(url)
    conn.request("GET", endpoint, headers=headers)

    response = conn.getresponse()
    estado = json.loads(response.read().decode("utf-8"))
    conn.close()
    with open("estado.json", "w") as json_file:
        json.dump(estado, json_file, indent=2)
    # Retorna um dicionário com  outro dicionário dentro chamado estado
    # As chaves dos dicionários são as UFs e os valores de cada chave é o nome do estado
    # 'estado': {'SC': 'SANTA CATARINA', 'SP': 'SAO PAULO', 'SE': 'SERGIPE'}
    return estado


def obter_orgao(token):
    url = "webservice.facta.com.br"
    endpoint = "/proposta-combos/orgao-emissor"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    conn = http.client.HTTPSConnection(url)
    conn.request("GET", endpoint, headers=headers)

    response = conn.getresponse()
    estado = json.loads(response.read().decode("utf-8"))
    conn.close()
    # Retorna um dicionário com  outro dicionário dentro chamado orgao_emissor
    # As chaves dos dicionários são as siglas dos orgaos e os valores de cada chave são os nomes completos
    # 'estado': {'SSP': 'Secretaria de Segurança Pública do Estado', 'DETRAN': 'Carteira Nacional de Habilitação'}
    return estado



def obter_patrimonio(token):
    url = "webservice.facta.com.br"
    endpoint = "/proposta-combos/valor-patrimonial"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    conn = http.client.HTTPSConnection(url)
    conn.request("GET", endpoint, headers=headers)

    response = conn.getresponse()
    patrimonio = json.loads(response.read().decode("utf-8"))
    conn.close()
    with open("patrimonio.json", "w") as json_file:
        json.dump(patrimonio, json_file, indent=2)
    return patrimonio


def obter_especie(token):
    url = "webservice.facta.com.br"
    endpoint = "/proposta-combos/tipo-beneficio"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    conn = http.client.HTTPSConnection(url)
    conn.request("GET", endpoint, headers=headers)

    response = conn.getresponse()
    especie = json.loads(response.read().decode("utf-8"))
    conn.close()
    with open("especie.json", "w") as json_file:
        json.dump(especie, json_file, indent=2)
    # Retorna um dicionário com  outro dicionário dentro chamado especie
    # As chaves dos dicionários são os códigos dos benefícios e os valores de cada chave são a descrição da espécie
    # 'estado': {'21': 'PENSÃO POR MORTE PREVIDENCIÁRIA', '42': 'APOSENTADORIA POR TEMPO DE CONTRIBUIÇÃO'}
    return especie
