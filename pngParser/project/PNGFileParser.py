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
        return self.__file_data # dane sa w systemie szesnastkowym, ale bez prefixu 0x oraz jako typ str np. file_data[0]=80 - co oznacza 0x80

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
    
    def check_if_file_header_is_proper(self):
        png_header=['89','50','4e','47','0d','0a','1a','0a']
        for i in range(0,8):
            if(png_header[i] != self.__file_data[i]):
                return False
        return True


    """
    czyta calego chunka od zadanej pozycji i zwraca dane o nim
    """
    def read_chunk(self,start_position:int):
        length_bytes=self.__file_data[start_position:start_position+4]
        length_bytes_joined = "".join(length_bytes)
        length=int(length_bytes_joined,16)
        
        chunk_type_bytes=self.__file_data[start_position+4:start_position+8]
        chunk_type_bytes_joined = "".join(chunk_type_bytes)
        chunk_type = bytes.fromhex(chunk_type_bytes_joined).decode()

        chunk_data_bytes_in_a_list = self.__file_data[start_position+8:start_position+8+length]
        end_position=start_position+8+length+4 # data start + data end + CRC

        return length,chunk_type,chunk_data_bytes_in_a_list,end_position
        # dlugosc:int, chunk_type: ASCI -nazwa, chunk_data: lista kolejnych bajtów z danymi, end_position:int - koniec chunka
    


    def do_parsing(self):
        if self.check_if_file_header_is_proper() is False:
            raise ValueError("PNG file has not proper file header")

        start_position=8
        
        while True:
            length,chunk_type,chunk_data_bytes,end_position=self.read_chunk(start_position)
            start_position=end_position


            if chunk_type == "IEND":
                break
            
            # jest jakis lepszy sposob, zeby zastapic te if, else na cos pokroju switcha ?

            if chunk_type == "IHDR":
                pass

            elif chunk_type == "PLTE":
                pass

            elif chunk_type == "IDAT":
                pass


    
    def saveFile(self,new_file_name:str):
        with open("img/"+new_file_name,'wb') as file:
            for byte in self.__file_data:
                file.write(bytes.fromhex(byte))
    
