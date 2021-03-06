from operator import concat
from classBanco import Banco
import datetime
from tratamento import concatenar_operacao, replace_dados, v_int, v_float


import threading


class cliente_Thread(threading.Thread):

    def __init__(self, addr, socket, sinc):

        threading.Thread.__init__(self)
        self.conex = socket
        self.sinc = sinc
        self.ban = Banco()
        self.sessao = ''
        print(f"Nova conexao de: {addr}")

    def run(self):
        """CRIANDO CONEXAO"""

        conexao = self.ban.criando_conexao(
            'localhost', 'root', '12345', 'banco')
        
        msg_recebida = ''
        while(msg_recebida != 'encerrar'):
            msg_recebida = self.conex.recv(1024).decode()
            if(msg_recebida == 'encerrar'):
                print("Cliente Encerrado com sucesso!")
                print("AGUARDANDO NOVAS CONEXÕES...")
            else:
                print(f'{msg_recebida}')

            operacao = msg_recebida.split(',')
            """Função realiza o cadastro de uma conta"""
            if(operacao[0] == '1'):  # cadastrar conta [1, numero, cpf_titular, saldo, limite]]

                numero = v_int(operacao[1])
                cpf_titular = v_int(operacao[2])
                saldo = v_float(operacao[3])
                limite = operacao[4]

                cliente = self.ban.Buscar_cliente_bd(conexao, cpf_titular)
                conta = self.ban.Buscar_conta_bd(conexao, cpf_titular)
                teste = self.ban.retorna_dado_conta(
                    conexao, numero, cpf_titular, 2)

                now = datetime.datetime.utcnow()
                if (cliente != None):

                    if(conta == None):
                        self.ban.gravar_abertura_conta(
                            conexao, cliente[0][0], now.strftime('%Y-%m-%d %H:%M:%S'))
                        inserindo_contas = f"INSERT INTO contas (numero, cpf_titular, saldo, limite) VALUES ({numero}, {cpf_titular}, {saldo}, {limite})"
                        self.ban.executando_query(conexao, inserindo_contas)
                        self.ban.InserirConta_cliente(conexao, cpf_titular)
                        self.conex.send(
                            '0, Cadastro realizado com sucesso!'.encode())
                    else:
                        self.conex.send('1, Essa conta já existe!'.encode())
                else:
                    self.conex.send('1, Cliente não cadastrado'.encode())

            # cadastrar cliente [2, nome1, endereco2, cpf3, nascimento4, usuario5, senha6]
            elif(operacao[0] == '2'):

                nome = str(operacao[1])
                endereco = str(operacao[2])
                cpf = v_int(operacao[3])
                nascimento = str(operacao[4])
                usuario = str(operacao[5])
                senha = operacao[6]

                buscar = self.ban.Buscar_cliente_bd(conexao, cpf)
                if(buscar == None):

                    inserindo_clientes = f'INSERT INTO clientes (nome, endereco, cpf, nascimento, usuario, senha) VALUES ("{nome}","{endereco}", {cpf}, "{nascimento}","{usuario}", MD5("{senha}"))'
                    self.ban.executando_query(conexao, inserindo_clientes)
                    self.conex.send(
                        '0, Cadastro realizado com sucesso!'.encode())
                else:
                    self.conex.send('1, O CPF já está cadastrado!'.encode())

            # logar [3, login, senha]
            elif(operacao[0] == '3'):  

                cursor = conexao.cursor()
                login = operacao[1]
                valor = operacao[2]
                senha = valor
                self.sessao = login

                cursor.execute(
                    f"select * from clientes where usuario = '{login}' ")
                busca = cursor.fetchall()
                convert_lista = list(busca)

                if(convert_lista != ''):
                    if (convert_lista):
                        if((convert_lista[0][4] and convert_lista[0][5]) == (login and senha)):

                            resultado = self.ban.tratamento_dados(
                                conexao, self.sessao)
                            self.conex.send(
                                ('0, Login Realizado com Sucesso! ,' + resultado).encode())

                        else:
                            self.conex.send(
                                '1, Dados de login incorretos'.encode())
                    else:
                        self.conex.send(
                            '2, Esse cliente não possue uma conta! Realiza um cadastro primeiro'.encode())

                else:
                    self.conex.send(
                        '3, Cliente não cadastrado!'.encode())

           

            elif(operacao[0] == '5'):  # sacar [5, login, valor_saq]

                cursor = conexao.cursor()

                login = self.sessao
                valor_saq = v_float(operacao[1])

                self.sinc.acquire()
                cursor.execute(
                    f"select * from clientes where usuario = '{login}'")
                valor = cursor.fetchall()
                convert_lista = list(valor)
                texto = str(valor_saq)

                if (convert_lista):
                    if((convert_lista[0][4]) == (login)):
                        conta = self.ban.Buscar_conta_bd(conexao, valor[0][0])

                        s = v_float(conta[0][2])

                        if (s >= valor_saq):
                            msg = (f'Saque no Valor de : {valor_saq}\n')
                            self.ban.gravar_historico(
                                conexao, conta[0][1], msg)
                            convert_conta = list(map(list, conta))
                            convert_conta[0][2] = (s - valor_saq)
                            alterar_saldo = (
                                f'UPDATE `banco`.`contas` SET saldo = {convert_conta[0][2]} WHERE (numero = {conta[0][0]});')
                            self.ban.executando_query(conexao, alterar_saldo)
                            resultado = self.ban.tratamento_dados(
                                conexao, self.sessao)
                            self.conex.send(
                                ('0, Saque feito com sucesso!,' + resultado).encode())
                        else:
                            self.conex.send('1, Saldo Insuficiente!'.encode())
                        self.sinc.release()

            elif(operacao[0] == '6'):  # Botão de depositar [6, conta_dep, valor]

                login = self.sessao
                conta_dep = self.ban.Buscar_conta_bd_login(conexao, login)
                numero_conta = conta_dep[0][0]

                valor = v_float(operacao[1])
                self.sinc.acquire()

                c = self.ban.retorna_dado_conta(
                    conexao, 'cpf_titular', 'numero', numero_conta)
                saldo = self.ban.retorna_dado_conta(
                    conexao, 'saldo', 'numero', numero_conta)
                list(saldo)
                if(c != None):
                    if not(c == None):

                        self.ban.altera_saldo(conexao, valor, c[0][0])
                        resultado = self.ban.tratamento_dados(
                            conexao, self.sessao)
                        self.conex.send(
                            ('0, Deposito feito com sucesso!,' + resultado).encode())
                self.sinc.release()

             # Botão de transferir [7, conta_destino, valor, cs]
            elif(operacao[0] == '7'): 

                conta_destino = v_int(operacao[1])
                valor = v_float(operacao[2])
                cs = self.sessao
                self.sinc.acquire()  # bloqueia para uma operação dessa por vez
                # retorna a chave primaria da conta que é o cpf
                buscar_conta = self.ban.Buscar_conta_bd_login(conexao, cs)
                Busca_conta_de_destino = self.ban.retorna_dado_conta(
                    conexao, 'cpf_titular', 'numero', conta_destino)
                if(Busca_conta_de_destino):

                    if (buscar_conta[0][0] != None):

                        saldo = self.ban.transferirBD(conexao, Busca_conta_de_destino[0][0], buscar_conta[0][1], valor)
                        if(saldo ==True):
                            resultado = self.ban.tratamento_dados(conexao, self.sessao)
                            self.conex.send(('0, Transferencia feita com sucesso!,' + resultado).encode())
                        else:
                            self.conex.send(('3, Saldo insuficiente!,' + resultado).encode())

                    else:
                        self.conex.send(
                            '1, Conta de destino não existe'.encode())
                else:
                    self.conex.send('1, Conta de saída não existe'.encode())
                self.sinc.release()  # Desbloqueia a operação em Thread
             # extrato [8, login]
            elif(operacao[0] == '8'): 

                resultado = self.ban.tratamento_dados(conexao, self.sessao)
                self.conex.send(
                    ('0, Extrato realizado com Sucesso!,' + resultado).encode())

            # historico [9, login]
            elif(operacao[0] == '9'):  

                resultado = self.ban.tratamento_dados(conexao, self.sessao)
                self.conex.send(
                    ('0, Histórico realizado com Sucesso!,' + resultado).encode())

            # Abrir menu de de depositar
            elif(operacao[0] == '10'):  

                resultado = self.ban.tratamento_dados(conexao, self.sessao)
                self.conex.send(('0,' + resultado).encode())

            # Abrir menu de saque
            elif(operacao[0] == '11'):  

                resultado = self.ban.tratamento_dados(conexao, self.sessao)
                self.conex.send(('0,' + resultado).encode())

            # Abrir menu de transferir
            elif(operacao[0] == '12'):  

                resultado = self.ban.tratamento_dados(conexao, self.sessao)
                self.conex.send(('0,' + resultado).encode())

             # Botão VOltar para o menu
            elif(operacao[0] == '13'): 
                resultado = self.ban.tratamento_dados(conexao, self.sessao)
                self.conex.send(('0,' + resultado).encode())
            else:
                self.conex.send('1, Operação Inválida!'.encode())

        self.sessao = ''
        self.conex.send('1, Conexão Encerrada!!!'.encode())
