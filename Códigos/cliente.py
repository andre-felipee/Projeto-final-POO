import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import pickle
import os.path

class Cliente():
    def __init__(self, nome, endereco, email, cpf):
        self.__nome = nome
        self.__endereco = endereco
        self.__email = email
        self.__cpf = cpf

    @property
    def nome(self):
        return self.__nome

    @property
    def endereco(self):
        return self.__endereco
 
    @property
    def email(self):
        return self.__email 
    
    @property
    def cpf(self):
        return self.__cpf
    
    
class LimiteCadastroCliente(tk.Toplevel):
    def __init__(self, controle):

        tk.Toplevel.__init__(self)
        self.controle = controle 
        self.geometry('250x150')
        self.title('Cadastro de cliente')

        self.frameNome = tk.Frame(self)
        self.frameEndereco = tk.Frame(self)
        self.frameEmail = tk.Frame(self)
        self.frameCPF = tk.Frame(self)
        self.frameButton = tk.Frame(self)
        self.frameNome.pack()
        self.frameEndereco.pack()
        self.frameEmail.pack()
        self.frameCPF.pack()
        self.frameButton.pack()
        
        self.labelNome = tk.Label(self.frameNome, text='Nome do cliente:')
        self.labelNome.pack(side='left')
        self.inputNome = tk.Entry(self.frameNome, width=20)
        self.inputNome.pack(side='left')

        self.labelEndereco = tk.Label(self.frameEndereco, text='Endereço:')
        self.labelEndereco.pack(side='left')
        self.inputEndereco = tk.Entry(self.frameEndereco, width=20)
        self.inputEndereco.pack(side='left')

        self.labelEmail = tk.Label(self.frameEmail, text='Email:')
        self.labelEmail.pack(side='left')
        self.inputEmail = tk.Entry(self.frameEmail, width=20)
        self.inputEmail.pack(side='left')

        self.labelCPF = tk.Label(self.frameCPF, text='CPF: ')
        self.labelCPF.pack(side='left')
        self.inputCPF = tk.Entry(self.frameCPF, width=20)
        self.inputCPF.pack(side='left')
        
        self.buttonCadastra = tk.Button(self.frameButton, text='Cadastrar')
        self.buttonCadastra.pack(side='left')
        self.buttonCadastra.bind('<Button>', controle.cadastraHandler)
        
        self.buttonLimpa = tk.Button(self.frameButton, text='Limpar')
        self.buttonLimpa.pack(side='left')
        self.buttonLimpa.bind('<Button>', controle.limpaHandler)

        self.buttonFecha = tk.Button(self.frameButton, text='Concluído')
        self.buttonFecha.pack(side='left')
        self.buttonFecha.bind('<Button>', controle.fechaHandler)
        
    def mostraJanela(Self, titulo, msg):
        messagebox.showinfo(titulo, msg)
        

class CtrlCliente():
    def __init__(self):
        
        #Verificação arquivo pickle com lista de clientes
        if not os.path.isfile('clientes.pickle'):
            self.listaClientes = []
        else:
            with open('clientes.pickle', 'rb') as f:
                self.listaClientes = pickle.load(f)
        
    #método para criação do limite do cadastro de clientes
    def cadastraCliente(self):
        self.limiteCadastraCliente = LimiteCadastroCliente(self)
        
    #callbacks de cadastro de cliente
    def cadastraHandler(self, event):
        nome = self.limiteCadastraCliente.inputNome.get()
        endereco = self.limiteCadastraCliente.inputEndereco.get()
        email = self.limiteCadastraCliente.inputEmail.get()
        cpf = int(self.limiteCadastraCliente.inputCPF.get())
        clt = Cliente(nome, endereco, email, cpf)
        aux = False
        for clt in self.listaClientes:
            if cpf == clt.cpf:
                aux = True
                self.limiteCadastraCliente.mostraJanela('Erro', 'CPF já cadastrado')
                self.limpaHandler(event)
            break
        if not aux:
            self.listaClientes.append(clt)
            if len(self.listaClientes) != 0:
                with open('clientes.pickle', 'wb') as f:
                    pickle.dump(self.listaClientes, f)
            self.limiteCadastraCliente.mostraJanela('Sucesso', 'Cliente cadastrado')
            self.limpaHandler(event)

    def limpaHandler(self, event):
        self.limiteCadastraCliente.inputNome.delete(0, len(self.limiteCadastraCliente.inputNome.get()))
        self.limiteCadastraCliente.inputEndereco.delete(0, len(self.limiteCadastraCliente.inputEndereco.get()))
        self.limiteCadastraCliente.inputEmail.delete(0, len(self.limiteCadastraCliente.inputEmail.get()))
        self.limiteCadastraCliente.inputCPF.delete(0, len(self.limiteCadastraCliente.inputCPF.get()))
        
    def fechaHandler(self, event):
        self.limiteCadastraCliente.destroy()

    #método de consulta de clientes
    def consultarCliente(self):
        msg = ''
        cpfParam = simpledialog.askinteger('Consulta de Cliente', 'Insira o CPF do cliente: ')
        aux = False
        for cliente in self.listaClientes:
            if cpfParam == int(cliente.cpf):
                aux = True
                msg += 'Nome: ' + cliente.nome + '\n'
                msg += 'Endereço: ' + cliente.endereco + '\n'
                msg += 'Email: ' + cliente.email + '\n'
                messagebox.showinfo('Cliente encontrado', msg)
            break
        if not aux:
            messagebox.showinfo('Erro', 'Não há cliente com esse CPF')
            
    #método de instanciação para controladores externos
    def getListaClientes(self):
        return self.listaClientes
            