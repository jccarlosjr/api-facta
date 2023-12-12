from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from subprocess import CREATE_NO_WINDOW
from selenium import webdriver
from tkinter import ttk
from tkinter import *
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument("--headless")
chrome_service = Service(ChromeDriverManager().install())
chrome_service.creation_flags = CREATE_NO_WINDOW
driver = webdriver.Chrome(service=chrome_service, options=options)
wait = WebDriverWait(driver, 20)

def calcula_taxa_juros(financiado, parcela, prazo):
    prec = 0.001
    tax_min = 0.0
    tax_max = 1.0

    while True:
        taxa = (tax_min + tax_max) / 2

        fin = financiado
        for _ in range(prazo):
            fin = fin * (1 + taxa) - parcela

        if abs(fin) < prec:
            return taxa
        
        if fin > 0:
            tax_max = taxa
        else:
            tax_min = taxa


def buscar_dados():
        ff_informar = ff_entry.get()
        driver.get(ff_informar) #self explained
        driver.maximize_window()
        wait.until(EC.invisibility_of_element((By.XPATH, '/html/body/div/p/i')))
        #wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-tipo-contrato/div/div[2]/form/div[4]/div[1]/div[1]/input')))
        telefone = driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-pessoais/div/div[2]/form/div/div[6]/div[2]/input').get_attribute("value")
        telefone = {'telefone': telefone}
        telefone = telefone.values() #Acessando valor do dict
        telefone = list(telefone) #Convertendo o valor em lista
        telefone_string = telefone[0] #Convertendo a lista em uma string
        telefone_string = telefone_string.replace('(', '')
        telefone_string = telefone_string.replace(')', '')
        telefone_string = telefone_string.replace('-', '')
        ddd = telefone_string[0:2].strip()
        telefone = telefone_string[2:].strip()
        celular = driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-pessoais/div/div[2]/form/div/div[6]/div[1]/input').get_attribute("value")
        celular = {'celular': celular}
        celular = celular.values() #Acessando valor do dict
        celular = list(celular) #Convertendo o valor em lista
        celular_string = celular[0] #Convertendo a lista em uma string
        celular_string = celular_string.replace('(', '')
        celular_string = celular_string.replace(')', '')
        celular_string = celular_string.replace('-', '')
        dddcelular = celular_string[0:2].strip()
        celular = celular_string[2:].strip()

        identidade = driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-pessoais/div/div[2]/form/div/div[3]/div[1]/input').get_attribute("value")
        identidade = identidade.replace('-', '')
        identidade = identidade.replace('.', '')

        parcela = driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-operacao/div/div[2]/form/div[2]/div[3]/div[1]/input').get_attribute("value")
        parcela = {'parcela': parcela}
        parcela = parcela.values()
        parcela = list(parcela)
        parcela = parcela[0]
        parcela = parcela.replace('R$', '')
        parcela = parcela.strip()
        parcela = parcela.replace('R$', '')
        parcela = parcela.strip()

        saldo = driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-operacao/div/div[2]/form/div[2]/div[3]/div[2]/input').get_attribute("value")
        saldo = {'saldo': saldo}
        saldo = saldo.values()
        saldo = list(saldo)
        saldo = saldo[0]
        saldo = saldo.replace('R$', '')
        saldo = saldo.strip()

        saldo_calculo = saldo.replace(".", "")
        saldo_calculo = saldo_calculo.replace(",", ".")
        saldo_calculo = float(saldo_calculo)
        parcela_calculo = parcela.replace(".", "")
        parcela_calculo = parcela_calculo.replace(",", ".")
        parcela_calculo = float(parcela_calculo)
        prazo = int(driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-operacao/div/div[2]/form/div[2]/div[2]/div[4]/input').get_attribute("value"))
        taxa = calcula_taxa_juros(saldo_calculo, parcela_calculo, prazo)
        ff = driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-proposta/div/div[2]/form/div/div[2]/input').get_attribute("value")
        ff = ff.replace('/', '-')
        if taxa > 0.0180:
            driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-operacao/div/div[2]/form/div[2]/div[3]/div[3]/i').click()
            taxa_driver = driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-operacao/div/div[2]/form/div[2]/div[4]/div[1]/input')
            taxa_driver.click()
            taxa_driver.send_keys(Keys.SHIFT + Keys.HOME, Keys.BACKSPACE)
            taxa_driver.send_keys("1.84")
            driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-operacao/div/div[2]/form/div[2]/div[4]/div[2]/i').click()
            driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-operacao/div/div[2]/form/div[2]/div[4]/div[4]/i').click()
            driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[3]/div/button[1]').click()
            saldo = driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-operacao/div/div[2]/form/div[2]/div[3]/div[2]/input').get_attribute("value")
            saldo = {'saldo': saldo}
            saldo = saldo.values()
            saldo = list(saldo)
            saldo = saldo[0]
            saldo = saldo.replace('R$', '')
            saldo = saldo.strip()
            info_label2.config(text="Taxa ajustada para 1,84%")
        elif taxa < 0.0170:
            driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-operacao/div/div[2]/form/div[2]/div[3]/div[3]/i').click()
            taxa_driver = driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-operacao/div/div[2]/form/div[2]/div[4]/div[1]/input')
            taxa_driver.click()
            taxa_driver.send_keys(Keys.SHIFT + Keys.HOME, Keys.BACKSPACE)
            taxa_driver.send_keys("1.75")
            driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-operacao/div/div[2]/form/div[2]/div[4]/div[2]/i').click()
            driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-operacao/div/div[2]/form/div[2]/div[4]/div[4]/i').click()
            driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[3]/div/button[1]').click()
            saldo = driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-operacao/div/div[2]/form/div[2]/div[3]/div[2]/input').get_attribute("value")
            saldo = {'saldo': saldo}
            saldo = saldo.values()
            saldo = list(saldo)
            saldo = saldo[0]
            saldo = saldo.replace('R$', '')
            saldo = saldo.strip()
            info_label2.config(text="Taxa ajustada para 1,65%")

        num_ctt = driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-operacao/div/div[2]/form/div[2]/div[2]/div[1]/input').get_attribute("value")
        num_ctt = {'saldo': num_ctt}
        num_ctt = num_ctt.values()
        num_ctt = list(num_ctt)
        num_ctt = num_ctt[0]
        num_ctt = num_ctt.replace('/', '')
        num_ctt = num_ctt.replace('.', '')
        num_ctt = num_ctt.replace('-', '')
        num_ctt = num_ctt.replace('_', '')
        num_ctt = num_ctt.strip()

        nascimento = driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-pessoais/div/div[2]/form/div/div[2]/div[2]/input').get_attribute("value")
        nascimento = {'saldo': nascimento}
        nascimento = nascimento.values()
        nascimento = list(nascimento)
        nascimento = nascimento[0]
        nascimento = nascimento.replace('-', '/')
        ano_nascimento = nascimento[0:4]
        mes_nascimento = nascimento[4:8]
        dia_nascimento = nascimento[8:]
        nascimento = [dia_nascimento + mes_nascimento + ano_nascimento]
        nascimento = nascimento[0]

        dados_cliente = {
            'NOME': [driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-pessoais/div/div[2]/form/div/div[1]/div[1]/input').get_attribute("value")],
            'CPF': [driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-pessoais/div/div[2]/form/div/div[1]/div[2]/input').get_attribute("value")],
            'NASCIMENTO': [nascimento],
            'SEXO': [driver.find_element(By.XPATH, '//*[@id="sexo"]').get_attribute("value")],
            'IDENTIDADE': [identidade],
            'MAE': [driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-pessoais/div/div[2]/form/div/div[5]/div[1]/input').get_attribute("value")],
            'PAI': [driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-pessoais/div/div[2]/form/div/div[5]/div[2]/input').get_attribute("value")],
            'UF_NASCIMENTO': [driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-pessoais/div/div[2]/form/div/div[4]/div[2]/input').get_attribute("value")], 
            'UF_RG': [driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-pessoais/div/div[2]/form/div/div[3]/div[3]/input').get_attribute("value")], 
            'CIDADE_NASCIMENTO': [driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-pessoais/div/div[2]/form/div/div[4]/div[1]/input').get_attribute("value")], 
            'DDD': [ddd],
            'TELEFONE': [telefone],
            'DDD_2': [dddcelular],
            'CELULAR': [celular],
            'CEP': [driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-pessoais/div/div[2]/form/div/div[7]/div[1]/input').get_attribute("value")],
            'ENDERECO': [driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-pessoais/div/div[2]/form/div/div[8]/div[1]/div[1]/input').get_attribute("value")],
            'UF_ENDERECO': [driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-pessoais/div/div[2]/form/div/div[7]/div[2]/input').get_attribute("value")],
            'NUMERO': [driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-pessoais/div/div[2]/form/div/div[8]/div[1]/div[2]/input').get_attribute("value")],
            'CIDADE': [driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-pessoais/div/div[2]/form/div/div[7]/div[3]/input').get_attribute("value")],
            'BAIRRO': [driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-pessoais/div/div[2]/form/div/div[8]/div[2]/div[1]/input').get_attribute("value")],
            'ESPECIE': [driver.find_element(By.XPATH, '//*[@id="codigo_beneficio"]').get_attribute("value")],
            'MATRICULA': [driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-tipo-contrato/div/div[2]/form/div[5]/div[1]/div[1]/input').get_attribute("value")],
            'SALARIO': [driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-tipo-contrato/div/div[2]/form/div[5]/div[1]/div[3]/input').get_attribute("value")],
            'UF_NB': [driver.find_element(By.XPATH, '//*[@id="beneficio_uf"]').get_attribute("value")],
            'BANCO_NB': [driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-bancarios/div/div[2]/form/div[1]/div[3]/input').get_attribute("value")],
            'AGENCIA_NB': [driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-bancarios/div/div[2]/form/div[2]/div[1]/input').get_attribute("value")],
            'CONTA_NB': [driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-bancarios/div/div[2]/form/div[2]/div[3]/input').get_attribute("value")],
            'DV_NB': [driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-bancarios/div/div[2]/form/div[2]/div[4]/input').get_attribute("value")],
            'BANCO_PORT': [driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-operacao/div/div[2]/form/div[2]/div[1]/div[2]/input').get_attribute("value")],
            'NUM_CONTRATO': [driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-operacao/div/div[2]/form/div[2]/div[2]/div[1]/input').get_attribute("value")],
            'NUM_PARCELA_TOTAL': [[driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-operacao/div/div[2]/form/div[2]/div[2]/div[3]/input').get_attribute("value")]],  
            'PAR_RESTANTE': [driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-operacao/div/div[2]/form/div[2]/div[2]/div[4]/input').get_attribute("value")],
            'PARCELA': [parcela],
            'SALDO': [saldo]
            }
        

        dados_cliente_df = pd.DataFrame.from_dict(dados_cliente)
        dados_cliente_df.to_excel(f'C6_{ff}.xlsx', index=False)
        ff_importada.config(text=f'{ff} Importada')


def clear_text():
   ff_entry.delete(0, END)
   ff_importada.config(text='')
   info_label2.config(text='')


def sair():
    driver.close()
    driver.quit()
    exit()


def buscar_dados_facta():
        ff_informar = ff_entry.get()
        driver.get(ff_informar) #self explained
        driver.maximize_window()
        wait.until(EC.invisibility_of_element((By.XPATH, '/html/body/div/p/i')))
        #wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-tipo-contrato/div/div[2]/form/div[4]/div[1]/div[1]/input')))
        telefone = driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-pessoais/div/div[2]/form/div/div[6]/div[2]/input').get_attribute("value")
        telefone = {'telefone': telefone}
        telefone = telefone.values() #Acessando valor do dict
        telefone = list(telefone) #Convertendo o valor em lista
        telefone_string = telefone[0] #Convertendo a lista em uma string
        telefone_string = telefone_string.replace('(', '')
        telefone_string = telefone_string.replace(')', '')
        telefone_string = telefone_string.replace('-', '')
        ddd = telefone_string[0:2].strip()
        telefone = telefone_string[2:].strip()
        celular = driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-pessoais/div/div[2]/form/div/div[6]/div[1]/input').get_attribute("value")
        celular = {'celular': celular}
        celular = celular.values() #Acessando valor do dict
        celular = list(celular) #Convertendo o valor em lista
        celular_string = celular[0] #Convertendo a lista em uma string
        celular_string = celular_string.replace('(', '')
        celular_string = celular_string.replace(')', '')
        celular_string = celular_string.replace('-', '')
        dddcelular = celular_string[0:2].strip()
        celular = celular_string[2:].strip()

        identidade = driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-pessoais/div/div[2]/form/div/div[3]/div[1]/input').get_attribute("value")
        identidade = identidade.replace('-', '')
        identidade = identidade.replace('.', '')

        parcela = driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-operacao/div/div[2]/form/div[2]/div[3]/div[1]/input').get_attribute("value")
        parcela = {'parcela': parcela}
        parcela = parcela.values()
        parcela = list(parcela)
        parcela = parcela[0]
        parcela = parcela.replace('R$', '')
        parcela = parcela.strip()
        parcela = parcela.replace('R$', '')
        parcela = parcela.strip()

        saldo = driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-operacao/div/div[2]/form/div[2]/div[3]/div[2]/input').get_attribute("value")
        saldo = {'saldo': saldo}
        saldo = saldo.values()
        saldo = list(saldo)
        saldo = saldo[0]
        saldo = saldo.replace('R$', '')
        saldo = saldo.strip()

        saldo_calculo = saldo.replace(".", "")
        saldo_calculo = saldo_calculo.replace(",", ".")
        saldo_calculo = float(saldo_calculo)
        parcela_calculo = parcela.replace(".", "")
        parcela_calculo = parcela_calculo.replace(",", ".")
        parcela_calculo = float(parcela_calculo)
        prazo = int(driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-operacao/div/div[2]/form/div[2]/div[2]/div[4]/input').get_attribute("value"))

        num_ctt = driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-operacao/div/div[2]/form/div[2]/div[2]/div[1]/input').get_attribute("value")
        num_ctt = {'saldo': num_ctt}
        num_ctt = num_ctt.values()
        num_ctt = list(num_ctt)
        num_ctt = num_ctt[0]
        num_ctt = num_ctt.replace('/', '')
        num_ctt = num_ctt.replace('.', '')
        num_ctt = num_ctt.replace('-', '')
        num_ctt = num_ctt.replace('_', '')
        num_ctt = num_ctt.strip()

        nascimento = driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-pessoais/div/div[2]/form/div/div[2]/div[2]/input').get_attribute("value")
        nascimento = {'saldo': nascimento}
        nascimento = nascimento.values()
        nascimento = list(nascimento)
        nascimento = nascimento[0]
        nascimento = nascimento.replace('-', '/')
        ano_nascimento = nascimento[0:4]
        mes_nascimento = nascimento[4:8]
        dia_nascimento = nascimento[8:]
        nascimento = [dia_nascimento + mes_nascimento + ano_nascimento]
        nascimento = nascimento[0]

        ff = driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-proposta/div/div[2]/form/div/div[2]/input').get_attribute("value")
        ff = ff.replace('/', '-')

        dados_cliente = {
            'NOME': [driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-pessoais/div/div[2]/form/div/div[1]/div[1]/input').get_attribute("value")],
            'CPF': [driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-pessoais/div/div[2]/form/div/div[1]/div[2]/input').get_attribute("value")],
            'NASCIMENTO': [nascimento],
            'SEXO': [driver.find_element(By.XPATH, '//*[@id="sexo"]').get_attribute("value")],
            'IDENTIDADE': [identidade],
            'MAE': [driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-pessoais/div/div[2]/form/div/div[5]/div[1]/input').get_attribute("value")],
            'PAI': [driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-pessoais/div/div[2]/form/div/div[5]/div[2]/input').get_attribute("value")],
            'UF_NASCIMENTO': [driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-pessoais/div/div[2]/form/div/div[4]/div[2]/input').get_attribute("value")], 
            'UF_RG': [driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-pessoais/div/div[2]/form/div/div[3]/div[3]/input').get_attribute("value")], 
            'CIDADE_NASCIMENTO': [driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-pessoais/div/div[2]/form/div/div[4]/div[1]/input').get_attribute("value")], 
            'DDD': [ddd],
            'TELEFONE': [telefone],
            'DDD_2': [dddcelular],
            'CELULAR': [celular],
            'CEP': [driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-pessoais/div/div[2]/form/div/div[7]/div[1]/input').get_attribute("value")],
            'ENDERECO': [driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-pessoais/div/div[2]/form/div/div[8]/div[1]/div[1]/input').get_attribute("value")],
            'UF_ENDERECO': [driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-pessoais/div/div[2]/form/div/div[7]/div[2]/input').get_attribute("value")],
            'NUMERO': [driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-pessoais/div/div[2]/form/div/div[8]/div[1]/div[2]/input').get_attribute("value")],
            'CIDADE': [driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-pessoais/div/div[2]/form/div/div[7]/div[3]/input').get_attribute("value")],
            'BAIRRO': [driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-pessoais/div/div[2]/form/div/div[8]/div[2]/div[1]/input').get_attribute("value")],
            'ESPECIE': [driver.find_element(By.XPATH, '//*[@id="codigo_beneficio"]').get_attribute("value")],
            'MATRICULA': [driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-tipo-contrato/div/div[2]/form/div[5]/div[1]/div[1]/input').get_attribute("value")],
            'SALARIO': [driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-tipo-contrato/div/div[2]/form/div[5]/div[1]/div[3]/input').get_attribute("value")],
            'UF_NB': [driver.find_element(By.XPATH, '//*[@id="beneficio_uf"]').get_attribute("value")],
            'BANCO_NB': [driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-bancarios/div/div[2]/form/div[1]/div[3]/input').get_attribute("value")],
            'AGENCIA_NB': [driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-bancarios/div/div[2]/form/div[2]/div[1]/input').get_attribute("value")],
            'CONTA_NB': [driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-bancarios/div/div[2]/form/div[2]/div[3]/input').get_attribute("value")],
            'DV_NB': [driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-bancarios/div/div[2]/form/div[2]/div[4]/input').get_attribute("value")],
            'BANCO_PORT': [driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-operacao/div/div[2]/form/div[2]/div[1]/div[2]/input').get_attribute("value")],
            'NUM_CONTRATO': [driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-operacao/div/div[2]/form/div[2]/div[2]/div[1]/input').get_attribute("value")],
            'NUM_PARCELA_TOTAL': [[driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-operacao/div/div[2]/form/div[2]/div[2]/div[3]/input').get_attribute("value")]],  
            'PAR_RESTANTE': [driver.find_element(By.XPATH, '/html/body/app-root/app-contrato/div/div/div[1]/div[2]/app-dados-operacao/div/div[2]/form/div[2]/div[2]/div[4]/input').get_attribute("value")],
            'PARCELA': [parcela],
            'SALDO': [saldo]
            }
        

        dados_cliente_df = pd.DataFrame.from_dict(dados_cliente)
        dados_cliente_df.to_excel(f'Facta_{ff}.xlsx', index=False)
        ff_importada.config(text=f'{ff} Importada')



janela = Tk()
janela.title("Importar")


info_label = ttk.Label(janela, text="Importar").grid(column=1, row=0, pady=5, padx=5)

ff_entry = ttk.Entry(janela, width=10)
ff_entry.grid(column=2, row=0,)

buscar_button = ttk.Button(janela, text="C6", command=buscar_dados)
buscar_button.grid(column=1, row=1)

buscar_button = ttk.Button(janela, text="Facta", command=buscar_dados_facta)
buscar_button.grid(column=2, row=1)

buscar_button = ttk.Button(janela, text="Limpar", command=clear_text)
buscar_button.grid(column=3, row=1)

buscar_button = ttk.Button(janela, text="Sair", command=sair)
buscar_button.grid(column=4, row=1)

ff_importada = ttk.Label(janela, text='')
ff_importada.grid(column=1, row=2, columnspan=3)

info_label2 = ttk.Label(janela, text='')
info_label2.grid(column=1, row=3, columnspan=3)

janela.mainloop()