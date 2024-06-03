# 📋 Etapas

## 1️⃣ Analise dos dados da planilha [google](/Sprint%203/Desafio/googleplaystore.csv)

- Primeiramente, foi realizado um estudo da base de dados enviada, olhando os dados das colunas e vendo os padrões que nela contiam, para fins de achar possiveis problemas para serem resolvidos

## 2️⃣ Tratamento de linha sem categoria

- Após a analise da base de dados, percebi que uma linha estava sem a categoria e estava pulanado as colunas, então adicionei a categoria 'Outro' nesta linha para não perder os dados que nela contiam
  <div style="text-align: center; padding: 10px;">
    <img src="/Sprint 3/Desafio/Evidencias/linha_sem_categoria.png" width="500" style="padding: 10px;">
  </div>

## 3️⃣ Tratamento de linhas duplicadas

- Ao análisar a base de dados, também percebi que muitas linhas estavam dúplicadas e algumas estavam variando apenas a coluna de reviews, então deixei apenas a linha que tinha o maior número de reviwes, em que lógicamente seria a última extração dos dados daquele aplicativo.
- Exemplo de algumas duplicações que tinham na base de dados:
  <div style="text-align: center; padding: 10px;">
    <img src="/Sprint 3/Desafio/Evidencias/exemplo_linha_duplicada.png" width="500" style="padding: 10px;">
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

## 4️⃣ Eliminação de caracteres em colunas contendo números e conversão para tipos primitivos

```
# Convertendo para int a coluna Installs, convertendo valores inválidos em NaN e removendo esses valores
dataset['Installs'] = pd.to_numeric(dataset['Installs'], errors='coerce')
dataset['Installs'] = dataset['Installs'].astype(int)

#Convertendo a coluna Price para float
dataset['Price'] = dataset['Price'].str.replace('$', '').astype(float)

#Retirando o caracter '_' das linhas de Category
dataset['Category'] = dataset['Category'].str.replace('_', ' ')
```

## 5️⃣ Criação do Script SQL `ModeloDimensional.sql`

- Ao executar o script, serão criadas _views_ das tabelas dimensões e a tabela fato, conforme mostrado no modelo dimensional. Essas _views_ serão criadas a partir do modelo relacional.
  [Modelo Dimensional SQL](ETAPA-III/ModeloDimensional.sql)

## 6️⃣ Criação do Script `Normalizando_ER_e_Dimensional.sql`

- Este script gera as tabelas do modelo relacional e as _views_ do modelo dimensional, tudo em um único script.
  [Normalizando ER e Dimensional SQL](ETAPA-III/Normalizando_ER_e_Dimencional.sql)

## 7️⃣ Criação do Script `Normalizando_e_Inserindo_dados_tb_locacao.sql`

- Este script gera as tabelas do modelo relacional, insere os dados de `tb_locacao` e gera as _views_ do modelo dimensional, tudo em um único script.

  ⚠️ **Obs.:** Este script só pode ser executado dentro da conexão com o banco `concessionaria.sqlite`.
  [Normalizando e Inserindo Dados SQL](ETAPA-III/Normalizando_e_Inserindo_dados_tb_locacao.sql)
