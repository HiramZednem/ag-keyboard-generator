import PyPDF2
from collections import Counter

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

# Ruta del archivo PDF
pdf_path = "./libros/go.pdf"

# Extraer texto del PDF
text = extract_text_from_pdf(pdf_path)

# Contar caracteres
character_count = count_characters(text)

# Ordenar caracteres por frecuencia
sorted_characters = sort_characters_by_frequency(character_count)

# Imprimir el resultado
for item in sorted_characters:
    print(item)