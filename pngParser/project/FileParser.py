"""
here are methods that can be used by gui class
"""
class FileParser(object):

    def __init__(self):
        pass
    
    """
    read file from pngParser/img directory to file_data variable
    file_name - valid png file name with .png extension - if not found - raising FileNotFoundError
    """
    def readFile(self,file_name):
        pass

    """
    save file with given file name
    file will be saved in pngParser/img directory
    new_file_name should have .png extension -> it is not checked in saveFile method
    file_data in PNGFileParser should be valid hex data when saving file
    """
    def saveFile(self,new_file_name):
        pass
    


