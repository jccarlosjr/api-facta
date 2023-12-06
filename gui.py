from tkinter import ttk, filedialog, scrolledtext
from urllib.parse import urlencode
import http.client, base64, json, sys, os, re, tkinter as tk, pandas as pd


class JanelaComConsole:
    def __init__(self, root):
        self.root = root
        self.root.title("API digitação port facta")

        # Criar um widget Text para o console
        self.console = scrolledtext.ScrolledText(root, wrap="none", width=40, height=10)
        self.console.grid(row=16, column=0, columnspan=5, sticky="nsew")

        # Configurar o peso das colunas e linhas para expandir com a janela
        #self.root.grid_rowconfigure(3, weight=1)
        #self.root.grid_columnconfigure(0, weight=1)

        # Centralizar o texto no console
        self.console.tag_configure("center", justify="center")

        # Redefinir a função print para escrever no console
        self.stdout_original = sys.stdout
        sys.stdout = self.ConsoleRedirector(self.console)

        # Elementos adicionais
        info_label = ttk.Label(root, text="DADOS DO CLIENTE")
        info_label.grid(row=1, column=0, columnspan=5, pady=5)

        parcela_confirma = ttk.Button(root, text="Select", command=lambda: select_file_facta())
        parcela_confirma.grid(row=0, column=1, pady=5)

        botao = ttk.Button(root, text="Digitar", command=lambda: digitar_port(token_gerado))
        botao.grid(row=0, column=2, pady=5)

        botao = ttk.Button(root, text="Limpar", command=clear_entry)
        botao.grid(row=0, column=3, pady=5)

        ttk.Label(root, text="Nome:").grid(row=2, column=0, padx=2)
        ttk.Label(root, text="CPF:").grid(row=2, column=1, padx=2)
        ttk.Label(root, text="Nascimento:").grid(row=2, column=2, padx=2)
        ttk.Label(root, text="UF Nascimento:").grid(row=2, column=3, padx=2)
        ttk.Label(root, text="RG:").grid(row=2, column=4, padx=2)

        global name_entry
        name_entry = ttk.Entry(root, justify="center")
        name_entry.grid(row=3, column=0, padx=2)

        global cpf_entry
        cpf_entry = ttk.Entry(root, justify="center")
        cpf_entry.grid(row=3, column=1, padx=2)

        global bdate_entry
        bdate_entry = ttk.Entry(root, justify="center")
        bdate_entry.grid(row=3, column=2, padx=2)

        global uf_nascimento_entry
        uf_nascimento_entry = ttk.Entry(root, justify="center")
        uf_nascimento_entry.grid(row=3, column=3, padx=2)

        global rg_entry
        rg_entry = ttk.Entry(root, justify="center")
        rg_entry.grid(row=3, column=4, padx=2)


        ttk.Label(root, text="Mãe:").grid(row=4, column=0, padx=2)
        ttk.Label(root, text="Pai:").grid(row=4, column=1, padx=2)
        ttk.Label(root, text="Cidade Natural:").grid(row=4, column=2, padx=2)
        ttk.Label(root, text="Celular:").grid(row=4, column=3, padx=2)
        ttk.Label(root, text="Sexo:").grid(row=4, column=4, padx=2)

        global mae_entry
        mae_entry = ttk.Entry(root, justify="center")
        mae_entry.grid(row=5, column=0, padx=2)

        global pai_entry
        pai_entry = ttk.Entry(root, justify="center")
        pai_entry.grid(row=5, column=1, padx=2)

        global city_entry
        city_entry = ttk.Entry(root, justify="center")
        city_entry.grid(row=5, column=2, padx=2)

        global cel_entry
        cel_entry = ttk.Entry(root, justify="center")
        cel_entry.grid(row=5, column=3, padx=2)

        global sexo_entry
        sexo_entry = ttk.Entry(root, justify="center")
        sexo_entry.grid(row=5, column=4, padx=2)

        ttk.Label(root, text="CEP:").grid(row=6, column=0, padx=2)
        ttk.Label(root, text="Endereço:").grid(row=6, column=1, padx=2)
        ttk.Label(root, text="Nº").grid(row=6, column=2, padx=2)
        ttk.Label(root, text="Cidade End:").grid(row=6, column=3, padx=2)
        ttk.Label(root, text="Bairro:").grid(row=6, column=4, padx=2)
        
        global cep_entry
        cep_entry = ttk.Entry(root, justify="center")
        cep_entry.grid(row=7, column=0, padx=2)

        global end_entry
        end_entry = ttk.Entry(root, justify="center")
        end_entry.grid(row=7, column=1, padx=2)

        global num_entry
        num_entry = ttk.Entry(root, justify="center")
        num_entry.grid(row=7, column=2, padx=2)

        global cidade_end_entry
        cidade_end_entry = ttk.Entry(root, justify="center")
        cidade_end_entry.grid(row=7, column=3, padx=2)

        global bairro_entry
        bairro_entry = ttk.Entry(root, justify="center")
        bairro_entry.grid(row=7, column=4, padx=2)

        ttk.Label(root, text="UF Endereço:").grid(row=8, column=0, padx=2)
        ttk.Label(root, text="Espécie:").grid(row=8, column=1, padx=2)
        ttk.Label(root, text="Matrícula:").grid(row=8, column=2, padx=2)
        ttk.Label(root, text="Renda:").grid(row=8, column=3, padx=2)
        ttk.Label(root, text="UF Benefício").grid(row=8, column=4, padx=2)

        global uf_endereco_entry
        uf_endereco_entry = ttk.Entry(root, justify="center")
        uf_endereco_entry.grid(row=9, column=0, padx=2)

        global especie_entry
        especie_entry = ttk.Entry(root, justify="center")
        especie_entry.grid(row=9, column=1, padx=2)

        global matricula_entry
        matricula_entry = ttk.Entry(root, justify="center")
        matricula_entry.grid(row=9, column=2, padx=2)

        global renda_entry
        renda_entry = ttk.Entry(root, justify="center")
        renda_entry.grid(row=9, column=3, padx=2)

        global uf_beneficio_entry
        uf_beneficio_entry = ttk.Entry(root, justify="center")
        uf_beneficio_entry.grid(row=9, column=4, padx=2)

        ttk.Label(root, text="Banco:").grid(row=10, column=0, padx=2)
        ttk.Label(root, text="Agência:").grid(row=10, column=1, padx=2)
        ttk.Label(root, text="Conta:").grid(row=10, column=2, padx=2)
        ttk.Label(root, text="Parcela").grid(row=10, column=3, padx=2)

        global banco_entry
        banco_entry = ttk.Entry(root, justify="center")
        banco_entry.grid(row=11, column=0, padx=2)
        
        global agencia_entry
        agencia_entry = ttk.Entry(root, justify="center")
        agencia_entry.grid(row=11, column=1, padx=2)

        global conta_entry
        conta_entry = ttk.Entry(root, justify="center")
        conta_entry.grid(row=11, column=2, padx=2)

        global parcela_entry
        parcela_entry = ttk.Entry(root, justify="center")
        parcela_entry.grid(row=11, column=3, padx=2)

        ttk.Label(root, text="Banco Originador:").grid(row=12, column=0, padx=2)
        ttk.Label(root, text="Contrato:").grid(row=12, column=1, padx=2)
        ttk.Label(root, text="Prazo Original:").grid(row=12, column=2, padx=2)
        ttk.Label(root, text="Prazo Restante").grid(row=12, column=3, padx=2)
        ttk.Label(root, text="Saldo Devedor").grid(row=12, column=4, padx=2)

        global banco_origem_entry
        banco_origem_entry = ttk.Entry(root, justify="center")
        banco_origem_entry.grid(row=13, column=0, padx=2)
        
        global contrato_entry
        contrato_entry = ttk.Entry(root, justify="center")
        contrato_entry.grid(row=13, column=1, padx=2)

        global prazo_origem_entry
        prazo_origem_entry = ttk.Entry(root, justify="center")
        prazo_origem_entry.grid(row=13, column=2, padx=2)

        global prazo_restante_entry
        prazo_restante_entry = ttk.Entry(root, justify="center")
        prazo_restante_entry.grid(row=13, column=3, padx=2)

        global saldo_entry
        saldo_entry = ttk.Entry(root, justify="center")
        saldo_entry.grid(row=13, column=4, padx=2)

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
    url_homologacao = "webservice-homol.facta.com.br"
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
        JanelaComConsole.adicionar_print(JanelaComConsole, f'Expira em: {expire}')
        print()
        return token
    else:
        JanelaComConsole.adicionar_print(JanelaComConsole, f"Erro na requisição: {response_json['mensagem']}")
        return None


token_gerado = gerar_token()

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
    cidade = city['cidade']
    chave_cidade = list(cidade.keys())[0]
    if city['erro'] == True:
        JanelaComConsole.adicionar_print(JanelaComConsole, f"{city}")
    else:
        pass
    return chave_cidade


def select_file_facta():
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
        ###
        name_entry.insert(0, f'{nome}')
        cpf_entry.insert(0, f'{cpf}')
        bdate_entry.insert(0, f'{data_nascimento}')
        rg_entry.insert(0, f'{identidade}')
        uf_nascimento_entry.insert(0, f'{uf_nascimento}')
        sexo_entry.insert(0, f'{sexo}')
        mae_entry.insert(0, f'{mae}')
        pai_entry.insert(0, f'{pai}')
        city_entry.insert(0, f'{cidade_nascimento}')
        cel_entry.insert(0, f'{telefone}')
        cep_entry.insert(0, f'{cep}')
        end_entry.insert(0, f'{endereco}')
        num_entry.insert(0, f'{numero}')
        cidade_end_entry.insert(0, f'{cidade_endereco}')
        bairro_entry.insert(0, f'{bairro}')
        uf_endereco_entry.insert(0, f'{uf_endereco}')
        especie_entry.insert(0, f'{especie}')
        matricula_entry.insert(0, f'{matricula}')
        renda_entry.insert(0, f'{salario}')
        uf_beneficio_entry.insert(0, f'{uf_nb}')
        banco_entry.insert(0, f'{banco}')
        agencia_entry.insert(0, f'{agencia}')
        conta_entry.insert(0, f'{conta}')
        parcela_entry.insert(0, f'{parcela}')
        banco_origem_entry.insert(0, f'{banco_port}')
        contrato_entry.insert(0, f'{contrato_port}')
        prazo_origem_entry.insert(0, f'{parcela_total}')
        prazo_restante_entry.insert(0, f'{parcela_restante}')
        saldo_entry.insert(0, f'{saldo}')


def clear_entry():
    base = None
    name_entry.delete(0, tk.END)
    cpf_entry.delete(0, tk.END)
    bdate_entry.delete(0, tk.END)
    rg_entry.delete(0, tk.END)
    mae_entry.delete(0, tk.END)
    pai_entry.delete(0, tk.END)
    city_entry.delete(0, tk.END)
    cel_entry.delete(0, tk.END)
    cep_entry.delete(0, tk.END)
    end_entry.delete(0, tk.END)
    cidade_end_entry.delete(0, tk.END)
    especie_entry.delete(0, tk.END)
    matricula_entry.delete(0, tk.END)
    renda_entry.delete(0, tk.END)
    uf_beneficio_entry.delete(0, tk.END)
    banco_entry.delete(0, tk.END)
    agencia_entry.delete(0, tk.END)
    conta_entry.delete(0, tk.END)
    parcela_entry.delete(0, tk.END)
    banco_origem_entry.delete(0, tk.END)
    contrato_entry.delete(0, tk.END)
    prazo_origem_entry.delete(0, tk.END)
    prazo_restante_entry.delete(0, tk.END)
    saldo_entry.delete(0, tk.END)
    uf_endereco_entry.delete(0, tk.END)
    bairro_entry.delete(0, tk.END)
    num_entry.delete(0, tk.END)
    sexo_entry.delete(0, tk.END)
    uf_nascimento_entry.delete(0, tk.END)


def simula_port_refin(token):
    # Essa função passa um dicionário codificado para o request 
    url_homologacao = "webservice-homol.facta.com.br"
    path = "/proposta/operacoes-disponiveis"
    produto = "D"
    tipo_operacao = "003500"
    averbador = "3"
    convenio = "3"
    opcao_valor = "2"
    valor_parcela = parcela_entry.get()
    prazo = prazo_origem_entry.get()
    cpf = cpf_entry.get()
    data_nascimento = bdate_entry.get()
    prazo_restante = prazo_restante_entry.get()
    saldo_devedor = saldo_entry.get()
    valor_parcela_original = parcela_entry.get()
    prazo_original = prazo_origem_entry.get()
    parametros = {
        "produto": produto,
        "tipo_operacao": tipo_operacao,
        "averbador": averbador,
        "convenio": convenio,
        "opcao_valor": opcao_valor,
        "valor_parcela": valor_parcela,
        "prazo": prazo,
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
    url_homologacao = "webservice-homol.facta.com.br"
    path = "/proposta/etapa1-simulador"
    cpf = cpf_entry.get()
    data_nascimento = bdate_entry.get()
    login_certificado = "93862_01067744509"
    valor_operacao = resultado_dict['tabelas_portabilidade'][0]['contrato']
    coeficiente = resultado_dict['tabelas_portabilidade'][0]['coeficiente']
    valor_parcela = resultado_dict['tabelas_portabilidade'][0]['parcela']
    prazo = resultado_dict['tabelas_portabilidade'][0]['prazo']
    saldo_devedor = resultado_dict['tabelas_portabilidade'][0]['contrato']
    codigo_tabela = resultado_dict['tabelas_portabilidade'][0]['codigoTabela']
    prazo_original = prazo_origem_entry.get()
    
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
    url_homologacao = "webservice-homol.facta.com.br"
    path = "/proposta/etapa1-refin-portabilidade"
    banco_compra = banco_origem_entry.get()
    contrato_compra = contrato_entry.get()
    prazo_restante = prazo_restante_entry.get()
    saldo_devedor = saldo_entry.get()
    parcela_original = parcela_entry.get()
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


def dados_pessoais(id_simulador, token):
    # Essa função vai passar uma url no body com os dados do cliente e salvar no id_simulador da função grava_port
    # Que já possui os dados do refin da função grava_refin
    url_homologacao = "webservice-homol.facta.com.br"
    path = "/proposta/etapa2-dados-pessoais"
    cpf = cpf_entry.get()
    nome = name_entry.get()
    sexo = sexo_entry.get()
    estado_civil = "4"
    data_nascimento = bdate_entry.get()
    rg = rg_entry.get()
    estado_rg = uf_nascimento_entry.get()
    orgao_emissor = "SSP"
    data_expedicao = "16/05/2017"
    estado_natural = uf_nascimento_entry.get()
    cidade_name = city_entry.get()
    cidade_natural = obter_cidade(token_gerado, estado_rg, cidade_name)
    nacionalidade = "1"
    celular = cel_entry.get()
    renda = renda_entry.get()
    cep = cep_entry.get()
    endereco = end_entry.get()
    numero = num_entry.get()
    complemento = "CASA"
    bairro = bairro_entry.get()
    estado = uf_endereco_entry.get()
    cidade_name = cidade_end_entry.get()
    cidade = obter_cidade(token_gerado, estado, cidade_name)
    nome_mae = mae_entry.get()
    nome_pai = pai_entry.get()
    valor_patrimonio = "1"
    cliente_iletrado_impossibilitado = "N"
    banco = banco_entry.get()
    agencia = agencia_entry.get()
    conta = conta_entry.get()
    matricula = matricula_entry.get()
    tipo_credito_nb = "1"
    tipo_beneficio = especie_entry.get()
    estado_beneficio = uf_beneficio_entry.get()
    banco_pagamento = banco_entry.get()
    agencia_pagamento = agencia_entry.get()
    conta_pagamento = conta_entry.get()

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



def digitar_port(token_gerado):
    resultado_dict = simula_port_refin(token_gerado)
    simulador = grava_port(resultado_dict, token_gerado)
    id_simulador = simulador["id_simulador"]
    grava_refin(id_simulador, resultado_dict, token_gerado)
    cadastro_cliente = dados_pessoais(id_simulador, token_gerado)
    codigo_cliente = cadastro_cliente["codigo_cliente"]
    #proposta = cadastro_proposta(token_gerado, codigo_cliente, id_simulador)
    #try:
    #    envio_link(token_gerado, proposta['codigo'])
    #    envio_link(token_gerado, proposta['codigo_refin_port'])
    #except:
    #    JanelaComConsole.adicionar_print(JanelaComConsole, "Falha ao enviar o link")    
    #JanelaComConsole.adicionar_print(JanelaComConsole, f"{proposta['mensagem']}\nAF Port: {proposta['codigo']}\nAF Refin: {proposta['codigo_refin_port']}\n{proposta['url_formalizacao']}\n")
    # print(f"{proposta['mensagem']}\nADE Port: {proposta['codigo']}\nADE Refin: {proposta['codigo_refin_port']}\n{proposta['url_formalizacao']}\n")




if __name__ == "__main__":
    root = tk.Tk()
    app = JanelaComConsole(root)

    #JanelaComConsole.adicionar_print(JanelaComConsole, f"{token_gerado[0:20]}")

    root.protocol("WM_DELETE_WINDOW", app.restaurar_print_original)
    root.mainloop()


print(name_entry.get())