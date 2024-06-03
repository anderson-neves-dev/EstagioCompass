# 📋 Etapas

## 1️⃣ Analise dos dados da base de dados [googleplaystore.csv](/Sprint%203/Desafio/googleplaystore.csv)

- Primeiramente, foi realizado um estudo da base de dados enviada, olhando os dados das colunas e vendo os padrões que nela contiam, para fins de achar possiveis problemas para serem resolvidos

## 1️⃣ Importação das bibliotecas pandas, matplotlib e leitura da base de dados

```
# Importação da biblioteca pandas e matplotlib
import pandas as pd
import matplotlib.pyplot as plt

# Leitura do arquivo googleplaystore.CSV
dataset = pd.read_csv('googleplaystore.csv')
```

## 2️⃣ Tratamento de linha sem categoria

- Após a analise da base de dados, percebi que uma linha estava sem a categoria e estava pulanado as colunas, então adicionei a categoria 'Outro' nesta linha para não perder os dados que nela contiam
  <div style="text-align: center; padding: 10px;">
    <img src="/Sprint 3/Desafio/Evidencias/linha_sem_categoria.png" width="100%" style="padding: 10px;">
  </div>

## 3️⃣ Tratamento de linhas duplicadas

- Ao análisar a base de dados, também percebi que muitas linhas estavam dúplicadas e algumas estavam variando apenas a coluna de reviews, então deixei apenas a linha que tinha o maior número de reviwes, em que lógicamente seria a última extração dos dados daquele aplicativo.
- Exemplo de algumas duplicações que tinham na base de dados:
  <div style="text-align: center; padding: 10px;">
    <img src="/Sprint 3/Desafio/Evidencias/exemplo_linha_duplicada.png" width="100%" style="padding: 10px;">
  </div>
- Código de solução para o problema:

```
#Covertendo a coluna Reviews para number
dataset['Reviews'] = pd.to_numeric(dataset['Reviews'], errors='coerce')

#Colocando em menusculo todos os carcateres da coluna de App
dataset['App'] = dataset['App'].str.lower()

# Remover linhas duplicatas mantendo o maior valor de 'Reviews'
dataset = dataset.sort_values('Reviews', ascending=False).drop_duplicates(subset=['App'], keep='first')
```

## 4️⃣ Eliminação de caracteres e conversão para tipos primitivos

```
# Convertendo para int a coluna Installs, convertendo valores inválidos em NaN e removendo esses valores
dataset['Installs'] = pd.to_numeric(dataset['Installs'], errors='coerce')
dataset['Installs'] = dataset['Installs'].astype(int)

#Convertendo a coluna Price para float
dataset['Price'] = dataset['Price'].str.replace('$', '').astype(float)

#Retirando o caracter '_' das linhas de Category
dataset['Category'] = dataset['Category'].str.replace('_', ' ')
```

## 5️⃣ Query para pegar os 5 apps mais instalados e criação do gráfico de barras

⚠️ **Obs.:** Como os tiveram mais de 5 aplicativos com o mesmo número de instalação (a play store arredonda esses números) foi utilizado o critério de desempate o número de visualização dos apps

```
top_5_apps = dataset.sort_values(['Installs','Reviews'], ascending=False, inplace=False).head(5)

fig, ax = plt.subplots(figsize=(6, 8))

ax.set_facecolor('#232321')

#Configurações de gráfico de barra
plt.bar(top_5_apps['App'], top_5_apps['Installs'], color='#6DD08E')
plt.xlabel('Aplicativos', fontsize=12)
plt.ylabel('Instalações (Bilhões)', fontsize=12)
plt.title('Top 5 Aplicativos Mais Instalados na Google Play Store\n Obs.: Critério de desempate adotado foi por numeros de reviews', fontsize=16)
plt.xticks(rotation=30, ha='right')
plt.tight_layout()

# Exibição do gráfico
plt.show()
```

- Gráfico gerado:
  <div style="text-align: center; padding: 10px;">
    <img src="/Sprint 3/Desafio/Evidencias/top_5_apps_mais_Instalados.png" width="100%" style="padding: 10px;">
  </div>

## 6️⃣ Criação do Script `Normalizando_ER_e_Dimensional.sql`

- Este script gera as tabelas do modelo relacional e as _views_ do modelo dimensional, tudo em um único script.
  [Normalizando ER e Dimensional SQL](ETAPA-III/Normalizando_ER_e_Dimencional.sql)

## 7️⃣ Criação do Script `Normalizando_e_Inserindo_dados_tb_locacao.sql`

- Este script gera as tabelas do modelo relacional, insere os dados de `tb_locacao` e gera as _views_ do modelo dimensional, tudo em um único script.

  ⚠️ **Obs.:** Este script só pode ser executado dentro da conexão com o banco `concessionaria.sqlite`.
  [Normalizando e Inserindo Dados SQL](ETAPA-III/Normalizando_e_Inserindo_dados_tb_locacao.sql)
