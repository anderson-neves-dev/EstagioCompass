# 📋 Etapas

## 1️⃣ Arquivo `Dockfile` para executar o código `carguru.py`

- Primeiramente, foi salvo o código [carguru.py](Etapa-1/app/carguru.py) dentro do diretório app.
- Após isso, foi criado o arquivo `Dockfile` abaixo para gerar uma imagem, em que utilizei como base a imagem python3.
```
FROM python:3

WORKDIR /app

COPY . .

CMD ["python3", "app/carguru.py"]
```
- Para criar a imagem e o container foram utilizados os seguintes comandos, respecticamente:
```
docker build -t carguru .
```
```
docker run -it --name container-carguru carguru
```
## 2️⃣ Após pesquisas, concluí que é possível sim reutilizar um dos containers parados, sendo não necessário criar novos para executar novamente a imagem. Segue abaixo o comando:
```
docker start -i <nome ou id do container>
```
## 🐋 [Programa completo etapa 1 e 2](Etapa-1/)
## 3️⃣ Criação de script capaz de receber strings via input, gerar o hash da string por meio do algoritmo `SHA-1` e imprimir na tela com o método `hexdigest()`.
- Script de mascaramento:
    ```
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
                
    ```
- Após isso, foi criado também um arquivo `Dockfile` para gerar uma imagem, em que também utilizei como base a imagem python3
  ```
  FROM python:3

  WORKDIR /app

  COPY . .

  CMD ["python3", "app/index.py"]
  ```

- Para criar a imagem e o container foram utilizados os seguintes comandos, respecticamente:
  ```
  docker build -t mascarar-dados .
  ```
  ```
  docker run -it --name container-mascaramento mascarar-dados
  ```
## 🐋 [Programa completo etapa 3](Etapa-3/)
