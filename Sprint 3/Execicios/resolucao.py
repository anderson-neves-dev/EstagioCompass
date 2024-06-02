#!/usr/local/bin/python3

with open('actors.csv') as arquivo:
    
    ator_com_mais_filmes = [0, ""]
    max_avg_per_movie = [0 , ""]
    top_movie_count = {}
    top_gloss_with_ator = {}

    soma_total_gross = 0.0
    for i, registro in enumerate(arquivo):
        if i == 0:
            continue
        #Observei que alguns atores tinha virgula no nome e estava bulgandoa sepração dos caracteres
        #Como os atores que tinham isso estavam entre aspas duplas, fiz a seguinte forma de pegar os dados onde aconteciam isso:
        if registro.startswith('"'):
            partes = registro.split('",')
            actor = partes[0] + '"'
            total_gross, number_of_movies, avg_per_movie, top_movie, top_gross = partes[1].split(',') + partes[2:]
        # Quando não tinham aspas no começo, peguei de forma normal mesmo
        else:
            actor, total_gross, number_of_movies, avg_per_movie, top_movie, top_gross = registro.split(',')
        #Etapa 1 pegando o ator com mais filmes
        number_of_movies = int(number_of_movies.strip())
        if number_of_movies > ator_com_mais_filmes[0]:
            ator_com_mais_filmes[0] = number_of_movies
            ator_com_mais_filmes[1] = actor
        #Etapa 2 fazendo a media de valores de bilheteria
        total_gross = float(total_gross.strip())
        soma_total_gross += total_gross
        media_total_gross = soma_total_gross / i

        #Etapa 3 pegando o ator com maior media por filme
        avg_per_movie = float(avg_per_movie.strip())
        if avg_per_movie > max_avg_per_movie[0]:
            max_avg_per_movie[0] = avg_per_movie
            max_avg_per_movie[1] = actor

        #Etapa 4 criando um dicionario para pegar a quantidade de vezes que repetia cada filme
        top_movie = top_movie.strip()
        if top_movie in top_movie_count:
            top_movie_count[top_movie] += 1
        else:
            top_movie_count[top_movie] = 1

        #Etapa 5 ordenando de forma decrecente os atores por renda bruta
        top_gross = float(top_gross.strip())
        top_gloss_with_ator[actor] = top_gross
# Ordenar o dicionário por contagem decrescente e depois por nome do filme. fonte que utilizei: https://py.checkio.org/forum/post/9298/sorted-function-explanation-please/
top_movie_count = sorted(top_movie_count.items(), key=lambda x: (-x[1], x[0]))


with open('Etapa-1.txt', 'w') as saida:
    print(f"O ator com o maior número de filmes é {ator_com_mais_filmes[1]} com {ator_com_mais_filmes[0]} filmes.", file=saida)

with open('Etapa-2.txt', 'w') as saida:
    print(f"A media de receita de bilheteria bruta foi de: {round(media_total_gross, 2)}", file=saida)

with open('Etapa-3.txt', 'w') as saida:
    print(f"O ator com a maior média por filme é {max_avg_per_movie[1]} com uma média de {max_avg_per_movie[0]:.2f}.", file=saida)

posicao = 1
with open('Etapa-4.txt', 'w') as saida:
    for movie, count in top_movie_count:
        print(f"{posicao}° - O filme {movie} aparece {count} vez(es) no dataset", file=saida)
        posicao += 1

with open('Etapa-5.txt', 'w') as saida:
    top_gloss_with_ator = sorted(top_gloss_with_ator.items(), key=lambda x: -x[1])
    for actor, top_gloss in top_gloss_with_ator:
        print(f"{actor} - {top_gloss}", file=saida)

if arquivo.closed:
    print('Arquivo foi fechado!')
if saida.closed:
    print('Arquivo de saída foi fechado')
