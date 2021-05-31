import zlib

import matplotlib.pyplot as plt
import numpy as np
from Crypto.Util import number
import png
import math
import random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def generate_p_and_q(bits):
    p = 2
    q = 2
    while True:
        p = number.getRandomNBitInteger(bits)
        if number.isPrime(p):
            break

    while True:
        q = number.getRandomNBitInteger(bits)
        if number.isPrime(q):
            break

    return p, q

def generate_keys():
    key_length = 520 # 64 bajty to 512 bitow, przy 520 bitach klucza mamy pewnosc ze tekst jawny bedzie krotszy niz klucz
    bits = int(key_length/2)

    euler = 0
    while euler.bit_length() != key_length:
        p, q = generate_p_and_q(bits)
        n = p * q
        euler = (p-1) * (q-1)

    e = 2**16 + 1

    while e >= euler or number.GCD(e,euler) != 1:
        e = number.getRandomNBitInteger(bits - 1)

    d = pow(e, -1, euler)

    return n,e,d

def encrypt_data_compressd(data, length):
    n,e,d = generate_keys()
    private_key = (n,d)
    size_of_block = 64 # rozmiar bloku w bajtach

    pixels = []
    for i in range(0,len(data),size_of_block):
        bytes_to_encrypt = bytearray(data[i: i + size_of_block])
        cipher_text = pow(int.from_bytes(bytes_to_encrypt, 'big'), e, n) # kodowanie do kryptogramu
        block = cipher_text.to_bytes(n.bit_length(), 'big') # tworzony jest blok o długości n w bajtach tak aby była stała szerokość

        for j in range(0,len(block)):
            pixels.append(block[j])   # każy bajt jest osobno dodawany do tablicy pikseli

    return pixels[:length], pixels[length:], private_key, size_of_block

def encrypt_library(data):
    keyPair = RSA.generate(1024)
    print('n: ', keyPair.n, keyPair.e)
    encryptor = PKCS1_OAEP.new(keyPair.public_key())
    size_of_block = 86 #maksymalny rozmiar bloku dla tego klucza
    data = bytearray(data)
    pixels = []
    for i in range(0, len(data), size_of_block):
        bytes_to_encrypt = data[i:i+size_of_block]
        block = encryptor.encrypt(bytes_to_encrypt)

        for j in range(0, len(block)):
            pixels.append(block[j])

    return pixels[:len(data)], pixels[len(data):], (keyPair.n, keyPair.d), size_of_block

def encrypt_data(data):
    n,e,d = generate_keys()
    private_key = (n,d)
    size_of_block = 64 # rozmiar bloku w bajtach

    pixels = []
    for i in range(0,len(data),size_of_block):
        bytes_to_encrypt = bytearray(data[i: i + size_of_block])
        cipher_text = pow(int.from_bytes(bytes_to_encrypt, 'big'), e, n) # kodowanie do kryptogramu
        block = cipher_text.to_bytes(n.bit_length(), 'big') # tworzony jest blok o długości n w bajtach tak aby była stała szerokość

        for j in range(0,len(block)):
            pixels.append(block[j])   # każy bajt jest osobno dodawany do tablicy pikseli

    return pixels[:len(data)], pixels[len(data):], private_key, size_of_block

def encrypt_data_CBC(data):
    n,e,d = generate_keys()
    private_key = (n,d)
    size_of_block = 64 # rozmiar bloku w bajtach
    data = bytearray(data)
    initialization_vector = number.getRandomNBitInteger(size_of_block * 8)
    previous_vector = initialization_vector

    pixels = []
    for i in range(0,len(data),size_of_block):
        bytes_to_encrypt = data[i: i + size_of_block]
        int_cipher = int.from_bytes(bytes_to_encrypt, 'big')

        previous_vector = previous_vector.to_bytes(int(n.bit_length()/8), 'big')
        previous_vector = int.from_bytes(previous_vector[0:len(bytes_to_encrypt)], 'big') # dopasowanie wektora inizjalizujacego do rozmiaru liczby z bloku
        int_cipher = int_cipher ^ previous_vector

        cipher_text = pow(int_cipher, e, n) # kodowanie do kryptogramu
        previous_vector = cipher_text
        block = cipher_text.to_bytes(n.bit_length(), 'big') # tworzony jest blok o długości n w bajtach

        for j in range(0,len(block)):
            pixels.append(block[j])   # każy bajt jest osobno dodawany do tablicy pikseli

    return pixels[:len(data)], pixels[len(data):], private_key, size_of_block, initialization_vector



def decrypt_data_CBC(data, private_key,chunk_size, vector,orginal_file_data_length):
    n = private_key[0]
    d = private_key[1]

    size_of_block = n.bit_length()
    data = bytearray(data)

    pixels_byte= []
    for i in range(0, len(data), size_of_block):
        bytes_to_decrypt = data[i: i + size_of_block]
        next_vector = int.from_bytes(bytes_to_decrypt, 'big')
        plain_text = pow(next_vector, d, n)

        vector = vector.to_bytes(int(n.bit_length()/8), 'big')
        vector = int.from_bytes(vector[0:chunk_size],'big')
        plain_text = plain_text ^ vector

        block = plain_text.to_bytes(chunk_size, 'big')

        if (len(pixels_byte)+chunk_size) > orginal_file_data_length: # ostatni chunk jest wiekszy niz rozmiar danych w ostatnim chunku w orignale
            # trzeba wiec skrocic jego rozmiar
            last_chunk_orginal_data_length = orginal_file_data_length - len(pixels_byte)
            block = block[chunk_size-last_chunk_orginal_data_length-1:] # przesuwamy blok tak aby jego poczatek
            # byl w poczatku wlasiwych danych

        for j in range(0,chunk_size):
            pixels_byte.append(block[j:j+1])   # dodajemy do tablicy pikselow/bajtow bajt po bajcie piksele

        vector = next_vector

    pixels = []
    for pixel in pixels_byte:
        pixels.append(int.from_bytes(pixel, 'big'))

    return pixels

def decrypt(data, private_key,chunk_size,orginal_file_data_length):

    n = private_key[0]
    d = private_key[1]

    size_of_block = n.bit_length()
    data = bytearray(data)

    pixels_byte= []
    for i in range(0, len(data), size_of_block):
        bytes_to_decrypt = data[i: i + size_of_block]
        plain_text = pow(int.from_bytes(bytes_to_decrypt, 'big'), d, n)
        block = plain_text.to_bytes(chunk_size, 'big')
        if (len(pixels_byte)+chunk_size) > orginal_file_data_length: # ostatni chunk jest wiekszy niz rozmiar danych w ostatnim chunku w orignale
            # trzeba wiec skrocic jego rozmiar
            last_chunk_orginal_data_length = orginal_file_data_length - len(pixels_byte)
            block = block[chunk_size-last_chunk_orginal_data_length:] # przesuwamy blok tak aby jego poczatek
            # byl w poczatku wlasiwych danych

        for j in range(0,chunk_size):
            pixels_byte.append(block[j:j+1])   # dodajemy do tablicy pikselow/bajtow bajt po bajcie piksele

    pixels = []
    for pixel in pixels_byte:
        pixels.append(int.from_bytes(pixel, 'big'))

    return pixels


def save_png_with_png_writer(data,data_exceeded,greyscale,alpha, width, height,bytes_per_pixel, filename='img/after_encrypting.png'):
    bytes_row_width = width * bytes_per_pixel
    pixels_grouped_by_rows = [data[i: i + bytes_row_width] for i in range(0, len(data), bytes_row_width)]

    writer = png.Writer(width, height, greyscale=greyscale, alpha=alpha)
    file = open(filename, 'wb')
    writer.write(file, pixels_grouped_by_rows)
    file.write(bytearray(data_exceeded))
    file.close()

    return data
