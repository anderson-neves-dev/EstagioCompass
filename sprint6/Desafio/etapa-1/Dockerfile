# Comando para criar uma imagem python versão 3.9 (a mais atual)
FROM python:3.9

# Instalando boto3 e o dotenv
RUN pip install boto3 
RUN pip install python-dotenv

# Criando o diretório de trabalho no container onde vão ficar os dados
WORKDIR /app

# Copiando oscript Python que faz o uload dos arquivos e o arquivo .env com as variáveis de ambiente para o diretório de trabalho
COPY index.py /app/index.py
COPY .env /app/.env

# Executando o código python para fazer upload dos arquivos no container
CMD ["python", "index.py"]
