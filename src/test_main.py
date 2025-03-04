from main import *
from textnode import *
from htmlnode import *
import unittest

class TestMain(unittest.TestCase):
    
    def test_extract_title(self):
        markdown = "# Title\n\nSome content."
        self.assertEqual(extract_title(markdown), "Title")
    
    def test_extract_title_no_title(self):
        markdown = "Some content."
        with self.assertRaises(ValueError):
            extract_title(markdown)
    
    def test_extract_title_multiple_lines(self):
        markdown = "# Title\n\n## Subtitle\nSome content."
        self.assertEqual(extract_title(markdown), "Title")



if __name__ == "__main__":
    unittest.main()