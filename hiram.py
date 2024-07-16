import random
import PyPDF2
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt

# Keyboards layout:
qwerty_chars = [ 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
                 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ñ',
                 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '-']

colemak_chars = [ 'q', 'w', 'f', 'p', 'g', 'j', 'l', 'u', 'y', ';', 
                  'a','r', 's', 't', 'd', 'h', 'n', 'e', 'i', 'o', 
                  'z', 'x', 'c', 'v', 'b', 'k', 'm', ',', '.', '-']

dvorak_chars = ['\'', ',', '.', 'p', 'y', 'f', 'g', 'c', 'r', 'l',
                 'a', 'o', 'e', 'u', 'i', 'd', 'h', 't', 'n', 's',
                   '-', 'q', 'j', 'k', 'x', 'b', 'm', 'w', 'v', 'z']

# Variables configuración:
distro_inicial = dvorak_chars
orden = [17,15,13,11,19,20,12,14,16,18,7,5,3,1,9,10,2,4,6,8,27,25,23,21,29,30,22,24,26,28]
pdf_path = "./libros/java.pdf"

# Variable configuración AG:
pobInicial = 10
pobMaxima = 30
generaciones = 50
probReproduccion = 0.5
probMutacion = 0.8
probMutacionGen = 0.5

def leerLibro():
    def extract_text_from_pdf(pdf_path):
        text = ""
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in range(len(reader.pages)):
                text += reader.pages[page].extract_text()
        return text

    def count_characters(text):
        return Counter(text)

    def sort_characters_by_frequency(counter):
        sorted_characters = sorted(counter.items(), key=lambda item: item[1], reverse=True)
        return [{"char": char, "quantity": quantity} for char, quantity in sorted_characters]
    
    print("Leyendo libro...")
    # Extraer texto del PDF
    text = extract_text_from_pdf(pdf_path)

    # Contar caracteres
    character_count = count_characters(text)

    # Ordenar caracteres por frecuencia
    sorted_characters = sort_characters_by_frequency(character_count)

    # Guardar los caracteres en un arreglo en el orden que vienen
    characters = [item['char'] for item in sorted_characters]

    characters.remove(' ')
    
    return characters

     
mejores = []
media = []
peores = []

def main():
    global layoutOrigen, layoutDeseadoLibro
    layoutOrigen = distro_inicial
    layoutDeseadoLibro = leerLibro()
    layoutDeseadoLibro = [char for char in layoutDeseadoLibro if char in layoutOrigen]

    poblacion = generarPoblacion(layoutOrigen)

    for i in range(generaciones):
        print(f'Generacion {i}')
        hijos = reproducir(poblacion)
        hijosMutados = mutar(hijos)

        poblacion = poblacion + hijosMutados

        evolucionAptitud(poblacion)

        poblacion = podar(poblacion)
        
    print(poblacion)
    graficar(poblacion)

def generarPoblacion(layout): 
    return [random.sample(layout, 30) for _ in range(pobInicial)]

def reproducir(poblacion):
    # Formacion de parejas
    # Estrategia A1: (100 %) para cada individuo, generar un número aleatorio m entre [0, n], m
    # representa la cantidad de individuos que se cruzarán con el individuo en cuestión, luego se
    # tienen que generar m números aleatorios que harán referencia a los individuos con que se
    # cruzarán. Se puede omitir que sea pareja de sí mismo. n <= Tamaño máximo de la
    # población y es un parámetro.
    nuevaPoblacion = []
    for individuo in poblacion:
        m = random.randint(0, min(pobMaxima, len(poblacion)-1))
        parejas = random.sample(range(len(poblacion)), m) # Selecciona el index de m parejas aleatorias, en el rango existente de la poblacion
        parejas = [p for p in parejas if p != poblacion.index(individuo)] # Elimina la pareja de si mismo
        for pareja in parejas:
            hijo1, hijo2 = cruza(individuo, poblacion[pareja]) # itera al individuo con las parejas seleccionadas
            nuevaPoblacion.append(hijo1)
            nuevaPoblacion.append(hijo2)
    return np.array(nuevaPoblacion)

def cruza(individuo1, individuo2):
   # Estrategia C1: (90 %) Un punto de cruza aleatorio, para cada pareja a cruzar, de los
    # posibles puntos de cruza de los individuos se selecciona aleatoriamente la posición.
    puntoCruza = random.randint(0, len(individuo1))

    hijo1 = np.concatenate((individuo1[:puntoCruza], individuo2[puntoCruza:]))
    hijo2 = np.concatenate((individuo2[:puntoCruza], individuo1[puntoCruza:]))

    ## Verificar que no haya caracteres repetidos y agregar los faltantes
    hijo1 = list(set(hijo1))
    hijo2 = list(set(hijo2))

    faltantes_hijo1 = [char for char in individuo2 if char not in hijo1]
    faltantes_hijo2 = [char for char in individuo1 if char not in hijo2]

    hijo1.extend(faltantes_hijo1)
    hijo2.extend(faltantes_hijo2)

    return hijo1, hijo2

def mutar(hijos):
    # Estrategia Propia: Por cada individuo, se recorre cada letra y se decide si mutar o no,
    # si se decide mutar, se genera un número aleatorio y se intercambia la letra en la posición
    hijos = hijos.tolist()
    for individuo in hijos:
        if random.random() < probMutacion:
            # individuo = [1,2,3,4]
            for i in range(len(individuo)):
                if random.random() < probMutacionGen:
                    if random.random() < probMutacionGen:
                        random_index = random.randint(0, len(individuo)-2)
                        if random_index != i:
                            individuo[i], individuo[random_index] = individuo[random_index], individuo[i] # Intercambio de posición entre dos caracteres adyacentes
    return hijos

def obtenerAptitud(poblacion):
    '''
        Aqui es donde esta la magia, voy a ponerle puntos a cada individuo, voy a buscar maximizar.
        Un individuo se va a ganar un punto si su letra en su posicion i es igual a la posicion i del layoutOrigen
        ganara otro punto, si su letra tambien es igual a la i del layoutDeseadoLibro
    '''
    aptitudes = []
    for individuo in poblacion:
        fitness = 0
        for i in range(len(individuo)):
            if individuo[i] == layoutOrigen[i]:
                fitness += 1
            if individuo[i] == layoutDeseadoLibro[i]:
                fitness += 1
        aptitudes.append(fitness)
    return aptitudes

def evolucionAptitud(poblacion):
    aptitudes = obtenerAptitud(poblacion)
    _, aptitudes_ordenada = zip(*sorted(zip(poblacion, aptitudes), key=lambda x: x[1], reverse=True))

    mejores.append(aptitudes_ordenada[0])
    peores.append(aptitudes_ordenada[-1])
    media.append(sum(aptitudes_ordenada) / len(aptitudes_ordenada))

def podar(poblacion):
    # Estrategia P1: (80 %) Mantener los mejores.
    poblacion = list(set(tuple(map(tuple, poblacion)))) # Elimina duplicados
    aptitudes = obtenerAptitud(poblacion)

    poblacion_ordenada, aptitudes_ordenada = zip(*sorted(zip(poblacion, aptitudes), key=lambda x: x[1], reverse=True))

    return list(poblacion_ordenada[:pobMaxima])
    
def graficar(poblacion):
    plt.plot(mejores, label='Mejores')
    plt.plot(peores, label='Peores')
    plt.plot(media, label='Media')
    plt.legend(['Mejores', 'Peores', 'Media'])
    plt.xlabel('Generaciones')
    plt.ylabel('Aptitud')
    plt.title('Evaluación de aptitud')
    plt.show()    

main()