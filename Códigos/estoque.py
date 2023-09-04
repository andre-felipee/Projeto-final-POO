import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import pickle
import os.path

class Mercadoria():
    def __init__(self,codigoNumerico,descricao,precoCompra,valorVenda, quant):
        self.__codigoNumerico = codigoNumerico
        self.__descricao = descricao
        self.__precoCompra = precoCompra
        self.__valorVenda = valorVenda
        self.__quant = quant

    @property
    def codigoNumerico(self):
        return self.__codigoNumerico

    @property
    def descricao(self):
        return self.__descricao
 
    @property
    def precoCompra(self):
        return self.__precoCompra 
    
    @property
    def valorVenda(self):
        return self.__valorVenda
    
    @property
    def quant(self):
        return self.__quant
    
    @quant.setter
    def quant(self, quant):
        self.__quant = quant

class LimiteCadastroMercadoria(tk.Toplevel):
    def __init__(self, controle):

        tk.Toplevel.__init__(self)
        self.geometry('280x150')
        self.title("Cadastrar Mercadoria")
        self.controle = controle

        #frames dos campos do Limite para inserir e empacotar os frames
        self.frameCodigo = tk.Frame(self)
        self.frameDescricao = tk.Frame(self)
        self.framePrecoCompra = tk.Frame(self)
        self.frameValorVenda = tk.Frame(self)
        self.frameQuant = tk.Frame(self)
        self.frameButton = tk.Frame(self)
        self.frameCodigo.pack()
        self.frameDescricao.pack()
        self.framePrecoCompra.pack()
        self.frameValorVenda.pack()
        self.frameQuant.pack()
        self.frameButton.pack()
      
        self.labelCodigo = tk.Label(self.frameCodigo,text="Código: ")
        self.labelCodigo.pack(side="left")

        self.inputCodigo = tk.Entry(self.frameCodigo, width=20)
        self.inputCodigo.pack(side="left")

        self.labelDescricao = tk.Label(self.frameDescricao,text="Descrição: ")
        self.labelDescricao.pack(side="left")

        self.inputDescricao = tk.Entry(self.frameDescricao, width=20)
        self.inputDescricao.pack(side="left")

        self.labelPrecoCompra = tk.Label(self.framePrecoCompra,text="Preço de compra: ")
        self.labelPrecoCompra.pack(side="left")  

        self.inputPrecoCompra = tk.Entry(self.framePrecoCompra, width=20)
        self.inputPrecoCompra.pack(side="left")

        self.labelValorVenda = tk.Label(self.frameValorVenda,text="Valor de Venda: ")
        self.labelValorVenda.pack(side="left")  

        self.inputValorVenda = tk.Entry(self.frameValorVenda, width=20)
        self.inputValorVenda.pack(side="left")  
        
        self.labelQuant = tk.Label(self.frameQuant, text='Quantidade: ')           
        self.labelQuant.pack(side='left')

        self.inputQuant = tk.Entry(self.frameQuant, width=20)
        self.inputQuant.pack(side='left')
      
        self.buttonSubmit = tk.Button(self.frameButton ,text="Enter")      
        self.buttonSubmit.pack(side="left")
        self.buttonSubmit.bind("<Button>", controle.enterHandlerCadastro)
      
        self.buttonClear = tk.Button(self.frameButton ,text="Clear")      
        self.buttonClear.pack(side="left")
        self.buttonClear.bind("<Button>", controle.clearHandlerCadastro)  

        self.buttonFecha = tk.Button(self.frameButton ,text="Concluído")      
        self.buttonFecha.pack(side="left")
        self.buttonFecha.bind("<Button>", controle.closeHandlerCadastro)

    def mostraJanela(self, titulo, msg):
        messagebox.showinfo(titulo, msg)


class CtrlEstoque():
    def __init__(self):
        
        #verificação arquivo pickle com controle de estoque
        if not os.path.isfile('estoque.pickle'):
            self.listaProdutos = []
        else:
            with open('estoque.pickle', 'rb') as f:
                self.listaProdutos = pickle.load(f)
                
    #método de criação do limite de cadastro de uma mercadoria
    def cadastraMercadoria(self):
        self.limiteCadastro = LimiteCadastroMercadoria(self)

    #callback de cadastro de produto com verificação de estoque 
    def enterHandlerCadastro(self, event):
        codigo = int(self.limiteCadastro.inputCodigo.get())
        descricao = self.limiteCadastro.inputDescricao.get()
        precoCompra = int(self.limiteCadastro.inputPrecoCompra.get())
        valorVenda = int(self.limiteCadastro.inputValorVenda.get())
        quant = int(self.limiteCadastro.inputQuant.get())
        for i in self.listaProdutos:
            if i.codigoNumerico == codigo:
                if i.descricao == descricao:
                    if i.precoCompra == precoCompra:
                        if i.valorVenda == valorVenda:
                            i.quant += int(quant)
                            print(i.quant)
                            self.limiteCadastro.mostraJanela('Produto já cadastrado', 'Estoque atualizado')
                            self.clearHandlerCadastro(event)
                        else:
                            self.limiteCadastro.mostraJanela('Erro', 'Já existe outro produto com esse código')
                            self.clearHandlerCadastro(event)
                    else:
                        self.limiteCadastro.mostraJanela('Erro', 'Já existe outro produto com esse código')
                        self.clearHandlerCadastro(event)
                else:
                    self.limiteCadastro.mostraJanela('Erro', 'Já existe outro produto com esse código')
                    self.clearHandlerCadastro(event)
            else:
                break
            return
        objMercadoria = Mercadoria(codigo, descricao, precoCompra, valorVenda, quant)
        self.listaProdutos.append(objMercadoria)
        self.limiteCadastro.mostraJanela("Sucesso", "Produto cadastrado!")
        self.clearHandlerCadastro(event)

    def clearHandlerCadastro(self, event):
        self.limiteCadastro.inputCodigo.delete(0, len(self.limiteCadastro.inputCodigo.get()))
        self.limiteCadastro.inputDescricao.delete(0, len(self.limiteCadastro.inputDescricao.get()))
        self.limiteCadastro.inputPrecoCompra.delete(0, len(self.limiteCadastro.inputPrecoCompra.get()))
        self.limiteCadastro.inputValorVenda.delete(0, len(self.limiteCadastro.inputValorVenda.get()))
        self.limiteCadastro.inputQuant.delete(0, len(self.limiteCadastro.inputQuant.get()))

    #callback para fechar a janela e persistir informações no sistema
    def closeHandlerCadastro(self, event):
        if len(self.listaProdutos) != 0:
            with open('estoque.pickle', 'wb') as f:
                pickle.dump(self.listaProdutos, f)
        self.limiteCadastro.destroy()

    #callback de consulta de produtos
    def consultarMercadoria(self):
        msg = ''
        codParam = simpledialog.askinteger('Consulta de Mercadoria', 'Insira o código da mercadoria: ')
        aux = False
        for prod in self.listaProdutos:
            if codParam == int(prod.codigoNumerico):
                aux = True
                msg += 'Estoque: ' + str(prod.quant) + '\n'
                msg += 'Descrição: ' + prod.descricao + '\n'
                msg += 'Preço de venda: ' + str(prod.valorVenda) + '\n'
        if not aux:
            messagebox.showinfo('Erro', 'Não há mercadoria com esse código')
        messagebox.showinfo('Mercadoria encontrada', msg)
        
    #Métodos de instanciação para controladores externos
    def getListaProdutos(self):
        return self.listaProdutos
    
    def criaMercadoria(self, codigo, descricao, precoCompra, valorVenda, quant):
        prodRet = None
        prodRet = Mercadoria(codigo, descricao, precoCompra, valorVenda, quant)
        return prodRet
    
    def atualizaEstoque(self, listaProdutos):
            with open('estoque.pickle', 'wb') as f:
                pickle.dump(listaProdutos, f)