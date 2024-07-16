import random
import PyPDF2
from collections import Counter

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
pdf_path = "./libros/go.pdf"


# random_chars = random.sample(qwerty_chars, 30) 
# print("random_chars: ", len(random_chars)) 
# print(random_chars)

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
    
    # Extraer texto del PDF
    text = extract_text_from_pdf(pdf_path)

    # Contar caracteres
    character_count = count_characters(text)

    # Ordenar caracteres por frecuencia
    sorted_characters = sort_characters_by_frequency(character_count)

    # Guardar los caracteres en un arreglo en el orden que vienen
    characters = [item['char'] for item in sorted_characters]

    characters.remove(' ')
    
    return characters[:30]


def configurar_distro():
    return [char for _, char in sorted(zip(orden, distro_inicial))]




def main():
    deseadoLibro = leerLibro()
    layout = configurar_distro()
    
    

main()