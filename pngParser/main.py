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
    #gui = PNGParserGui()

    png_parser = PngFileParser()
    img = 'exif.png'
    png_parser.readFile(img)
    png_parser.do_parsing()
    #png_parser._meta_data.show_data()
    png_parser.encrypt()




if __name__ == '__main__':
    main()