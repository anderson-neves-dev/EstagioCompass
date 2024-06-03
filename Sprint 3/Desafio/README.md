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

## 7️⃣ Query para selecionar o aplicativo mais caro do dataset e organizar os dados em caixa de texto

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

## 7️⃣ Query para contagem de apps com classificação `Mature 17+` e organizar os dados em caixa de texto

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
