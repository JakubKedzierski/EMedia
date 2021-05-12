import zlib

import matplotlib.pyplot as plt
import numpy as np
from Crypto.Util import number
import png


def encrypt_data(data,width, height,bytes_per_pixel):
    p, q = generate_p_and_q()


    for i in range(0, len(data)):
        data[i]=120

    return data

def generate_p_and_q():
    p = number.getRandomNBitInteger(10)
    q = number.getRandomNBitInteger(10)
    while not number.isPrime(p) and not number.isPrime(p):
        p = number.getRandomNBitInteger(10)
        q = number.getRandomNBitInteger(10)

    return p,q


def save_png_with_png_writer(data,greyscale,alpha, width, height,bytes_per_pixel):
    bytes_row_width = width * bytes_per_pixel
    pixels_grouped_by_rows = [data[i: i + bytes_row_width] for i in range(0, len(data), bytes_row_width)]

    writer = png.Writer(width, height, greyscale=greyscale, alpha=alpha)
    file = open('png.png', 'wb')
    writer.write(file, pixels_grouped_by_rows)
    file.close()
    return data
