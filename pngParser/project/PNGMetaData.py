"""
here we store png metada info like width, height of image, author, modification time etc
"""
class PngMetadata:

    def color_type_explanation(self, number):
        if(number == 0):
            print('Each pixel is a grayscale sample')
        if(number == 2):
            print('Each pixel is an R,G,B triple')
        if(number == 3):
            print('Each pixel is a grayscale sample, followed by an alpha sample')
        if(number == 4): 
            print('Each pixel is an R,G,B triple, followed by an alpha sample')
        if(number == 6):
            print('Each pixel is an R,G,B triple, followed by an alpha sample')
        if(number != 0 and number!=2 and number!=3 and number!=4 and number!=6):
            print('Invalid color type data')

    def interlace_method_explanation(self, number):
        if(number == 0):
            print('No interlace')
        if(number == 1):
            print('Interlace')
        if(number != 0 and number != 1):
            print('Invalid interlace data')

    def physical_explanation(self, phys_unit, pixels_per_x, pixels_per_y):
        if(phys_unit == 1):
            print("Pixels per one meter, X axis: ", pixels_per_x)
            print("Pixels per one meter, Y axis: ", pixels_per_y)
        if(phys_unit == 0):
            print("Unit is unknown")
            print("Pixels per one unit, X axis: ", pixels_per_x)
            print("Pixels per one unit, Y axis: ", pixels_per_y)


    def show_data(self):
        print("Width:",self.width,"px")
        print("Height:",self.height,"px")
        self.physical_explanation(self.phys_unit, self.pixels_per_x, self.pixels_per_y)
        print("Depht:",self.depth)
        print("Color Type", self.color_type)
        self.color_type_explanation(self.color_type)
        print("Gamma value: ", self.gamma_value)
        print("Compression method",self.compression_method)
        print("Filter method:",self.filter_method)
        #print("Interlace method",self.interlace_method)
        self.interlace_method_explanation(self.interlace_method)
        print("Last modyfied:",self.time_of_last_edit)
        for keys in self.textual_information_dict:
            print("|text chunk info|",keys,": ",self.textual_information_dict[keys])





    def __init__(self):
        # IHDR chunks
        self.width=None
        self.height=None
        self.depth=None
        self.color_type=None
        self.compression_method=None
        self.filter_method=None
        self.interlace_method=None
        self.time_of_last_edit=None
        self.gamma_value=None
        self.pixels_per_x=None
        self.pixels_per_y=None
        self.phys_unit=None

        # PLTE chunks
        self.palete_of_colors=None
        self.palette_entires=None
        # etc, any other critical or ancillary chunk info


        """
        dictionary where we will store textual information like: 
        title: title data
        author: author data
        pairs -> str:str
        """
        self.textual_information_dict={}


        