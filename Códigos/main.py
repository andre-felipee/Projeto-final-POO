import tkinter as tk
from tkinter import messagebox
import estoque as est
import venda as vnd
import cliente as clt
import faturamento as fat

class LimitePrincipal():
    def __init__(self, root, controle):
        self.controle = controle
        self.root = root
        self.root.geometry('300x100')
        self.menubar = tk.Menu(self.root)        
        self.estoqueMenu = tk.Menu(self.menubar)    
        self.vendaMenu = tk.Menu(self.menubar)
        self.clienteMenu = tk.Menu(self.menubar)
        self.faturamentoMenu = tk.Menu(self.menubar)   

        self.estoqueMenu.add_command(label="Cadastrar mercadoria", command=self.controle.cadastrarMercadoria)
        self.estoqueMenu.add_command(label='Consultar mercadoria', command=self.controle.consultarMercadoria)
        self.menubar.add_cascade(label="Estoque", menu=self.estoqueMenu)
        
        self.clienteMenu.add_command(label='Cadastrar cliente', command=self.controle.cadastrarCliente)
        self.clienteMenu.add_command(label='Consultar cliente', command=self.controle.consultarCliente)
        self.menubar.add_cascade(label='Cliente', menu=self.clienteMenu)
        
        self.vendaMenu.add_command(label="Emitir Nota Fiscal", command=self.controle.emitirNotaFiscal)
        self.menubar.add_cascade(label="Venda", menu=self.vendaMenu)
        
        self.faturamentoMenu.add_command(label='Consultar faturamento por cliente', command=self.controle.consultarFatCPF)
        self.faturamentoMenu.add_command(label='Consultar faturamento por produto', command=self.controle.consultarFatCod)
        self.menubar.add_cascade(label='Faturamento', menu=self.faturamentoMenu)
        
        self.root.config(menu=self.menubar)
          

class ControlePrincipal():
    def __init__(self):
        self.root = tk.Tk()

        self.ctrlEstoque = est.CtrlEstoque()
        self.ctrlVenda = vnd.CtrlVenda(self)
        self.ctrlCliente = clt.CtrlCliente()
        self.ctrlFaturamento = fat.CtrlFaturamento(self)

        self.limite = LimitePrincipal(self.root, self) 

        self.root.title("Loja de Confecções")
        
        # Inicia o mainloop
        self.root.mainloop()

    def cadastrarMercadoria(self):
        self.ctrlEstoque.cadastraMercadoria()
        
    def consultarMercadoria(self):
        self.ctrlEstoque.consultarMercadoria()

    def cadastrarCliente(self):
        self.ctrlCliente.cadastraCliente()
        
    def consultarCliente(self):
        self.ctrlCliente.consultarCliente()
        
    def emitirNotaFiscal(self):
        self.ctrlVenda.emitirNota()
        
    def consultarFatCPF(self):
        self.ctrlFaturamento.consultarFatCliente()
        
    def consultarFatCod(self):
        self.ctrlFaturamento.consultarFatProduto()           

if __name__ == "__main__":
    c = ControlePrincipal() 