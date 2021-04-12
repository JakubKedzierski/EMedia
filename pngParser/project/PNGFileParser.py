import sys
from project.FileParser import FileParser
from project.PNGMetaData import PngMetadata
import datetime
import matplotlib.pyplot as plt
import matplotlib.image as img
import zlib
from xml.etree import cElementTree as ElementTree
import numpy as np


class PngFileParser(FileParser):

    def __init__(self):
        self.__file_data = []  #whole png file with headers and each chunk, data is in hex notation
        self._meta_data = PngMetadata()   # png file metada
        self._chunk_positions = []

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
        png_header=['89', '50', '4e', '47', '0d', '0a', '1a', '0a']
        for i in range(0,8):
            if png_header[i] != self.__file_data[i]:
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
        end_position=start_position+8+length+4 # data start + data end + CRC

        return length,chunk_type,chunk_data_bytes_in_a_list,end_position
        # dlugosc:int, chunk_type: ASCI -nazwa, chunk_data: lista kolejnych bajtów z danymi, end_position:int - koniec chunka
    

    def parse_ihdr_chunk(self, chunk_data_bytes):
        height_list = chunk_data_bytes[0:4]
        width_list = chunk_data_bytes[4:8] 
        ihdr_list = chunk_data_bytes[8:13]

        height_list_joined = "".join(height_list)
        width_list_joined = "".join(width_list)

        self._meta_data.height = int(height_list_joined, 16)
        self._meta_data.width = int(width_list_joined, 16)
        self._meta_data.depth = int(ihdr_list[0], 16)
        self._meta_data.color_type = int(ihdr_list[1], 16)

        compression_method = int(ihdr_list[2], 16)
        if compression_method == 0:
            self._meta_data.compression_method = \
                'deflate / inflate compression with a sliding window of at most 32768 bytes'
        else:
            self._meta_data.compression_method = 'compression method not specified in png standard'

        filter_method = int(ihdr_list[3], 16)

        if filter_method == 0:
            self._meta_data.filter_method = 'adaptive filtering with five basic filter types'
        else:
            self._meta_data.filter_method = 'filter method not specified in png standard'

        self._meta_data.interlace_method = int(ihdr_list[4], 16)

    def parse_plte_chunk(self,chunk_data_bytes):
        for i in range(0,len(chunk_data_bytes)):
            chunk_data_bytes[i] = int(chunk_data_bytes[i],16)
        
        chunk_data = np.array(chunk_data_bytes)
        chunk_data = np.reshape(chunk_data,(-1,3))
        self.meta_data.palette_entires = chunk_data
        image = []
        for i in range(0, int(len(chunk_data_bytes)/3)):
            image.append([(chunk_data_bytes[3*i],chunk_data_bytes[3*i+1],chunk_data_bytes[3*i+2])])
        plt.imshow(image)
        plt.show()

    def __parse_ifd_directory(self, offset, chunk_data_bytes):
        bytes_per_entry = 12
        crop_data = chunk_data_bytes[offset:]

        number_of_directory_entry = crop_data[0:2]
        number_of_directory_entry = "".join(number_of_directory_entry)
        number_of_directory_entry = int(number_of_directory_entry, 16)

        crop_data=crop_data[2:]

        dir_entry = [[0] * bytes_per_entry] * number_of_directory_entry
        for i in range(0, number_of_directory_entry):
            for j in range(0,bytes_per_entry):
                dir_entry[i][j] = crop_data[i*bytes_per_entry+j]

        end_of_data = number_of_directory_entry * bytes_per_entry
        offset_to_next_ifd = crop_data[end_of_data : end_of_data + 4]
        offset_to_next_ifd = "".join(offset_to_next_ifd)
        offset_to_next_ifd = int(offset_to_next_ifd, 16)

        return offset_to_next_ifd, dir_entry

    def __parse_data_format_entry(self, data_entry):
        tag_number = "".join(data_entry[0:2])
        data_format = "".join(data_entry[2:4])
        data_format = int(data_format,16)
        number_of_components = "".join(data_entry[4:8])
        number_of_components = int(number_of_components,16)

        bytes_per_component = 1
        if data_format == 3 or data_format == 8:
            bytes_per_component = 2
        elif data_format == 4 or data_format == 9 or data_format == 11:
            bytes_per_component = 4
        elif data_format == 5 or data_format == 10 or data_format == 12:
            bytes_per_component = 8

        is_data = True
        if bytes_per_component * number_of_components >= 4:
            is_data = False

        data_or_offset = "".join(data_entry[8:])

        return tag_number, data_or_offset, is_data

    def parse_exif_chunk(self, chunk_data_bytes):
        exif_info = ''
        bit_order = chunk_data_bytes[0:2]
        bit_order = "".join(bit_order)
        bit_order = bytes.fromhex(bit_order).decode()
        if bit_order == 'MM':
            exif_info += "Bit order: Motorola order \n"
        elif bit_order == 'II':
            exif_info += "Bit order: Intel order \n"

        tag_mark = chunk_data_bytes[2:4]
        tag_mark = "".join(tag_mark)
        if tag_mark == '002a':
            exif_info += "Exif has proper tag mark \n"
        else:
            exif_info += "Exif has unknown tag mark \n"
            return

        offset_to_next_ifd = chunk_data_bytes[4:8]
        offset_to_next_ifd = "".join(offset_to_next_ifd)
        offset_to_next_ifd = int(offset_to_next_ifd, 16)

        while offset_to_next_ifd != 0:
            offset_to_next_ifd, dir_entry = self.__parse_ifd_directory(offset_to_next_ifd, chunk_data_bytes)

            for entry in dir_entry:
                tag_number, data_or_offset, is_data = self.__parse_data_format_entry(entry)
                exif_info += "tag number:" + str(tag_number) + "\n"


        self._meta_data.exif_info = exif_info

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

    def parse_ztext_chunk(self, chunk_data_bytes):
        keyword = []
        value = []
        null_value_found = False
        for data in chunk_data_bytes:
            if data == '00' and not null_value_found:
                null_value_found = True
                continue

            if not null_value_found:
                keyword.append(data)

            if null_value_found:
                value.append(data)

        if value[0] == '00':
            value = ''.join(value[1:])
            value = bytes.fromhex(value)
            value = zlib.decompress(value)
            value = str(value, 'utf-8')
        else:
            print(" Unknown compress method in zTXt chunk")
            return

        keyword = ''.join(keyword)
        keyword = bytes.fromhex(keyword).decode()

        self.meta_data.textual_information_dict[keyword] = value

    def parse_time_chunk(self,chunk_data):
        year = int("".join(chunk_data[0:2]),16)
        month = int("".join(chunk_data[2:3]),16)
        day = int("".join(chunk_data[3:4]),16)
        hour = int("".join(chunk_data[4:5]),16)
        minute = int("".join(chunk_data[5:6]),16)
        second = int("".join(chunk_data[6:7]),16)
        try:
            time_of_modyfication = datetime.datetime(year=year,month=month,day=day,hour=hour,minute=minute,second=second)
        except ValueError:
            print('Invalid tIMe data')
            return

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
        print('XMP DATA:')
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


    def do_parsing(self):
        if self.check_if_file_header_is_proper() is False:
            raise ValueError("PNG file has not proper file header")

        start_position=8

        while True:
            length,chunk_type,chunk_data_bytes,end_position=self.read_chunk(start_position)
            self._chunk_positions.append((start_position, end_position, chunk_type))
            start_position=end_position

            #critical chunks:
    
            if chunk_type == "IEND":
                break

            if chunk_type == "IHDR":
                self.parse_ihdr_chunk(chunk_data_bytes)

            elif chunk_type == "PLTE":
                self.parse_plte_chunk(chunk_data_bytes)
            
            #and ancillary chunks:

            elif chunk_type == "eXIf":
                self.parse_exif_chunk(chunk_data_bytes)

            elif chunk_type == "tEXt":
                self.parse_text_chunk(chunk_data_bytes)

            elif chunk_type == 'zTXt':
                self.parse_ztext_chunk(chunk_data_bytes)

            elif chunk_type == "tIME":
                self.parse_time_chunk(chunk_data_bytes)

            elif chunk_type == "iTXt":
                self.parse_international_text_info(chunk_data_bytes)

            elif chunk_type == "gAMA":
                self.parse_gama_chunk(chunk_data_bytes)

            elif chunk_type == "pHYs":
                self.parse_physical_chunk(chunk_data_bytes)

    def save_with_anonimization(self,new_file_name:str):
        png_header = ['89', '50', '4e', '47', '0d', '0a', '1a', '0a']
        with open("img/" + new_file_name, 'wb') as file:
            for header_byte in png_header:
                file.write(bytes.fromhex(header_byte))
            for chunk in self._chunk_positions:
                start_position = chunk[0]
                if not chunk[2][0].islower():
                    for i in range(start_position, chunk[1]):
                        file.write(bytes.fromhex(self.__file_data[i]))
                else:
                    for i in range(start_position, start_position+8):
                        file.write(bytes.fromhex(self.__file_data[i]))
                    for i in range(start_position+8, chunk[1]):
                        file.write(bytes.fromhex('00'))

    def saveFile(self,new_file_name:str):
        with open("img/"+new_file_name,'wb') as file:
            for byte in self.__file_data:
                file.write(bytes.fromhex(byte))

