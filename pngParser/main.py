from project.PNGFileParser import PngFileParser
from project.global_operations import *
from project.PNGParserGui import *


def main():
    #gui = PNGParserGui()


    png_parser = PngFileParser()
    img = 'simple.png'
    png_parser.readFile(img)
    #display_image("img/" + img)
    #fast_fourier_transformation("img/" + img)
    png_parser.do_parsing()
    png_parser.encrypt()
    #png_parser.saveFile("after_test.png")
    png_parser.save_with_anonimization("after_test.png")
    #png_parser.meta_data.show_data()


if __name__ == '__main__':
    main()