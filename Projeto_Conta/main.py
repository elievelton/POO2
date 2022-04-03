# -*- coding: utf-8 -*-
__author__ = "Elievelto & Bruna"
__copyright__ = "Copyright 2022, Por mim"
__credits__ = ["Elievelto & Bruna"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "eu também"
__email__ = "suporte@gamesbruna.com"
__status__ = "Production"
'''Sistema que simula um aplicativo bancario'''

import sys
import os


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QApplication, QFileDialog
from PyQt5.QtCore import QCoreApplication

"""importando as telas"""
from telas.tela_menuCadastrar import Tela_Menu_Cadastrar
from telas.tela_menu import Tela_Menu
from telas.tela_login import Tela_Login
from telas.tela_CadastroCon import Tela_CadastroCon
from telas.tela_CadastroCli import Tela_CadastroCli
from telas.tela_transferir import Tela_Transferir
from telas.tela_sacar import Tela_Sacar
from telas.tela_historico import Tela_Historico
from telas.tela_extrato import Tela_Extrato
from telas.tela_depositar import Tela_Depositar


"""import das classes"""
from classBanco import Banco
from classCadastro import Cadastro
from classHisto import Historico
from classConta import Conta
from classCliente import Cliente


"""Ainda precisa ajustar esse código, depois que todas as telas estiverem prontas"""


class Ui_Main(QtWidgets.QWidget):
    def setupUi(self, Main):
        """ Função que realiza as configurações das telas"""
        Main.setObjectName('Main')
        Main.resize(640, 480)

        self.QtStack = QtWidgets.QStackedLayout()  # pilhas de telas

        self.stack0 = QtWidgets.QMainWindow()
        self.stack1 = QtWidgets.QMainWindow()
        self.stack2 = QtWidgets.QMainWindow()
        self.stack3 = QtWidgets.QMainWindow()
        self.stack4 = QtWidgets.QMainWindow()
        self.stack5 = QtWidgets.QMainWindow()
        self.stack6 = QtWidgets.QMainWindow()
        self.stack7 = QtWidgets.QMainWindow()
        self.stack8 = QtWidgets.QMainWindow()
        self.stack9 = QtWidgets.QMainWindow()

        self.tela_login = Tela_Login()
        self.tela_login.setupUi(self.stack0)
        self.tela_menu = Tela_Menu()
        self.tela_menu.setupUi(self.stack1)
        self.tela_menuCadastrar = Tela_Menu_Cadastrar()
        self.tela_menuCadastrar.setupUi(self.stack2)
        self.tela_CadastroCli = Tela_CadastroCli()
        self.tela_CadastroCli.setupUi(self.stack3)
        self.tela_CadastroCon = Tela_CadastroCon()
        self.tela_CadastroCon.setupUi(self.stack4)
        self.tela_depositar = Tela_Depositar()
        self.tela_depositar.setupUi(self.stack5)
        self.tela_sacar = Tela_Sacar()
        self.tela_sacar.setupUi(self.stack6)
        self.tela_transferir = Tela_Transferir()
        self.tela_transferir.setupUi(self.stack7)
        self.tela_extrato = Tela_Extrato()
        self.tela_extrato.setupUi(self.stack8)
        self.tela_historico = Tela_Historico()
        self.tela_historico.setupUi(self.stack9)

        self.QtStack.addWidget(self.stack0)
        self.QtStack.addWidget(self.stack1)
        self.QtStack.addWidget(self.stack2)
        self.QtStack.addWidget(self.stack3)
        self.QtStack.addWidget(self.stack4)
        self.QtStack.addWidget(self.stack5)
        self.QtStack.addWidget(self.stack6)
        self.QtStack.addWidget(self.stack7)
        self.QtStack.addWidget(self.stack8)
        self.QtStack.addWidget(self.stack9)


"""Classe principal"""


class Main(QMainWindow, Ui_Main):

    def __init__(self, parent=None):
        """ Função que realiza as configurações do que está presente nas telas"""
        super(Main, self).__init__(parent)
        self.setupUi(self)

        self.cad = Cadastro()
        self.his = Historico()

        """CRIANDO O BANCO DE DADOS E AS TABELAS"""
        self.ban = Banco()
        database_query = "CREATE DATABASE IF NOT EXISTS banco"


        conexao = self.ban.criando_conexao(
            'localhost', 'root', '12345', 'banco')

        self.ban.criando_bancodedados(conexao, database_query)

        tabela_clientes = "CREATE TABLE IF NOT EXISTS clientes( cpf bigint(11) NOT NULL PRIMARY KEY, nome text NOT NULL , endereco text NOT NULL, nascimento text NOT NULL, usuario text NOT NULL, senha VARCHAR(32) NOT NULL);"
        self.ban.executando_query(conexao, tabela_clientes)

        tabela_contas = "CREATE TABLE IF NOT EXISTS contas( numero int(5) NOT NULL , cpf bigint(11) NOT NULL PRIMARY KEY, saldo FLOAT(5,2) NOT NULL, limite text NOT NULL, historico text DEFAULT NULL);"
        self.ban.executando_query(conexao, tabela_contas)


        self.tela_login.pushButton.clicked.connect(self.botaoLogin)
        self.tela_login.pushButton_2.clicked.connect(
            self.abrirTelaMenu_Cadastro)

        self.tela_menu.pushButton.clicked.connect(self.abrirTelaDepositar)
        self.tela_menu.pushButton_2.clicked.connect(self.abrirTelaSacar)
        self.tela_menu.pushButton_3.clicked.connect(self.abrirTelaTransferir)
        self.tela_menu.pushButton_4.clicked.connect(self.abrirTelaExtrato)
        self.tela_menu.pushButton_5.clicked.connect(self.abrirTelaLogin)

        self.tela_menuCadastrar.pushButton.clicked.connect(
            self.abrirTelaCadastroCliente)
        self.tela_menuCadastrar.pushButton_2.clicked.connect(
            self.abrirTelaCadastroConta)
        self.tela_menuCadastrar.pushButton_3.clicked.connect(
            self.abrirTelaLogin)

        self.tela_CadastroCli.pushButton.clicked.connect(
            self.cadastrar_cliente)
        self.tela_CadastroCli.pushButton_2.clicked.connect(
            self.abrirTelaMenu_Cadastro)

        self.tela_CadastroCon.pushButton.clicked.connect(self.cadastrar_conta)
        self.tela_CadastroCon.pushButton_2.clicked.connect(
            self.abrirTelaMenu_Cadastro)

        self.tela_depositar.pushButton.clicked.connect(self.botaoDepositar)
        self.tela_depositar.pushButton_2.clicked.connect(self.abrirTelaMenu)

        self.tela_sacar.pushButton.clicked.connect(self.botaoSacar)
        self.tela_sacar.pushButton_2.clicked.connect(self.abrirTelaMenu)

        self.tela_transferir.pushButton.clicked.connect(self.botaoTransferir)
        self.tela_transferir.pushButton_2.clicked.connect(self.abrirTelaMenu)

        self.tela_extrato.pushButton.clicked.connect(self.botaoExtrato)
        self.tela_extrato.pushButton_2.clicked.connect(self.abrirTelaMenu)
        self.tela_extrato.pushButton_3.clicked.connect(self.abriTelaHistorico)

        self.tela_historico.pushButton.clicked.connect(self.botaoHistorico)
        self.tela_historico.pushButton_2.clicked.connect(self.abrirTelaExtrato)

    def abrirTelaLogin(self):
        """Carrega tela inicial"""
        self.QtStack.setCurrentIndex(0)

    def abrirTelaMenu(self):
        """Carrega tela menu"""
        self.QtStack.setCurrentIndex(1)

    def abrirTelaMenu_Cadastro(self):
        """Carrega tela menu cadastro"""
        self.QtStack.setCurrentIndex(2)

    def abrirTelaCadastroCliente(self):
        """Carrega tela para cadastrar clientes"""
        self.QtStack.setCurrentIndex(3)

    def abrirTelaCadastroConta(self):
        """Carrega tela para cadastrar contas"""
        self.QtStack.setCurrentIndex(4)

    def abrirTelaDepositar(self):
        """Carrega tela para realizar depósito e informa os atributos do cliente"""
        self.QtStack.setCurrentIndex(5)
        login = self.tela_login.lineEdit.text()
        x = self.cad.buscarConCli(login)
        y = self.cad.buscarCliCon(login)
        self.tela_depositar.lineEdit_4.setText(x.nome)
        self.tela_depositar.lineEdit_5.setText(str(y.numero))
        self.tela_depositar.lineEdit_3.setText('R$ ' + str(y.saldo))

    def abrirTelaSacar(self):
        """Carrega tela para realizar saque e informa os atributos do cliente"""
        self.QtStack.setCurrentIndex(6)
        login = self.tela_login.lineEdit.text()
        x = self.cad.buscarConCli(login)
        y = self.cad.buscarCliCon(login)
        self.tela_sacar.lineEdit_4.setText(x.nome)
        self.tela_sacar.lineEdit_5.setText(str(y.numero))
        self.tela_sacar.lineEdit_3.setText('R$ ' + str(y.saldo))

    def abrirTelaTransferir(self):
        """Carrega tela para realizar transferência e informa os atributos do cliente"""
        self.QtStack.setCurrentIndex(7)
        login = self.tela_login.lineEdit.text()
        x = self.cad.buscarConCli(login)
        y = self.cad.buscarCliCon(login)
        self.tela_transferir.lineEdit_6.setText(x.nome)
        self.tela_transferir.lineEdit_5.setText(str(y.numero))
        self.tela_transferir.lineEdit_4.setText('R$ ' + str(y.saldo))

    def abrirTelaExtrato(self):
        """Carrega tela para mostrar o extrato do cliente"""
        self.QtStack.setCurrentIndex(8)

    def abriTelaHistorico(self):
        """Carrega tela para mostrar o histórico do cliente"""
        self.QtStack.setCurrentIndex(9)

    def botaoLogin(self):
        """Faz o login e verifica se existe usuário"""
        login = self.tela_login.lineEdit.text()
        senha = self.tela_login.lineEdit_2.text()
        conexao = self.ban.criando_conexao(
                    'localhost',
                    'root',
                    '12345',
                    'banco',
                )
        cursor= conexao.cursor()


        try:
            cursor.execute("SELECT senha FROM clientes WHERE usuario = '{}'".format(login))
            bd_busca = cursor.fetchall()
            conexao.close()
        except:
            self.tela_login.textBrowser.setText("Dados de login incorretos!")

        if(senha == bd_busca[0][0]):
            self.abrirTelaMenu()

        else:


            existe = self.cad.buscarUsuario(login)
            x = self.cad.buscarConCli(login)
            y = self.cad.buscarCliCon(login)
            if(existe != None):

                if (x != None):
                    if((existe.usuario and existe.senha) == (login and senha)):
                        self.abrirTelaMenu()
                        self.tela_menu.lineEdit_2.setText(existe.nome)
                        self.tela_menu.lineEdit_3.setText(y.numero)
                        self.tela_menu.lineEdit.setText('R$ ' + str(y.saldo))
                    else:
                        self.tela_login.textBrowser.setText(
                            "Dados de login incorretos!")
                        self.tela_login.lineEdit.setText('')
                        self.tela_login.lineEdit_2.setText('')
                else:
                    QMessageBox.information(
                        None, 'POO2', 'Esse cliente não possue uma conta! Realize um cadastro primeiro')
            else:
                QMessageBox.information(
                    None, 'POO2', 'Cliente não existe! Clique no botão Cadastrar e faça seu cadastro')
                self.tela_login.lineEdit.setText('')
                self.tela_login.lineEdit_2.setText('')

    def cadastrar_cliente(self):
        """ Função para cadastrar o cliente"""
        nome = self.tela_CadastroCli.lineEdit.text()
        endereco = self.tela_CadastroCli.lineEdit_2.text()
        cpf = self.tela_CadastroCli.lineEdit_3.text()
        nascimento = self.tela_CadastroCli.lineEdit_4.text()
        usuario = self.tela_CadastroCli.lineEdit_5.text()
        senha = self.tela_CadastroCli.lineEdit_6.text()

        if not (nome == '' or endereco == '' or cpf == '' or nascimento == '' or usuario == ' ' or senha == ''):
            c = Cliente(nome, endereco, cpf, nascimento, usuario, senha)
            if(self.cad.cadastrarCli(c)):
                QMessageBox.information(
                    None, 'POO2', 'Cadastro Realizado com sucesso!')
                conexao = self.ban.criando_conexao(
                    'localhost',
                    'root',
                    '12345',
                    'banco',
                )
                inserindo_clientes = f"INSERT INTO clientes (cpf, nome, endereco, nascimento, usuario, senha) VALUES ({cpf}, {nome}, {endereco}, {nascimento},{usuario}, {senha})"
                self.ban.executando_query(conexao, inserindo_clientes)

                self.tela_CadastroCli.lineEdit.setText('')
                self.tela_CadastroCli.lineEdit_2.setText('')
                self.tela_CadastroCli.lineEdit_3.setText('')
                self.tela_CadastroCli.lineEdit_4.setText('')
                self.tela_CadastroCli.lineEdit_5.setText('')
                self.tela_CadastroCli.lineEdit_6.setText('')
            else:
                QMessageBox.information(
                    None, 'POO2', 'O Cpf já foi cadastrado!')
        else:
            QMessageBox.information(
                None, 'POO2', 'Todos os valores devem ser preenchidos')

    def cadastrar_conta(self):
        """função para cadastrar conta"""
        numero = self.tela_CadastroCon.lineEdit.text()
        cpf_titular = self.tela_CadastroCon.lineEdit_2.text()
        saldo = 0
        limite = self.tela_CadastroCon.lineEdit_3.text()

        existe = self.cad.buscarCli(cpf_titular)
        if (existe != None):
            if not(numero == '' or cpf_titular == '' or limite == ''):
                co = Conta(numero, cpf_titular, saldo, limite)
                if(self.cad.cadastrarCon(co)):
                    QMessageBox.information(
                        None, 'POO2', 'Cadastro Realizado com sucesso!')
                    conexao = self.ban.criando_conexao(
                    'localhost',
                    'root',
                    '12345',
                    'banco',
                )
                    inserindo_contas = f"INSERT INTO contas (numero, cpf, saldo, limite) VALUES ({numero}, {cpf_titular}, {saldo}, {limite})"
                    self.ban.executando_query(conexao, inserindo_contas)
                    self.tela_CadastroCon.lineEdit.setText('')
                    self.tela_CadastroCon.lineEdit_2.setText('')
                    self.tela_CadastroCon.lineEdit_3.setText('')
                else:
                    QMessageBox.information(
                        None, 'POO2', 'Essa conta já existe!')
            else:
                QMessageBox.information(
                    None, 'POO2', 'Todos os campos devem ser preenchidos')
        else:
            QMessageBox.information(None, 'POO2', 'Cliente não cadastrado!')
    # chamada para a tela de depositar

    def botaoDepositar(self):
        """ Função para realizar depoósito"""
        conta_dep = self.tela_depositar.lineEdit.text()
        valor = self.tela_depositar.lineEdit_2.text()
        c = self.cad.buscarCon(conta_dep)
        if(c != None):
            if not(conta_dep == '' or valor == ''):

                c.deposita(int(valor))

                QMessageBox.information(
                    None, 'POO2', 'deposito feito com sucesso!')
                self.tela_depositar.lineEdit.setText('')
                self.tela_depositar.lineEdit_2.setText('')
                self.tela_depositar.lineEdit_3.setText('R$ ' + str(c.saldo))
                self.tela_menu.lineEdit.setText('R$ ' + str(c.saldo))
            else:
                QMessageBox.information(
                    None, 'POO2', 'Todos os campos devem ser preenchidos!')
# chamada para tela de sacar

    def botaoSacar(self):
        """ Função para realizar saque"""
        login = self.tela_login.lineEdit.text()
        conta_saq = self.cad.buscarCliCon(login)
        valor = self.tela_sacar.lineEdit_2.text()
        cs = self.cad.buscarCon(conta_saq.numero)
        if not(valor == ''):
            conta_saq.sacar(int(valor))
            QMessageBox.information(
                None, 'POO2', 'Saque feito com sucesso!')
            self.tela_sacar.lineEdit.setText('')
            self.tela_sacar.lineEdit_2.setText('')
            self.tela_sacar.lineEdit_3.setText('R$ ' + str(cs.saldo))
            self.tela_menu.lineEdit.setText('R$ ' + str(cs.saldo))
        else:
            QMessageBox.information(
                None, 'POO2', 'Todos os campos devem ser preenchidos!')

    # chamada para a tela de transferencia
    def botaoTransferir(self):
        """ Função para realizar transferência"""
        login = self.tela_login.lineEdit.text()
        conta_saida = self.cad.buscarCliCon(login)
        conta_destino = self.tela_transferir.lineEdit.text()
        valor = self.tela_transferir.lineEdit_2.text()
        cs = self.cad.buscarCon(conta_saida)
        if not(conta_destino == '' or valor == ''):
            if(self.cad.buscarCon(conta_destino)):
                d = self.cad.buscarCon(conta_destino)
                d.transfere(cs, d, int(valor))
                QMessageBox.information(
                    None, 'POO2', 'Transferencia feita com sucesso')
                self.tela_transferir.lineEdit_3.setText(
                    'R$ ' + str(cs.saldo))
                self.tela_menu.lineEdit.setText('R$ ' + str(cs.saldo))
            else:
                QMessageBox.information(
                    None, 'POO2', 'Conta de destino não existe!')
        else:
            QMessageBox.information(
                None, 'POO2', 'Todos os campos devem ser preenchidos!')
# chamada para tela de extrato

    def botaoExtrato(self):
        """ Função para informar o extrato"""
        login = self.tela_login.lineEdit.text()
        y = self.cad.buscarCliCon(login)
        c = self.cad.buscarCon(y.numero)
        if (c != None):
            x = c.extrato()
            self.tela_extrato.textBrowser.setText(x)
        else:
            QMessageBox.information(None, 'POO2', 'Essa conta não existe!')
    
# chamada para a tela historico

    def botaoHistorico(self):
        """ Função para informar o histórico"""
        login = self.tela_login.lineEdit.text()
        y = self.cad.buscarCliCon(login)
        c = self.cad.buscarCon(y.numero)
        if (c != None):
            self.tela_historico.textBrowser.setText(self.his.data_de_abertura.strftime("%Y-%m-%d %H:%M:%S"))
            # para conseguir imprimir no TextBrowser, ainda falta ajustes para imprimir data na tela
            msg = ""
            for x in c.historico.transacoes:
                msg += str(x)+"\n"
            self.tela_historico.textBrowser.setText(msg)
        else:
            QMessageBox.information(None, 'POO2', 'Essa conta não existe!')

if __name__ == "__main__":

    app = QApplication(sys.argv)
    show_main = Main()
    sys.exit(app.exec_())
