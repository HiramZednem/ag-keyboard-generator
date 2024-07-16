import random

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




# random_chars = random.sample(qwerty_chars, 30) 
# print("random_chars: ", len(random_chars)) 
# print(random_chars)

def configurar_distro():

    distro_ordenado = [char for _, char in sorted(zip(orden, distro_inicial))]
    print("Distro ordenado: ", distro_ordenado)
    return distro_ordenado



def main():
    configurar_distro()
    print("Hello, World!")

main()