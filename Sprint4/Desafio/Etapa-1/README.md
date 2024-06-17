# Comandos
- Criação da imagem
```
docker build -t carguru .
```
-  Rodando a imagem em um container de forma interativa
```
docker run -it --name container-carguru carguru
```
- Reutilizando o container criado
```
docker start -i container-carguru
```
# Resposta do item 4.2: 
### É possivel sim reutilizar um dos containers parados e não precisar criar novos para executar novamente a imagem. O comando é:

```
docker start -i <nome ou id do container>
```
