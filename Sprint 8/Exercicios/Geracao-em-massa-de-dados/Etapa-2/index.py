import csv
# Declarando e inicializando uma lista com 20 nomes de animais
animais = [
    "cavalo", "búfalo", "galinha", "vaca", "cachorro",
    "gato", "elefante", "rato", "gato", "peixe",
    "zebra", "pato", "raposa", "crocodilo", "tartaruga",
    "pinguim", "cobra", "lobo", "camelo", "macaco"
]
# Ordenando a lista em ordem crescente
animais.sort()

# Iterando sobre a lista e imprimindo cada nome de animal
for animal in animais:
    print(animal)

# Armazenando o conteúdo da lista em um arquivo CSV
with open('Etapa-2/animais.csv', 'w') as arquivo:
    escritor = csv.writer(arquivo)
    for animal in animais:
        escritor.writerow([animal])
