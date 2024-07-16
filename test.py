import matplotlib.pyplot as plt

# Caracteres qwerty en un arreglo 3x10
qwerty_chars = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
                'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ñ',
                'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '-']

# Crear la figura y los subplots
fig, ax = plt.subplots(3, 10, figsize=(12, 6))

# Iterar sobre los caracteres y asignarlos a los subplots
for i, char in enumerate(qwerty_chars):
    row = i // 10
    col = i % 10
    ax[row, col].text(0.5, 0.5, char, fontsize=14, ha='center')

# Eliminar los ejes para que parezca un teclado
for ax_row in ax:
    for ax_cell in ax_row:
        ax_cell.axis('off')

# Ajustar el espacio entre subplots
plt.subplots_adjust(wspace=0.1, hspace=0.1)

# Agregar título al gráfico
plt.title("Teclado QWERTY")

# Mostrar el gráfico
plt.show()