import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

class CtrlFaturamento():
    def __init__(self, ctrlPrincipal):
        self.ctrlPrincipal = ctrlPrincipal

    def mostraJanela(self, titulo, msg):
        messagebox.showinfo(titulo, msg)    

    def consultarFatProduto (self):
        codProduto = simpledialog.askinteger('Consultar Faturamento do Produto', 'Insira o código do produto')
        listaNotasFiscais = self.ctrlPrincipal.ctrlVenda.getListaNotasFiscais()
        valorProd = 0
        fatTotal = 0
        for notas in listaNotasFiscais:
            for produtos in notas.produtos:
                if (produtos.codigoNumerico == codProduto):
                    valorProd = int(produtos.quant) * int(produtos.valorVenda)
                    fatTotal += valorProd
        self.mostraJanela(f'Faturamento do produto: {codProduto}',f'R${fatTotal}')        

    def consultarFatCliente (self):
        codCliente = simpledialog.askinteger('Consulta Faturamento do Cliente', 'Insira o CPF do cliente')
        listaNotasFiscais = self.ctrlPrincipal.ctrlVenda.getListaNotasFiscais()
        fatCliente = 0
        for notas in listaNotasFiscais:
            if notas.cpfCliente == codCliente:
                for produtos in notas.produtos:
                    valorProd = int(produtos.valorVenda) * int(produtos.quant)
                    fatCliente += valorProd
        self.mostraJanela(f'Valor do faturamento do cliente: {codCliente}',f'R${fatCliente}')             


        