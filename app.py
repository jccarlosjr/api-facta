import http.client, base64, json, sys, os, re, pandas as pd, tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
from urllib.parse import urlencode
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class JanelaComConsole:
    def __init__(self, root):
        self.root = root
        self.root.title("Facta")

        self.console = scrolledtext.ScrolledText(
            root, wrap="none", width=40, height=10)
        self.console.grid(row=16, column=0, columnspan=5, sticky="nsew")

        nova_fonte = ("Sans Serif", 9, "bold")
        self.console.tag_configure("center", justify="center", font=nova_fonte)


        self.stdout_original = sys.stdout
        sys.stdout = self.ConsoleRedirector(self.console)

        info_label = ttk.Label(root, text="DADOS DO CLIENTE", font=nova_fonte)
        info_label.grid(row=1, column=0, columnspan=5, pady=5)

        parcela_confirma = ttk.Button(root, text="Select", style='Estilo.TButton', command=lambda: select_file_facta())
        parcela_confirma.grid(row=0, column=0, pady=5)

        style_btt = ttk.Style()
        style_btt.configure('Estilo.TButton', font=("Sans Serif", 9, "bold"))

        botao = ttk.Button(root, text="Digitar", style='Estilo.TButton',
                           command=lambda: digitar_port(token_gerado))
        botao.grid(row=0, column=1, pady=5)

        botao = ttk.Button(root, text="LOAS", style='Estilo.TButton',
                           command=lambda: digitar_port_LOAS(token_gerado))
        botao.grid(row=0, column=2, pady=5)

        botao = ttk.Button(root, text="Limpar",
                           style='Estilo.TButton', command=clear_entry)
        botao.grid(row=0, column=3, pady=5)

        ttk.Label(root, text="Nome:", font=nova_fonte).grid(
            row=2, column=0, padx=2)
        ttk.Label(root, text="CPF:", font=nova_fonte).grid(
            row=2, column=1, padx=2)
        ttk.Label(root, text="Nascimento:", font=nova_fonte).grid(
            row=2, column=2, padx=2)
        ttk.Label(root, text="UF Nascimento:", font=nova_fonte).grid(
            row=2, column=3, padx=2)
        ttk.Label(root, text="Cidade Natural:", font=nova_fonte).grid(
            row=2, column=4, padx=2)

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

        global city_entry
        city_entry = ttk.Entry(root, justify="center")
        city_entry.grid(row=3, column=4, padx=2)

        ttk.Label(root, text="Mãe:", font=nova_fonte).grid(
            row=4, column=0, padx=2)
        ttk.Label(root, text="Pai:", font=nova_fonte).grid(
            row=4, column=1, padx=2)
        ttk.Label(root, text="RG:", font=nova_fonte).grid(
            row=4, column=2, padx=2)
        ttk.Label(root, text="Celular:", font=nova_fonte).grid(
            row=4, column=3, padx=2)
        ttk.Label(root, text="Sexo:", font=nova_fonte).grid(
            row=4, column=4, padx=2)

        global mae_entry
        mae_entry = ttk.Entry(root, justify="center")
        mae_entry.grid(row=5, column=0, padx=2)

        global pai_entry
        pai_entry = ttk.Entry(root, justify="center")
        pai_entry.grid(row=5, column=1, padx=2)

        global rg_entry
        rg_entry = ttk.Entry(root, justify="center")
        rg_entry.grid(row=5, column=2, padx=2)

        global cel_entry
        cel_entry = ttk.Entry(root, justify="center")
        cel_entry.grid(row=5, column=3, padx=2)

        global sexo_entry
        sexo_entry = ttk.Entry(root, justify="center")
        sexo_entry.grid(row=5, column=4, padx=2)

        ttk.Label(root, text="CEP:", font=nova_fonte).grid(
            row=6, column=0, padx=2)
        ttk.Label(root, text="Endereço:", font=nova_fonte).grid(
            row=6, column=1, padx=2)
        ttk.Label(root, text="Nº", font=nova_fonte).grid(
            row=6, column=2, padx=2)
        ttk.Label(root, text="Cidade End:", font=nova_fonte).grid(
            row=6, column=3, padx=2)
        ttk.Label(root, text="Bairro:", font=nova_fonte).grid(
            row=6, column=4, padx=2)

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

        ttk.Label(root, text="UF Endereço:", font=nova_fonte).grid(
            row=8, column=0, padx=2)
        ttk.Label(root, text="Espécie:", font=nova_fonte).grid(
            row=8, column=1, padx=2)
        ttk.Label(root, text="Matrícula:", font=nova_fonte).grid(
            row=8, column=2, padx=2)
        ttk.Label(root, text="Renda:", font=nova_fonte).grid(
            row=8, column=3, padx=2)
        ttk.Label(root, text="UF Benefício", font=nova_fonte).grid(
            row=8, column=4, padx=2)

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

        ttk.Label(root, text="Banco:", font=nova_fonte).grid(
            row=10, column=0, padx=2)
        ttk.Label(root, text="Agência:", font=nova_fonte).grid(
            row=10, column=1, padx=2)
        ttk.Label(root, text="Conta:", font=nova_fonte).grid(
            row=10, column=2, padx=2)
        ttk.Label(root, text="Parcela", font=nova_fonte).grid(
            row=10, column=3, padx=2)

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

        ttk.Label(root, text="Banco Originador:", font=nova_fonte).grid(
            row=12, column=0, padx=2)
        ttk.Label(root, text="Contrato:", font=nova_fonte).grid(
            row=12, column=1, padx=2)
        ttk.Label(root, text="Prazo Original:", font=nova_fonte).grid(
            row=12, column=2, padx=2)
        ttk.Label(root, text="Prazo Restante", font=nova_fonte).grid(
            row=12, column=3, padx=2)
        ttk.Label(root, text="Saldo Devedor", font=nova_fonte).grid(
            row=12, column=4, padx=2)

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
            self.console.see(tk.END)

    def adicionar_print(self, texto):
        print(texto)

    def restaurar_print_original(self):
        sys.stdout = self.stdout_original
        self.root.destroy()

    def limpar_console(self):
        self.console.delete(1.0, tk.END)

    def centralizar_janela(root):
        root.update_idletasks()
        largura_janela = root.winfo_width()
        altura_janela = root.winfo_height()

        largura_tela = root.winfo_screenwidth()
        altura_tela = root.winfo_screenheight()

        x_pos = (largura_tela - largura_janela) // 2
        y_pos = (altura_tela - altura_janela) // 2

        root.geometry(f"+{x_pos}+{y_pos}")


URL_PRODUCAO = "webservice.facta.com.br"
URL_HOMOLOGACAO = "webservice-homol.facta.com.br"


def get_token():
    url = URL_PRODUCAO
    path = "/gera-token"
    usuario = "93862"
    senha = "3rpl7ds11psjo3cloae6"
    credenciais = f"{usuario}:{senha}"
    credenciais_base64 = base64.b64encode(credenciais.encode()).decode('utf-8')
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
        JanelaComConsole.adicionar_print(
            JanelaComConsole, f"Erro na requisição: {response_json['mensagem']}")
        return None


token_gerado = get_token()


def remove_special_char(name):
    text = re.sub(r'[^a-zA-Z\s]', '', name)
    return text


def format_city(city_name):
    if city_name[-1] == " ":
        city_name[-1] = ""
    city_name = city_name.upper()
    city_name = city_name.replace("Ã", "A").replace("À", "A").replace("Á", "A").replace("Â", "A")
    city_name = city_name.replace("Õ", "O").replace("Ò", "O").replace("Ó", "O").replace("Ô", "O")
    city_name = city_name.replace("È", "E").replace("É", "E").replace("Ê", "E")
    city_name = city_name.replace("Í", "I").replace("Ì", "I").replace("Î", "I")
    city_name = city_name.replace("Ú", "U").replace("Ù", "U").replace("Û", "U")
    city_name = city_name.replace("Ç", "C")
    city_name = city_name.replace(" ", "_").strip()
    return city_name


def get_city(token, uf=str, nome=str):
    cidade = format_city(nome)
    uf = uf.upper()
    url = URL_PRODUCAO
    endpoint = f"/proposta-combos/cidade?estado={uf}&nome_cidade={cidade}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    conn = http.client.HTTPSConnection(url)
    conn.request("GET", endpoint, headers=headers)

    response = conn.getresponse()
    city = json.loads(response.read().decode("utf-8"))
    conn.close()
    if city['erro'] == True:
        JanelaComConsole.adicionar_print(
            JanelaComConsole, f"Cidade não encontrada")
    else:
        cidade = city['cidade']
        chave_cidade = list(cidade.keys())[0]
    return chave_cidade


def select_file_facta():
    # A função vai importar o excel e preencher automaticamente os campos entry na gui
    # Ao mesmo tempo que vai formatar adequadamente para os padrões aceito pela api
    arquivo_path = filedialog.askopenfilename(
        title="Selecione um arquivo", filetypes=[("Arquivos Excel", "*.xlsx;*.xls")])
    if arquivo_path:
        nome_arquivo = os.path.basename(arquivo_path)
        nome_arquivo = f'{nome_arquivo[6:11]}/{nome_arquivo[12:14]}/{nome_arquivo[15:]}'
        JanelaComConsole.adicionar_print(
            JanelaComConsole, f"Arquivo selecionado: {nome_arquivo}")
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
        if numero == "SN":
            numero = "1"
        cidade_endereco = str(base['CIDADE'].values[0]).upper()
        bairro = str(base['BAIRRO'].values[0]).upper()
        especie = str(base['ESPECIE'].values[0])
        matricula = str(base['MATRICULA'].values[0]).replace("-", "").replace(".", "").replace("[", "").replace("]", "").replace("'", "").strip()
        matricula = int(matricula)
        salario = str(base['SALARIO'].values[0]).replace(".", "").replace(",", ".").replace("R", "").replace("$", "").replace("[", "").replace("]", "").replace("'", "").strip()
        uf_nb = str(base['UF_NB'].values[0]).upper()
        banco = str(base['BANCO_NB'].values[0])
        agencia = str(base['AGENCIA_NB'].values[0])
        conta = str(base['CONTA_NB'].values[0]) + str(base['DV_NB'].values[0])
        banco_port = str(base['BANCO_PORT'].values[0])
        if banco_port == "626":
            banco_port = "336"
        contrato_port = str(base['NUM_CONTRATO'].values[0]).replace("-", "").replace("/", "").replace("_", "")
        parcela_total = str(base['NUM_PARCELA_TOTAL'].values[0]).replace("[", "").replace("]", "").replace("'", "")
        parcela_restante = str(base['PAR_RESTANTE'].values[0])
        parcela = str(base['PARCELA'].values[0]).replace(".", "").replace(",", ".")
        saldo = str(base['SALDO'].values[0]).replace(".", "").replace(",", ".")
        
        # Preenchendo os entrys da janela do tkinter com os valores recebidos pelo excel

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
    # Função para limpar o df e as entrys da gui
    app.limpar_console()
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
    # O retorno é um código de simulação necessário para digitar a proposta
    url = URL_PRODUCAO
    path = "/proposta/operacoes-disponiveis"
    produto = "D"
    tipo_operacao = "003500"
    averbador = "3"
    convenio = "3"
    opcao_valor = "2"
    valor_parcela = parcela_entry.get()
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
        "prazo": "84",
        "cpf": cpf,
        "data_nascimento": data_nascimento,
        "prazo_restante": prazo_restante,
        "saldo_devedor": saldo_devedor,
        "valor_parcela_original": valor_parcela_original,
        "prazo_original": prazo_original,
    }

    parametros_codificados = urlencode(parametros)
    connection = http.client.HTTPSConnection(url)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": "PHPSESSID=olqno6ge8khacr1g3stplm8tmj",
    }

    connection.request(
        "GET", f"{path}?{parametros_codificados}", headers=headers)
    response = connection.getresponse()
    content = response.read().decode("utf-8")
    response_dict = json.loads(content)
    if response_dict['erro'] == True:
        try:
            JanelaComConsole.adicionar_print(
                JanelaComConsole, f"Tabela Port: {response_dict['tabelas_portabilidade'][0]['tabela']}")
        except:
            JanelaComConsole.adicionar_print(
                JanelaComConsole, "Sem tabela disponível para portabilidade")
        try:
            JanelaComConsole.adicionar_print(
                JanelaComConsole, f"Tabela Refin: {response_dict['tabelas_refin_portabilidade'][0]['tabela']}")
        except:
            JanelaComConsole.adicionar_print(
                JanelaComConsole, "Sem tabela disponível para refin da port")
    else:
        pass
    with open("simulacao.json", "w") as json_file:
        json.dump(response_dict, json_file, indent=2)
    connection.close()
    return response_dict


def grava_port(resultado_dict, token):
    # Essa função vai passar uma url no body com os dados retornados da função simula_port_refin
    # O retorno é o código da simulação, selecionando a primeira tabela disponibilizada pela simulação
    url = URL_PRODUCAO
    path = "/proposta/etapa1-simulador"
    cpf = cpf_entry.get()
    data_nascimento = bdate_entry.get()
    login_certificado = "93862_01067744509"
    valor_operacao = resultado_dict['tabelas_portabilidade'][0]['contrato']
    coeficiente = resultado_dict['tabelas_portabilidade'][0]['coeficiente']
    valor_parcela = resultado_dict['tabelas_portabilidade'][0]['parcela']
    prazo = resultado_dict['tabelas_portabilidade'][0]['prazo']
    saldo_devedor = resultado_dict['tabelas_portabilidade'][0]['contrato']

    tabelas = resultado_dict["tabelas_portabilidade"]

    nova_tabelas = []

    try:
        for dicionario in tabelas:
            if 'LOAS' not in dicionario['tabela'] and 'GRUPO 2' in dicionario['grupos']:
                nova_tabelas.append(dicionario)
    except:
        for dicionario in tabelas:
            if 'LOAS' not in dicionario['tabela'] and 'GRUPO 3' in dicionario['grupos']:
                nova_tabelas.append(dicionario)

    codigo_tabela = nova_tabelas[0]['codigoTabela']

    prazo_original = prazo_origem_entry.get()

    body = (
        f"produto=D&tipo_operacao=003500&averbador=3&convenio=3&cpf={cpf}"
        f"&data_nascimento={data_nascimento}&login_certificado={login_certificado}&valor_operacao={valor_operacao}"
        f"&coeficiente={coeficiente}&valor_parcela={valor_parcela}&prazo={prazo}&saldo_devedor={saldo_devedor}"
        f"&codigo_tabela={codigo_tabela}&prazo_original={prazo_original}"
    )

    connection = http.client.HTTPSConnection(url)
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
        JanelaComConsole.adicionar_print(JanelaComConsole, f"{response_dict['mensagem']}")
    else:
        pass
    connection.close()
    return response_dict


def grava_refin(id_simulador, resultado_dict, token):
    # Essa função vai passar uma url no body com os dados do refin e salvar no id_simulador da função grava_port
    # O retorno é o código da simulação, adicionando os dados da portabilidade ao código da simulação
    url = URL_PRODUCAO
    path = "/proposta/etapa1-refin-portabilidade"
    banco_compra = banco_origem_entry.get()
    contrato_compra = contrato_entry.get()
    prazo_restante = prazo_restante_entry.get()
    saldo_devedor = saldo_entry.get()
    parcela_original = parcela_entry.get()
    tabelas = resultado_dict["tabelas_refin_portabilidade"]
    nova_tabelas = []

    try:
        for dicionario in tabelas:
            if 'LOAS' not in dicionario['tabela'] and 'GRUPO 2' in dicionario['grupos']:
                nova_tabelas.append(dicionario)
    except:
        for dicionario in tabelas:
            if 'LOAS' not in dicionario['tabela'] and 'GRUPO 3' in dicionario['grupos']:
                nova_tabelas.append(dicionario)
    
    codigo_tabela = nova_tabelas[0]['codigoTabela']

    coeficiente = resultado_dict['tabelas_refin_portabilidade'][0]['coeficiente']
    valor_operacao = resultado_dict['tabelas_refin_portabilidade'][0]['contrato']
    valor_parcela = resultado_dict['tabelas_refin_portabilidade'][0]['parcela']
    body = (
        f"id_simulador={id_simulador}&banco_compra={banco_compra}&contrato_compra={contrato_compra}&prazo_restante={prazo_restante}"
        f"&saldo_devedor={saldo_devedor}&parcela_original={parcela_original}&prazo=84"
        f"&codigo_tabela={codigo_tabela}&coeficiente={coeficiente}&valor_operacao={valor_operacao}&valor_parcela={valor_parcela}"
    )

    connection = http.client.HTTPSConnection(url)
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
        # print(response_dict)
        JanelaComConsole.adicionar_print(JanelaComConsole, f"{response_dict['mensagem']}")

    else:
        # print(f"{response_dict['mensagem']}")
        pass
    connection.close()
    return response_dict


def grava_port_LOAS(resultado_dict, token):
    # Essa função vai passar uma url no body com os dados retornados da função simula_port_refin
    # O retorno é o código da simulação, selecionando a primeira tabela disponibilizada pela simulação
    url = URL_PRODUCAO
    path = "/proposta/etapa1-simulador"
    cpf = cpf_entry.get()
    data_nascimento = bdate_entry.get()
    login_certificado = "93862_01067744509"
    valor_operacao = resultado_dict['tabelas_portabilidade'][0]['contrato']
    coeficiente = resultado_dict['tabelas_portabilidade'][0]['coeficiente']
    valor_parcela = resultado_dict['tabelas_portabilidade'][0]['parcela']
    prazo = resultado_dict['tabelas_portabilidade'][0]['prazo']
    saldo_devedor = resultado_dict['tabelas_portabilidade'][0]['contrato']

    tabelas = resultado_dict["tabelas_portabilidade"]

    nova_tabelas = []

    try:
        for dicionario in tabelas:
            if 'LOAS' in dicionario['tabela'] and 'GRUPO LOAS 2' in dicionario['grupos']:
                nova_tabelas.append(dicionario)
    except:
        for dicionario in tabelas:
            if 'LOAS' in dicionario['tabela'] and 'GRUPO LOAS 3' in dicionario['grupos']:
                nova_tabelas.append(dicionario)
    
    print(nova_tabelas)
    codigo_tabela = nova_tabelas[0]['codigoTabela']

    prazo_original = prazo_origem_entry.get()

    body = (
        f"produto=D&tipo_operacao=003500&averbador=3&convenio=3&cpf={cpf}"
        f"&data_nascimento={data_nascimento}&login_certificado={login_certificado}&valor_operacao={valor_operacao}"
        f"&coeficiente={coeficiente}&valor_parcela={valor_parcela}&prazo={prazo}&saldo_devedor={saldo_devedor}"
        f"&codigo_tabela={codigo_tabela}&prazo_original={prazo_original}"
    )

    connection = http.client.HTTPSConnection(url)
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
        JanelaComConsole.adicionar_print(JanelaComConsole, f"{response_dict['mensagem']}")
    else:
        pass
    connection.close()
    return response_dict


def grava_refin_LOAS(id_simulador, resultado_dict, token):
    # Essa função vai passar uma url no body com os dados do refin e salvar no id_simulador da função grava_port
    # O retorno é o código da simulação, adicionando os dados da portabilidade ao código da simulação
    url = URL_PRODUCAO
    path = "/proposta/etapa1-refin-portabilidade"
    banco_compra = banco_origem_entry.get()
    contrato_compra = contrato_entry.get()
    prazo_restante = prazo_restante_entry.get()
    saldo_devedor = saldo_entry.get()
    parcela_original = parcela_entry.get()
    tabelas = resultado_dict["tabelas_refin_portabilidade"]
    nova_tabelas = []

    try:
        for dicionario in tabelas:
            if 'LOAS' in dicionario['tabela'] and 'GRUPO LOAS 2' in dicionario['grupos']:
                nova_tabelas.append(dicionario)
    except:
        for dicionario in tabelas:
            if 'LOAS' in dicionario['tabela'] and 'GRUPO LOAS 3' in dicionario['grupos']:
                nova_tabelas.append(dicionario)
    
    codigo_tabela = nova_tabelas[0]['codigoTabela']

    coeficiente = resultado_dict['tabelas_refin_portabilidade'][0]['coeficiente']
    valor_operacao = resultado_dict['tabelas_refin_portabilidade'][0]['contrato']
    valor_parcela = resultado_dict['tabelas_refin_portabilidade'][0]['parcela']
    body = (
        f"id_simulador={id_simulador}&banco_compra={banco_compra}&contrato_compra={contrato_compra}&prazo_restante={prazo_restante}"
        f"&saldo_devedor={saldo_devedor}&parcela_original={parcela_original}&prazo=84"
        f"&codigo_tabela={codigo_tabela}&coeficiente={coeficiente}&valor_operacao={valor_operacao}&valor_parcela={valor_parcela}"
    )

    connection = http.client.HTTPSConnection(url)
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
        # print(response_dict)
        JanelaComConsole.adicionar_print(JanelaComConsole, f"{response_dict['mensagem']}")

    else:
        # print(f"{response_dict['mensagem']}")
        pass
    connection.close()
    return response_dict


def dados_pessoais(id_simulador, token):
    # Essa função vai passar uma url no body com os dados do cliente e salvar no id_simulador da função grava_port
    # Que já possui os dados do refin da função grava_refin
    # O retorno é o código do cliente com os dados pessoais
    url = URL_PRODUCAO
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
    cidade_natural = get_city(token_gerado, estado_rg, cidade_name)
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
    cidade = get_city(token_gerado, estado, cidade_name)
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
    tipo_conta = "C"

    connection = http.client.HTTPSConnection(url)
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
        f"&estado_beneficio={estado_beneficio}&banco_pagamento={banco_pagamento}&agencia_pagamento={agencia_pagamento}&conta_pagamento={conta_pagamento}&tipo_conta={tipo_conta}"
    )

    connection.request("POST", path, body, headers)
    response = connection.getresponse()
    content = response.read().decode("utf-8")
    response_dict = json.loads(content)
    if response_dict['erro'] == True:
        JanelaComConsole.adicionar_print(JanelaComConsole, f"{response_dict['mensagem']}")
    else:
        JanelaComConsole.adicionar_print(
            JanelaComConsole, f"{response_dict['mensagem']}")
    connection.close()
    return response_dict


def cadastro_proposta(token, codigo_cliente, id_simulador):
    # Essa função vai passar uma url no body com o código do cliente gerado pela função dados_pessoais
    # E tbm os dados da proposta através do id vinculado
    url = URL_PRODUCAO
    path = "/proposta/etapa3-proposta-cadastro"
    body = f"codigo_cliente={codigo_cliente}&id_simulador={id_simulador}"

    connection = http.client.HTTPSConnection(url)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    connection.request("POST", path, body, headers)
    response = connection.getresponse()
    content = response.read().decode("utf-8")

    json_start_index = content.find('{"erro":')

    if json_start_index != -1:
        json_content = content[json_start_index:]
        response_dict = json.loads(json_content)
        JanelaComConsole.adicionar_print(
            JanelaComConsole, f"{response_dict['mensagem']}")
        return response_dict
    else:
        JanelaComConsole.adicionar_print(
            JanelaComConsole, 'A resposta não contém um JSON válido.')
        return None


def envio_link(token, codigo_af):
    # Essa função vai passar uma url no body com o codigo af gerado pelo cadastro proposta e o tipo de envio
    url = URL_PRODUCAO
    path = "/proposta/envio-link"
    body = (
        f"codigo_af={codigo_af}&tipo_envio=sms"
    )

    connection = http.client.HTTPSConnection(url)
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
    simula_port = simula_port_refin(token_gerado)
    gravar_port = grava_port(simula_port, token_gerado)
    id_simulador = gravar_port["id_simulador"]
    grava_refin(id_simulador, simula_port, token_gerado)
    cadastro_cliente = dados_pessoais(id_simulador, token_gerado)
    codigo_cliente = cadastro_cliente["codigo_cliente"]
    proposta = cadastro_proposta(token_gerado, codigo_cliente, id_simulador)
    try:
        envio_link(token_gerado, proposta['codigo_refin_port'])
    except:
        JanelaComConsole.adicionar_print(
            JanelaComConsole, "Falha ao enviar o link, proposta cancelada")
    JanelaComConsole.adicionar_print(
        JanelaComConsole, f"{proposta['mensagem']}\nAF Port: {proposta['codigo']}\nAF Refin: {proposta['codigo_refin_port']}\n{proposta['url_formalizacao']}\n")


def digitar_port_LOAS(token_gerado):
    simula_port = simula_port_refin(token_gerado)
    gravar_port = grava_port_LOAS(simula_port, token_gerado)
    id_simulador = gravar_port["id_simulador"]
    grava_refin_LOAS(id_simulador, simula_port, token_gerado)
    cadastro_cliente = dados_pessoais(id_simulador, token_gerado)
    codigo_cliente = cadastro_cliente["codigo_cliente"]
    proposta = cadastro_proposta(token_gerado, codigo_cliente, id_simulador)
    try:
        envio_link(token_gerado, proposta['codigo_refin_port'])
    except:
        JanelaComConsole.adicionar_print(
            JanelaComConsole, "Falha ao enviar o link, proposta cancelada")
    JanelaComConsole.adicionar_print(
        JanelaComConsole, f"{proposta['mensagem']}\nAF Port: {proposta['codigo']}\nAF Refin: {proposta['codigo_refin_port']}\n{proposta['url_formalizacao']}\n")




if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style("yeti")
    app = JanelaComConsole(root)
    caminho_icone = "favicon.ico"
    root.iconbitmap(caminho_icone)
    app.adicionar_print(f"{token_gerado[0:20]}")

    root.protocol("WM_DELETE_WINDOW", app.restaurar_print_original)
    JanelaComConsole.centralizar_janela(root)
    root.mainloop()
