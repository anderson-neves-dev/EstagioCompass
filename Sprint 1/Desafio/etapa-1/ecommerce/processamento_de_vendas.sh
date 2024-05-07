#!/bin/bash
#Criar o diretorio vendas
mkdir vendas

#Copiar dados_de_vendas.csv pra dentro de vendas
cp dados_de_vendas.csv vendas

#Criar o diretorio de backup dentro de vendas
mkdir -p vendas/backup
cd vendas
#copiar o arquivo de dados_de_vendas.csv para dentro de backup mudando o começo do seu nome para a data atual 

#Copiar o arquivo dados_de_vendas.csv para o subbdiretorio backup mudando o seu nome para dados-data.csv
data=$(date "+%Y%m%d") 
cp dados_de_vendas.csv backup/dados-$data.csv
cd backup 

#renomerar o aquivo para backup-dados-data.csv
mv dados-$data.csv backup-dados-$data.csv

#Criando o aquivo relatorio dentro de backup
{
echo "##################################################################"
echo "Data do sistema: $(date "+%Y/%m/%d %H:%M")"
echo "Data do primeiro registro de venda: "
awk -F',' 'NR==2{print $5}' ../dados_de_vendas.csv
echo "Data do ultimo registro de venda: "
awk -F',' 'END{print $5}' ../dados_de_vendas.csv
echo "Quantidade total de itens diferentes vendidos: "
awk -F ',' 'NR > 1 {print $2}' ../dados_de_vendas.csv | sort | uniq | wc -l
echo "As 10 primeiras linhas do arquivo: "
} > relatorio-$data.txt
echo "As 10 primeiras linhas do arquivo: "
head -n 10 backup-dados-$data.csv | tee -a relatorio-$data.txt

#Comprimindo o arquivo
zip backup-dados-$data.zip backup-dados-$data.csv

#Apagando os arquivos de vendas
rm backup-dados-$data.csv
rm ../dados_de_vendas.csv

