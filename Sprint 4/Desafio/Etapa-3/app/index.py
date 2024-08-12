import hashlib

# Loop while para aceitar mais de uma entrada, conforme solicitado no passo 4 da etapa 3
loop = True
while loop:
    # Recebendo string via input
    stringInput = input("Coloque a string para mascaramento: ")

    #Criando objeto textHash de algoritmo SHA-1
    textHash = hashlib.sha1()

    #Atualizando o obejeto hash pra receber a string enviada por input
    textHash.update(stringInput.encode())

    #Imprimindo hash no terminal utilizando o método hexdigest 
    print("String mascarada: {}".format(textHash.hexdigest()))

    # Loop while para saber se o usuário quer ou não continuar inserindo string
    while True:
        option = input("Deseja mascara mais caracteres?(Sim/Não) ").upper()
        if(option == 'NAO' or option == 'NÃO'):
            # Parando os dois loops
            loop = False
            break
        elif(option == 'SIM'):
            break
        else:
            print('Opção inválida')
            