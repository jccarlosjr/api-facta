from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from tkinter import ttk
from tkinter import *
import pandas as pd
from tkinter import filedialog
import time
import os
from subprocess import CREATE_NO_WINDOW 


def softWriter(element, text):
    script = "arguments[0].value += arguments[1];"
    for char in text:
        driver.execute_script(script, element, char)
    element.send_keys(Keys.TAB)


def elementClickable(xpath):
    element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    return element


def idClickable(id):
    element = wait.until(EC.element_to_be_clickable((By.ID, id)))
    return element


def find_xpath(xpath):
    elementClickable(xpath)
    element = driver.find_element(By.XPATH, xpath)
    return element


def find_id(id):
    element = driver.find_element(By.ID, id)
    return element


def sendKeys(element, keys):
    element = element
    element.send_keys(Keys.SHIFT, Keys.END + Keys.BACK_SPACE)
    element.send_keys(Keys.SHIFT, Keys.HOME + Keys.BACK_SPACE)
    element.send_keys(keys)
    element.send_keys(Keys.TAB)


def loadC6():
    time.sleep(1)
    try:
        load = driver.find_element(By.ID, 'ctl00_Image2')
        if load:
            waitload = WebDriverWait(driver, 60)
            waitload.until(EC.invisibility_of_element((By.ID, 'ctl00_Image2')))
    except:
        pass


def open_driver():
    chrome_service = Service(ChromeDriverManager().install())
    chrome_service.creation_flags = CREATE_NO_WINDOW
    global driver
    driver = webdriver.Chrome(service=chrome_service)
    global wait
    wait = WebDriverWait(driver, 5)
    global action
    action = ActionChains(driver)


def close_driver():
    try:
        driver.close()
        driver.quit()
    except:
        info_label.config(text="Driver não encontrado")


def select_file_c6():
    arquivo_path = filedialog.askopenfilename(
        title="Selecione um arquivo", filetypes=[("Arquivos Excel", "*.xlsx;*.xls")])
    if arquivo_path:
        global nome_arquivo
        nome_arquivo = os.path.basename(arquivo_path)
        info_label.config(text=f"Arquivo selecionado: {nome_arquivo}")
        global base
        base = pd.read_excel(f'{arquivo_path}')
        global cpf_planilha
        for i,  cpf_planilha in enumerate(base['CPF']):
            global data_nascimento_cliente
            data_nascimento_cliente = base.loc[i, 'NASCIMENTO']
            global matricula_cliente
            matricula_cliente1 = base.loc[i, 'MATRICULA']
            matricula_cliente = str(matricula_cliente1)
            global nome_cliente
            nome_cliente = base.loc[i, 'NOME']
            global sexo_cliente
            sexo_cliente = base.loc[i, 'SEXO']
            global mae_cliente
            mae_cliente = base.loc[i, 'MAE']
            global pai_cliente
            pai_cliente = base.loc[i, 'PAI']
            global uf_nascimento
            uf_nascimento = base.loc[i, 'UF_NASCIMENTO']
            global uf_rg_cliente
            uf_rg_cliente = base.loc[i, 'UF_RG']
            global cidade_nascimento
            cidade_nascimento = base.loc[i, 'CIDADE_NASCIMENTO']
            global rg_cliente
            rg_cliente = base.loc[i, 'IDENTIDADE']
            global ddd_cliente
            ddd_cliente = str(base.loc[i, 'DDD'])
            global telefone_cliente
            telefone_cliente = str(base.loc[i, 'TELEFONE'])
            global ddd_celular
            ddd_celular = str(base.loc[i, 'DDD_2'])
            global celular
            celular = str(base.loc[i, 'CELULAR'])
            global especie_cliente
            especie_cliente = base.loc[i, 'ESPECIE']
            global cep_cliente
            cep_cliente = base.loc[i, 'CEP']
            global endereco_cliente
            endereco_cliente = base.loc[i, 'ENDERECO']
            global numero_casa_cliente
            numero_casa_cliente = base.loc[i, 'NUMERO']
            global bairro_cliente
            bairro_cliente = base.loc[i, 'BAIRRO']
            global cidade_cliente
            cidade_cliente = base.loc[i, 'CIDADE']
            global uf_endereco_cliente
            uf_endereco_cliente = base.loc[i, 'UF_ENDERECO']
            global uf_beneficio_cliente
            uf_beneficio_cliente = base.loc[i, 'UF_ENDERECO']
            global banco_cliente
            banco_cliente = base.loc[i, 'BANCO_NB']
            global agencia_cliente
            agencia_cliente = base.loc[i, 'AGENCIA_NB']
            global conta_cliente
            conta_cliente = base.loc[i, 'CONTA_NB']
            global dv_conta
            dv_conta = str(base.loc[i, 'DV_NB'])
            global bancoport_cliente
            bancoport_cliente = base.loc[i, 'BANCO_PORT']
            global num_ctt
            num_ctt = base.loc[i, 'NUM_CONTRATO']
            global parcela
            parcela = base.loc[i, 'PARCELA']
            global parcela_total
            parcela_total = base.loc[i, 'NUM_PARCELA_TOTAL']
            global parcela_restante
            parcela_restante = base.loc[i, 'PAR_RESTANTE']
            global saldo_devedor_planilha
            saldo_devedor_planilha = base.loc[i, 'SALDO']
            if dv_conta == "":
                dv_conta = "0"
    else:
        info_label.config(text="Nenhum arquivo selecionado")


def alert_confirm():
    try:
        wait = WebDriverWait(driver, 1)
        wait.until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()
    except:
        pass


def login_c6():
    try:
        usuario = login_usuario_entry.get()
        usuario = usuario.strip()
        senha = login_senha_entry.get()
        senha = senha.strip()
        driver.get('https://c6.c6consig.com.br/WebAutorizador/')
        find_xpath('//*[@id="EUsuario_CAMPO"]').send_keys(str(usuario))
        find_xpath('//*[@id="ESenha_CAMPO"]').send_keys(str(senha))
        find_xpath('//*[@id="lnkEntrar"]').click()
        open_writer()
        alert_confirm()
        info_label.config(text='Login efetuado')
    except:
        info_label.config(text='Erro ao logar')


def open_writer(): 
    alert_confirm()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.LINK_TEXT, 'Cadastro')))
    cadastro = driver.find_element(By.LINK_TEXT, 'Cadastro')
    action.move_to_element(cadastro).perform()
    proposta = driver.find_element(By.LINK_TEXT, 'Proposta Consignado')
    action.move_to_element(proposta).click().perform()
    time.sleep(0.5)


def iniciar_digitacao():
    alert_confirm()
    elementClickable('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnDadosIniciais_UcDIni_cboTipoOperacao_CAMPO"]/option[3]').click()
    elementClickable('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnDadosIniciais_UcDIni_cboGrupoConvenio_CAMPO"]/option[3]').click()
    loadC6()


def dados_iniciais():
    find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnDadosIniciais_UcDIni_txtCPF_CAMPO"]').send_keys((str(cpf_planilha)), Keys.TAB)
    alert_confirm()
    loadC6()
    try:
        driver.switch_to.frame('ctl00_Cph_UcPrp_FIJN1_JnDadosIniciais_UcDIni_popCliente_frameAjuda')
        driver.find_element(By.XPATH, '//*[@id="ctl00_cph_FIJanela1_FIJanelaPanel1_btnNovo_dvTxt"]/table/tbody/tr/td').click()
        time.sleep(1)
        driver.switch_to.default_content()
    except:
        pass
    
    time.sleep(0.5)
    find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnDadosIniciais_UcDIni_txtDataNascimento_CAMPO"]').send_keys(str(data_nascimento_cliente) + Keys.TAB)
    time.sleep(0.5)
    if(len(matricula_cliente) == 10):
        find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnDadosIniciais_UcDIni_ucMatricula_txtMatricula_CAMPO"]').send_keys(str(matricula_cliente), Keys.TAB)
    else:
        find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnDadosIniciais_UcDIni_ucMatricula_txtMatricula_CAMPO"]').send_keys(str(matricula_cliente).zfill(10), Keys.TAB)
    time.sleep(0.5)
    alert_confirm()
    loadC6
    find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnDadosIniciais_UcDIni_txtRenda_CAMPO"]').send_keys(Keys.SHIFT+Keys.HOME, Keys.BACK_SPACE)
    find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnDadosIniciais_UcDIni_txtRenda_CAMPO"]').send_keys(Keys.SHIFT+Keys.END, Keys.BACK_SPACE)
    find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnDadosIniciais_UcDIni_txtRenda_CAMPO"]').send_keys('2890,00', Keys.TAB)
    loadC6()            
    find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnDadosIniciais_UcDIni_txtDataContraCheque_CAMPO"]').send_keys('11/2023', Keys.TAB)
    loadC6()
    find_xpath('//*[@id="btnObterMargem_txt"]').click()
    alert_confirm()
    alert_confirm()


def dados_port():
    find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnCompraDivida_UcCompra_FIJN1_JnC_txtBanco_CAMPO"]').send_keys(str(bancoport_cliente), Keys.ENTER)
    alert_confirm()
    loadC6()
    time.sleep(0.5)
    alert_confirm()
    find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnCompraDivida_UcCompra_FIJN1_JnC_txtNrContrato_CAMPO"]').send_keys(str(num_ctt), Keys.TAB)
    find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnCompraDivida_UcCompra_FIJN1_JnC_txtValorParcela_CAMPO"]').send_keys(Keys.SHIFT+Keys.HOME, Keys.BACK_SPACE)
    find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnCompraDivida_UcCompra_FIJN1_JnC_txtValorParcela_CAMPO"]').send_keys(str(parcela), Keys.TAB)
    saldo_devedor = str(saldo_devedor_planilha)
    saldo_devedor = saldo_devedor.replace(".", "")
    saldo_devedor = saldo_devedor.strip()
    find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnCompraDivida_UcCompra_FIJN1_JnC_txtValorQuitacaoDivida_CAMPO"]').send_keys(Keys.SHIFT+Keys.HOME, Keys.BACK_SPACE)
    find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnCompraDivida_UcCompra_FIJN1_JnC_txtValorQuitacaoDivida_CAMPO"]').send_keys(saldo_devedor, Keys.TAB)
    loadC6()
    find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnCompraDivida_UcCompra_FIJN1_JnC_txtQtdeParc_CAMPO"]').send_keys(str(parcela_restante), Keys.TAB)
    find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnCompraDivida_UcCompra_FIJN1_JnC_lbkIncluir"]').click()
    alert_confirm()


def dados_cliente():
    find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnDadosCliente_UcDadosPessoaisClienteSnt_FIJN1_JnC_txtNome_CAMPO"]').send_keys(Keys.SHIFT+Keys.HOME, Keys.BACKSPACE, nome_cliente, Keys.ENTER)
    time.sleep(1)
    sex_xpath = '//*[@id="ctl00_Cph_UcPrp_FIJN1_JnDadosCliente_UcDadosPessoaisClienteSnt_FIJN1_JnC_cbxSexo_CAMPO"]/option[3]' if sexo_cliente == 'Feminino' else '//*[@id="ctl00_Cph_UcPrp_FIJN1_JnDadosCliente_UcDadosPessoaisClienteSnt_FIJN1_JnC_cbxSexo_CAMPO"]/option[2]'
    sex = find_xpath(sex_xpath)
    sex.click()
    time.sleep(1)
    find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnDadosCliente_UcDadosPessoaisClienteSnt_FIJN1_JnC_cbxEstadoCivil_CAMPO"]/option[2]').click()
    time.sleep(1)
    find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnDadosCliente_UcDadosPessoaisClienteSnt_FIJN1_JnC_txtDocumento_CAMPO"]').send_keys(Keys.SHIFT+Keys.UP, Keys.BACKSPACE, Keys.SHIFT+Keys.DOWN, Keys.BACKSPACE)
    find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnDadosCliente_UcDadosPessoaisClienteSnt_FIJN1_JnC_txtDocumento_CAMPO"]').send_keys(str(rg_cliente))
    time.sleep(1)
    find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnDadosCliente_UcDadosPessoaisClienteSnt_FIJN1_JnC_txtMae_CAMPO"]').send_keys(Keys.SHIFT+Keys.HOME, Keys.BACK_SPACE, mae_cliente)
    time.sleep(0.5)
    # if str(ddd_cliente) == "0" or str(ddd_cliente) == "":
    #     find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnDadosCliente_UcDadosPessoaisClienteSnt_FIJN1_JnC_txtDddTelResidencial_CAMPO"]').send_keys(Keys.SHIFT+Keys.HOME, Keys.BACKSPACE, str(ddd_celular))
    #     find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnDadosCliente_UcDadosPessoaisClienteSnt_FIJN1_JnC_txtDddTelResidencial_CAMPO"]').send_keys(Keys.SHIFT+Keys.HOME, Keys.BACKSPACE, str(celular))
    #     time.sleep(1)
    #     find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnDadosCliente_UcDadosPessoaisClienteSnt_FIJN1_JnC_txtDddTelCelular_CAMPO"]').send_keys(Keys.SHIFT+Keys.HOME, Keys.BACKSPACE, str(ddd_celular))
    #     find_xpath('///*[@id="ctl00_Cph_UcPrp_FIJN1_JnDadosCliente_UcDadosPessoaisClienteSnt_FIJN1_JnC_txtTelCelular_CAMPO"]').send_keys(Keys.SHIFT+Keys.HOME, Keys.BACKSPACE, str(celular))
    # else:
    if ddd_cliente == "0" or ddd_cliente == "":
        ddd = find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnDadosCliente_UcDadosPessoaisClienteSnt_FIJN1_JnC_txtDddTelResidencial_CAMPO"]')
        sendKeys(ddd, str(ddd_celular))
        time.sleep(1)
        telefone = find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnDadosCliente_UcDadosPessoaisClienteSnt_FIJN1_JnC_txtTelResidencial_CAMPO"]')
        sendKeys(telefone, str(celular))
        time.sleep(1)
        ddd2 = find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnDadosCliente_UcDadosPessoaisClienteSnt_FIJN1_JnC_txtDddTelCelular_CAMPO"]')
        sendKeys(ddd2, str(ddd_celular))
        time.sleep(1)
        telefone2 = find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnDadosCliente_UcDadosPessoaisClienteSnt_FIJN1_JnC_txtTelCelular_CAMPO"]')
        sendKeys(telefone2, str(celular))
    else:
        ddd = find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnDadosCliente_UcDadosPessoaisClienteSnt_FIJN1_JnC_txtDddTelResidencial_CAMPO"]')
        sendKeys(ddd, str(ddd_cliente))
        time.sleep(1)
        telefone = find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnDadosCliente_UcDadosPessoaisClienteSnt_FIJN1_JnC_txtTelResidencial_CAMPO"]')
        sendKeys(telefone, str(telefone_cliente))
        time.sleep(1)
        ddd2 = find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnDadosCliente_UcDadosPessoaisClienteSnt_FIJN1_JnC_txtDddTelCelular_CAMPO"]')
        sendKeys(ddd2, str(ddd_cliente))
        time.sleep(1)
        telefone2 = find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnDadosCliente_UcDadosPessoaisClienteSnt_FIJN1_JnC_txtTelCelular_CAMPO"]')
        sendKeys(telefone2, str(telefone_cliente))
    find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnDadosCliente_UcDadosPessoaisClienteSnt_FIJN1_JnC_cbxUFDoc_CAMPO"]').send_keys(str(uf_rg_cliente))
    find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnDadosCliente_UcDadosPessoaisClienteSnt_FIJN1_JnCR_txtCEP_CAMPO"]').send_keys(Keys.SHIFT+Keys.UP, Keys.BACKSPACE)
    find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnDadosCliente_UcDadosPessoaisClienteSnt_FIJN1_JnCR_txtCEP_CAMPO"]').send_keys(str(cep_cliente), Keys.TAB)
    alert_confirm()
    loadC6()
    time.sleep(0.5)
    endereco = find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnDadosCliente_UcDadosPessoaisClienteSnt_FIJN1_JnCR_txtEndereco_CAMPO"]')
    sendKeys(endereco, str(endereco_cliente))
    time.sleep(0.5)
    numero = find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnDadosCliente_UcDadosPessoaisClienteSnt_FIJN1_JnCR_txtNumero_CAMPO"]')
    sendKeys(numero, str(numero_casa_cliente))
    time.sleep(0.5)
    bairro = find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnDadosCliente_UcDadosPessoaisClienteSnt_FIJN1_JnCR_txtBairro_CAMPO"]')
    sendKeys(bairro, str(bairro_cliente))
    time.sleep(0.5)
    try:
        find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnDadosCliente_UcDadosPessoaisClienteSnt_FIJN1_JnCR_txtCidade_CAMPO"]').send_keys(str(cidade_cliente))
        find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnDadosCliente_UcDadosPessoaisClienteSnt_FIJN1_JnCR_cbxUF_CAMPO"]').send_keys(str(uf_endereco_cliente))
    except:
        pass
    time.sleep(0.5)


def calculo():
    find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnSimulacao_UcSimulacaoSnt_FIJanela1_FIJanelaPanel1_txtVlrParcela_CAMPO"]').send_keys(Keys.SHIFT+Keys.HOME, Keys.BACK_SPACE)
    find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnSimulacao_UcSimulacaoSnt_FIJanela1_FIJanelaPanel1_txtVlrParcela_CAMPO"]').send_keys(str(parcela), Keys.TAB)
    find_xpath('//*[@id="btnCalcular_txt"]').click()
    alert_confirm()
    time.sleep(0.5)
    loadC6()
    try:
        driver.find_element(By.XPATH, '//*[@id="ctl00_Cph_UcPrp_FIJN1_JnSimulacao_UcSimulacaoSnt_FIJanela1_FIJanelaPanel1_grdCondicoes_ctl02_ckSelecao"]').click()
    except:
        pass
    alert_confirm()
    time.sleep(0.5)


def averbacao():
    especie = find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnClientes_UcDadosClienteSnt_FIJN1_JnC_txtBeneficio_CAMPO"]')
    sendKeys(especie, str(especie_cliente))
    time.sleep(0.5)
    loadC6()
    uf_nb = find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnClientes_UcDadosClienteSnt_FIJN1_JnC_cbxUFBeneficio_CAMPO"]')
    sendKeys(uf_nb, str(uf_beneficio_cliente))
    find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnClientes_UcDadosClienteSnt_FIJN1_JnC_cbxCartaoBeneficio_CAMPO"]/option[1]').click()
    time.sleep(0.5)
    banco = find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnClientes_UcDadosClienteSnt_FIJN1_JnC_UcDadosBancarios_txtBanco_CAMPO"]')
    sendKeys(banco, str(banco_cliente))
    loadC6()
    time.sleep(0.5)
    agencia = find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnClientes_UcDadosClienteSnt_FIJN1_JnC_UcDadosBancarios_txtAgencia_CAMPO"]')
    sendKeys(agencia, str(agencia_cliente))
    loadC6()
    time.sleep(0.5)
    try:
        find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnClientes_UcDadosClienteSnt_FIJN1_JnC_UcDadosBancarios_txtDvAgencia_CAMPO"]').send_keys('0')
        find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnClientes_UcDadosClienteSnt_FIJN1_JnC_UcDadosBancarios_txtDvAgencia_CAMPO"]').send_keys(Keys.TAB)
        time.sleep(0.5)
    except:
        pass
    loadC6()
    conta = find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnClientes_UcDadosClienteSnt_FIJN1_JnC_UcDadosBancarios_txtConta_CAMPO"]')
    sendKeys(conta, str(conta_cliente))
    loadC6()
    time.sleep(0.5)
    dv = find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnClientes_UcDadosClienteSnt_FIJN1_JnC_UcDadosBancarios_txtDvConta_CAMPO"]')
    sendKeys(dv, dv_conta)
    loadC6()
    time.sleep(0.5)
    try:
        find_xpath('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnClientes_UcDadosClienteSnt_FIJN1_FIJanelaPanel3_txtCpfOrigem3o_CAMPO"]').send_keys('01862439524', Keys.TAB)
    except:
        pass


def popup1():
    time.sleep(1)
    driver.switch_to.frame('ctl00_Cph_UcPrp_popConfirmacao_frameAjuda')
    find_xpath('//*[@id="btnCancelar_txt"]').click()
    driver.switch_to.default_content()


def popup2():
    time.sleep(1)
    driver.switch_to.frame('ctl00_Cph_UcPrp_popConfirmacao_frameAjuda')
    find_xpath('//*[@id="btnGravar_txt"]').click()
    driver.switch_to.default_content()


def select_refin():
    loadC6()
    alert_confirm()
    time.sleep(0.5)
    elementClickable('//*[@id="ctl00_Cph_UcPrp_FIJN1_JnDadosIniciais_UcDIni_cboTipoProduto_CAMPO"]/option[2]').click()
    time.sleep(0.5)
    loadC6()
    parcela_refin = find_id('ctl00_Cph_UcPrp_FIJN1_JnSimulacao_UcSimulacaoSnt_FIJanela1_FIJanelaPanel1_txtVlrParcela_CAMPO')
    parcela_refin.click()
    sendKeys(parcela_refin, str(parcela))
    alert_confirm()
    time.sleep(0.5)
    find_xpath('//*[@id="btnCalcular_txt"]').click()
    alert_confirm()
    time.sleep(0.5)
    loadC6()
    try:
        tabela5 = find_id('ctl00_Cph_UcPrp_FIJN1_JnSimulacao_UcSimulacaoSnt_FIJanela1_FIJanelaPanel1_grdCondicoes_ctl06_ckSelecao')
        tabela5.click()
        time.sleep(0.5)
        alert_confirm()
        find_xpath('//*[@id="btnGravar_txt"]').click()
        loadC6()
        alert_confirm()
        info_label.config(text=f"Digitado {parcela}")
    except:
        pass


def gravar_proposta():
    try:
        find_xpath('//*[@id="btnGravar_txt"]').click()
        loadC6()
        alert_confirm()
        time.sleep(0.5)
        try:
            popup1()
            alert_confirm()
            loadC6()
            popup2()
            alert_confirm()
            loadC6()
            select_refin()
        except:
            pass
        base = pd.DataFrame()
    except:
        info_label.config(text="Falha ao gravar")


def logout_c6():
    logout_button = driver.find_element(By.XPATH, '//*[@id="ctl00_lk_Sair"]')
    logout_button.click()


def digitando_proposta():
    try:
        iniciar_digitacao()
    except:
        pass
    dados_iniciais()
    dados_port()
    dados_cliente()
    calculo()
    averbacao()
    try:
        gravar_proposta()
    except:
        pass


def digitando_manual():
    iniciar_digitacao()
    dados_iniciais()
    dados_port()
    dados_cliente()
    calculo()
    averbacao()

#################facta

def loadFacta():
    # Function for the load icon
    time.sleep(1)
    try:
        load = driver.find_element(By.ID, 'statusGiraGira')
        waitload = WebDriverWait(driver, 60)
        if load:
            waitload.until(EC.invisibility_of_element(
                (By.ID, 'statusGiraGira')))
    except:
        pass
    time.sleep(1)


def openProp():
    driver.get('https://desenv.facta.com.br/sistemaNovo/propostaSimulador.php')
    loadFacta()


def writeProp():
    # Remember to optimize this
    find_xpath('//*[@id="produto"]/option[7]').click()  # Select venda digital
    # Select Port + refin
    find_xpath('//*[@id="tipoOperacao"]/option[19]').click()
    find_xpath('//*[@id="averbador"]/option[3]').click()  # Select orgao inss
    find_xpath('//*[@id="banco"]/option[2]').click()  # Select Facta Financeira


def clientData():
    driver.execute_script(f"document.getElementById('cpf').value = '{cpf_planilha}';")
    driver.execute_script(f"document.getElementById('dataNascimento').value = '{data_nascimento_cliente}';")
    driver.execute_script(f"document.getElementById('nomeCliente').value = '{nome_cliente}';")
    nb = find_id('codigoBeneficio')
    driver.execute_script(f"document.getElementById('codigoBeneficio').value = '{str(matricula_cliente).replace("-", "").replace(".", "").strip()}';")
    nb.send_keys(Keys.TAB)
    time.sleep(0.5)
    loadFacta()


def portData():
    driver.execute_script(f"document.getElementById('ajinContratoPortado').value = '{str(num_ctt)}';")
    contract = find_xpath('//*[@id="ajinContratoPortado"]')
    contract.send_keys(Keys.TAB)
    time.sleep(0.5)
    loadFacta()
    driver.execute_script(f"document.getElementById('valorParcelaPort').value = '{str(parcela).replace(".", "").replace(",", ".").strip()}';")
    term = find_xpath('//*[@id="prazoRestantePort_Original"]')
    sendKeys(term, str(parcela_total))
    time.sleep(0.5)
    term_left = find_xpath('//*[@id="prazoRestantePort"]')
    sendKeys(term_left, str(parcela_restante))
    time.sleep(0.5)
    try:
        find_xpath('//*[@id="divContakoWidgetJSPopUpIntegrado"]/img[1]').click()
    except:
        pass
    calculator = find_xpath('//*[@id="tab1"]/fieldset[10]/div/div[6]/img')
    calculator.click()
    loadFacta()
    time.sleep(0.5)
    driver.execute_script(f"document.getElementById('valorSaldoDevedorPort').value = '{str(saldo_devedor_planilha).replace(".", "").replace(",", ".").strip()}';")
    driver.execute_script(f"document.getElementById('valorSaldoDevedorRefinPort').value = '{str(saldo_devedor_planilha).replace(".", "").replace(",", ".").strip()}';")
    driver.execute_script(f"document.getElementById('valorParcelaRefinPort').value = '{str(parcela).replace(".", "").replace(",", ".").strip()}';")
    term_ref = find_id('prazoRefinPort')
    sendKeys(term_ref, '84')
    time.sleep(0.5)
    search_button = find_id('pesquisar')
    search_button.click()
    time.sleep(0.5)
    loadFacta()
    WebDriverWait(driver, 60).until(EC.invisibility_of_element(
        (By.XPATH, '//*[@id="resultado"]/progress')))
    tablePort = driver.find_elements(By.CLASS_NAME, 'sorting_1')
    time.sleep(3)
    for table in tablePort:
        try:
            table.click()
            table.click()
            continue
        except:
            pass
    next_button = find_xpath('//*[@id="etapa1"]')
    driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
    next_button.click()
    time.sleep(3)
    loadFacta()


def firstPage():
    # A function that calls only 2 functions lol
    # This isnt good at all
    clientData()
    portData()


def secondPage():
    driver.switch_to.default_content()
    agent = find_xpath('//*[@id="vendedor"]/option[2]')
    agent.click()
    bank_code = find_xpath('//*[@id="txtCodBancoCompra[]"]')
    sendKeys(bank_code, str(bancoport_cliente))
    loadFacta()
    next_button = find_xpath('//*[@id="etapa_2"]')
    driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
    next_button.click()
    loadFacta()


def thirdPage():
    sex_xpath = '//*[@id="sexo"]/option[2]' if sexo_cliente == 'Feminino' else '//*[@id="sexo"]/option[3]'
    sex = find_xpath(sex_xpath)
    sex.click()
    time.sleep(0.5)
    stat = find_xpath('//*[@id="estadoCivil"]/option[9]')
    stat.click()
    time.sleep(0.5)
    rg = find_xpath('//*[@id="rg"]')
    sendKeys(rg, str(rg_cliente))
    time.sleep(0.5)
    ssp = find_xpath('//*[@id="orgaoEmissor"]/option[2]')
    ssp.click()
    time.sleep(0.5)
    uf = find_xpath('//*[@id="estadoRg"]')
    sendKeys(uf, str(uf_rg_cliente))
    time.sleep(0.5)
    exp = find_xpath('//*[@id="emissaoRg"]')
    sendKeys(exp, '07/11/2017 ')
    time.sleep(0.5)
    nation = find_xpath('//*[@id="nacionalidade"]/option[2]')
    nation.click()
    time.sleep(0.5)
    loadFacta()
    find_xpath('//*[@id="estadoNatural"]/option[2]').click()
    time.sleep(0.5)
    loadFacta()
    uf_birth = find_xpath('//*[@id="estadoNatural"]')
    sendKeys(uf_birth, str(uf_nascimento))
    loadFacta()
    time.sleep(1)
    city_birth = find_xpath('//*[@id="cidadeNatural"]')
    sendKeys(city_birth, str(cidade_nascimento))
    loadFacta()
    mother_name = find_xpath('//*[@id="nomeMae"]')
    sendKeys(mother_name, mae_cliente)
    father_name = find_xpath('//*[@id="nomePai"]')
    sendKeys(father_name, str(pai_cliente))
    value_pat = find_xpath('//*[@id="valorPatrimonio"]/option[2]')
    value_pat.click()
    illiterate = find_xpath('//*[@id="clienteAnalfabeto"]/option[3]')
    illiterate.click()
    num_beneficio = str(matricula_cliente)
    # Get an example to optmize this if statement
    # I cant get a data who gets 2 numBeneficio

    try:
        input_beneficio = driver.find_element(By.XPATH, '//*[@id="tab3"]/fieldset[2]/div[2]/div[3]')
        sendKeys(input_beneficio, num_beneficio)
    except:
        pass

    try:
        find_xpath('//*[@id="campoBeneficio"]/option[2]').click()
        loadFacta()
        time.sleep(0.5)
        nb = find_id('matricula').get_attribute("value")
        if nb == num_beneficio:
            find_xpath('//*[@id="campoBeneficio"]/option[2]').click()
            time.sleep(0.5)
            loadFacta()
        if nb != num_beneficio:
            find_xpath('//*[@id="campoBeneficio"]/option[3]').click()
            time.sleep(0.5)
            loadFacta()
            if nb == num_beneficio:
                pass
    except:
        pass

    income = find_xpath('//*[@id="valorDoBeneficio"]')
    sendKeys(income, '5230,00')
    cep = find_xpath('//*[@id="cep"]')
    softWriter(cep, str(cep_cliente))
    time.sleep(0.5)
    button_search_cep = find_xpath('//*[@id="pesquisar_cep"]')
    button_search_cep.click()
    time.sleep(1)
    try:
        button_modal = find_xpath('//*[@id="corpo"]/div[10]/div[2]/a')
        button_modal.click()
        softWriter(cep, str(cep_cliente))
    except:
        pass
    adress = find_xpath('//*[@id="endereco"]')
    sendKeys(adress, str(endereco_cliente))
    house_number = find_xpath('//*[@id="numero"]')
    sendKeys(house_number, str(numero_casa_cliente))
    comp = find_xpath('//*[@id="complemento"]')
    sendKeys(comp, 'CASA')
    nbhood = find_xpath('//*[@id="bairro"]')
    sendKeys(nbhood, str(bairro_cliente))
    city = find_xpath('//*[@id="cidade"]')
    sendKeys(city, str(cidade_cliente))
    loadFacta()
    celphone = find_xpath('//*[@id="celular"]')
    numeroTelefone = (f'0{ddd_cliente} 9{telefone_cliente[0:4]}-{telefone_cliente[4:]}' if len(
        telefone_cliente) != 10 else f'0{ddd_celular} {celular[0:4]}-{celular[4:]}' if len(telefone_cliente) >= 1 else None)
    softWriter(celphone, numeroTelefone)
    email = find_xpath('//*[@id="email"]')
    email.send_keys(Keys.SHIFT, Keys.END + Keys.BACK_SPACE)
    email.send_keys(Keys.SHIFT, Keys.HOME + Keys.BACK_SPACE)
    email_cliente = f'{str(nome_cliente[:5]).strip()}_{str(data_nascimento_cliente[6:]).strip()}@GMAIL.COM'
    email_cliente = email_cliente.lower()
    softWriter(email, str(email_cliente))
    next_button = find_xpath('//*[@id="etapa_3"]')
    driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
    next_button.click()
    try:
        button_modal_celphone = find_xpath('//*[@id="corpo"]/div[10]/div[2]/a')
        button_modal_celphone.click()
        new_digits = '42'
        new_number = numeroTelefone[:-2] + new_digits
        softWriter(celphone, new_number)
        next_button.click()
    except:
        pass
    modalContrat = find_xpath(
        '//*[@id="modalSeguroCombo"]/div/div/div[2]/div/div/button[2]')
    modalContrat.click()


def fourthPage():
    loadFacta()
    try:
        account_type = find_xpath('//*[@id="tipoCreditoDesconto"]/option[2]')
        account_type.click()
        bank = find_xpath('//*[@id="bancoDesconto"]')
        sendKeys(bank, str(banco_cliente))
        agency = find_xpath('//*[@id="agenciaDesconto"]')
        sendKeys(agency, str(agencia_cliente))
        account = find_xpath('//*[@id="contaDesconto"]')
        sendKeys(account, str(f'{conta_cliente}{digito_verificador_cliente}'))
        find_xpath('//*[@id="id_tipo_profissao"]/option[2]').click()
    except:
        pass

    try:
        bank = find_xpath('//*[@id="bancoDesconto"]')
        sendKeys(bank, str(banco_cliente))
        agency = find_xpath('//*[@id="agenciaDesconto"]')
        sendKeys(agency, str(agencia_cliente))
        account = find_xpath('//*[@id="contaDesconto"]')
        sendKeys(account, str(f'{conta_cliente}{digito_verificador_cliente}'))
        find_xpath('//*[@id="id_tipo_profissao"]/option[2]').click()
    except:
        pass

    next_button = find_xpath('//*[@id="etapa_4"]')
    driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
    next_button.click()
    modal_button = find_xpath(
        '//*[@id="modalConfirmaDocumentos"]/div/div/div[2]/div[2]/button[2]')
    modal_button.click()


def propWrite():
    openProp()
    writeProp()
    firstPage()
    secondPage()
    thirdPage()
    fourthPage()
    loadFacta()
    base = pd.DataFrame()


def close_driver():
    try:
        driver.close()
        driver.quit()
    except:
        info_label.config(text="Driver não encontrado")


def propWrite2ndPage():
    secondPage()
    thirdPage()
    fourthPage()
    loadFacta()


def propWrite3ndPage():
    thirdPage()
    fourthPage()
    loadFacta()


def propWrite4ndPage():
    fourthPage()
    loadFacta()


def login_facta():
    user = login_user_facta_entry.get()
    user = user.strip()
    password = login_pass_facta_entry.get()
    password = password.strip()
    driver.get('https://desenv.facta.com.br/')
    driver.execute_script(f"document.getElementById('login').value = '{str(user)}';")
    driver.execute_script(f"document.getElementById('senha').value = '{str(password)}';")
    find_xpath('//*[@id="btnLogin"]').click()  # Button submit


def select_file_facta():
    arquivo_path = filedialog.askopenfilename(
        title="Selecione um arquivo", filetypes=[("Arquivos Excel", "*.xlsx;*.xls")])
    if arquivo_path:
        nome_arquivo = os.path.basename(arquivo_path)
        info_label.config(text=f"Arquivo selecionado: {nome_arquivo}")
        base = pd.read_excel(f'{arquivo_path}')
        global cpf_planilha
        for i,  cpf_planilha in enumerate(base['CPF']):
            global data_nascimento_cliente
            data_nascimento_cliente = base.loc[i, 'NASCIMENTO']
            global matricula_cliente
            matricula_cliente1 = base.loc[i, 'MATRICULA']
            matricula_cliente = str(matricula_cliente1) 
            global nome_cliente
            nome_cliente = base.loc[i, 'NOME']
            global sexo_cliente
            sexo_cliente = base.loc[i, 'SEXO']
            global mae_cliente
            mae_cliente = base.loc[i, 'MAE']
            global pai_cliente
            pai_cliente = base.loc[i, 'PAI']
            global uf_nascimento
            uf_nascimento = base.loc[i, 'UF_NASCIMENTO']
            global uf_rg_cliente
            uf_rg_cliente = base.loc[i, 'UF_RG']
            global cidade_nascimento
            cidade_nascimento = base.loc[i, 'CIDADE_NASCIMENTO']
            global rg_cliente
            rg_cliente = base.loc[i, 'IDENTIDADE']
            global ddd_cliente
            ddd_cliente = str(base.loc[i, 'DDD'])
            global telefone_cliente
            telefone_cliente = str(base.loc[i, 'TELEFONE'])
            global ddd_celular
            ddd_celular = str(base.loc[i, 'DDD_2'])
            global celular
            celular = str(base.loc[i, 'CELULAR'])
            global especie_cliente
            especie_cliente = base.loc[i, 'ESPECIE']
            global cep_cliente
            cep_cliente = base.loc[i, 'CEP']
            global endereco_cliente
            endereco_cliente = base.loc[i, 'ENDERECO']
            global numero_casa_cliente
            numero_casa_cliente = base.loc[i, 'NUMERO']
            global bairro_cliente
            bairro_cliente = base.loc[i, 'BAIRRO']
            global cidade_cliente
            cidade_cliente = base.loc[i, 'CIDADE']
            global uf_endereco_cliente
            uf_endereco_cliente = base.loc[i, 'UF_ENDERECO']
            global uf_beneficio_cliente
            uf_beneficio_cliente = base.loc[i, 'UF_ENDERECO']
            global banco_cliente
            banco_cliente = base.loc[i, 'BANCO_NB']
            global agencia_cliente
            agencia_cliente = base.loc[i, 'AGENCIA_NB']
            global conta_cliente
            conta_cliente = base.loc[i, 'CONTA_NB']
            global digito_verificador_cliente
            digito_verificador_cliente = base.loc[i, 'DV_NB']
            global bancoport_cliente
            bancoport_cliente = base.loc[i, 'BANCO_PORT']
            global num_ctt
            num_ctt = base.loc[i, 'NUM_CONTRATO']
            global parcela
            parcela = base.loc[i, 'PARCELA']
            global parcela_total
            parcela_total = base.loc[i, 'NUM_PARCELA_TOTAL']
            global parcela_restante
            parcela_restante = base.loc[i, 'PAR_RESTANTE']
            global saldo_devedor_planilha
            saldo_devedor_planilha = base.loc[i, 'SALDO']
            if numero_casa_cliente == "SN":
                numero_casa_cliente = 1
    else:
        info_label.config(text="Nenhum arquivo selecionado")

#####

def alert_confirm_crefisa():
    try:
        wait = WebDriverWait(driver, 3)
        wait.until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()
    except:
        pass


def loadCrefisa():
    time.sleep(1)
    try:
        load = driver.find_element(By.ID, 'ctl00_Image2')
        waitload = WebDriverWait(driver, 90)
        waitload.until(EC.invisibility_of_element((By.ID, 'ctl00_Image2')))
    except:
        pass


def login_crefisa():
    try:
        usuario = login_user_crefisa.get()
        usuario = usuario.strip()
        senha = login_senha_crefisa_entry.get()
        senha = senha.strip()
        driver.get('https://sfc.sistemascr.com.br/autorizador/Login/AC.UI.LOGIN.aspx')
        find_xpath('//*[@id="EUsuario_CAMPO"]').send_keys(str(usuario))
        find_xpath('//*[@id="ESenha_CAMPO"]').send_keys(str(senha))
        find_xpath('//*[@id="lnkEntrar"]').click()
        alert_confirm_crefisa()
        info_label.config(text='Login efetuado')
    except:
        info_label.config(text='Erro ao logar')


def open_writer_crefisa(): 
    alert_confirm_crefisa()
    WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.LINK_TEXT, 'Cadastro')))
    cadastro = driver.find_element(By.LINK_TEXT, 'Cadastro')
    action.move_to_element(cadastro).perform()
    proposta = driver.find_element(By.LINK_TEXT, 'Proposta Consignado')
    action.move_to_element(proposta).click().perform()
    time.sleep(0.5)


def iniciar_digitacao_crefisa():
    alert_confirm_crefisa()
    driver.get('https://sfc.sistemascr.com.br/autorizador/MenuWeb/Cadastro/Proposta/UI.PropostaSintetizada.aspx?Origem3=032052')
    elementClickable('//*[@id="ctl00_Cph_UcPrp_J1_JnDadoIni_UcDIni_cboTipoOperacao_CAMPO"]/option[3]').click()
    elementClickable('//*[@id="ctl00_Cph_UcPrp_J1_JnDadoIni_UcDIni_cboGrupoConvenio_CAMPO"]/option[5]').click()
    elementClickable('//*[@id="ctl00_Cph_UcPrp_J1_JnDadoIni_UcDIni_cboOrigem4_CAMPO"]/option[2]').click()


def dados_iniciais_crefisa():
    time.sleep(1)
    find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnDadoIni_UcDIni_txtCPF_CAMPO"]').send_keys((str(cpf_planilha)), Keys.TAB)
    alert_confirm_crefisa()
    loadCrefisa()
    try:
        driver.switch_to.frame('ctl00_Cph_UcPrp_J1_JnDadoIni_UcDIni_popCliente_panelAjuda')
        driver.find_element(By.XPATH, '//*[@id="ctl00_cph_FIJanela1_FIJanelaPanel1_btnNovo_dvTxt"]/table/tbody/tr/td').click()
        time.sleep(1)
        driver.switch_to.default_content()
        loadCrefisa()
    except:
        pass
    alert_confirm_crefisa()
    loadCrefisa()
    nasc = find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnDadoIni_UcDIni_txtDataNascimento_CAMPO"]')
    sendKeys(nasc, (str(data_nascimento_cliente)))
    loadCrefisa()
    if(len(matricula_cliente) == 10):
        find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnDadoIni_UcDIni_ucMatr_txtMatricula_CAMPO"]').send_keys(str(matricula_cliente), Keys.TAB)
    else:
        find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnDadoIni_UcDIni_ucMatr_txtMatricula_CAMPO"]').send_keys(str(matricula_cliente).zfill(10), Keys.TAB)
    time.sleep(0.5)
    loadCrefisa()
    find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnDadoIni_UcDIni_txtRenda_CAMPO"]').send_keys("3782,55", Keys.TAB)
    loadCrefisa()
    time.sleep(0.5)
    btn_obt = find_id('btnObterMargem_txt')
    btn_obt.click()
    try:
        wait = WebDriverWait(driver, 5)
        wait.until(EC.alert_is_present())
        alert = driver.switch_to.alert
        loadCrefisa()
        if alert:
            #alert.accept()
            loadCrefisa()
            time.sleep(0.5)
            find_xpath('//*[@id="btnAutorizacao_txt"]').click()
            loadCrefisa()
            alert_confirm_crefisa()
            driver.switch_to.frame('ctl00_Cph_UcPrp_J1_JnDadoIni_UcDIni_popBeneficiarioTermo_frameAjuda')
            time.sleep(0.5)
            find_xpath('//*[@id="ctl00_cph_jp1_pnlDadosBeneficiario_Container_AbaTermoAutorizacao_txtNomeCli_CAMPO"]').send_keys(str(nome_cliente), Keys.TAB)
            time.sleep(0.5)
            find_xpath('//*[@id="ctl00_cph_jp1_pnlDadosBeneficiario_Container_AbaTermoAutorizacao_txtLocalAssTermo_CAMPO"]').send_keys(str(cidade_cliente), Keys.TAB)
            time.sleep(0.5)
            find_xpath('//*[@id="btnImprimirTermo_txt"]').click()
            alert_confirm_crefisa()
            time.sleep(1)
            loadCrefisa()
            find_xpath('//*[@id="__tab_ctl00_cph_jp1_pnlDadosBeneficiario_Container_ConsultaDadosBeneficio"]').click()
            loadCrefisa()
            chave = find_xpath('//*[@id="ctl00_cph_jp1_pnlDadosBeneficiario_Container_ConsultaDadosBeneficio_cboChaveTermo_CAMPO"]')
            chave.click()
            chave.send_keys(Keys.PAGE_DOWN, Keys.TAB)
            loadCrefisa()
            alert_confirm_crefisa()
            rg_option = find_xpath('//*[@id="ctl00_cph_jp1_pnlDadosBeneficiario_Container_ConsultaDadosBeneficio_cboDocIdentifCli_CAMPO"]/option[7]')
            rg_option.click()
            time.sleep(1)
            loadCrefisa()
            elementClickable('//*[@id="ctl00_cph_jp1_pnlDadosBeneficiario_Container_ConsultaDadosBeneficio_grdArquivosUpload_ctl02_btnAnexarArquivoUpload"]')
            time.sleep(0.5)
            try:
                button1 = driver.find_element(By.ID, 'FileMultArqUpload')
                button1.send_keys(os.getcwd() + "/imagem.png")
                time.sleep(0.5)
                loadCrefisa()
                alert_confirm_crefisa()
                find_xpath('//*[@id="btnRealizarUpload_txt"]').click()
                loadCrefisa()
                alert_confirm_crefisa()
            except:
                pass
            try:
                button2 = driver.find_element(By.ID, 'FileUpGrd2')
                button2.send_keys(os.getcwd() + "/imagem.png")
                time.sleep(0.5)
                loadCrefisa()
                alert_confirm_crefisa()
            except:
                pass
            find_xpath('//*[@id="btnSolicitarAutorizacao_txt"]').click()
            time.sleep(0.5)
            alert_confirm_crefisa()
            loadCrefisa()
            find_xpath('//*[@id="btnVoltar_txt"]').click()
            loadCrefisa()
            driver.switch_to.default_content()
            find_xpath('//*[@id="btnObterMargem_txt"]').click()
            loadCrefisa()
    except:
        print('ja possui consulta in100')
        loadCrefisa()


def dados_port_crefisa():
    loadCrefisa()
    find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnCpaDiv_UcCompra_FIJN1_JnC_cboTipoQuitacao_CAMPO"]/option[1]').click()
    find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnCpaDiv_UcCompra_FIJN1_JnC_txtBanco_CAMPO"]').send_keys(str(bancoport_cliente), Keys.TAB)
    loadCrefisa()
    alert_confirm_crefisa()
    find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnCpaDiv_UcCompra_FIJN1_JnC_txtNrContrato_CAMPO"]').send_keys(str(num_ctt), Keys.TAB)
    find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnCpaDiv_UcCompra_FIJN1_JnC_txtValorParcela_CAMPO"]').send_keys(str(parcela), Keys.TAB)
    find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnCpaDiv_UcCompra_FIJN1_JnC_txtValorQuitacaoDivida_CAMPO"]').send_keys(str(saldo_devedor_planilha), Keys.TAB)
    find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnCpaDiv_UcCompra_FIJN1_JnC_txtQtdeParc_CAMPO"]').send_keys(str(parcela_restante), Keys.TAB)
    find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnCpaDiv_UcCompra_FIJN1_JnC_cboEnteConsignante_CAMPO"]/option[2]').click()
    find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnCpaDiv_UcCompra_FIJN1_JnC_lbkIncluir"]').click()
    loadCrefisa()


def dados_cliente_crefisa():
    find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnDadoCli_UcDadosPessoaisClienteSnt_FIJN1_JnC_txtNatural_CAMPO"]').send_keys(str(cidade_nascimento), Keys.TAB)
    time.sleep(0.5)
    sex_xpath = '//*[@id="ctl00_Cph_UcPrp_J1_JnDadoCli_UcDadosPessoaisClienteSnt_FIJN1_JnC_cbxSexo_CAMPO"]/option[3]' if sexo_cliente == 'Feminino' else '//*[@id="ctl00_Cph_UcPrp_J1_JnDadoCli_UcDadosPessoaisClienteSnt_FIJN1_JnC_cbxSexo_CAMPO"]/option[2]'
    sex = find_xpath(sex_xpath)
    sex.click()
    time.sleep(0.5)
    find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnDadoCli_UcDadosPessoaisClienteSnt_FIJN1_JnC_cbxEstadoCivil_CAMPO"]/option[2]').click()
    time.sleep(0.5)
    find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnDadoCli_UcDadosPessoaisClienteSnt_FIJN1_JnC_txtDocumento_CAMPO"]').send_keys(str(rg_cliente), Keys.TAB)
    time.sleep(0.5)
    find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnDadoCli_UcDadosPessoaisClienteSnt_FIJN1_JnC_txtEmissor_CAMPO"]').send_keys('SSP')
    time.sleep(0.5)
    find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnDadoCli_UcDadosPessoaisClienteSnt_FIJN1_JnC_cbxUFDoc_CAMPO"]').send_keys(str(uf_rg_cliente), Keys.TAB)
    time.sleep(0.5)
    find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnDadoCli_UcDadosPessoaisClienteSnt_FIJN1_JnC_txtDataEmissao_CAMPO"]').send_keys('08/05/2012')
    time.sleep(0.5)
    find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnDadoCli_UcDadosPessoaisClienteSnt_FIJN1_JnC_txtMae_CAMPO"]').send_keys(str(mae_cliente), Keys.TAB)
    time.sleep(0.5)
    find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnDadoCli_UcDadosPessoaisClienteSnt_FIJN1_JnC_txtDddTelResidencial_CAMPO"]').send_keys(str(ddd_celular), Keys.TAB)
    time.sleep(0.5)
    find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnDadoCli_UcDadosPessoaisClienteSnt_FIJN1_JnC_txtTelResidencial_CAMPO"]').send_keys(str(celular), Keys.TAB)
    time.sleep(0.5)
    find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnDadoCli_UcDadosPessoaisClienteSnt_FIJN1_JnCR_txtCEP_CAMPO"]').send_keys(str(cep_cliente), Keys.TAB)
    alert_confirm_crefisa()
    loadCrefisa()
    time.sleep(0.5)
    find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnDadoCli_UcDadosPessoaisClienteSnt_FIJN1_JnCR_txtEndereco_CAMPO"]').send_keys(str(endereco_cliente), Keys.TAB)
    time.sleep(0.5)
    find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnDadoCli_UcDadosPessoaisClienteSnt_FIJN1_JnCR_txtNumero_CAMPO"]').send_keys(str(numero_casa_cliente), Keys.TAB)
    time.sleep(0.5)
    find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnDadoCli_UcDadosPessoaisClienteSnt_FIJN1_JnCR_txtBairro_CAMPO"]').send_keys(str(bairro_cliente), Keys.TAB)
    time.sleep(0.5)
    try:
        find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnDadoCli_UcDadosPessoaisClienteSnt_FIJN1_JnCR_txtCidade_CAMPO"]').send_keys(str(cidade_cliente), Keys.TAB)
        time.sleep(0.5)
        find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnDadoCli_UcDadosPessoaisClienteSnt_FIJN1_JnCR_cbxUF_CAMPO"]').send_keys(str(uf_endereco_cliente), Keys.TAB)
        time.sleep(0.5)
    except:
        pass


def simula_port_crefisa():
    parcela_c = find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnSim_UcSimulacaoSnt_J1_JP1_txtVlrParcela_CAMPO"]')
    sendKeys(parcela_c, str(parcela))
    time.sleep(0.5)
    find_xpath('//*[@id="btnCalcular_txt"]').click()
    loadCrefisa()
    time.sleep(1)
    alert_confirm_crefisa()
    try:
        find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnSim_UcSimulacaoSnt_J1_JP1_grdCondicoes_ctl02_ckSelecao"]').click()
    except:
        pass
    loadCrefisa()
    alert_confirm_crefisa()
    especie = find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnCli_UcDadosClienteSnt_J1_JP_txtBeneficio_CAMPO"]')
    sendKeys(especie, str(especie_cliente))
    loadCrefisa()
    time.sleep(0.5)
    uf_nb = find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnCli_UcDadosClienteSnt_J1_JP_cbxUFBeneficio_CAMPO"]')
    sendKeys(uf_nb, str(uf_beneficio_cliente))
    time.sleep(0.5)
    bank = find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnCli_UcDadosClienteSnt_J1_JP_UcDadoBanc_txtBanco_CAMPO"]')
    sendKeys(bank, str(banco_cliente))
    loadCrefisa()
    time.sleep(0.5)
    agencia = find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnCli_UcDadosClienteSnt_J1_JP_UcDadoBanc_txtAgencia_CAMPO"]')
    sendKeys(agencia, str(agencia_cliente))
    loadCrefisa()
    time.sleep(0.5)
    conta = find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnCli_UcDadosClienteSnt_J1_JP_UcDadoBanc_txtConta_CAMPO"]')
    sendKeys(conta, str(conta_cliente))
    time.sleep(0.5)
    dv = find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnCli_UcDadosClienteSnt_J1_JP_UcDadoBanc_txtDvConta_CAMPO"]')
    sendKeys(dv, str(dv_conta))


def gravar_port_crefisa():
    find_xpath('//*[@id="btnGravar_txt"]').click()
    loadCrefisa()
    driver.switch_to.frame('ctl00_Cph_UcPrp_popConfirmacao_frameAjuda')
    find_xpath('//*[@id="btnCancelar_txt"]').click()
    driver.switch_to.default_content()
    loadCrefisa()
    driver.switch_to.frame('ctl00_Cph_UcPrp_popConfirmacao_frameAjuda')
    find_xpath('//*[@id="btnCancelar_txt"]').click()
    driver.switch_to.default_content()
    loadCrefisa()
    driver.switch_to.frame('ctl00_Cph_UcPrp_popConfirmacao_frameAjuda')
    find_xpath('//*[@id="btnGravar_txt"]').click()
    driver.switch_to.default_content()


def gravar_port_crefisa_refin_crefisa():
    find_xpath('//*[@id="btnGravar_txt"]').click()
    loadCrefisa()
    driver.switch_to.frame('ctl00_Cph_UcPrp_popConfirmacao_frameAjuda')
    find_xpath('//*[@id="btnCancelar_txt"]').click()
    driver.switch_to.default_content()
    loadCrefisa()
    driver.switch_to.frame('ctl00_Cph_UcPrp_popConfirmacao_frameAjuda')
    find_xpath('//*[@id="btnGravar_txt"]').click()
    driver.switch_to.default_content()
    alert_confirm_crefisa()
    loadCrefisa()


def refin_port_crefisa():
    driver.switch_to.default_content()
    parcela_c = find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnSim_UcSimulacaoSnt_J1_JP1_txtVlrParcela_CAMPO"]')
    sendKeys(parcela_c, str(parcela))
    valor_financiado = find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnSim_UcSimulacaoSnt_J1_JP1_txtVlrSolicitado_CAMPO"]')
    sendKeys(valor_financiado, '')
    find_xpath('//*[@id="btnCalcular_txt"]').click()
    alert_confirm_crefisa()
    time.sleep(0.5)
    loadCrefisa()
    find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnSim_UcSimulacaoSnt_J1_JP1_grdCondicoes_ctl02_ckSelecao"]').click()
    loadCrefisa()
    find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnCli_UcDadosClienteSnt_J1_JP2_UcDadoPgto_cbxTipoConta_CAMPO"]/option[2]').click()
    find_xpath('//*[@id="btnGravar_txt"]').click()
    loadCrefisa()
    info_label.config(text=f"Digitado: {nome_arquivo}")
    alert_confirm_crefisa()
    

def digitar_crefisa():
    try:
        open_writer_crefisa()
    except:
        pass
    iniciar_digitacao_crefisa()
    dados_iniciais_crefisa()
    dados_port_crefisa()
    dados_cliente_crefisa()
    simula_port_crefisa()
    gravar_port_crefisa_refin_crefisa()
    refin_port_crefisa()


def digitar_port_crefisa():
    try:
        open_writer_crefisa()
    except:
        pass
    iniciar_digitacao_crefisa()
    dados_iniciais_crefisa()
    dados_port_crefisa()
    dados_cliente_crefisa()
    simula_port_crefisa()
    gravar_port_crefisa()


janela = Tk()
janela.title("")

info_label = ttk.Label(janela, text=" ")
info_label.grid(column=0, row=0, columnspan=5)

parcela_confirma = ttk.Button(janela, text="Select", command=select_file_c6)
parcela_confirma.grid(column=2, row=1)

lablc6 = ttk.Label(janela, text="C6")
lablc6.grid(column=0, row=2, columnspan=3)

login_label = ttk.Label(janela, text="Usuário:").grid(column=0, row=3)
login_usuario_entry = ttk.Entry(janela, width=11)
login_usuario_entry.insert(0, "07422214589_002137")
login_usuario_entry.grid(column=1, row=3)

login_label = ttk.Label(janela, text="Senha:").grid(column=0, row=4)
login_senha_entry = ttk.Entry(janela, width=11)
login_senha_entry.insert(0, "Senha@20")
login_senha_entry.grid(column=1, row=4)

login_button = ttk.Button(janela, text="Login", command=login_c6)
login_button.grid(column=0, row=5)

iniciar_digitacao_button = ttk.Button(janela, text="Digitar", command=digitando_proposta)
iniciar_digitacao_button.grid(column=1, row=5)

iniciar_digitacao_button = ttk.Button(janela, text="Manual", command=digitando_manual)
iniciar_digitacao_button.grid(column=2, row=5)

confirma_button = ttk.Button(janela, text="Gravar", command=gravar_proposta)
confirma_button.grid(column=0, row=6)

confirma_button = ttk.Button(janela, text="Refin", command=select_refin)
confirma_button.grid(column=1, row=6)

label0 = ttk.Label(janela, text=" ")
label0.grid(column=0, row=8, columnspan=5)

####
lablcrefisa = ttk.Label(janela, text="Crefisa")
lablcrefisa.grid(column=3, row=2, columnspan=3)

login_label_crefisa = ttk.Label(janela, text="Usuário:").grid(column=3, row=3)
login_user_crefisa = ttk.Entry(janela, width=11)

login_user_crefisa.insert(0, "1253.06033005538")
login_user_crefisa.grid(column=4, row=3)

login_label_crefisa = ttk.Label(janela, text="Senha:").grid(column=3, row=4)
login_senha_crefisa_entry = ttk.Entry(janela, width=11)

login_senha_crefisa_entry.insert(0, "Eayu@158")
login_senha_crefisa_entry.grid(column=4, row=4)

login_button_crefisa = ttk.Button(janela, text="Login", command=login_crefisa)
login_button_crefisa.grid(column=3, row=5)

login_button_crefisa = ttk.Button(janela, text="Port + Refin", command=digitar_crefisa)
login_button_crefisa.grid(column=4, row=5)

login_button_crefisa = ttk.Button(janela, text="Port", command=digitar_port_crefisa)
login_button_crefisa.grid(column=5, row=5)

login_button_crefisa = ttk.Button(janela, text="Gravar P", command=gravar_port_crefisa)
login_button_crefisa.grid(column=3, row=6)

login_button_crefisa = ttk.Button(janela, text="Gravar P+R", command=gravar_port_crefisa_refin_crefisa)
login_button_crefisa.grid(column=4, row=6)

####

lablfacta = ttk.Label(janela, text="Facta")
lablfacta.grid(column=0, row=9, columnspan=5)

parcela_confirma = ttk.Button(janela, text="Select File", command=select_file_facta)
parcela_confirma.grid(column=2, row=10)

login_label = ttk.Label(janela, text="Usuário:").grid(column=0, row=11)
login_user_facta_entry = ttk.Entry(janela, width=11)
login_user_facta_entry.insert(0, "93862_01067744509")
login_user_facta_entry.grid(column=1, row=11)

login_label = ttk.Label(janela, text="Senha:").grid(column=0, row=12)
login_pass_facta_entry = ttk.Entry(janela, width=11)
login_pass_facta_entry.insert(0, "QueBosta@80")
login_pass_facta_entry.grid(column=1, row=12)

login_button = ttk.Button(janela, text="Login", command=login_facta)
login_button.grid(column=0, row=13)

iniciar_digitacao_button = ttk.Button(
    janela, text="Digitar", command=propWrite)
iniciar_digitacao_button.grid(column=1, row=13)

iniciar_digitacao_button = ttk.Button(
    janela, text="2nd Page", command=propWrite2ndPage)
iniciar_digitacao_button.grid(column=2, row=13)

iniciar_digitacao_button = ttk.Button(
    janela, text="3rd Page", command=propWrite3ndPage)
iniciar_digitacao_button.grid(column=0, row=14)

fechar_driver_button = ttk.Button(
    janela, text="4rd Page", command=propWrite4ndPage)
fechar_driver_button.grid(column=1, row=14)

label1 = ttk.Label(janela, text=" ")
label1.grid(column=0, row=15, columnspan=5)

open_driver_button = ttk.Button(janela, text="Abrir Driver", command=open_driver)
open_driver_button.grid(column=2, row=16)

close_driver_button = ttk.Button(janela, text="Fechar Driver", command=close_driver)
close_driver_button.grid(column=3, row=16)

label2 = ttk.Label(janela, text=" ")
label2.grid(column=0, row=17, columnspan=5)

janela.mainloop()