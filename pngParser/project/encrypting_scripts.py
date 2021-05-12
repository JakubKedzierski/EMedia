import zlib

import matplotlib.pyplot as plt
import numpy as np
from Crypto.Util import number
import png


def encrypt_data(data,width, height,bytes_per_pixel):
    bits = 10
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

    data = bytearray(data)
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


    print(m_size<n)
    print(d,e,p,q,n,euler)

    for i in range(0, len(data)):
        data[i]=120

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
