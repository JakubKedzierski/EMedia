"""
here we store png metada info like width, height of image, author, modification time etc
"""
class PngMetadata:

    def show_data(self):
        print("Width:",self.width)
        print("Height:",self.height)
        print("Depht:",self.depth)
        print("Color Type",self.color_type)
        print("Compression method",self.compression_method)
        print("Filter method:",self.filter_method)
        print("Interlace method",self.interlace_method)
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


        