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

def deposito(saldo, valor, extrato,/):  
  if valor > 0: 
    saldo += valor 
    extrato += f"Depósito: R${valor:2f}\n"
    print("Depósito realizado com sucesso!")
  else:
      print("Valor inválido! Tente novamente")
  return saldo, extrato



def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saque):
    execedeu_litime = valor > limite 
    execedeu_saldo = valor > saldo
    execedeu_saque = numero_saques >= limite_saque


    if execedeu_saldo:
         print("Operação Falhou! Você não tem saldo suficiente.")
    
    elif execedeu_litime:
        print("Operação falhou! Execedeu o limite de saque.")
    
    elif execedeu_saque:
        print("Operação Falhou! Execedeu o número de saques")       
    
    
    elif valor >0:
      saldo -= valor
      extrato += f"Saque: R${valor:.2f}\n"
      numero_saques = numero_saques + 1
      print("Saque realizado com sucesso! ")
    
    else:
            print("Operação Falhou! O valor informado é inválido")  
    
    return saldo, extrato
    
def exibir_extrato(saldo,/,*,extrato):
    print("\n======EXTRATO=======")
    print(f"Sem movimentação: "if not extrato else extrato)
    print(f"\n Saldo: R${saldo:2f}")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (Somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Já existe usuário com esse CPF ")
        return
    nome = input("Nome Completo: ")
    data_nascimento = input("Data de nascimento (dd-mm-aaaa)")
    endereço = input("Endereço completo (logradouro, nro - barrio - cidade/sigla estado):")

    usuarios.append({'nome':nome, 'data_nascimento':data_nascimento, 'endereço':endereço, 'cpf':cpf})


    print("Usuários criados com sucesso...")


def filtrar_usuario(cpf,usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario['cpf'] == cpf]
    return usuarios_filtrados[0]  if usuarios_filtrados else None

def criar_conta(agencia, numero_conta,usuarios):
    cpf = input("Informe seu CPF: ")
    usuario = filtrar_usuario(cpf,usuarios)

    if usuario:
        print("Conta criada com sucesso...")
        return {'agencia':agencia,'numero_conta':numero_conta, 'usuario':usuario}
    
    print("Usuário ainda não cadastrato, tente o cadastro primeiro...")

def listar_contas(contas):
    for conta in contas:
        linha = f"""
        Agência: {conta['agencia']}
        C/c: {conta['numero_conta']}
        Titular: {conta['usuario']['nome']}

"""
    print(linha)

def main():
    LIMITE_SAQUE = 3
    AGENCIA = "0001"
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == '1':
            valor = float(input("Informe o valor do depósito: "))

            saldo, extrato = deposito(saldo, valor, extrato)
             

            
        elif opcao == '2':
            valor = float(input("Digite o valor que deseja sacar: "))

            saldo, extrato   = sacar(saldo=saldo,
                                    valor=valor,
                                    extrato=extrato,
                                    limite=limite,
                                    numero_saques=numero_saques,
                                    limite_saque=LIMITE_SAQUE,
                                  )
             
        elif opcao == '3':
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == '4':
            criar_usuario(usuarios)
        
        elif opcao == '5':
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)
        elif opcao == '6':
            listar_contas(contas)
        elif opcao == '7':
            break



main()