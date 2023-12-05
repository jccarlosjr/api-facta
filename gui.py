from tkinter import ttk, filedialog, scrolledtext
from urllib.parse import urlencode
import http.client, base64, json, sys, os, re, tkinter as tk, pandas as pd


class JanelaComConsole:
    def __init__(self, root):
        self.root = root
        self.root.title("API digitação port facta")

        # Criar um widget Text para o console
        self.console = scrolledtext.ScrolledText(root, wrap="none", width=40, height=10)
        self.console.grid(row=6, column=0, columnspan=5, sticky="nsew")

        # Configurar o peso das colunas e linhas para expandir com a janela
        #self.root.grid_rowconfigure(3, weight=1)
        #self.root.grid_columnconfigure(0, weight=1)

        # Centralizar o texto no console
        self.console.tag_configure("center", justify="center")

        # Redefinir a função print para escrever no console
        self.stdout_original = sys.stdout
        sys.stdout = self.ConsoleRedirector(self.console)

        # Elementos adicionais
        info_label = ttk.Label(root, text="Selecione um arquivo")
        info_label.grid(row=0, column=0, columnspan=5)

        parcela_confirma = ttk.Button(root, text="Select", command=lambda: select_file_facta())
        parcela_confirma.grid(row=1, column=1)

        botao = ttk.Button(root, text="Digitar")
        botao.grid(row=1, column=2)

        ttk.Label(root, text="Nome:").grid(row=2, column=0)
        ttk.Label(root, text="CPF:").grid(row=2, column=1)
        ttk.Label(root, text="Nascimento:").grid(row=2, column=2)
        ttk.Label(root, text="RG:").grid(row=2, column=3)


        global name_entry
        name_entry = ttk.Entry(root, justify="center")
        name_entry.grid(row=3, column=0)

        global cpf_entry
        cpf_entry = ttk.Entry(root, justify="center")
        cpf_entry.grid(row=3, column=1)

        global bdate_entry
        bdate_entry = ttk.Entry(root, justify="center")
        bdate_entry.grid(row=3, column=2)

        global rg_entry
        rg_entry = ttk.Entry(root, justify="center")
        rg_entry.insert(0, 'rg')
        rg_entry.grid(row=3, column=3)

        ttk.Label(root, text="Mãe:").grid(row=4, column=0)
        ttk.Label(root, text="Pai:").grid(row=4, column=1)
        ttk.Label(root, text="Cidade:").grid(row=4, column=2)

        mae_entry = ttk.Entry(root, justify="center")
        mae_entry.insert(0, 'mae')
        mae_entry.grid(row=5, column=0)

        pai_entry = ttk.Entry(root, justify="center")
        pai_entry.insert(0, 'pai')
        pai_entry.grid(row=5, column=1)

        city_entry = ttk.Entry(root, justify="center")
        city_entry.insert(0, 'city')
        city_entry.grid(row=5, column=2)

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



def select_file_facta():
    arquivo_path = filedialog.askopenfilename(
        title="Selecione um arquivo", filetypes=[("Arquivos Excel", "*.xlsx;*.xls")])
    if arquivo_path:
        nome_arquivo = os.path.basename(arquivo_path)
        JanelaComConsole.adicionar_print(JanelaComConsole, f"Arquivo selecionado: {nome_arquivo}")
        base = pd.read_excel(arquivo_path)
        nome = str(base['NOME'].values[0]).upper()
        cpf = str(base['CPF'].values[0]).replace("-", "").replace(".", "")
        data_nascimento = str(base['NASCIMENTO'].values[0])
        global cliente
        cliente = {
            "cpf": cpf,
            "data_nascimento": data_nascimento,
            "nome": nome,
        }
        #insertJanela(JanelaComConsole.name_entry, cliente["nome"])
        name_entry.insert(0, f'{cliente["nome"]}')
        cpf_entry.insert(0, f'{cliente["cpf"]}')
        bdate_entry.insert(0, f'{cliente["data_nascimento"]}')


def insertJanela(entry, value):
    entry.insert(0, f'{value}')





if __name__ == "__main__":
    root = tk.Tk()
    app = JanelaComConsole(root)

    JanelaComConsole.adicionar_print(JanelaComConsole, f"")

    root.protocol("WM_DELETE_WINDOW", app.restaurar_print_original)
    root.mainloop()
