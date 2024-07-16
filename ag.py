import pandas as pd
import numpy as np
import random
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt

def get_values():
    global pobInicial, pobMaxima, generaciones, probReproduccion, probMutacion, probMutacionGen
    pobInicial = int(pobInicial_entry.get())
    pobMaxima = int(pobMaxima_entry.get())
    generaciones = int(generaciones_entry.get())
    probReproduccion = float(probReproduccion_entry.get())
    probMutacion = float(probMutacion_entry.get())
    probMutacionGen = float(probMutacionGen_entry.get())
    
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

# Button
submit_button = ttk.Button(root, text="Submit", command=get_values)
submit_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()

# Leer el dataset desde el archivo CSV
data = pd.read_csv('raw_data.csv')
x = data.iloc[:, :-1].values # Selecciona todos las columnas menos la última -> [['123','123','123','123'],[...]]
y = data.iloc[:, -1].values # Selecciona la última columna -> ['123','123','123','123']
'''
    En el codigo viene hardcodeado la formula para sacar la aptitud de un individuo
    Formula:
    x[0] + 1*x[1] + 2*x[2] + 3*x[3] + 4*x[4] = 0

    Por tanto, si en el dataset, columnas_x <> 4 , el codigo no va a funcionar
'''

mejores = []
media = []
peores = []

def main():
    poblacion = generarPoblacion(pobInicial)

    for i in range(generaciones):
        print(f'Generacion {i}')
        hijos = reproducir(poblacion)
        hijosMutados = mutar(hijos)
        poblacion = poblacion.tolist() + hijosMutados

        evolucionAptitud(poblacion);

        poblacion = podar(poblacion)

    graficar(poblacion)

def generarPoblacion(pobInicial): 
    return np.random.randint(0, 11, (pobInicial, x.shape[1] + 1)) # Genera un arreglo de valores enteros aleatorios de 0 a 10 de la longitud de las columnas de x

def reproducir(poblacion):
    # Formacion de parejas
    # Estrategia A1: (100 %) para cada individuo, generar un número aleatorio m entre [0, n], m
    # representa la cantidad de individuos que se cruzarán con el individuo en cuestión, luego se
    # tienen que generar m números aleatorios que harán referencia a los individuos con que se
    # cruzarán. Se puede omitir que sea pareja de sí mismo. n <= Tamaño máximo de la
    # población y es un parámetro.
    poblacion = poblacion.tolist()
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

    hijo1 = np.concatenate((individuo1[:puntoCruza], individuo2[puntoCruza:])).astype(int)
    hijo2 = np.concatenate((individuo2[:puntoCruza], individuo1[puntoCruza:])).astype(int)
    return hijo1, hijo2

def mutar(hijos):
    # Estrategia Propia: Por cada individuo, se recorre cada x y se decide si mutar o no,
    # si se decide mutar, se le suma o resta un valor aleatorio entre -1 y 1
    hijos = hijos.tolist()
    for individuo in hijos:
        if random.random() < probMutacion:
            # individuo = [1,2,3,4]
            for i in range(len(individuo)):
                if random.random() < probMutacionGen:
                    individuo[i] = individuo[i] + random.choice([-1, 1]) # Para realizar la mutacion le voy a restar uno o sumar uno aleatoriamente
    return hijos

def obtenerAptitud(poblacion):
    ''' 
        Aqui es donde esta la magia
        Necesito calcular el valor de y de mi individuo.
        Se debe de evaluar el individuo con el dataset de y.
        Por cada valor de y, apendare a un arreglo de errores el valor de y - y_individuo
        utilizare np.linalg.norm sobre el arreglo para calcular el fitness
        busco minimizar y que la longuitud de ese vector sea 0
        https://www.youtube.com/watch?v=qAXsB3CYdBY 
    '''
    aptitudes = []
    for individuo in poblacion:
        errores = []
        
        for i, yd in enumerate(y):
            xd = x[i]
            y_individuo = individuo[0] + xd[0]*individuo[1] + xd[1]*individuo[2] + xd[2]*individuo[3] + xd[3]*individuo[4]
            errores.append(yd - y_individuo)
        fitness = np.linalg.norm(errores)
        aptitudes.append(fitness)
    return aptitudes

def evolucionAptitud(poblacion):
    aptitudes = obtenerAptitud(poblacion)
    _, aptitudes_ordenada = zip(*sorted(zip(poblacion, aptitudes), key=lambda x: x[1]))
    mejores.append(aptitudes_ordenada[0])
    peores.append(aptitudes_ordenada[-1])
    media.append(sum(aptitudes_ordenada) / len(aptitudes_ordenada))

def podar(poblacion):
    # Estrategia P1: (80 %) Mantener los mejores.
    poblacion = list(set(tuple(map(tuple, poblacion)))) # Elimina duplicados
    aptitudes = obtenerAptitud(poblacion)

    poblacion_ordenada, aptitudes_ordenada = zip(*sorted(zip(poblacion, aptitudes), key=lambda x: x[1]))

    return np.array(poblacion_ordenada[:pobMaxima])

def graficar(poblacion):
    plt.plot(mejores, label='Mejores')
    plt.plot(peores, label='Peores')
    plt.plot(media, label='Media')
    plt.legend(['Mejores', 'Peores', 'Media'])
    plt.xlabel('Generaciones')
    plt.ylabel('Aptitud')
    plt.title('Evaluación de aptitud')

    yc = []
    for i, yd in enumerate(y):
            individuo = poblacion[0]
            xd = x[i]
            y_individuo = individuo[0] + xd[0]*individuo[1] + xd[1]*individuo[2] + xd[2]*individuo[3] + xd[3]*individuo[4]
            yc.append(y_individuo) 

    plt.figure()
    plt.plot(y, label='yd', linewidth=3.0)
    plt.plot(yc, label='yc', linewidth=1.0)
    plt.legend(['yd', 'yc'])
    plt.xlabel('id muestra')
    plt.ylabel('Valor')
    plt.title('Evolución del Valor')

    aptitudes = obtenerAptitud(poblacion)
    poblacion_ordenada, aptitudes_ordenada = zip(*sorted(zip(poblacion, aptitudes), key=lambda x: x[1]))
    data = {
        'x0': poblacion_ordenada[0][0],
        'x1': poblacion_ordenada[0][1],
        'x2': poblacion_ordenada[0][2],
        'x3': poblacion_ordenada[0][3],
        'x4': poblacion_ordenada[0][4],
        'Aptitud': round(aptitudes_ordenada[0],2)
    }
    cellText = [list(data.values())]
    colLabels = list(data.keys())
    fig, ax = plt.subplots(figsize=(8, 4))  # Increase the figure size
    ax.axis('off')
    table = ax.table(cellText=cellText, colLabels=colLabels, loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 1.2)
    ax.set_title('Mejor Individuo') 

    plt.show()

main()

# print(obtenerAptitud([[3,1,2,6,7]]))