import zlib

import matplotlib.pyplot as plt
import numpy as np
import png


def encrypt_data(data,width, height,bytes_per_pixel):

    for i in range(0, len(data)):
        data[i]=120

    return data

def save_png_with_png_writer(data,greyscale,alpha, width, height,bytes_per_pixel):
    bytes_row_width = width * bytes_per_pixel
    pixels_grouped_by_rows = [data[i: i + bytes_row_width] for i in range(0, len(data), bytes_row_width)]

    w = png.Writer(width, height, greyscale=greyscale, alpha=alpha)
    f = open('png.png', 'wb')
    w.write(f, pixels_grouped_by_rows)
    f.close()
    return data
