from split_nodes_delimiter import split_nodes_delimiter
from textnode import *
import unittest

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        old_nodes = [TextNode("a,b,c", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, ",", TextType.LINK) 
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "a")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "b")
        self.assertEqual(new_nodes[1].text_type, TextType.LINK)
        self.assertEqual(new_nodes[2].text, "c")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
    
    def test_split_nodes_delimiter_empty_and_filled(self):
        old_nodes = TextNode("", TextType.TEXT)
        old_nodes2 = TextNode("a,b,c", TextType.TEXT)
        old_nodes3 = TextNode("", TextType.IMAGE)
        node_list = [old_nodes, old_nodes2, old_nodes3]
        new_nodes = split_nodes_delimiter(node_list, ",", TextType.LINK) 
        self.assertEqual(len(new_nodes), 3)
    
    def test_split_nodes_delimiter_bold(self):
        old_nodes = [TextNode("a**b**c", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "a")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "b")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, "c")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

if __name__ == "__main__":
    unittest.main()