## Comandos
- Criação da imagem
```
docker build -t mascarar-dados .
```
-  Rodando a imagem em um container de forma interativa
```
docker run -it --name container-mascaramento mascarar-dados
```
- Reutilizando o container criado
```
docker start -i container-mascaramento
```