import sys
from project.FileParser import FileParser
from project.PNGMetaData import PngMetadata


"""
class read, parse, save png file
"""
class PngFileParser(FileParser):

    def __init__(self):
        self.__file_data=[]  #whole png file with headers and each chunk, data is in hex notation
        self.__meta_data=PngMetadata()   # png file metada

    @property
    def file_data(self):
        return self.__file_data

    @file_data.setter
    def file_data(self, value):
        self.__file_data = value

    @property
    def meta_data(self):
        return self.__meta_data



    def readFile(self,file_name:str):
        try:
            with open("img/"+file_name, "rb") as file:
                byte = file.read(1)
                while byte != b"":
                    self.__file_data.append(byte.hex())
                    byte = file.read(1)
        except FileNotFoundError:
            print("File not found.")
            raise FileNotFoundError
    

    def saveFile(self,new_file_name:str):
        with open("img/"+new_file_name,'wb') as file:
            for byte in self.__file_data:
                file.write(bytes.fromhex(byte))
    
