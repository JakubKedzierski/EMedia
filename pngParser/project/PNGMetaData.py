"""
here we store png metada info like width, height of image, author, modification time etc
"""
class PngMetadata:

    def __init__(self):
        self.__width=None
        self.__height=None
        self.__depth=None
        self.__palete_of_colors=None
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
        self.__textual_information_dict=None
        