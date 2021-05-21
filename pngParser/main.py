from project.PNGFileParser import PngFileParser
from project.global_operations import *
from project.PNGParserGui import *


def main():
    #gui = PNGParserGui()


    png_parser = PngFileParser()
    img = 'after_encrypting.png'
    png_parser.readFile(img)
    png_parser.do_parsing()
    png_parser._meta_data.show_data()
    #png_parser.encrypt()
    png_parser.decrypt()



if __name__ == '__main__':
    main()