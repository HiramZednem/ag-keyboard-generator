import random
import PyPDF2
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk


qwerty_chars = [ 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
                 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';',
                 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '-']

colemak_chars = [ 'q', 'w', 'f', 'p', 'g', 'j', 'l', 'u', 'y', ';', 
                  'a','r', 's', 't', 'd', 'h', 'n', 'e', 'i', 'o', 
                  'z', 'x', 'c', 'v', 'b', 'k', 'm', ',', '.', '-']

dvorak_chars = ['\'', ',', '.', 'p', 'y', 'f', 'g', 'c', 'r', 'l',
                 'a', 'o', 'e', 'u', 'i', 'd', 'h', 't', 'n', 's',
                   '-', 'q', 'j', 'k', 'x', 'b', 'm', 'w', 'v', 'z']

def get_values():
    global pobInicial, pobMaxima, generaciones, probReproduccion, probMutacion, probMutacionGen, distro_inicial, pdf_path
    pobInicial = int(pobInicial_entry.get())
    pobMaxima = int(pobMaxima_entry.get())
    generaciones = int(generaciones_entry.get())
    probReproduccion = float(probReproduccion_entry.get())
    probMutacion = float(probMutacion_entry.get())
    probMutacionGen = float(probMutacionGen_entry.get())
    
    layout = layout_combo.get()
    if layout == "Qwerty":
        distro_inicial = qwerty_chars
    elif layout == "Dvorak":
        distro_inicial = dvorak_chars
    elif layout == "Colemak":
        distro_inicial = colemak_chars
    
    libro = libro_combo.get()
    if libro == "go":
        pdf_path = "./libros/go.pdf"
    elif libro == "java":
        pdf_path = "./libros/java.pdf"
    elif libro == "js":
        pdf_path = "./libros/js.pdf"
    elif libro == "r":
        pdf_path = "./libros/r.pdf"

    root.destroy()
    
root = tk.Tk()
root.title("Parameter Values")

# Labels
pobInicial_label = ttk.Label(root, text="pobInicial:")
pobMaxima_label = ttk.Label(root, text="pobMaxima:")
generaciones_label = ttk.Label(root, text="generaciones:")
probReproduccion_label = ttk.Label(root, text="probReproduccion:")
probMutacion_label = ttk.Label(root, text="probMutacion:")
probMutacionGen_label = ttk.Label(root, text="probMutacionGen:")

pobInicial_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
pobMaxima_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
generaciones_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
probReproduccion_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
probMutacion_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
probMutacionGen_label.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)

# Entry fields
pobInicial_entry = ttk.Entry(root)
pobMaxima_entry = ttk.Entry(root)
generaciones_entry = ttk.Entry(root)
probReproduccion_entry = ttk.Entry(root)
probMutacion_entry = ttk.Entry(root)
probMutacionGen_entry = ttk.Entry(root)

pobInicial_entry.insert(0, "10")
pobMaxima_entry.insert(0, "30")
generaciones_entry.insert(0, "10")
probReproduccion_entry.insert(0, "0.5")
probMutacion_entry.insert(0, "0.8")
probMutacionGen_entry.insert(0, "0.5")

pobInicial_entry.grid(row=0, column=1, padx=5, pady=5)
pobMaxima_entry.grid(row=1, column=1, padx=5, pady=5)
generaciones_entry.grid(row=2, column=1, padx=5, pady=5)
probReproduccion_entry.grid(row=3, column=1, padx=5, pady=5)
probMutacion_entry.grid(row=4, column=1, padx=5, pady=5)
probMutacionGen_entry.grid(row=5, column=1, padx=5, pady=5)


layout_label = ttk.Label(root, text="Layout Origen:")
layout_combo = ttk.Combobox(root, values=["Qwerty", "Dvorak", "Colemak"])
layout_label.grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
layout_combo.grid(row=6, column=1, padx=5, pady=5)
layout_combo.current(0)

libro_label = ttk.Label(root, text="Layout Libro:")
libro_combo = ttk.Combobox(root, values=["go", "java", "js", "r"])
libro_label.grid(row=7, column=0, padx=5, pady=5, sticky=tk.W)
libro_combo.grid(row=7, column=1, padx=5, pady=5)
libro_combo.current(1)

# Button
submit_button = ttk.Button(root, text="Submit", command=get_values)
submit_button.grid(row=14, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
























# Keyboards layout:


# Variables configuración:
orden = [17,15,13,11,19,20,12,14,16,18,7,5,3,1,9,10,2,4,6,8,27,25,23,21,29,30,22,24,26,28]

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
    layoutDeseadoLibro = leerLibro() # regresa mayor a menor
    layoutDeseadoLibro = [char for char in layoutDeseadoLibro if char in layoutOrigen] # deja los que esten en comun (tema simbolos)

    # esta es la clave del algoritmo, se ordena segun la carga de trabajo balanceada y de una manera separada
    layoutDeseadoLibro = [char for _, char in sorted(zip(orden, layoutDeseadoLibro))] # mas info en proceso-orden-base

    poblacion = generarPoblacion(layoutOrigen)

    for i in range(generaciones):
        print(f'Generacion {i}')
        hijos = reproducir(poblacion)
        hijosMutados = mutar(hijos)

        poblacion = poblacion + hijosMutados

        evolucionAptitud(poblacion)

        poblacion = podar(poblacion)
        
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
            elif individuo[i] == layoutDeseadoLibro[i]:
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

def obtenerPosiciones(individuo):
    posMejor = []
    posOrigen = []
    posLibro = []
    for i in range(len(individuo)):
        if individuo[i] == layoutOrigen[i]:
            posOrigen.append(i)
            posMejor.append(i)
        elif individuo[i] == layoutDeseadoLibro[i]:
            posLibro.append(i)
            posMejor.append(i)
    return posMejor, posOrigen, posLibro
    
def graficar(poblacion):
    plt.plot(mejores, label='Mejores')
    plt.plot(peores, label='Peores')
    plt.plot(media, label='Media')
    plt.legend(['Mejores', 'Peores', 'Media'])
    plt.xlabel('Generaciones')
    plt.ylabel('Aptitud')
    plt.title('Evaluación de aptitud')

    distroI = ""
    if layoutOrigen == qwerty_chars:
        distroI = "Qwerty"
    elif layoutOrigen == colemak_chars:
        distroI = "Colemak"
    elif layoutOrigen == dvorak_chars:
        distroI = "Dvorak"

    posMejor, posOrigen, posLibro = obtenerPosiciones(poblacion[0])

    data = {
        'Distro Inicial': distroI,
        'Libro': pdf_path,
        'Letras Origen': len(posOrigen),
        'Letras Libro': len(posLibro), 
        'Total': len(posMejor)
    }
    cellText = [list(data.values())]
    colLabels = list(data.keys())
    fig, ax = plt.subplots(figsize=(12, 2))  # Increase the figure size
    ax.axis('off')
    table = ax.table(cellText=cellText, colLabels=colLabels, loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 1.2)
    ax.set_title('Detalles de configuración') 

    
    # MEJOR CONFIGURACION
    fig, ax2 = plt.subplots(3, 10, figsize=(6, 4))
    for i, char in enumerate(poblacion[0]):
        row = i // 10
        col = i % 10
        if i in posOrigen:
            ax2[row, col].text(0.5, 0.5, char, fontsize=14, ha='center', color='orange')
        elif i in posLibro:
            ax2[row, col].text(0.5, 0.5, char, fontsize=14, ha='center', color='blue')
        else: 
            ax2[row, col].text(0.5, 0.5, char, fontsize=14, ha='center')
    for ax_row in ax2:
        for ax_cell in ax_row:
            ax_cell.axis('off')
    fig.suptitle("Mejor configuración")

    # DISTRO ORIGEN
    fig2, ax3 = plt.subplots(3, 10, figsize=(6, 4))
    for i, char in enumerate(distro_inicial):
        row = i // 10
        col = i % 10
        if i in posOrigen:
            ax3[row, col].text(0.5, 0.5, char, fontsize=14, ha='center', color='orange')
        else:
            ax3[row, col].text(0.5, 0.5, char, fontsize=14, ha='center')
    for ax_row in ax3:
        for ax_cell in ax_row:
            ax_cell.axis('off')
    fig2.suptitle("Distro origen")

    # DISTRO ORIGEN
    fig3, ax4 = plt.subplots(3, 10, figsize=(6, 4))
    for i, char in enumerate(layoutDeseadoLibro):
        row = i // 10
        col = i % 10
        if i in posLibro:
            ax4[row, col].text(0.5, 0.5, char, fontsize=14, ha='center', color='blue')
        else:
            ax4[row, col].text(0.5, 0.5, char, fontsize=14, ha='center')
    for ax_row in ax4:
        for ax_cell in ax_row:
            ax_cell.axis('off')
    fig3.suptitle("Distro libro")


    plt.subplots_adjust(wspace=0.1, hspace=0.1)
    plt.show()    

main()