menu = """
[1] Deposito
[2] Saque
[3] Extrato
[4] Sair
"""
saldo = 0
extrato = " "
limite = 500
numero_saques = 0
LIMITE_SAQUE = 3

while True:
    opcao = str(input(menu))

    if opcao == "1":
        valor = float(input("Digite o valor que deseja depositar: "))
        if valor > 0: 
            saldo += valor 
            extrato += f"Depósito: R${valor:2f}\n"
        else:
            print("Valor inválido! Tente novamente")
        
    elif opcao == "2":
        valor_saque = float(input("Digite o valor para saque: "))
        
        execedeu_litime = valor_saque > limite 
        execedeu_saldo = valor_saque > saldo
        execedeu_saque = numero_saques >= LIMITE_SAQUE


        if execedeu_saldo:
            print("Operação Falhou! Você não tem saldo suficiente.")
        elif execedeu_litime:
            print("Operação falhou! Execedeu o limite de saque.")
        elif execedeu_saque:
            print("Operação Falhou! Execedeu o número de saques")       
        elif valor_saque >0:
            saldo -= valor_saque
            extrato += f"Saque: R${valor_saque:.2f}\n"
            numero_saques+= 1 
        else:
            print("Operação Falhou! O valor informado é inválido")
        
        
    elif opcao == "3":
        print("\n======EXTRATO=======")
        print(f"Sem movimentação: "if not extrato else extrato)
        print(f"\n Saldo: R${saldo:2f}")
  
    elif opcao == "4":
        print("Obrigado por usar o sistema ")
        break
    
    else:
        print("Tente Novamente!")

            
            
    