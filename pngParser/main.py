from project.PNGFileParser import PngFileParser
from project.global_operations import *
from project.encrypting_scripts import *
import numpy as np
from Crypto.Util import number
import png
import math
import random

import random


def main():
    """
    #gui = PNGParserGui()
    data = [0, 1,234,123,1,253]

    n,e,d = generate_keys()
    public_key = (n,e)
    private_key = (n,d)

    size_of_block = 2  # rozmiar bloku w bajtach
    chunk_size = size_of_block
    blocks = []
    for i in range(0,len(data),size_of_block):
        chunk_to_enrypt_hex = bytes(data[i: i + size_of_block])
        cipher_int = pow(int.from_bytes(chunk_to_enrypt_hex, 'big'), e, n)
        block = cipher_int.to_bytes(n.bit_length(), 'big')
        for j in range(0,len(block)):
            blocks.append(block[j])


    data_to_decrypt = blocks
    print(blocks)
    size_of_block = n.bit_length()

    pixels = []
    for i in range(0, len(data_to_decrypt), size_of_block):
        chunk_to_decrypt_hex = bytearray(data_to_decrypt[i: i + size_of_block])
        plain_text = pow(int.from_bytes(chunk_to_decrypt_hex, 'big'), d, n)
        block = plain_text.to_bytes(2, 'big')
        for i in range(0,chunk_size):
            pixels.append(block[i:i+1])

    for pixel in pixels:
        print(int.from_bytes(pixel, 'big'))

   # wykład godzina 1.08

    """

    png_parser = PngFileParser()
    img = 'tux.png'
    png_parser.readFile(img)
    png_parser.do_parsing()
    #png_parser._meta_data.show_data()
    private_key, size_of_block = png_parser.encrypt()
    #private_key, size_of_block, vector = png_parser.encryptCBC()

    png_parser = PngFileParser()
    img = 'after_encrypting.png'
    png_parser.readFile(img)
    png_parser.do_parsing()
    png_parser.decrypt(private_key,size_of_block)
    #png_parser.decryptCBC(private_key, size_of_block,vector )





if __name__ == '__main__':
    main()