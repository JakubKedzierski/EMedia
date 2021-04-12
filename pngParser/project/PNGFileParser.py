import sys
from project.FileParser import FileParser
from project.PNGMetaData import PngMetadata
import datetime
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img
import zlib
from xml.etree import cElementTree as ElementTree

"""
class read, parse, save png file
"""
class PngFileParser(FileParser):

    def __init__(self):
        self.__file_data=[]  #whole png file with headers and each chunk, data is in hex notation
        self._meta_data=PngMetadata()   # png file metada
        self._chunk_positions=[]

    @property
    def file_data(self):
        return self.__file_data # dane sa w systemie szesnastkowym, ale bez prefixu 0x oraz jako typ str np. file_data[0]=80 - co oznacza 0x80

    @property
    def meta_data(self):
        return self._meta_data


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
    def parse_ihdr_chunk(self, chunk_data_bytes):
        height_list = chunk_data_bytes[0:4]
        width_list = chunk_data_bytes[4:8] 
        ihdr_list = chunk_data_bytes[8:13]

        # łączenie list w jeden string
        height_list_joined = "".join(height_list)
        width_list_joined = "".join(width_list)

        # odkodowanie danych i przypisanie ich do obiektu klasy PngMetadata()
        self._meta_data.height = int(height_list_joined, 16)
        self._meta_data.width = int(width_list_joined, 16)
        self._meta_data.depth = int(ihdr_list[0], 16)
        self._meta_data.color_type = int(ihdr_list[1], 16)
        self._meta_data.compression_method = int(ihdr_list[2], 16)
        self._meta_data.filter_method = int(ihdr_list[3], 16)
        self._meta_data.interlace_method = int(ihdr_list[4], 16)

    def parse_plte_chunk(self,chunk_data_bytes):
        for i in range(0,len(chunk_data_bytes)):
            chunk_data_bytes[i] = int(chunk_data_bytes[i],16)
        
        chunk_data = np.array(chunk_data_bytes)
        chunk_data = np.reshape(chunk_data,(-1,3))
        self.meta_data.palette_entires=chunk_data

    def parse_exif_chunk(self, chunk_data_bytes):
        #for i in range(0, len(chunk_data_bytes)):
        #    print(chunk_data_bytes[i])
        pass

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
        self._meta_data.time_of_last_edit = time_of_modyfication

    def parse_international_text_info(self,chunk_data):

        keyword = []
        iter=0
        for data in chunk_data:
            iter+=1
            if data == '00':
                break;
            keyword.append(data)

        keyword = ''.join(keyword)
        keyword = bytes.fromhex(keyword).decode()
        compress_flag = int(chunk_data[iter],16)
        compress_method = int(chunk_data[iter+1],16)
        chunk_data=chunk_data[iter+2:len(chunk_data)]

        iter=0
        lang_tag=[]
        for data in chunk_data:
            iter+=1
            if data == '00':
                break;
            lang_tag.append(data)

        lang_tag = "".join(lang_tag)
        lang_tag = bytes.fromhex(lang_tag).decode()

        chunk_data = chunk_data[iter:len(chunk_data)]
        iter=0
        translated_key=[]
        for data in chunk_data:
            iter+=1
            if data == '00':
                break;
            translated_key.append(data)

        translated_key = ''.join(translated_key)
        translated_key = bytes.fromhex(translated_key).decode()

        text = chunk_data[iter:len(chunk_data)]
        if compress_flag == 0:
            text = ''.join(text)
            text = bytes.fromhex(text).decode()
        else:
            text = ''.join(text)
            text = bytes.fromhex(text)
            text = zlib.decompress(text)
            text = str(text, 'utf-8')

        if keyword == 'XML:com.adobe.xmp':
            text = self.parse_xmp_in_itxt_chunk(text)

        text_data="translated key: " + "(" + lang_tag  + ") "  + translated_key + " || Info: " + text.__str__()
        self._meta_data.textual_information_dict[keyword] = text_data

    def parse_xmp_in_itxt_chunk(self,data):
        root = ElementTree.fromstring(data)
        print(data)
        xmp_information = {}
        for item in root[0][0]:
            for nested in item:
                for children in nested:
                    xmp_information[item.tag]=children.text

        return xmp_information

    def parse_gama_chunk(self, chunk_data_bytes):
        gama = ''.join(chunk_data_bytes)
        gamma = int(gama, 16)/100000
        self.meta_data.gamma_value = gamma

    def parse_physical_chunk(self, chunk_data_bytes):
        pixels_per_X = int(''.join(chunk_data_bytes[0:4]), 16)
        pixels_per_Y = int(''.join(chunk_data_bytes[4:8]), 16)
        unit = int(chunk_data_bytes[8])
        self.meta_data.pixels_per_x = pixels_per_X
        self.meta_data.pixels_per_y = pixels_per_Y
        self.meta_data.phys_unit = unit

    def anonimize(self):
        for chunk in self._chunk_positions:
            if chunk[2][0].islower():
                for i in range(chunk[0]+8, chunk[1]):
                    self.__file_data[i] = '00'

    def do_parsing(self):
        if self.check_if_file_header_is_proper() is False:
            raise ValueError("PNG file has not proper file header")

        start_position=8

        while True:
            length,chunk_type,chunk_data_bytes,end_position=self.read_chunk(start_position)
            self._chunk_positions.append((start_position,end_position,chunk_type))
            start_position=end_position

            #critical chunks:
    
            if chunk_type == "IEND":
                break

            if chunk_type == "IHDR":
                self.parse_ihdr_chunk(chunk_data_bytes)

            elif chunk_type == "PLTE":
                self.parse_plte_chunk(chunk_data_bytes)
            
            #and ancillary chunks:

            elif chunk_type =="eXIf":
                self.parse_exif_chunk(chunk_data_bytes)

            elif chunk_type == "tEXt":
                self.parse_text_chunk(chunk_data_bytes)

            elif chunk_type == "tIME":
                self.parse_time_chunk(chunk_data_bytes)

            elif chunk_type ==  "iTXt":
                self.parse_international_text_info(chunk_data_bytes)

            elif chunk_type == "gAMA":
                self.parse_gama_chunk(chunk_data_bytes)

            elif chunk_type == "pHYs":
                self.parse_physical_chunk(chunk_data_bytes)


    def saveFile(self,new_file_name:str):
        with open("img/"+new_file_name,'wb') as file:
            for byte in self.__file_data:
                file.write(bytes.fromhex(byte))

    # funkcja wyświetlająca obrazek 
    def display_image(self,image_path):
        im_data = cv.imread(image_path)
        cv.namedWindow('Image',cv.WINDOW_NORMAL)
        cv.imshow('Image',im_data)
        cv.waitKey(0)

    def fast_fourier_transformation(self, image_path):
        im_data = cv.imread(image_path, cv.IMREAD_GRAYSCALE)
        f = np.fft.fft2(im_data)
        f_shifted = np.fft.fftshift(f)
    
        magnitude = 20*np.log(np.abs(f_shifted))
        magnitude = 255*magnitude/np.max(magnitude)
        magnitude = np.asarray(magnitude, dtype=np.uint8)

        phase = np.angle(f_shifted)

        cv.namedWindow('magnitude', cv.WINDOW_NORMAL)
        cv.imshow('magnitude', magnitude)

        cv.namedWindow('phase', cv.WINDOW_NORMAL)
        cv.imshow('phase', phase)
        cv.waitKey(0)

    
