from project.PNGFileParser import PngFileParser
from project.global_operations import *


def main():
    png_parser = PngFileParser()
    png_parser.readFile("lots_of_chunks.png")
    #display_image("img/test.png")
    #fast_fourier_transformation("img/test.png")
    png_parser.do_parsing()
    #png_parser.saveFile("after_test.png")
    png_parser.save_with_anonimization("after_test.png")
    png_parser.meta_data.show_data()


if __name__ == '__main__':
    main()