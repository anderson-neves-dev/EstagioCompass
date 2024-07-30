#importando bibliotecas
import json
import requests
import boto3
from datetime import datetime
import os

# Resgatando a data atual de compilação da função
request_year = datetime.now().year
month_requisition = f'{datetime.now().month:02d}'
day_requisition = f'{datetime.now().day:02d}'

# Inicializando o cliente S3 como boto3
s3 = boto3.client('s3')

# Definindo nome do bucket e caminho do bucket s3
bucket_name = 'desafio-final-filmes-e-series-anderson-neves'
storage_path_s3 = f'Raw/TMDB/JSON/Movies/{request_year}/{month_requisition}/{day_requisition}/'

# Resgatando variável de ambiente (token da api TMDB)
access_token_auth = os.environ['ACCESS_TOKEN_AUTH']

# Definindo a URL base e os cabeçalhos correspondentes a api
discover_url = "https://api.themoviedb.org/3/discover/movie"
movie_url = "https://api.themoviedb.org/3/movie/"
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {access_token_auth}"
}

# Definindo o intervalo dos filmes que serão consultados por ano
start_year = 2012
final_year = 2022

# Definindo os gêneros dos filmes e seus respectivos IDs no TMDB que serão usados para consulta
genres_ids = {
    "crime": "80",
    "war": "10752"
}

# Demais parametros para requisição
sort_by = "vote_average.desc"
vote_average_gte = 0
vote_count_gte = 5

# Variavel global para somar o tamanho total dos arquivos em MB
total_size_of_jsons_mb = 0;

# Função para remover campos indesejados de atores, diretores e filme
def remove_unwanted_fields(items, fields_to_remove):
    for item in items:
        for field in fields_to_remove:
            item.pop(field, None)

# Função para salvar os dados resgatados da API TMDB em arquivos JSON com limite de 100 filmes por arquivo e armazená-los no S3
# Parametro da função: gênero dos filmes, ano de lançamento, os dados da requisição, nome do bucket s3 e o caminho para onde os dados serão enviados
def save_data(genre, year, data, bucket_s3_name, storage_path_s3):

    global total_size_of_jsons_mb
    part = 1

    while data:
        # Definindo nome do arquivo no padrão: movie_<genre>_<ano>_part_<x>_<AAAAMMDD>.json
        file_name = f'movie_{genre}_{year}_part_{part}_{request_year}{month_requisition}{day_requisition}.json'

        # Definindo local temporário onde será armazenado o arquivo transformado em json na cache da função lambda
        local_temporary_file_path = f'/tmp/{file_name}'
        
        # Gravando os primeiros 100 itens do json com adição de uma indetação igual a 4, calculando o tamanho total do arquivo salvo concatenando com o valor total dos arquivos gravados, e excluindo os 100 itens já gravados 
        with open(local_temporary_file_path, 'w') as json_file:
            json.dump(data[:100], json_file, indent=4)
        total_size_of_jsons_mb += os.path.getsize(local_temporary_file_path) / (1024 * 1024)
        data = data[100:]
        part += 1

        # Enviando o arquivo json gerado para o bucket s3
        try:
            s3.upload_file(local_temporary_file_path, bucket_s3_name, storage_path_s3 + file_name)
            print(f'Arquivo {file_name} enviado para o bucket {bucket_s3_name}')
        except FileNotFoundError:
            print(f'O arquivo {file_name} não foi encontrado.')

# Função lambda para fazer as requisições
def lambda_handler(event, context):

    # Definindo as variaveis globais
    global total_size_of_jsons_mb;

    # Loop para fazer as resquisições por gênero
    for genre, genre_id in genres_ids.items():
        # Loop para fazer as requisições por ano do intervalo de ano proposto
        for year in range(start_year, final_year + 1):
            # Definindo os parametros com os filtros para realizar a requisição
            params = {
                "include_adult": "false",
                "include_video": "false",
                "language": "en-US",
                "primary_release_date.gte": f"{year}-01-01",
                "primary_release_date.lte": f"{year}-12-31",
                "sort_by": {sort_by},
                "vote_average.gte": {vote_average_gte},
                "vote_count.gte": {vote_count_gte},
                "with_genres": genre_id,  
                "page": 1 
            }
            
            # Lista para armazenar todos os dados das requisições
            all_movies_with_details = []
            continue_pagination = True

            # Loop para realizar requisição em todas as paginas
            while continue_pagination:
                # Realizando a solicitação para a API Discover
                response = requests.get(discover_url, headers=headers, params=params)
                # Verificando se a solicitação foi bem-sucedida
                if response.status_code == 200:
                    # Convertendo a resposta para JSON
                    movie_data = response.json()

                    # Loop para realizar resquest em details e credits do TMDB de cada filme para pegar o orçamento, pais de origem e os 5 atores principais e diretores de cada filme
                    for movie in movie_data['results']:
                        # Realizando request de detalhes dos filmes em cada filme
                        movie_id = movie['id']
                        movie_details_response = requests.get(f"{movie_url}{movie_id}", headers=headers)
                        # Realizando request de creditos dos filmes em cada filme
                        credits_response = requests.get(f"{movie_url}{movie_id}/credits", headers=headers)
                        # Verifica se as solicitações foram bem-sucedidas e converter em json os dados
                        if movie_details_response.status_code == 200 and credits_response.status_code == 200:
                            movie_details = movie_details_response.json()
                            credits = credits_response.json()
                            
                            # Filtrando apenas os 5 atores principais e os diretores       
                            actors = [
                                # Loop para filtrar no elenco apenas os 5 atores de 'credits'
                                member for member in credits.get('cast', [])
                                if member['known_for_department'] == 'Acting'
                            ][:5]
                            directors = [
                                # Loop para filtrar apenas os diretores de 'credits'
                                member for member in credits.get('crew', [])
                                if member['job'] == 'Director'
                            ]

                            # Removendo os campos indesejados de atores e diretores
                            fields_to_remove = ['known_for_department', 'profile_path', 'cast_id', 'credit_id', 'department', 'adult', 'original_name']
                            remove_unwanted_fields(actors, fields_to_remove)
                            remove_unwanted_fields(directors, fields_to_remove)

                            # Removendo os campos indesejados do filme
                            fields_to_remove_from_movie = ['adult', 'backdrop_path', 'original_title', 'overview', 'video']
                            remove_unwanted_fields([movie], fields_to_remove_from_movie)
                            
                            # Adicionando os campos de orçamento, imdb_id, pais de origem, 5 atores principais e diretores a lista filme do loop
                            movie['budget'] = movie_details.get('budget', 0)
                            movie['imdb_id'] = movie_details.get('imdb_id', '')
                            movie['origin_country'] = movie_details.get('origin_country', [])
                            movie['actors'] = actors
                            movie['directors'] = directors

                            # Adicionando para a lista do conjunto de todos os filmes apenas se o orçamento for maior que 0
                            if movie['budget'] > 0:
                                all_movies_with_details.append(movie)
                        else:
                            print(f"Erro ao obter detalhes ou créditos do filme {movie_id}: {movie_details_response.status_code}, {credits_response.status_code}")

                    # Retornando a página atual já percorrida
                    print(f'Página {params["page"]} de {movie_data["total_pages"]}')

                    # Verificando se há mais páginas para recuperar, caso exista adiciona mais um ao parametro 'page' e entra em loop novamente para fazer requisição de novas páginas 
                    if params['page'] < movie_data['total_pages']:
                        params['page'] += 1
                    # Caso não exista, o loop é parado
                    else:
                        continue_pagination = False
                else:
                    print(f"Erro na solicitação: {response.status_code}")
                    continue_pagination = False

            # Ordenando a lista com todos os filmes por ordem decrescente do orçamento
            all_movies_with_details = sorted(all_movies_with_details, key=lambda x: x['budget'], reverse=True)

            # Chamando função para armazenar os dados dos filmes em arquivos json para o ano e gênero atual
            save_data(genre, year, all_movies_with_details, bucket_name, storage_path_s3)

    print(f'Tamanho total dos arquivos carregados no bucket: {total_size_of_jsons_mb:.2f} MB')