from project.PNGFileParser import PngFileParser


def main():
    png_parser = PngFileParser()
    png_parser.readFile("lots_of_chunks.png")
    #png_parser.display_image("img/test.png")
    #png_parser.fast_fourier_transformation("img/test.png")
    png_parser.do_parsing()
    png_parser.anonimize()
    png_parser.saveFile("after_test.png")
    png_parser.meta_data.show_data()

    # this png_parser variable should be used in gui class
    # sth like 
    # png_parser_gui=PNGParserGui(png_parser)


if __name__ == '__main__':
    main()