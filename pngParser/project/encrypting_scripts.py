import zlib

import matplotlib.pyplot as plt
import numpy as np
from Crypto.Util import number
import png
import math

def encrypt_data(data,width, height,bytes_per_pixel):
    bits = 34
    p, q = generate_p_and_q(bits)
    n = p * q
    euler = (p-1) * (q-1)
    e = 2**16 + 1

    while e >= euler or number.GCD(e,euler) != 1:
        e = number.getRandomNBitInteger(bits - 1)

    d = pow(e, -1, euler)

    m_size = 2**16 #number.getRandomNBitInteger(n.bit_length()-1)
    if m_size > n:
        raise ValueError()

    #data = bytearray(data)
    #print(data)
    i=0
    size = 2
    block = []
    while True:
        block=data[i:i+size]
        block = int.from_bytes(block,"big")
        #print(block)

        i=i+size
        if i >= len(data):
            break


    size_of_block = 8 # rozmiar bloku w bajtach
    number_of_blocks = math.ceil(len(data)/size_of_block) # obliczenie liczby bloków (zaokrąglenie w górę)


    for i in range (0, len(data)): # zamiana na liczby binarne
        data[i] = format(data[i], 'b')


    blocks = [] # lista z blokami w zapisie dziesiętnym

    for i in range(0, number_of_blocks):
        block_list = [] # lista ze składowymi bloku

        for _number in data[i*size_of_block:i*size_of_block + size_of_block]: # do zautomatyzowania
            new_number = None
            if len(_number) == 8:
                new_number = _number
            if len(_number) == 7:
                new_number = '0' + _number
            if len(_number) == 6:
                new_number = '00' + _number
            if len(_number) == 5:
                new_number = '000' + _number
            if len(_number) == 4:
                new_number = '0000' + _number
            if len(_number) == 3:
                new_number = '00000' + _number
            if len(_number) == 2:
                new_number = '000000' + _number
            if len(_number) == 1:
                new_number = '0000000' + _number
            block_list.append(new_number)

        binary_block = ''.join(block_list)
        decimal_block = int(binary_block, 2)
        blocks.append(decimal_block)

    print('Liczba bloków:', len(blocks), 'Liczba pikseli:', len(data)) 
    #print(blocks)
    

    for i in range(0, len(data)):
        data[i]=120

    print(m_size<n)
    
    ciphered_blocks = [] # lista na zaszyfrowane bloki

    for i in range(0, len(blocks)): # szyfrowanie wszystkich bloków
        ciphered = pow(blocks[i], e, n)
        ciphered_blocks.append(ciphered)


    print('Zaszyfrowane bloki:', ciphered_blocks)
    print('d:', d, 'e:',e, 'p:', p, 'q:', q, 'n:', n, 'euler:',euler)
    return data

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
