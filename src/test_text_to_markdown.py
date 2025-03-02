from textnode import *
from text_to_textnode import text_to_textnode
import unittest

class TestTextToTextNode(unittest.TestCase):
    def test_plain_text(self):
        result = text_to_textnode("This is a plain text")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "This is a plain text")
        self.assertEqual(result[0].text_type, TextType.TEXT)
    
    def test_bold_text(self):
        result = text_to_textnode("This is **bold** text")
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " text")
        self.assertEqual(result[2].text_type, TextType.TEXT)
    
    def test_italic_text(self):
        result = text_to_textnode("This is _italic_ text")
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "italic")
        self.assertEqual(result[1].text_type, TextType.ITALIC)
        self.assertEqual(result[2].text, " text")
        self.assertEqual(result[2].text_type, TextType.TEXT)
    
    def test_code_text(self):
        result = text_to_textnode("This is `code` text")
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "code")
        self.assertEqual(result[1].text_type, TextType.CODE)
        self.assertEqual(result[2].text, " text")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_image_text(self):
        result = text_to_textnode("This is ![alt text](image.jpg) text")
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "alt text")
        self.assertEqual(result[1].text_type, TextType.IMAGE)
        self.assertEqual(result[1].url, "image.jpg")
        self.assertEqual(result[2].text, " text")
        self.assertEqual(result[2].text_type, TextType.TEXT)
        
    def test_link_text(self):
        result = text_to_textnode("This is [link text](http://example.com) text")
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "link text")
        self.assertEqual(result[1].text_type, TextType.LINK)
        self.assertEqual(result[1].url, "http://example.com")
        self.assertEqual(result[2].text, " text")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_mixed_text(self):
        result = text_to_textnode("This is **bold** and _italic_ and `code` and ![alt text](image.jpg) and [link text](http://example.com) ")
        self.assertEqual(len(result), 11)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " and ")
        self.assertEqual(result[2].text_type, TextType.TEXT)
        self.assertEqual(result[3].text, "italic")
        self.assertEqual(result[3].text_type, TextType.ITALIC)
        self.assertEqual(result[4].text, " and ")
        self.assertEqual(result[4].text_type, TextType.TEXT)
        self.assertEqual(result[5].text, "code")
        self.assertEqual(result[5].text_type, TextType.CODE)
        self.assertEqual(result[6].text, " and ")
        self.assertEqual(result[6].text_type, TextType.TEXT)
        self.assertEqual(result[7].text, "alt text")
        self.assertEqual(result[7].text_type, TextType.IMAGE)
        self.assertEqual(result[7].url, "image.jpg")
        self.assertEqual(result[8].text, " and ")
        self.assertEqual(result[8].text_type, TextType.TEXT)
        self.assertEqual(result[9].text, "link text")
        self.assertEqual(result[9].text_type, TextType.LINK)
        self.assertEqual(result[9].url, "http://example.com")
        self.assertEqual(result[10].text, " ")
        self.assertEqual(result[10].text_type, TextType.TEXT)   

    def test_empty_text(self):
        result = text_to_textnode("")
        self.assertNotEqual(len(result), 1)
        
    def test_mixed_and_multiple_text(self):
        result = text_to_textnode("This is **bold** and _italic_ and `code` and ![alt text](image.jpg) and [link text](http://example.com) ![secondimage](blah.org)**bold**")
        self.assertEqual(len(result), 13)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " and ")
        self.assertEqual(result[2].text_type, TextType.TEXT)
        self.assertEqual(result[3].text, "italic")
        self.assertEqual(result[3].text_type, TextType.ITALIC)
        self.assertEqual(result[4].text, " and ")
        self.assertEqual(result[4].text_type, TextType.TEXT)
        self.assertEqual(result[5].text, "code")
        self.assertEqual(result[5].text_type, TextType.CODE)
        self.assertEqual(result[6].text, " and ")
        self.assertEqual(result[6].text_type, TextType.TEXT)
        self.assertEqual(result[7].text, "alt text")
        self.assertEqual(result[7].text_type, TextType.IMAGE)
        self.assertEqual(result[7].url, "image.jpg")
        self.assertEqual(result[8].text, " and ")
        self.assertEqual(result[8].text_type, TextType.TEXT)
        self.assertEqual(result[9].text, "link text")
        self.assertEqual(result[9].text_type, TextType.LINK)
        self.assertEqual(result[9].url, "http://example.com")
        self.assertEqual(result[10].text, " ")
        self.assertEqual(result[10].text_type, TextType.TEXT)
        self.assertEqual(result[11].text, "secondimage")
        self.assertEqual(result[11].text_type, TextType.IMAGE)
        self.assertEqual(result[11].url, "blah.org")
        self.assertEqual(result[12].text, "bold")
        self.assertEqual(result[12].text_type, TextType.BOLD)
        


if __name__ == "__main__":
    unittest.main()