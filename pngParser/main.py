from project.PNGFileParser import PngFileParser

def main():
    png_parser = PngFileParser()
    png_parser.readFile("test2.png")
    png_parser.do_parsing()
    png_parser.saveFile("after_test.png")

    # this png_parser variable should be used in gui class
    # sth like 
    # png_parser_gui=PNGParserGui(png_parser)


if __name__ == '__main__':
    main()