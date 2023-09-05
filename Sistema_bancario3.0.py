from abc import ABC, abstractclassmethod
from datetime import datetime

class Cliente:
    def __init__(self,endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self,conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)
        

class PessoaFisica(Cliente):
   def __init__(self,nome,data_nasc,cpf, endereco):
       super().__init__(endereco) 
       self.nome = nome
       self.data_nasc = data_nasc
       self.cpf = cpf

class Conta:
    def __init__(self,numero,cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod 
    def nova_conta(cls,cliente, numero):
     return cls(numero, cliente)      
    
    @property
    def saldo(self):
     return self._saldo

    @property
    def numero(self):
     return self._numero

    @property
    def agencia(self):
     return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico


    def sacar(self, valor):
     saldo = self.saldo 
     execedeu_saldo = valor > saldo

     if execedeu_saldo:
         print("Operação Falhou! Você não tem saldo suficiente.")

     elif valor > 0:
        self._saldo -= valor
        print("\n Saque realizado com sucesso...")
        return True
     else:
        print("Operação falhou, tente novamente...")
     return False

    def deposito(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n Deposito realizado com sucesso...")
        else:
            print("Operação falhou, Valor informado é inválido...")
            return False
        return True    

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite= 500, limite_saque =3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saque = limite_saque

    def sacar(self,valor):
        numero_saque = len(
            [transacoes for transacoes in self.historico.
             transacoes if transacoes["tipo"] == Saque.__name__]

        )

        execedeu_litime = valor > self.limite 
        execedeu_saque = numero_saque >= self.limite_saque

        if execedeu_litime:
            print("Operação falhou! Execedeu o limite de saque.")


        elif execedeu_saque:
            print("Operação Falhou! Execedeu o número de saques")

        else:
            return super().sacar(valor) 
        
        return False
    
    def __str__(self):
       return f"""
                Agência:\t{self._agencia}
                C/c:\t{self.numero}
                Titular:\t{self.cliente.nome}
              """


class Historico:
    def __init__(self):
       self._transacoes = []

    @property
    def transacoes(self):
       return self._transacoes
    def adicionar_transacao(self, transacao):
       
       self._transacoes.append(
          {
             
             "tipo": transacao.__class__.__name__,
             "valor": transacao.valor,
             "data": datetime.now()
          }

       )       

class Transacao(ABC):
    @property
    
    @abstractclassmethod
    def valor(self):
       pass
    @abstractclassmethod
    def registrar(self, conta):
       pass

class Saque(Transacao):
    def __init__(self,valor):
        self._valor = valor
    
    @property
    def valor(self):
       return self._valor
    def registrar(self,conta):
       sucesso_transacao = conta.sacar(self._valor)

       if sucesso_transacao:
          conta.historico.adicionar_transacao(self)
       
class Deposito(Transacao):
    def __init__(self, valor):
       self._valor = valor
       
    @property
    def valor(self):
      return self._valor
       
    def registrar(self, conta):
        sucesso_transacao = conta.deposito(self._valor)

        if sucesso_transacao:
          conta.historico.adicionar_transacao(self)
       
       

# Parte 2 

def menu():
    menu = """
    "Escolha a operação desejada: "
    [1] Deposito
    [2] Saque
    [3] Extrato
    [4] Novo Usuário
    [5] Nova Conta
    [6] Listar Contas
    [7] Sair
    """
    return input(menu)
   
def filtrar_cliente(cpf, clientes):
   cliente_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
   return cliente_filtrados[0] if cliente_filtrados else None

def recuperar_conta_cliente(cliente):
   if not cliente.contas:
      print("\nCliente não possue conta...")
      return

   return cliente.contas[0]
   
def depositar(clientes):
   cpf = input("Informe o CPF do cliente: ")
   cliente = filtrar_cliente(cpf,clientes)

   if not cliente:
      print("\n Cliente não encontrado...")
      return

   valor = float(input("Informe o valor do deposito: "))
   transacao = Deposito(valor)

   conta = recuperar_conta_cliente(cliente)
   if not conta:
    return

   cliente.realizar_transacao(conta, transacao) 


def sacar(clientes):


    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf,clientes)

    if not cliente:
      print("\n Cliente não encontrado...")
      return

    valor = float(input("Informe o valor do deposito: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
     return

    cliente.realizar_transacao(conta, transacao) 


def exibir_extrato(clientes):
   cpf = input("Informe o CPF do cliente: ")
   cliente = filtrar_cliente(cpf, clientes)

   if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

   conta = recuperar_conta_cliente(cliente)
   if not conta:
        return

   print("\n================ EXTRATO ================")
   transacoes = conta.historico.transacoes

   extrato = ""
   if not transacoes:
        extrato = "Não foram realizadas movimentações."
   else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

   print(extrato)
   print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
   print("==========================================")

def criar_cliente(clientes):

    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nasc = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nasc=data_nasc, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n=== Conta criada com sucesso! ===")


def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print((str(conta)))


def main():

    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            depositar(clientes)

        elif opcao == "2":
            sacar(clientes)

        elif opcao == "3":
            exibir_extrato(clientes)

        elif opcao == "4":
            criar_cliente(clientes)

        elif opcao == "5":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "6":
            listar_contas(contas)

        elif opcao == "7":
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")


        

main()