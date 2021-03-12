import sys
from project.PNGFileParser import PngFileParser
from project.FileParser import FileParser

import unittest


class TestPNGFileParser(unittest.TestCase):

   png_parser = PngFileParser()

   def test_reading_invalid_file(self):
      parser=PngFileParser()
      with self.assertRaises(FileNotFoundError):
         parser.readFile("test")
      
   def test_file_with_proper_file_header(self):
      
      self.png_parser.readFile("test.png")
      self.assertTrue(self.png_parser.check_if_file_header_is_proper()) 

   def test_file_with_known_first_chunk(self):
      self.png_parser.readFile("test.png")
      results=self.png_parser.read_chunk(8)
      self.assertEqual(13,results[0])
      self.assertEqual("IHDR",results[1])
      known_first_chunk_data=['00', '00', '08', 'ea', '00', '00', '07', '93', '08', '06', '00', '00','00']
      self.assertListEqual(results[2],known_first_chunk_data)


if __name__ == '__main__':
   unittest.main()
