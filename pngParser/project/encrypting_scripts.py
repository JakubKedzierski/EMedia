import zlib

import matplotlib.pyplot as plt
import numpy as np
from Crypto.Util import number
import png
import math
import random


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
    key_length = 520
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

def encrypt_data(data,width, height,bytes_per_pixel):
    n,e,d = generate_keys()
    private_key = (n,d)
    size_of_block = 64 # rozmiar bloku w bajtach

    pixels = []
    for i in range(0,len(data),size_of_block):
        bytes_to_encrypt = bytearray(data[i: i + size_of_block])
        cipher_text = pow(int.from_bytes(bytes_to_encrypt, 'big'), e, n) # kodowanie do kryptogramu
        block = cipher_text.to_bytes(n.bit_length(), 'big') # tworzony jest blok o długości n w bajtach

        for j in range(0,len(block)):
            pixels.append(block[j])   # każy bajt jest osobno dodawany do tablicy pikseli

    return pixels[:len(data)], pixels[len(data):], private_key, size_of_block

def decrypt(data, private_key,chunk_size):
    n = private_key[0]
    d = private_key[1]

    size_of_block = n.bit_length()

    pixels_byte= []
    for i in range(0, len(data), size_of_block):
        bytes_to_decrypt = bytearray(data[i: i + size_of_block])
        plain_text = pow(int.from_bytes(bytes_to_decrypt, 'big'), d, n)
        block = plain_text.to_bytes(chunk_size, 'big')

        for j in range(0,chunk_size):
            pixels_byte.append(block[j:j+1])

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
