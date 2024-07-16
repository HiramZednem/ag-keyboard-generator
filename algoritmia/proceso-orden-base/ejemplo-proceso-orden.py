dvorak_chars = ['\'', ',', '.', 'p', 'y', 'f', 'g', 'c', 'r', 'l',
                 'a', 'o', 'e', 'u', 'i', 'd', 'h', 't', 'n', 's',
                   '-', 'q', 'j', 'k', 'x', 'b', 'm', 'w', 'v', 'z']

orden = [17,15,13,11,19,20,12,14,16,18,7,5,3,1,9,10,2,4,6,8,27,25,23,21,29,30,22,24,26,28]

dvorak_chars_ordenados = [char for _, char in sorted(zip(orden, dvorak_chars))]
print(dvorak_chars_ordenados) 