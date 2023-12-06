from tkinter import ttk, filedialog, scrolledtext
from urllib.parse import urlencode
import http.client, base64, json, sys, os, re, tkinter as tk, pandas as pd



class JanelaComConsole:
    def __init__(self, root):
        self.root = root
        self.root.title("API digitação port facta")

        # Criar um widget Text para o console
        self.console = scrolledtext.ScrolledText(root, wrap="none", width=40, height=10)
        self.console.grid(row=3, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")

        # Configurar o peso das colunas e linhas para expandir com a janela
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Centralizar o texto no console
        self.console.tag_configure("center", justify="center")

        # Redefinir a função print para escrever no console
        self.stdout_original = sys.stdout
        sys.stdout = self.ConsoleRedirector(self.console)

        # Elementos adicionais
        info_label = ttk.Label(root, text="Selecione um arquivo")
        info_label.grid(row=0, column=0, columnspan=5)

        parcela_confirma = ttk.Button(root, text="Select", command=lambda: select_file_facta(token_gerado))
        parcela_confirma.grid(row=1, column=0, columnspan=5)

        botao = ttk.Button(root, text="Digitar", command=lambda: digitar_port(token_gerado))
        botao.grid(row=2, column=0, columnspan=5)

    class ConsoleRedirector:
        def __init__(self, console):
            self.console = console

        def write(self, text):
            self.console.insert(tk.END, text, "center")
            self.console.see(tk.END)  # Rolar automaticamente para o final do texto

    def adicionar_print(self, texto):
        print(texto)

    def restaurar_print_original(self):
        sys.stdout = self.stdout_original
        self.root.destroy()


def gerar_token():
    #Alterar a url de homologacao para produção depois de finalizado
    url_homologacao = "webservice.facta.com.br"
    path = "/gera-token"
    #Código do usuário master
    usuario = "93862"
    #Senha gerada pelo operador da api do facta
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
        print(f'Token: {token}')
        print(f'Expira em: {expire}')
        return token
    else:
        print(f'Erro na requisição: {response_json["mensagem"]}')
        return None


token_gerado = gerar_token()


def obter_cidade(token, uf=str, nome=str):
    uf = uf.upper()
    nome = nome.upper()
    nome = nome.replace("Ã", "A").replace("À", "A").replace("Á", "A").replace("Â", "A")
    nome = nome.replace("Õ", "O").replace("Ò", "O").replace("Ó", "O").replace("Ô", "O")
    nome = nome.replace("È", "E").replace("É", "E").replace("Ê", "E")
    nome = nome.replace("Í", "I").replace("Ì", "I").replace("Î", "I")
    nome = nome.replace("Ú", "U").replace("Ù", "U").replace("Û", "U")
    nome = nome.replace("Ç", "C")
    nome = nome.replace(" ", "_").strip()

    url = "webservice.facta.com.br"
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
    cidade = city['cidade']
    chave_cidade = list(cidade.keys())[0]
    if city['erro'] == True:
        JanelaComConsole.adicionar_print(JanelaComConsole, f"{city}")
    else:
        pass
    return chave_cidade


def select_file_facta(token_gerado):
    arquivo_path = filedialog.askopenfilename(
        title="Selecione um arquivo", filetypes=[("Arquivos Excel", "*.xlsx;*.xls")])
    if arquivo_path:
        nome_arquivo = os.path.basename(arquivo_path)
        JanelaComConsole.adicionar_print(JanelaComConsole, f"Arquivo selecionado: {nome_arquivo}")
        global base
        base = pd.read_excel(arquivo_path)
        nome = str(base['NOME'].values[0]).upper()
        cpf = str(base['CPF'].values[0]).replace("-", "").replace(".", "")
        data_nascimento = str(base['NASCIMENTO'].values[0])
        sexo = str(base['SEXO'].values[0])[0]
        if sexo == "n":
            sexo = "F"
        identidade = str(base['IDENTIDADE'].values[0]).replace("-", "").replace(".", "")
        mae = str(base['MAE'].values[0]).upper()
        pai = str(base['PAI'].values[0]).upper()
        uf_nascimento = str(base['UF_NASCIMENTO'].values[0]).upper()
        cidade_nascimento = str(base['CIDADE_NASCIMENTO'].values[0]).upper()
        ddd = str(base['DDD_2'].values[0])
        celular = str(base['CELULAR'].values[0])
        telefone = f'(0{ddd}) {celular[0:5]}-{celular[5:]}'
        cep = str(base['CEP'].values[0]).replace("-", "").replace(".", "")
        endereco = remove_special_char(str(base['ENDERECO'].values[0]).upper())
        uf_endereco = str(base['UF_ENDERECO'].values[0]).upper()
        numero = str(base['NUMERO'].values[0]).replace("-", "").replace(".", "").strip()
        cidade_endereco = str(base['CIDADE'].values[0]).upper()
        bairro = str(base['BAIRRO'].values[0]).upper()
        especie = str(base['ESPECIE'].values[0])
        matricula = str(base['MATRICULA'].values[0]).replace("-", "").replace(".", "")
        salario = str(base['SALARIO'].values[0]).replace(".", "").replace(",", ".").replace("R", "").replace("$", "").strip()
        uf_nb = str(base['UF_NB'].values[0]).upper()
        banco = bank_3char(str(base['BANCO_NB'].values[0]))
        agencia = agency_4char(str(base['AGENCIA_NB'].values[0]))
        conta = str(base['CONTA_NB'].values[0]) + str(base['DV_NB'].values[0])
        banco_port = bank_3char(str(base['BANCO_PORT'].values[0]))
        contrato_port = str(base['NUM_CONTRATO'].values[0]).replace("-", "").replace("/", "").replace("_", "")
        parcela_total = bank_3char(str(base['NUM_PARCELA_TOTAL'].values[0])).replace("[", "").replace("]", "").replace("'", "")
        parcela_restante = str(base['PAR_RESTANTE'].values[0])
        parcela = str(base['PARCELA'].values[0]).replace(".", "").replace(",", ".")
        saldo = str(base['SALDO'].values[0]).replace(".", "").replace(",", ".")
        global cliente
        cliente = {
            "cpf": cpf,
            "data_nascimento": data_nascimento,
            "nome": nome,
            "sexo": sexo, #M ou F
            "estado_civil": "4", #4 para Solteiro
            "rg": identidade,
            "estado_rg": uf_nascimento,
            "orgao_emissor": "SSP",
            "data_expedicao": "16/05/2017",
            "estado_natural": uf_nascimento,
            "cidade_cliente": cidade_nascimento,
            "cidade_natural": obter_cidade(token_gerado, uf_nascimento, cidade_nascimento),
            "nacionalidade": "1",
            "celular": telefone,
            "renda": "3372.57",
            "cep": cep,
            "endereco": endereco,
            "numero": numero,
            "complemento": "CASA",
            "bairro": bairro,
            "cidade_endereco": cidade_endereco,
            "estado": uf_endereco,
            "cidade": obter_cidade(token_gerado, uf_endereco, cidade_endereco),
            "nome_mae": mae,
            "nome_pai": pai,
            "valor_patrimonio": "1",
            "cliente_iletrado_impossibilitado": "N",
            "banco": banco,
            "agencia": agencia,
            "conta": conta,
            "matricula": matricula,
            "tipo_credito_nb": "1",
            "tipo_beneficio": especie,
            "estado_beneficio": uf_nb,
            "banco_pagamento": banco,
            "agencia_pagamento": agencia,
            "conta_pagamento": conta,
            "valor_parcela": parcela,
            "prazo_original": parcela_total,
            "prazo_restante": parcela_restante,
            "saldo_devedor": saldo,
            "banco_originador": banco_port,
            "numero_contrato": contrato_port,
        }
        return


def simula_port_refin(token, cliente):
    # Essa função passa um dicionário codificado para o request 
    url_homologacao = "webservice.facta.com.br"
    path = "/proposta/operacoes-disponiveis"
    produto = "D"
    tipo_operacao = "003500"
    averbador = "3"
    convenio = "3"
    opcao_valor = "2"
    valor_parcela = cliente["valor_parcela"]
    prazo = cliente["prazo_original"]
    cpf = cliente["cpf"]
    data_nascimento = cliente["data_nascimento"]
    prazo_restante = cliente["prazo_restante"]
    saldo_devedor = cliente["saldo_devedor"]
    valor_parcela_original = cliente["valor_parcela"]
    prazo_original = cliente["prazo_original"]
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
        print(response_dict)
        JanelaComConsole.adicionar_print(JanelaComConsole, f"Tabela Port:\n{response_dict['tabelas_portabilidade']}")
        JanelaComConsole.adicionar_print(JanelaComConsole, f"Tabela Refin:\n{response_dict['tabelas_refin_portabilidade']}")
    else:
        JanelaComConsole.adicionar_print(JanelaComConsole, "Sucesso na simulação")
    with open("simulacao.json", "w") as json_file:
        json.dump(response_dict, json_file, indent=2)
    connection.close()
    return response_dict


def grava_port(resultado_dict, token):
    # Essa função vai passar uma url no body com os dados retornados da função simula_port_refin
    url_homologacao = "webservice.facta.com.br"
    path = "/proposta/etapa1-simulador"
    cpf = cliente["cpf"]
    data_nascimento = cliente["data_nascimento"]
    login_certificado = "93862_01067744509"
    valor_operacao = resultado_dict['tabelas_portabilidade'][0]['contrato']
    coeficiente = resultado_dict['tabelas_portabilidade'][0]['coeficiente']
    valor_parcela = resultado_dict['tabelas_portabilidade'][0]['parcela']
    prazo = resultado_dict['tabelas_portabilidade'][0]['prazo']
    saldo_devedor = resultado_dict['tabelas_portabilidade'][0]['contrato']
    codigo_tabela = resultado_dict['tabelas_portabilidade'][0]['codigoTabela']
    prazo_original = cliente["prazo_original"]
    
    body = (
        f"produto=D&tipo_operacao=003500&averbador=3&convenio=3&cpf={cpf}"
        f"&data_nascimento={data_nascimento}&login_certificado={login_certificado}&valor_operacao={valor_operacao}"
        f"&coeficiente={coeficiente}&valor_parcela={valor_parcela}&prazo={prazo}&saldo_devedor={saldo_devedor}"
        f"&codigo_tabela={codigo_tabela}&prazo_original={prazo_original}"
    )

    connection = http.client.HTTPSConnection(url_homologacao)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": " PHPSESSID=cup7bgnk6ou2nppmvlh5hlf20o",
    }

    connection.request("POST", path, body, headers)
    response = connection.getresponse()
    content = response.read().decode("utf-8")
    response_dict = json.loads(content)
    if response_dict['erro'] == True:
        #print(response_dict)
        JanelaComConsole.adicionar_print(JanelaComConsole, f"{response_dict}")
    else:
        #print(f"{response_dict['mensagem']}\nID Simulador = {response_dict['id_simulador']}")
        JanelaComConsole.adicionar_print(JanelaComConsole,f"{response_dict['mensagem']}\nID Simulador = {response_dict['id_simulador']}")
    connection.close()
    return response_dict


def grava_refin(id_simulador, resultado_dict, token):
    # Essa função vai passar uma url no body com os dados do refin e salvar no id_simulador da função grava_port
    url_homologacao = "webservice.facta.com.br"
    path = "/proposta/etapa1-refin-portabilidade"
    banco_compra = cliente["banco_originador"]
    contrato_compra = cliente["numero_contrato"]
    prazo_restante = cliente["prazo_restante"]
    saldo_devedor = cliente["saldo_devedor"]
    parcela_original = cliente["valor_parcela"]
    codigo_tabela = resultado_dict['tabelas_refin_portabilidade'][0]['codigoTabela']
    coeficiente = resultado_dict['tabelas_refin_portabilidade'][0]['coeficiente']
    valor_operacao = resultado_dict['tabelas_refin_portabilidade'][0]['contrato']
    valor_parcela = resultado_dict['tabelas_refin_portabilidade'][0]['parcela']
    body = (
        f"id_simulador={id_simulador}&banco_compra={banco_compra}&contrato_compra={contrato_compra}&prazo_restante={prazo_restante}"
        f"&saldo_devedor={saldo_devedor}&parcela_original={parcela_original}&prazo=84"
        f"&codigo_tabela={codigo_tabela}&coeficiente={coeficiente}&valor_operacao={valor_operacao}&valor_parcela={valor_parcela}"
    )

    connection = http.client.HTTPSConnection(url_homologacao)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": " PHPSESSID=cup7bgnk6ou2nppmvlh5hlf20o",
    }

    connection.request("POST", path, body, headers)
    response = connection.getresponse()
    content = response.read().decode("utf-8")
    response_dict = json.loads(content)
    if response_dict['erro'] == True:
        #print(response_dict)
        JanelaComConsole.adicionar_print(JanelaComConsole, f"{response_dict}")
        
    else:
        # print(f"{response_dict['mensagem']}")
        JanelaComConsole.adicionar_print(JanelaComConsole, f"{response_dict['mensagem']}")
    connection.close()
    return response_dict


def dados_pessoais(id_simulador, token, cliente):
    # Essa função vai passar uma url no body com os dados do cliente e salvar no id_simulador da função grava_port
    # Que já possui os dados do refin da função grava_refin
    url_homologacao = "webservice.facta.com.br"
    path = "/proposta/etapa2-dados-pessoais"
    cpf = cliente["cpf"]
    nome = cliente["nome"]
    sexo = cliente["sexo"]
    estado_civil = cliente["estado_civil"]
    data_nascimento = cliente["data_nascimento"]
    rg = cliente["rg"]
    estado_rg = cliente["estado_rg"]
    orgao_emissor = cliente["orgao_emissor"]
    data_expedicao = cliente["data_expedicao"]
    estado_natural = cliente["estado_natural"]
    cidade_natural = cliente["cidade_natural"]
    nacionalidade = cliente["nacionalidade"]
    celular = cliente["celular"]
    renda = cliente["renda"]
    cep = cliente["cep"]
    endereco = cliente["endereco"]
    numero = cliente["numero"]
    complemento = cliente["complemento"]
    bairro = cliente["bairro"]
    cidade = cliente["cidade"]
    estado = cliente["estado"]
    nome_mae = cliente["nome_mae"]
    nome_pai = cliente["nome_pai"]
    valor_patrimonio = cliente["valor_patrimonio"]
    cliente_iletrado_impossibilitado = cliente["cliente_iletrado_impossibilitado"]
    banco = cliente["banco"]
    agencia = cliente["agencia"]
    conta = cliente["conta"]
    matricula = cliente["matricula"]
    tipo_credito_nb = cliente["tipo_credito_nb"]
    tipo_beneficio = cliente["tipo_beneficio"]
    estado_beneficio = cliente["estado_beneficio"]
    banco_pagamento = cliente["banco_pagamento"]
    agencia_pagamento = cliente["agencia_pagamento"]
    conta_pagamento = cliente["conta_pagamento"]

    connection = http.client.HTTPSConnection(url_homologacao)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": " PHPSESSID=cup7bgnk6ou2nppmvlh5hlf20o",
    }

    body = (
        f"id_simulador={id_simulador}&cpf={cpf}&nome={nome}&sexo={sexo}&estado_civil={estado_civil}"
        f"&data_nascimento={data_nascimento}&rg={rg}&estado_rg={estado_rg}&orgao_emissor={orgao_emissor}"
        f"&data_expedicao={data_expedicao}&estado_natural={estado_natural}&cidade_natural={cidade_natural}"
        f"&nacionalidade={nacionalidade}&celular={celular}&renda={renda}&cep={cep}&endereco={endereco}"
        f"&numero={numero}&complemento={complemento}&bairro={bairro}&cidade={cidade}&estado={estado}"
        f"&nome_mae={nome_mae}&nome_pai={nome_pai}&valor_patrimonio={valor_patrimonio}"
        f"&cliente_iletrado_impossibilitado={cliente_iletrado_impossibilitado}&banco={banco}&agencia={agencia}"
        f"&conta={conta}&matricula={matricula}&tipo_credito_nb={tipo_credito_nb}&tipo_beneficio={tipo_beneficio}"
        f"&estado_beneficio={estado_beneficio}&banco_pagamento={banco_pagamento}&agencia_pagamento={agencia_pagamento}&conta_pagamento={conta_pagamento}"
    )

    connection.request("POST", path, body, headers)
    response = connection.getresponse()
    content = response.read().decode("utf-8")
    response_dict = json.loads(content)
    if response_dict['erro'] == True:
        # print(response_dict)
        JanelaComConsole.adicionar_print(JanelaComConsole, f"{response_dict}")
    else:
        # print(f"{response_dict['mensagem']}\nCódigo cliente = {response_dict['codigo_cliente']}")
        JanelaComConsole.adicionar_print(JanelaComConsole, f"{response_dict['mensagem']}\nCódigo cliente = {response_dict['codigo_cliente']}")
    connection.close()
    return response_dict


def cadastro_proposta(token, codigo_cliente, id_simulador):
    # Essa função vai passar uma url no body com o código do cliente gerado pela função dados_pessoais
    # E tbm os dados da proposta através do id vinculado
    # https://webservice.facta.com.br/proposta/etapa3-proposta-cadastro
    url_homologacao = "webservice.facta.com.br"
    path = "/proposta/etapa3-proposta-cadastro"
    body = f"codigo_cliente={codigo_cliente}&id_simulador={id_simulador}"

    connection = http.client.HTTPSConnection(url_homologacao)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    connection.request("POST", path, body, headers)
    response = connection.getresponse()
    content = response.read().decode("utf-8")
    response_dict = json.loads(content)
    connection.close()
    return response_dict


def envio_link(token, codigo_af):
    # Essa função vai passar uma url no body com o codigo af gerado pelo cadastro proposta e o tipo de envio
    url_homologacao = "webservice.facta.com.br"
    path = "/proposta/envio-link"
    body = (
        f"codigo_af={codigo_af}&tipo_envio=whatsapp"
    )

    connection = http.client.HTTPSConnection(url_homologacao)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": " PHPSESSID=cup7bgnk6ou2nppmvlh5hlf20o",
    }

    connection.request("POST", path, body, headers)
    response = connection.getresponse()
    content = response.read().decode("utf-8")
    response_dict = json.loads(content)
    connection.close()
    return response_dict


def digitar_port(token_gerado):
    resultado_dict = simula_port_refin(token_gerado, cliente)
    simulador = grava_port(resultado_dict, token_gerado)
    id_simulador = simulador["id_simulador"]
    grava_refin(id_simulador, resultado_dict, token_gerado)
    cadastro_cliente = dados_pessoais(id_simulador, token_gerado, cliente)
    codigo_cliente = cadastro_cliente["codigo_cliente"]
    proposta = cadastro_proposta(token_gerado, codigo_cliente, id_simulador)
    try:
        envio_link(token_gerado, proposta['codigo'])
        envio_link(token_gerado, proposta['codigo_refin_port'])
    except:
        JanelaComConsole.adicionar_print(JanelaComConsole, "Falha ao enviar o link")    
    JanelaComConsole.adicionar_print(JanelaComConsole, f"{proposta['mensagem']}\nAF Port: {proposta['codigo']}\nAF Refin: {proposta['codigo_refin_port']}\n{proposta['url_formalizacao']}\n")
    base = None
    # print(f"{proposta['mensagem']}\nADE Port: {proposta['codigo']}\nADE Refin: {proposta['codigo_refin_port']}\n{proposta['url_formalizacao']}\n")


def remove_special_char(name):
    text = re.sub(r'[^a-zA-Z\s]', '', name)
    return text


def bank_3char(cod):
    if len(cod) < 3:
        cod = cod.zfill(3)
    return cod


def agency_4char(cod):
    if len(cod) < 4:
        cod = cod.zfill(4)
    return cod


if __name__ == "__main__":
    root = tk.Tk()
    app = JanelaComConsole(root)

    JanelaComConsole.adicionar_print(JanelaComConsole, f"{token_gerado[0:20]}")

    root.protocol("WM_DELETE_WINDOW", app.restaurar_print_original)
    root.mainloop()
