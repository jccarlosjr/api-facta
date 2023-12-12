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


def open_driver():
    chrome_service = Service(ChromeDriverManager().install())
    chrome_service.creation_flags = CREATE_NO_WINDOW
    global driver
    driver = webdriver.Chrome(service=chrome_service)
    global wait
    wait = WebDriverWait(driver, 5)
    global action
    action = ActionChains(driver)


def select_file():
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


def alert_confirm():
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
        usuario = login_usuario_entry.get()
        usuario = usuario.strip()
        senha = login_senha_entry.get()
        senha = senha.strip()
        driver.get('https://sfc.sistemascr.com.br/autorizador/Login/AC.UI.LOGIN.aspx')
        find_xpath('//*[@id="EUsuario_CAMPO"]').send_keys(str(usuario))
        find_xpath('//*[@id="ESenha_CAMPO"]').send_keys(str(senha))
        find_xpath('//*[@id="lnkEntrar"]').click()
        alert_confirm()
        info_label.config(text='Login efetuado')
    except:
        info_label.config(text='Erro ao logar')


def open_writer(): 
    alert_confirm()
    WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.LINK_TEXT, 'Cadastro')))
    cadastro = driver.find_element(By.LINK_TEXT, 'Cadastro')
    action.move_to_element(cadastro).perform()
    proposta = driver.find_element(By.LINK_TEXT, 'Proposta Consignado')
    action.move_to_element(proposta).click().perform()
    time.sleep(0.5)


def iniciar_digitacao():
    alert_confirm()
    driver.get('https://sfc.sistemascr.com.br/autorizador/MenuWeb/Cadastro/Proposta/UI.PropostaSintetizada.aspx?Origem3=032052')
    elementClickable('//*[@id="ctl00_Cph_UcPrp_J1_JnDadoIni_UcDIni_cboTipoOperacao_CAMPO"]/option[3]').click()
    elementClickable('//*[@id="ctl00_Cph_UcPrp_J1_JnDadoIni_UcDIni_cboGrupoConvenio_CAMPO"]/option[5]').click()
    elementClickable('//*[@id="ctl00_Cph_UcPrp_J1_JnDadoIni_UcDIni_cboOrigem4_CAMPO"]/option[2]').click()


def dados_iniciais():
    time.sleep(1)
    find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnDadoIni_UcDIni_txtCPF_CAMPO"]').send_keys((str(cpf_planilha)), Keys.TAB)
    alert_confirm()
    loadCrefisa()
    try:
        driver.switch_to.frame('ctl00_Cph_UcPrp_J1_JnDadoIni_UcDIni_popCliente_panelAjuda')
        driver.find_element(By.XPATH, '//*[@id="ctl00_cph_FIJanela1_FIJanelaPanel1_btnNovo_dvTxt"]/table/tbody/tr/td').click()
        time.sleep(1)
        driver.switch_to.default_content()
        loadCrefisa()
    except:
        pass
    alert_confirm()
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
            alert_confirm()
            driver.switch_to.frame('ctl00_Cph_UcPrp_J1_JnDadoIni_UcDIni_popBeneficiarioTermo_frameAjuda')
            time.sleep(0.5)
            find_xpath('//*[@id="ctl00_cph_jp1_pnlDadosBeneficiario_Container_AbaTermoAutorizacao_txtNomeCli_CAMPO"]').send_keys(str(nome_cliente), Keys.TAB)
            time.sleep(0.5)
            find_xpath('//*[@id="ctl00_cph_jp1_pnlDadosBeneficiario_Container_AbaTermoAutorizacao_txtLocalAssTermo_CAMPO"]').send_keys(str(cidade_cliente), Keys.TAB)
            time.sleep(0.5)
            find_xpath('//*[@id="btnImprimirTermo_txt"]').click()
            alert_confirm()
            time.sleep(1)
            loadCrefisa()
            find_xpath('//*[@id="__tab_ctl00_cph_jp1_pnlDadosBeneficiario_Container_ConsultaDadosBeneficio"]').click()
            loadCrefisa()
            chave = find_xpath('//*[@id="ctl00_cph_jp1_pnlDadosBeneficiario_Container_ConsultaDadosBeneficio_cboChaveTermo_CAMPO"]')
            chave.click()
            chave.send_keys(Keys.PAGE_DOWN, Keys.TAB)
            loadCrefisa()
            alert_confirm()
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
                alert_confirm()
                find_xpath('//*[@id="btnRealizarUpload_txt"]').click()
                loadCrefisa()
                alert_confirm()
            except:
                pass
            try:
                button2 = driver.find_element(By.ID, 'FileUpGrd2')
                button2.send_keys(os.getcwd() + "/imagem.png")
                time.sleep(0.5)
                loadCrefisa()
                alert_confirm()
            except:
                pass
            find_xpath('//*[@id="btnSolicitarAutorizacao_txt"]').click()
            time.sleep(0.5)
            alert_confirm()
            loadCrefisa()
            find_xpath('//*[@id="btnVoltar_txt"]').click()
            loadCrefisa()
            driver.switch_to.default_content()
            find_xpath('//*[@id="btnObterMargem_txt"]').click()
            loadCrefisa()
    except:
        print('ja possui consulta in100')
        loadCrefisa()


def dados_port():
    loadCrefisa()
    find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnCpaDiv_UcCompra_FIJN1_JnC_cboTipoQuitacao_CAMPO"]/option[1]').click()
    find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnCpaDiv_UcCompra_FIJN1_JnC_txtBanco_CAMPO"]').send_keys(str(bancoport_cliente), Keys.TAB)
    loadCrefisa()
    alert_confirm()
    find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnCpaDiv_UcCompra_FIJN1_JnC_txtNrContrato_CAMPO"]').send_keys(str(num_ctt), Keys.TAB)
    find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnCpaDiv_UcCompra_FIJN1_JnC_txtValorParcela_CAMPO"]').send_keys(str(parcela), Keys.TAB)
    find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnCpaDiv_UcCompra_FIJN1_JnC_txtValorQuitacaoDivida_CAMPO"]').send_keys(str(saldo_devedor_planilha), Keys.TAB)
    find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnCpaDiv_UcCompra_FIJN1_JnC_txtQtdeParc_CAMPO"]').send_keys(str(parcela_restante), Keys.TAB)
    find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnCpaDiv_UcCompra_FIJN1_JnC_cboEnteConsignante_CAMPO"]/option[2]').click()
    find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnCpaDiv_UcCompra_FIJN1_JnC_lbkIncluir"]').click()
    loadCrefisa()


def dados_cliente():
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
    alert_confirm()
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


def simula_port():
    parcela_c = find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnSim_UcSimulacaoSnt_J1_JP1_txtVlrParcela_CAMPO"]')
    sendKeys(parcela_c, str(parcela))
    time.sleep(0.5)
    find_xpath('//*[@id="btnCalcular_txt"]').click()
    loadCrefisa()
    time.sleep(1)
    alert_confirm()
    find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnSim_UcSimulacaoSnt_J1_JP1_grdCondicoes_ctl02_ckSelecao"]').click()
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


def gravar_port():
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
    driver.switch_to.frame('ctl00_cph_UcBotoes_btnGravar_dvCBtn')
    find_xpath('//*[@id="btnCancelar_txt"]').click()
    driver.switch_to.default_content()


def gravar_port_refin():
    find_xpath('//*[@id="btnGravar_txt"]').click()
    loadCrefisa()
    driver.switch_to.frame('ctl00_Cph_UcPrp_popConfirmacao_frameAjuda')
    find_xpath('//*[@id="btnCancelar_txt"]').click()
    driver.switch_to.default_content()
    loadCrefisa()
    driver.switch_to.frame('ctl00_Cph_UcPrp_popConfirmacao_frameAjuda')
    find_xpath('//*[@id="btnGravar_txt"]').click()
    driver.switch_to.default_content()
    alert_confirm()
    loadCrefisa()


def refin_port():
    driver.switch_to.default_content()
    parcela_c = find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnSim_UcSimulacaoSnt_J1_JP1_txtVlrParcela_CAMPO"]')
    sendKeys(parcela_c, str(parcela))
    valor_financiado = find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnSim_UcSimulacaoSnt_J1_JP1_txtVlrSolicitado_CAMPO"]')
    sendKeys(valor_financiado, '')
    find_xpath('//*[@id="btnCalcular_txt"]').click()
    alert_confirm()
    time.sleep(0.5)
    loadCrefisa()
    find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnSim_UcSimulacaoSnt_J1_JP1_grdCondicoes_ctl02_ckSelecao"]').click()
    loadCrefisa()
    find_xpath('//*[@id="ctl00_Cph_UcPrp_J1_JnCli_UcDadosClienteSnt_J1_JP2_UcDadoPgto_cbxTipoConta_CAMPO"]/option[2]').click()
    find_xpath('//*[@id="btnGravar_txt"]').click()
    loadCrefisa()
    info_label.config(text=f"Digitado: {nome_arquivo}")
    alert_confirm()
    

def digitar():
    try:
        open_writer()
    except:
        pass
    iniciar_digitacao()
    dados_iniciais()
    dados_port()
    dados_cliente()
    simula_port()
    gravar_port_refin()
    refin_port()
    


def digitarPort():
    try:
        open_writer()
    except:
        pass
    iniciar_digitacao()
    dados_iniciais()
    dados_port()
    dados_cliente()
    simula_port()
    gravar_port()






janela = Tk()
janela.title("")

info_label = ttk.Label(janela, text="Label")
info_label.grid(column=0, row=0, columnspan=5)

parcela_confirma = ttk.Button(janela, text="Select", command=select_file)
parcela_confirma.grid(column=1, row=1)

login_label = ttk.Label(janela, text="Usuário:").grid(column=0, row=2)
login_usuario_entry = ttk.Entry(janela, width=11)

login_usuario_entry.insert(0, "1253.06033005538")
login_usuario_entry.grid(column=1, row=2)

login_label = ttk.Label(janela, text="Senha:").grid(column=0, row=3)
login_senha_entry = ttk.Entry(janela, width=11)

login_senha_entry.insert(0, "Eayu@158")
login_senha_entry.grid(column=1, row=3)

login_button = ttk.Button(janela, text="Login", command=login_crefisa)
login_button.grid(column=2, row=2)

login_button = ttk.Button(janela, text="Digitar", command=digitar)
login_button.grid(column=2, row=3)

open_driver_button = ttk.Button(janela, text="Abrir Driver", command=open_driver)
open_driver_button.grid(column=0, row=4)

janela.mainloop()