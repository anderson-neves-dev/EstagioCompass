# 📋 Etapas

## 1️⃣ Analise dos dados da base de dados [googleplaystore.csv](/Sprint%203/Desafio/googleplaystore.csv)

- Primeiramente, foi realizado um estudo da base de dados enviada, olhando os dados das colunas e vendo os padrões que nela contiam, para fins de achar possiveis problemas para serem resolvidos

## 2️⃣ Importação das bibliotecas pandas, matplotlib e leitura da base de dados

```
# Importação da biblioteca pandas e matplotlib
import pandas as pd
import matplotlib.pyplot as plt

# Leitura do arquivo googleplaystore.CSV
dataset = pd.read_csv('googleplaystore.csv')
```

## 3️⃣ Tratamento de linha sem categoria

- Após a analise da base de dados, percebi que uma linha estava sem a categoria e estava pulanado as colunas, então adicionei a categoria 'Outro' nesta linha para não perder os dados que nela contiam
  <div style="text-align: center; padding: 10px;">
    <img src="/Sprint 3/Desafio/Evidencias/linha_sem_categoria.png" width="100%" style="padding: 10px;">
  </div>

## 4️⃣ Tratamento de linhas duplicadas

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

## 5️⃣ Eliminação de caracteres e conversão para tipos primitivos

```
# Convertendo para int a coluna Installs, convertendo valores inválidos em NaN e removendo esses valores
dataset['Installs'] = pd.to_numeric(dataset['Installs'], errors='coerce')
dataset['Installs'] = dataset['Installs'].astype(int)

#Convertendo a coluna Price para float
dataset['Price'] = dataset['Price'].str.replace('$', '').astype(float)

#Retirando o caracter '_' das linhas de Category
dataset['Category'] = dataset['Category'].str.replace('_', ' ')
```

## 6️⃣ Query para pegar os 5 apps mais instalados e criação do gráfico de barras

⚠️ **Obs.:** Como os tiveram mais de 5 aplicativos com o mesmo número de instalação (a play store arredonda esses números) foi utilizado o critério de desempate o número de visualização dos apps

- Código:

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

## 7️⃣ Query para pegar a frequência de aplicativos por categoria e criação do gráfico de pizza

- Código:

```
# Contando a frequencia de cada categoria
frequency_apps_by_category = dataset['Category'].value_counts()
```

-Como tiveram muitos dados para o gráfico de pizza utilizei o parametro 'explode' para organizar as categorias que tiveram pouca quantidade de apps

```
#Adicionando explode diferentes para quantidades variadas para fins de legibilidade
explode = []
for count in frequency_apps_by_category:
    if count > 300:
        explode.append(0.01)
    elif count >50:
        explode.append(0.2)
    else:
        explode.append(0.6)

#Configurando o gráfico de pizza
plt.figure(figsize=(16, 12))
plt.pie(
    frequency_apps_by_category,
    explode=explode,
    labels=frequency_apps_by_category.index,
    labeldistance= 1.07,
    autopct='%1.1f%%',
    pctdistance=0.94,
    startangle=27,
)
plt.title('Frequência de Aplicativos por Categoria',fontsize=16)
plt.axis('equal')

#Adicionando legenda e ajustando sua posição com loc e bbox_to_anchor
plt.legend( frequency_apps_by_category.index, title="Categorias", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

plt.show()
```

- Gráfico gerado:
  <div style="text-align: center; padding: 10px;">
    <img src="/Sprint 3/Desafio/Evidencias/frequencia_de_apps_por_categoria.png" width="100%" style="padding: 10px;">
  </div>

## 8️⃣ Query para selecionar o aplicativo mais caro do dataset e organizar os dados em caixa de texto

- Código:

```
# Selecionando o aplicativo mais caro
most_expensive_app = dataset.loc[dataset['Price'].idxmax()]

# Configurando a figura
fig, ax = plt.subplots(figsize=(6, 4))

# Removendo os eixos e deixando só o card
ax.axis('off')

plt.title('Aplicativo mais caro', fontsize=16, weight='bold')

# Adicionando informações do app com maior preço
texto = (
    f"App mais caro\n\n"
    f"App: {most_expensive_app['App']}\n"
    f"Categoria: {most_expensive_app['Category']}\n"
    f"Preço: ${most_expensive_app['Price']:.2f}"
)


# Adicionando texto ao card e estilizando as cores, bordas e padding
plt.text(0.5, 0.5, texto, fontsize=16, color='#6DD08E', va='center', ha='center', bbox=dict(
    facecolor='#232323',
    edgecolor='#6DD08E',
    boxstyle='round, pad=2',
    alpha=0.9,
))


plt.show()
```

- Resultado:
  <div style="text-align: center; padding: 10px;">
    <img src="/Sprint 3/Desafio/Evidencias/app_mais_caro.png" width="100%" style="padding: 10px;">
  </div>

## 9️⃣ Query para contagem de apps com classificação `Mature 17+` e organizar os dados em caixa de texto

- Código:

```
# Selecionando apenas apps com classificação 'Mature 17+'
mature_17_apps = dataset[dataset['Content Rating'] == 'Mature 17+']
# Realizando a contagem da quantidade de aplicativos com classificação 'Mature 17+'
count_mature_17_apps = mature_17_apps['Content Rating'].value_counts().get('Mature 17+', 0)

# Configurando a figura
fig, ax = plt.subplots(figsize=(6, 4))

# Removendo os eixos e deixando só o card
ax.axis('off')

# Adicionando título
plt.title('Contagem de Apps com Classificação Mature 17+', fontsize=16, weight='bold')

# Adicionando informações da contagem dos apps com classificação 'Mature 17+'
texto = (
    f"Apps classicados como Mature 17+ \nTotal:  {count_mature_17_apps}"
)

# Adicionando texto ao card e estilizando as cores, bordas e padding
plt.text(0.5, 0.5, texto, fontsize=16, color='#6DD08E', va='center', ha='center', bbox=dict(
    facecolor='#232323',
    edgecolor='#6DD08E',
    boxstyle='round, pad=2',
    alpha=0.9,
))
plt.show()
```

- Resultado:
  <div style="text-align: center; padding: 10px;">
    <img src="/Sprint 3/Desafio/Evidencias/qtd_apps_mature_17.png" width="100%" style="padding: 10px;">
  </div>

## 🔟 Query para `Top 10 apps mais visualizados`

- Código:

```
# Criando um dataFrame para armenar apenas os aplicativos pagos
paid_apps = dataset.loc[df['Type'] == 'Paid']

# Selecionando os 5 apps com mais visualizações
top_5_apps_paid = paid_apps.sort_values(['Reviews'], ascending=False, inplace=False).head(5)

# Selecionado apenas as colunas Apps, Reviews e Category
top_5_apps_paid = top_5_apps_paid[['App', 'Reviews', 'Category']].reset_index(drop=True)

# Criando a coluna de ranking com 1°, 2°, 3°...
ranking = [f"{i}°" for i in range(1, 6)]

# Adicionando a coluna de ranking ao DataFrame
top_5_apps_paid.insert(0, 'Ranking', ranking)

# Estilizando o DataFrame para centralizar o conteúdo
top_5_apps_paid = top_5_apps_paid.style.set_table_styles(
    [{'selector': 'td', 'props': [('text-align', 'left')]},
     {'selector': 'th', 'props': [('text-align', 'left')]}]
).set_properties(**{'text-align': 'left'}).hide(axis='index')

# Exibi o dataFrame
display(top_5_apps_paid)
```

- Resultado obtido:
<div style="text-align: center; padding: 10px;">
  <img src="/Sprint 3/Desafio/Evidencias/ranking_apps_mais_visualizados.png" width="100%" style="padding: 10px;">
</div>

## 1️⃣1️⃣ Query para `Top 5 Apps pagos com mais visualizações`

- Código:

```
# Criando um dataFrame para armenar apenas os aplicativos pagos
paid_apps = dataset.loc[df['Type'] == 'Paid']

# Selecionando os 5 apps com mais visualizações
top_5_apps_paid = paid_apps.sort_values(['Reviews'], ascending=False, inplace=False).head(5)

# Selecionado apenas as colunas Apps, Reviews e Category
top_5_apps_paid = top_5_apps_paid[['App', 'Reviews', 'Category']].reset_index(drop=True)

# Criando a coluna de ranking com 1°, 2°, 3°...
ranking = [f"{i}°" for i in range(1, 6)]

# Adicionando a coluna de ranking ao DataFrame
top_5_apps_paid.insert(0, 'Ranking', ranking)

# Estilizando o DataFrame para centralizar o conteúdo
top_5_apps_paid = top_5_apps_paid.style.set_table_styles(
    [{'selector': 'td', 'props': [('text-align', 'left')]},
     {'selector': 'th', 'props': [('text-align', 'left')]}]
).set_properties(**{'text-align': 'left'}).hide(axis='index')

# Exibi o dataFrame
display(top_5_apps_paid)
```

- Resultado obtido:
<div style="text-align: center; padding: 10px;">
  <img src="/Sprint 3/Desafio/Evidencias/top_5_apps_pagos_mais_Instalados.png" width="100%" style="padding: 10px;">
</div>

## 1️⃣2️⃣ Query para `App pago com melhor avaliação e o mais instalado`

- Código:

```
# Ordenando aplicativos pagos pelos valores das colunas 'Rating' e 'Installs' em ordem decrescente
best_rated_and_viewed_apps = paid_apps.sort_values(['Rating', 'Installs'], ascending=False, inplace=False)

# Selecionar apenas as colunas 'App', 'Installs' e 'Rating', retirando o índice e pegando apenas o primeiro
best_rated_and_viewed_apps = best_rated_and_viewed_apps[['App', 'Installs', 'Rating']].reset_index(drop=True).head(1)

# Criando a figura e os eixos
fig, ax = plt.subplots(figsize=(4,4))

# Removendo os eixos
ax.axis('off')

# Adicionando título
plt.title('Aplicativo pago com melhor avaliação e o mais instalado', fontsize=16)

# Adicionando informações do app com maior preço
texto = (
   f"App pago melhor avaliado e o mais instalado\n\n"
   f"App: {best_rated_and_viewed_apps.loc[0, 'App']}\n"
   f"Avaliação: {best_rated_and_viewed_apps.loc[0, 'Rating']}\n"
   f"Downloads: {best_rated_and_viewed_apps.loc[0, 'Installs']:,}"
)

# Adicionando texto ao card e estilizando as cores, bordas e padding
plt.text(0.5, 0.5, texto, fontsize=16, color='#6DD08E', va='center', ha='center', bbox=dict(
   facecolor='#232323',
   edgecolor='#6DD08E',
   boxstyle='round, pad=2',
   alpha=0.9,
))

plt.show()
```

- Resultado obtido:
 <div style="text-align: center; padding: 10px;">
  <img src="/Sprint 3/Desafio/Evidencias/App_Pago_melhor_avaliado_e_visualizado.png" width="100%" style="padding: 10px;">
</div>

## 1️⃣3️⃣ Query para `Quantidade de preços de apps pagos` e gerar gráfico modelo dispersão

- Código:

```
# Realizando a soma das quantidades de preços de apps pagos
price_frequency = paid_apps['Price'].value_counts()

# Criando uma array para mudar o tamanho dos pontos que aparecem no gráfico de acordo a sua quantidade
point_size = []
for count in price_frequency:
        point_size.append(count+100)

# Criando a figura, os eixos e colocando uma cor de fundo
fig, ax = plt.subplots(figsize=(8, 5))
ax.set_facecolor('#232321')

# Adicionando títulos, rótulos, grid e customizando as cores de fundo
plt.title('Frequência de preços de apps pagos', fontsize=20)
plt.xlabel('Preço ($)', fontsize=13)
plt.ylabel('Quantidade', fontsize=13)
plt.grid(True, color='#203f1f')

# Criando gráfico dispersão
plt.scatter(price_frequency.index, price_frequency, s=point_size , color='#6DD08E')
plt.show()
```

- Gráfico obtido:
 <div style="text-align: center; padding: 10px;">
  <img src="/Sprint 3/Desafio/Evidencias/frequencia_de_precos.png" width="100%" style="padding: 10px;">
</div>

## 1️⃣4️⃣ Query para `Numero de últimas atualizações por Mês e Ano` e criação e gráfico de linha

- Código:

```
#Conversão da coluna 'Last Update' para o tipo date
dataset['Last Updated'] = pd.to_datetime(dataset['Last Updated'], errors='coerce')

# Criando coluna com apenas ano de ultima atualização
dataset['Last Updated Year'] = dataset['Last Updated'].dt.year

# Criando coluna com apenas mes de ultima atualização
dataset['Last Updated Month'] = dataset['Last Updated'].dt.month

# Agrupando os dados por ano e mes e fazendo a conta de quantos aplicativos aparecem e adicionando a um dataFRame
month_and_year_grouped = dataset.groupby(['Last Updated Year', 'Last Updated Month']).size().reset_index(name='Counts')

#Criando a coluna de mes e ano no dataFrame
month_and_year_grouped['YearMonth'] = month_and_year_grouped['Last Updated Year'].astype(str) + '-' + grouped['Last Updated Month'].astype(str).str.zfill(2)

#Criando figura, gráfico de linha, titulos e rotulos e suas estilizações para ficar mais legível
fig, ax = plt.subplots(figsize=(26, 10))
ax.set_facecolor('#232321')
plt.plot(month_and_year_grouped['YearMonth'], month_and_year_grouped['Counts'], marker='o', color='#6DD08E', linestyle='-')
plt.title('Número de ultimas atualizações por Mês e Ano', fontsize=16)
plt.xlabel('Ano-Mês', fontsize=16)
plt.ylabel('Número de Atualizações',fontsize=16)
plt.grid(True, color='#20581f')
plt.ylim(top = 2500)
plt.xticks(rotation=80, fontsize= 14)
plt.show()
```
# 🐍 Código completo em `jupyter`
[desafio.ipynb](desafio.ipynb)
