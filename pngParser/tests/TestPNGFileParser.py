import sys
from project.PNGFileParser import PngFileParser
from project.FileParser import FileParser

import unittest


class TestPNGFileParser(unittest.TestCase):

   def test_reading_invalid_file(self):
      parser=PngFileParser()
      with self.assertRaises(FileNotFoundError):
         parser.readFile("test")
      
   
        
if __name__ == '__main__':
   unittest.main()
