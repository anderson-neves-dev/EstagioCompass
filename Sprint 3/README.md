# 📝 Exercício

## 1️⃣ Código do exercício 3 - ETL com Python

- Dado a base de dados [actors.csv](Execicios/actors.csv) foi solicitado para fazer querys divididas em etapas neste arquivo e armazenar cada uma em um arquivo .txt.
 
### Código para resolução
 [resolução.py](Execicios/resolucao.py)

### Etapa 1

#### Apresentar o ator/atriz com maior número de filmes e a respectiva quantidade

[Resposta](Execicios/Etapa-1.txt)

### Etapa 2

#### Apresentar a média de receita de bilheteria bruta dos principais filmes, considerando todos os atores

[Resposta](Execicios/Etapa-2.txt)

### Etapa 3

#### Apresentar o ator/atriz com a maior média de receita de bilheteria bruta por filme do conjunto de dados

[Resposta](Execicios/Etapa-3.txt)

### Etapa 4

#### Realizar a contagem de aparições dos filmes no dataset, listando-os pela quantidade de vezes em que estão presentes. Considerando a ordem decrescente e, em segundo nível, o nome do filme.

[Resposta](Execicios/Etapa-4.txt)

### Etapa 5

#### Apresentar a lista dos atores ordenada pela receita bruta de bilheteria de seus filmes (coluna Total Gross), em ordem decrescente.

[Resposta](Execicios/Etapa-5.txt)

# 🔍 Evidências

- Algumas linhas da base de dados [actors.csv](Execicios/actors.csv) contiam `,` no nome dos atores e gerava o dataFrame de forma errada. Mas, nas linhas que ocorriam isso estavam dentro de aspas dupla, como o exemplo abaixo:

```
"Robert Downey, Jr.",3947.30 ,53,74.50 ,The Avengers,623.40
```

- Para resolver isso, utilizei a seguinte lógica:

```
    for i, registro in enumerate(arquivo):
        if i == 0:
            continue
        #Detectando linha começando com aspas dúplas
        if registro.startswith('"'):
            partes = registro.split('",')
            actor = partes[0] + '"'
            total_gross, number_of_movies, avg_per_movie, top_movie, top_gross = partes[1].split(',') + partes[2:]
        # Quando não tinham aspas no começo, peguei de forma normal mesmo
        else:
            actor, total_gross, number_of_movies, avg_per_movie, top_movie, top_gross = registro.split(',')
```

# 🏆 Certificados
