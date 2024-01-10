# Digitador de Portabilidade Facta

Esse programa foi desenvolvido para digitação de propostas de portabilidade utilizando os serviços de API da Facta Financeira

## 🚀 Começando

Estas instruções fornecerão uma cópia do projeto em funcionamento em sua máquina local para fins de desenvolvimento e teste.

### 📋 Pré-requisitos

A única biblioteca a ser instalada é o pandas, para leitura dos arquivos em excel

### 🔧 Instalação

Instalação do pandas e pyinstaller para criar o executável

No windows
```
pip install pandas
pip install pyinstaller
```

No linux
```
pip3 install pandas
```

## 📦 Implantação

Para criação do executável, realizar os seguintes passos:
1 - Executar no terminal: pyinstaller --icon=favicon.ico --onefile  app.py
2 - Garantir que os arquivos "favicon.ico" e "facta.png" estejam no mesmo diretório do executável

## 🛠️ Construído com

* [Pandas](https://pandas.pydata.org/)
* [Tkinter](https://docs.python.org/pt-br/3/library/tkinter.html)
* [Pyinstaller](https://pyinstaller.org/en/stable/)

## 📄 Licença

Este projeto está sob a licença MIT License - veja o arquivo [LICENSE.md](https://github.com/jccarlosjr/api-facta/blob/main/LICENSE) para detalhes.