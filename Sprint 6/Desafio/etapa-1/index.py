import boto3
import os
from datetime import datetime
from dotenv import load_dotenv

# Importando o arquivo .env que tem as variáveis de ambiente com os dados de login root
load_dotenv('/app/.env')

# Pegando o ano, mes e dia do dia do upload com datetime().now
ano = datetime.now().year
mes = datetime.now().month
dia = datetime.now().day

#Criando as variveis com o caminho onde vai ficar os arquivos
caminho_movies = f"Raw/File/CSV/Movies/{ano}/{mes}/{dia}/movies.csv"
caminho_series = f"Raw/File/CSV/Series/{ano}/{mes}/{dia}/series.csv"

#Nome do bucket 
bucket_S3 = 'desafio-final-filmes-e-series-anderson-neves'
#caminho dos arquivos no volume do container que vão fazer upload 
caminho_arquivo_series = '/data/series.csv'
caminho_arquivo_movies = '/data/movies.csv'

print(f"Tamanho do arquivo de series: {os.path.getsize(caminho_arquivo_series)} bytes")
print(f"Tamanho do arquivo de filmes: {os.path.getsize(caminho_arquivo_movies)} bytes")

#Criando o client da aws utilizando o boto3 com as credencias vindas do arquivo .env que está no container
s3_client = boto3.client(
    's3',
    region_name='us-east-1',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    aws_session_token=os.getenv('AWS_SESSION_TOKEN'),
)

try:
    #Upload do arquivo de series
    s3_client.upload_file(caminho_arquivo_series, bucket_S3, caminho_series)
    print(f"Arquivo de series enviado com sucesso para o bucket {bucket_S3} para o caminho {caminho_series}.")

    #Upload do arquivo de filmes
    s3_client.upload_file(caminho_arquivo_movies, bucket_S3, caminho_movies)
    print(f"Arquivo de filme enviado com sucesso para o bucket {bucket_S3} para o caminho {caminho_movies}.")
except Exception as UploadError:
    print(f"Erro ao enviar o arquivo: {UploadError}")
