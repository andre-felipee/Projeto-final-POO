import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import os.path
import pickle

class MercadoriaTemp():
    def __init__(self, codigo, quant, valorVenda):
        self.__codigo = codigo
        self.__quant = quant
        self.__valorVenda = valorVenda

    @property
    def codigo(self):
        return self.__codigo

    @property
    def quant(self):
        return self.__quant
    
    @property
    def valorVenda(self):
        return self.__valorVenda
    

class NotaFiscal():
    def __init__(self, cpfCliente, num, produtos, dia, mes, ano):
        self.__cpfCliente = cpfCliente
        self.__num = num
        self.__produtos = produtos
        self.__dia = dia
        self.__mes = mes
        self.__ano = ano
        
    @property
    def cpfCliente(self):
        return self.__cpfCliente

    @property
    def num(self):
        return self.__num

    @property
    def produtos(self):
        return self.__produtos
    
    @property
    def dia(self):
        return self.__dia

    @property
    def mes(self):
        return self.__mes
    
    @property
    def ano(self):
        return self.__ano
    

class LimiteEmitirNota(tk.Toplevel):
    def __init__(self, controle, nomeCliente):

        tk.Toplevel.__init__(self)
        self.geometry('450x450')
        self.title("Emissão de note fiscal")
        self.controle = controle

        #frames dos campos do Limite para inserir e empacotar os frames
        self.frameCliente = tk.Frame(self)
        self.frameCliente.pack()
        self.frameProdutos = tk.Frame(self)
        self.frameProdutos.pack()
        self.frameData = tk.Frame(self)
        self.frameData.pack()
        self.frameButton = tk.Frame(self)
        self.frameButton.pack(pady=15)

        self.labelCliente = tk.Label(self.frameCliente, text='Cliente: ')
        self.labelCliente.pack(side='left')
        self.labelNomeCliente = tk.Label(self.frameCliente, text=nomeCliente)
        self.labelNomeCliente.pack(side='left')

        self.textProdutos = tk.Text(self.frameProdutos, height=20, width=40)
        self.textProdutos.pack()
        self.textProdutos.config(state=tk.DISABLED)
        
        self.labelDia = tk.Label(self.frameData, text='Dia:')
        self.labelDia.pack(side='left')
        self.inputDia = tk.Entry(self.frameData, width=3)
        self.inputDia.pack(side='left')
        
        self.labelMes = tk.Label(self.frameData, text='Mês:')
        self.labelMes.pack(side='left')
        self.inputMes = tk.Entry(self.frameData, width=3)
        self.inputMes.pack(side='left')
        
        self.labelAno = tk.Label(self.frameData, text='Ano:')
        self.labelAno.pack(side='left')
        self.inputAno = tk.Entry(self.frameData, width=5)
        self.inputAno.pack(side='left')
        
        self.buttonAdicionar = tk.Button(self.frameButton, text='Adicionar produto')
        self.buttonAdicionar.pack(side='left')
        self.buttonAdicionar.bind('<Button>', controle.adicionarProduto)
        
        self.buttonCancela = tk.Button(self.frameButton, text='Cancelar nota')
        self.buttonCancela.pack(side='left')
        self.buttonCancela.bind('<Button>', controle.cancelaHandler)
        
        self.buttonConcluido = tk.Button(self.frameButton, text='Emitir nota')
        self.buttonConcluido.pack(side='left')
        self.buttonConcluido.bind('<Button>', controle.fechaNota)
        
        self.buttonFecha = tk.Button(self.frameButton, text='Fechar janela')
        self.buttonFecha.pack(side='left')
        self.buttonFecha.bind('<Button>', controle.fechaJanela)

    def mostraJanela(self, titulo, msg):
        messagebox.showinfo(titulo, msg)
        

class LimiteAdicionaProd(tk.Toplevel):
    def __init__(self, controle):
        
        tk.Toplevel.__init__(self)
        self.controle = controle
        self.geometry('250x100')
        self.title('Adição de produto')
        
        self.frameCodigo = tk.Frame(self)
        self.frameCodigo.pack()
        self.frameQuant = tk.Frame(self)
        self.frameQuant.pack()
        self.frameButton = tk.Frame(self)
        self.frameButton.pack()

        self.labelCodigo = tk.Label(self.frameCodigo, text='Código do produto: ')
        self.labelCodigo.pack(side='left')
        self.inputCodigo = tk.Entry(self.frameCodigo, width=15)
        self.inputCodigo.pack(side='left')

        self.labelQuant = tk.Label(self.frameQuant, text='Quantidade vendida')
        self.labelQuant.pack(side='left')
        self.inputQuant = tk.Entry(self.frameQuant, width=15)
        self.inputQuant.pack(side='left')

        self.buttonInsere = tk.Button(self.frameButton, text='Inserir')
        self.buttonInsere.pack(side='left')
        self.buttonInsere.bind('<Button>', controle.inserirHandler)

        self.buttonConcluido = tk.Button(self.frameButton, text='Concluído')
        self.buttonConcluido.pack(side='left')
        self.buttonConcluido.bind('<Button>', controle.fechaHandler)


class CtrlVenda():
    def __init__(self, ctrlPrincipal):
        self.ctrlPrincipal = ctrlPrincipal
        
        #verificação do arquivo pickle com o registro das vendas
        if not os.path.isfile('vendas.pickle'):
            self.listaNotas = []
        else:
            with open('vendas.pickle', 'rb') as f:
                self.listaNotas = pickle.load(f)

    #Callbacks de emissão de nota fiscal            
    def emitirNota(self):
        self.listaMercNota = []
        self.cpf = simpledialog.askinteger('Emissão de nota', 'Insira o CPF do cliente')
        listaClientes = self.ctrlPrincipal.ctrlCliente.getListaClientes()
        aux = False
        for cliente in listaClientes:
            if self.cpf == cliente.cpf:
                aux = True
                self.limiteEmite = LimiteEmitirNota(self, cliente.nome)
            break
        if not aux:
            messagebox.showinfo('Erro', 'Cliente não cadastrado')
            self.ctrlPrincipal.ctrlCliente.cadastraCliente()
            
    def adicionarProduto(self, event):
        self.limiteAdiciona = LimiteAdicionaProd(self)
        
    def cancelaHandler(self, event):
        listaProdutos = self.ctrlPrincipal.ctrlEstoque.getListaProdutos()
        for prod in listaProdutos:
            for merc in self.listaMercNota:
                if merc.codigo == prod.codigoNumerico:
                    prod.quant += int(merc.quant)
                    self.ctrlPrincipal.ctrlEstoque.atualizaEstoque(listaProdutos)
                    self.limiteEmite.mostraJanela('Sucesso', 'Nota fiscal cancelada')
                    self.limiteEmite.destroy()

    def fechaNota(self, event):
        valorMerc = 0
        valorTotal = 0
        msg = 'Valor da nota fiscal: R$'
        num = len(self.listaNotas) + 1
        dia = self.limiteEmite.inputDia.get()
        mes = self.limiteEmite.inputMes.get()
        ano = self.limiteEmite.inputAno.get()
        nota = NotaFiscal(self.cpf, num, self.listaMercNota, dia, mes, ano)
        self.listaNotas.append(nota)
        if len(self.listaNotas) != 0:
            with open('vendas.pickle', 'wb') as f:
                pickle.dump(self.listaNotas, f)
        #contador pro valor total
        for merc in self.listaMercNota:
            valorMerc = int(merc.valorVenda) * int(merc.quant)
            valorTotal += valorMerc
        msg += str(valorTotal)
        self.limiteEmite.mostraJanela('Nota emitida', msg)
        self.fechaJanela(event)
            
        
    def fechaJanela(self, event):
        self.limiteEmite.destroy()
        
    #Callbacks de inserção de produtos na nota
    def inserirHandler(self, event):
        msg = ''
        msg2 = ''
        listaProdutos = self.ctrlPrincipal.ctrlEstoque.getListaProdutos()
        codigo = self.limiteAdiciona.inputCodigo.get()
        quant = self.limiteAdiciona.inputQuant.get()
        aux = False
        for prod in listaProdutos:
            if int(codigo) == int(prod.codigoNumerico):
                aux = True
                if int(quant) <= int(prod.quant):
                    #mostragem dos produtos na tela
                    self.limiteEmite.textProdutos.config(state=tk.NORMAL)
                    msg += 'Produto: '+ prod.descricao + '\n'
                    msg += 'Preço: ' + str(prod.valorVenda) + '\n'
                    msg += 'Quantidade: ' + str(quant) + '\n'
                    msg += '\n' 
                    self.limiteEmite.textProdutos.insert(tk.END, msg)
                    self.limiteEmite.textProdutos.config(state=tk.DISABLED)
                    #alteração do estoque do produto
                    prod.quant -= int(quant)
                    self.ctrlPrincipal.ctrlEstoque.atualizaEstoque(listaProdutos)
                    #inserção do produto em uma lista temporária para criação de uma instância de nota
                    codigo = prod.codigoNumerico
                    valorVenda = prod.valorVenda
                    merc = self.ctrlPrincipal.ctrlEstoque.criaMercadoria(codigo, None, None, valorVenda, quant)
                    self.listaMercNota.append(merc)
                else:
                    msg2 += 'Quantidade solicitada é maior que o estoque atual do produto' + '\n'
                    msg2 += 'Estoque: ' + str(prod.quant)
                    self.limiteEmite.mostraJanela('Erro', msg2)
                    self.limiteAdiciona.inputQuant.delete(0, len(self.limiteAdiciona.inputQuant.get()))
        if not aux:
            self.limiteEmite.mostraJanela('Erro', 'Código de produto inválido')
            self.limiteAdiciona.inputCodigo.delete(0, len(self.limiteAdiciona.inputCodigo.get()))
            
    def fechaHandler(self, event):
        self.limiteAdiciona.destroy()
        
    #Métodos adicionais
    def getListaNotasFiscais(self):
        return self.listaNotas