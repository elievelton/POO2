import Class_Cliente
import Class_Conta
import Class_Histo

cliente1 = Cliente('elievelto','edimar','00899987')
cliente2 = Cliente('dougla','edimar','0231231')
conta1 = Conta(1243,cliente1,200,500)
conta2= Conta(122,cliente1,400,1000)
conta1.deposita(100)
conta1.sacar(50)
conta1.historico.imprime()
conta2.deposita(200)
conta2.sacar(100)
conta2.historico.imprime()
conta2.transfere(conta1,126)
conta1.extrato
conta1.transfere(conta2,235)
conta1.historico.imprime()
conta2.historico.imprime()
Conta.get_contador_de_contas()