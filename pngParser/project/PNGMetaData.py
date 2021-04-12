"""
here we store png metada info like width, height of image, author, modification time etc
"""
class PngMetadata:

    def color_type_explanation(self):

        explanation = 'Invalid color type data'
        if self.color_type == 0:
            explanation = 'Each pixel is a grayscale sample'
        if self.color_type == 2:
            explanation = 'Each pixel is an R,G,B triple'
        if self.color_type == 3:
            explanation = 'Each pixel is a palette index, a PLTE chunk must appear'
        if self.color_type == 4:
            explanation = ' Each pixel is a grayscale sample, followed by an alpha sample'
        if self.color_type == 6:
            explanation = 'Each pixel is an R,G,B triple, followed by an alpha sample'

        return explanation

    def interlace_method_explanation(self):
        if self.interlace_method == 0:
            return 'No interlace'
        elif self.interlace_method == 1:
            return 'Interlace'
        else:
            return 'Invalid interlace data'

    def physical_explanation(self):
        if self.phys_unit == 1:
            print("Pixels per one meter, X axis: ", self.pixels_per_x)
            print("Pixels per one meter, Y axis: ", self.pixels_per_y)
        if self.phys_unit == 0:
            print("Unit is unknown")
            print("Pixels per one unit, X axis: ", self.pixels_per_x)
            print("Pixels per one unit, Y axis: ", self.pixels_per_y)


    def show_data(self):
        print('\n\nIHDR CHUNK:')
        print("Width:", self.width, "px")
        print("Height:", self.height, "px")
        print("Depht: ", self.depth, 'bits per sample or per palette index')
        print("Color Type:", self.color_type_explanation())
        print("Compression method: ", self.compression_method)
        print("Filter method (preprocessing method applied to the image data before compression): ", self.filter_method)
        self.interlace_method_explanation()

        if self.gamma_value is not None:
            print('\n\ngAMA CHUNK:')
            print('Gamma specifies the relationship between the image samples and the desired display output intensity')
            print("Gamma value: ", self.gamma_value)

        if self.time_of_last_edit is not None:
            print('\n\ntIME CHUNK:')
            print("Last modified:", self.time_of_last_edit)

        if self.phys_unit is not None:
            print('\n\npHYs CHUNK:')
            print('The pHYs chunk specifies the intended pixel size or aspect ratio for display of the image')
            self.physical_explanation()

        if self.textual_information_dict is not None:
            print('\n\ntextual chunks:')
            for keys in self.textual_information_dict:
                print("|text chunk info|", keys, ": ", self.textual_information_dict[keys])

    def __init__(self):
        # IHDR chunks
        self.width = None
        self.height = None
        self.depth = None
        self.color_type = None
        self.compression_method = None
        self.filter_method = None
        self.interlace_method = None
        self.time_of_last_edit = None
        self.gamma_value = None
        self.pixels_per_x = None
        self.pixels_per_y = None
        self.phys_unit = None

        # PLTE chunks
        self.palete_of_colors = None
        self.palette_entires = None
        # etc, any other critical or ancillary chunk info


        """
        dictionary where we will store textual information like: 
        title: title data
        author: author data
        pairs -> str:str
        """
        self.textual_information_dict={}
