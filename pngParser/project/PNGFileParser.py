import sys
from project.FileParser import FileParser
from project.PNGMetaData import PngMetadata
import datetime
import numpy as np


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
        if length_bytes_joined != '':
            length=int(length_bytes_joined,16)
        else: 
            length=0
        
        chunk_type_bytes=self.__file_data[start_position+4:start_position+8] 
        chunk_type_bytes_joined = "".join(chunk_type_bytes) 
        chunk_type = bytes.fromhex(chunk_type_bytes_joined).decode() 

        chunk_data_bytes_in_a_list = self.__file_data[start_position+8:start_position+8+length]
        end_position=start_position+8+length+4 # data start + data end + CRCz

        return length,chunk_type,chunk_data_bytes_in_a_list,end_position
        # dlugosc:int, chunk_type: ASCI -nazwa, chunk_data: lista kolejnych bajtów z danymi, end_position:int - koniec chunka
    
    # funkcja służąca do odczytu danych z chunka IHDR - headera
    def read_ihdr_chunk(self, start_position:int):
        # lista pierwszych 4 chunków zawierających informację o wysokości pliku
        height_list = self.__file_data[start_position:start_position+4]
        #lista kolejnych 4 chunków zawierających informację o szerokości pliku
        width_list = self.__file_data[start_position+4:start_position+8] 
        #lista ostatnich 5 chunków zawierających pozostałe informacje
        ihdr_list = self.__file_data[start_position+8:start_position+13]

        # łączenie list w jeden string
        height_list_joined = "".join(height_list)
        width_list_joined = "".join(width_list)

        # odkodowanie danych i przypisanie ich do obiektu klasy PngMetadata()
        self.__meta_data.height = int(height_list_joined, 16)
        self.__meta_data.width = int(width_list_joined, 16)
        self.__meta_data.depth = int(ihdr_list[0], 16)
        self.__meta_data.color_type = int(ihdr_list[1], 16)
        self.__meta_data.compression_method = int(ihdr_list[2], 16)
        self.__meta_data.filter_method = int(ihdr_list[3], 16)
        self.__meta_data.interlace_method = int(ihdr_list[4], 16)

    def parse_plte_chunk(self,chunk_data_bytes):
        for i in range(0,len(chunk_data_bytes)):
            chunk_data_bytes[i] = int(chunk_data_bytes[i],16)
        
        chunk_data = np.array(chunk_data_bytes)
        chunk_data = np.reshape(chunk_data,(-1,3))
        self.meta_data.palette_entires=chunk_data
    
    def parse_text_chunk(self,chunk_data_bytes):
        
        keyword=[]
        value=[]
        null_value_found=False
        for data in chunk_data_bytes:
            if data == '00':
                null_value_found=True
            
            if null_value_found == False:
                keyword.append(data)
            
            if null_value_found == True:
                if data != '00':
                    value.append(data)
        
        keyword = ''.join(keyword)
        value = ''.join(value)
        keyword = bytes.fromhex(keyword).decode()
        value = bytes.fromhex(value).decode()
        
        self.meta_data.textual_information_dict[keyword]=value 

    def parse_time_chunk(self,chunk_data):
        year = int("".join(chunk_data[0:2]),16)
        month = int("".join(chunk_data[2:3]),16)
        day = int("".join(chunk_data[3:4]),16)
        hour = int("".join(chunk_data[4:5]),16)
        minute = int("".join(chunk_data[5:6]),16)
        second = int("".join(chunk_data[6:7]),16)
        time_of_modyfication = datetime.datetime(year=year,month=month,day=day,hour=hour,minute=minute,second=second)
        self.__meta_data.time_of_last_edit = time_of_modyfication

    def do_parsing(self):
        if self.check_if_file_header_is_proper() is False:
            raise ValueError("PNG file has not proper file header")

        start_position=8

        while True:
            length,chunk_type,chunk_data_bytes,end_position=self.read_chunk(start_position)
            start_position=end_position

            #critical chunks:
    
            if chunk_type == "IEND":
                break

            if chunk_type == "IHDR":
                self.read_ihdr_chunk(start_position)

            elif chunk_type == "PLTE":
                self.parse_plte_chunk(chunk_data_bytes)

            elif chunk_type == "tIME":
                self.parse_time_chunk(chunk_data_bytes)
            
            #and ancillary chunks:
            
            elif chunk_type == "tEXt":
                self.parse_text_chunk(chunk_data_bytes)


    
    def saveFile(self,new_file_name:str):
        with open("img/"+new_file_name,'wb') as file:
            for byte in self.__file_data:
                file.write(bytes.fromhex(byte))
    
