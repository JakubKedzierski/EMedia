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
        return self.__file_data # dane sa w systemie szesnastkowym, ale bez prefixu 0x oraz jako typ str

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
    
    def __check_if_file_header_is_proper(self):
        png_header=['89','50','4e','47','0d','0a','1a','0a']
        for i in range(0,8):
            if(png_header[i] != self.__file_data[i]):
                return False
        return True

    def __read_chunk(self,start_position:int):
        length_bytes=self.__file_data[start_position:start_position+4]
        length=int(length_bytes[0],16)*16**3+int(length_bytes[1])*16**2+int(length_bytes[2])*16**1+int(length_bytes[3],16)
        print(length)


    def do_parsing(self):
        if self.__check_if_file_header_is_proper() is False:
            raise ValueError("PNG file has not proper file header")

        self.__read_chunk(8)




    
    def saveFile(self,new_file_name:str):
        with open("img/"+new_file_name,'wb') as file:
            for byte in self.__file_data:
                file.write(bytes.fromhex(byte))
    
