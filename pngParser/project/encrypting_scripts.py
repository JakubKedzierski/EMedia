import zlib

import matplotlib.pyplot as plt
import numpy as np
from Crypto.Util import number
import png
import math

######################################################
###   Bloki jawne o długości 64bajtów, 
def encrypt_data(data,width, height,bytes_per_pixel):
    #print(data)
    bits = 260
    p, q = generate_p_and_q(bits)
    n = p * q
    euler = (p-1) * (q-1)
    e = 2**16 + 1

    while e >= euler or number.GCD(e,euler) != 1:
        e = number.getRandomNBitInteger(bits - 1)

    d = pow(e, -1, euler)

    m_size = 2**67 #number.getRandomNBitInteger(n.bit_length()-1)
    if m_size > n:
        raise ValueError()


    size_of_block = 64 # rozmiar bloku w bajtach
    number_of_blocks = math.ceil(len(data)/size_of_block) # obliczenie liczby bloków (zaokrąglenie w górę), 1 piksel zajmuje 1 bajt

    
    for i in range (0, len(data)): # zamiana na liczby binarne
        data[i] = format(data[i], 'b')

    blocks = [] # lista z blokami w zapisie dziesiętnym

    for i in range(0, number_of_blocks):
        block_list = [] # lista ze składowymi bloku

        for _number in data[i*size_of_block:i*size_of_block + size_of_block]: 
            new_number = None
            if len(_number) == 8:
                new_number = _number
            else:
                prefix = '0'
                for i in range (0, 7 - len(_number)):
                    prefix = '0' + prefix
                new_number = prefix + _number
            block_list.append(new_number)
            

        binary_block = ''.join(block_list)
        decimal_block = int(binary_block, 2)
        blocks.append(decimal_block)

    print('Liczba bloków:', len(blocks), 'Liczba pikseli:', len(data)) 
    #print(blocks)

    print(m_size<n)
    
    ciphered_blocks = [] # lista na zaszyfrowane bloki

    for i in range(0, len(blocks)): # szyfrowanie wszystkich bloków
        ciphered = pow(blocks[i], e, n)
        ciphered_blocks.append(ciphered)

    

    #print('Zaszyfrowane bloki:', ciphered_blocks)
    print('d:', d, 'e:',e, 'p:', p, 'q:', q, 'n:', n, 'euler:',euler)
    
    #for block in ciphered_blocks:
        #print('DLUGOSC',len(format(block, 'b')))
    ###### Zmiana zaszyfrowanych bloków na piksele
    pixels = []
    print(ciphered_blocks)
    # dla wszystkich bloków poza ostatnim
    for j in range (0, len(ciphered_blocks) - 1):
        binary_block = format(ciphered_blocks[j], 'b')
        for i in range(0, size_of_block):
            binary_number = binary_block[i*8:i*8+8]
            decimal_number = int(binary_number, 2)
            pixels.append(decimal_number)
        binary_number = binary_block[size_of_block*8: len(binary_block)]
        decimal_number = int(binary_number, 2)
        pixels.append(decimal_number)

    # ostatni blok - do zrobienia
    #last_block = ciphered_blocks[len(ciphered_blocks)-1]

    
    #print('PIXELE:', pixels)
    print(len(pixels)) # bez ostatniego bloku
    
    # program wywala się przy zapisywaniu, jeżeli liczba danych jest inna niż początkowa
    pi = []
    for i in range(0,len(data)):
        pi.append(pixels[i])
    return pi

""" 
    #last_block = ciphered_blocks[len(ciphered_blocks) - 1]
    #binary_last_block = format(last_block, 'b')
    #for i in range(0, len(data) - len(pixels)):
    #    binary_number = binary_last_block[i*8:i*8+8]
    #    decimal_number = int(binary_number, 2)
    #    pixels.append(decimal_number)
    pixels.append(1)
    pixels.append(1)
    pixels.append(1)
    pixels.append(1)

    for i in range(0, len(pixels)):
        if(pixels[i] > 255):
            pixels[i] = 255
    #print(pixels, len(pixels))
    return pixels
"""


def generate_p_and_q(bits):
    p = number.getRandomNBitInteger(bits)
    q = number.getRandomNBitInteger(bits)
    while not number.isPrime(p) and not number.isPrime(p):
        p = number.getRandomNBitInteger(bits)
        q = number.getRandomNBitInteger(bits)

    return p,q


def save_png_with_png_writer(data,greyscale,alpha, width, height,bytes_per_pixel):
    bytes_row_width = width * bytes_per_pixel
    pixels_grouped_by_rows = [data[i: i + bytes_row_width] for i in range(0, len(data), bytes_row_width)]

    writer = png.Writer(width, height, greyscale=greyscale, alpha=alpha)
    file = open('png.png', 'wb')
    writer.write(file, pixels_grouped_by_rows)
    file.close()
    return data
