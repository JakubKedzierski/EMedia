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