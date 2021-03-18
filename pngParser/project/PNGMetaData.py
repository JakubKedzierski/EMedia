"""
here we store png metada info like width, height of image, author, modification time etc
"""
class PngMetadata:

    def __init__(self):
        # IHDR chunks
        self.width=None
        self.height=None
        self.depth=None
        self.color_type=None
        self.compression_method=None
        self.filter_method=None
        self.interlace_method=None

        # PLTE chunks
        self.palete_of_colors=None
        self.palette_entires=None
        # etc, any other critical or ancillary chunk info


        """
        dictionary where we will store textual information like: 
        title: title data
        author: author data
        description:
        creation time:
        copyright:
        pairs -> str:str
        """
        self.textual_information_dict={}
        