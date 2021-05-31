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


    png_encrypter = PngFileParser()
    img = 'lots_of_chunks.png'
    png_encrypter.readFile(img)
    png_encrypter.do_parsing()
    private_key, size_of_block = png_encrypter.encrypt()
    #private_key, size_of_block,size = png_encrypter.encrypt_compressed()
    #private_key, size_of_block, vector = png_encrypter.encryptCBC()


    png_decrypter = PngFileParser()
    img = 'after_encrypting.png'
    png_decrypter.readFile(img)
    png_decrypter.do_parsing()
    png_decrypter.decrypt(private_key, size_of_block)
    #png_decrypter.decrypt_compressed(private_key, size_of_block,size)
    #png_decrypter.decryptCBC(private_key, size_of_block,vector)





if __name__ == '__main__':
    main()