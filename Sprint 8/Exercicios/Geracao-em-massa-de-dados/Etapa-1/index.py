import random

# Declarando e inicializando uma lista com 250 inteiros aleatórios entre 0 a 500
lista = [random.randint(0, 500) for i in range(250)]

# Invertendo a lista
lista.reverse()

# Imprimindo a lista invertida
print(lista)
