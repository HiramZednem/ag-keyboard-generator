import random

# Keyboards layout:
qwerty_chars = [ 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
                 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ñ',
                 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '-']

random_chars = random.sample(qwerty_chars, 30) 
print("random_chars: ", len(random_chars)) 
print(random_chars)