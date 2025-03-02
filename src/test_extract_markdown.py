from extract_markdown import *
import unittest

class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
            )
    
    def test_extract_markdown_both_empty(self):
        matches = extract_markdown_links(
            "This is text with no links or images"
        )
        self.assertListEqual([], matches)
        matches2 = extract_markdown_images(
            "This is text with no links or images"
        )
        self.assertListEqual([], matches2)
    
    def test_extract_markdown_multiple(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
            )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)
        matches2 = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![image2](https://i.imgur.com/zjjcJKZ2.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("image2", "https://i.imgur.com/zjjcJKZ2.png")], matches2)


class TestSplitNodes(unittest.TestCase):
    def test_split_nodes_image(self):
        nodes = [TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)]
        new_nodes = split_nodes_image(nodes)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "This is text with an ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "image")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[1].url, "https://i.imgur.com/zjjcJKZ.png")
    
    def test_split_nodes_image_empty(self):
        nodes = [TextNode("This is text with no images", TextType.TEXT)]
        new_nodes = split_nodes_image(nodes)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is text with no images")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
    
    def test_split_nodes_image_multiple(self):
        node1 = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![image2](https://i.imgur.com/zjjcJKZ2.png)", TextType.TEXT)
        node2 = TextNode("This is a test that has no images", TextType.TEXT)
        node3 = TextNode("This is text with an ![image](https://i.imgur.blahahblah) ", TextType.TEXT)
        node_list = [node1, node2, node3]
        new_nodes = split_nodes_image(node_list)
        self.assertEqual(len(new_nodes), 8)
        self.assertEqual(new_nodes[0].text, "This is text with an ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "image")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[1].url, "https://i.imgur.com/zjjcJKZ.png")
        self.assertEqual(new_nodes[2].text, " and ")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[3].text, "image2")
        self.assertEqual(new_nodes[3].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[3].url, "https://i.imgur.com/zjjcJKZ2.png")
        self.assertEqual(new_nodes[4].text, "This is a test that has no images")
        self.assertEqual(new_nodes[4].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[5].text, "This is text with an ")
        self.assertEqual(new_nodes[5].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[6].text, "image")
        self.assertEqual(new_nodes[6].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[6].url, "https://i.imgur.blahahblah")
        self.assertEqual(new_nodes[7].text, " ")
        self.assertEqual(new_nodes[7].text_type, TextType.TEXT)
    
    def test_split_nodes_link(self):
        nodes = [TextNode("This is text with a link [to boot dev](https://www.boot.dev)", TextType.TEXT)]
        new_nodes = split_nodes_link(nodes)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "This is text with a link ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "to boot dev")
        self.assertEqual(new_nodes[1].text_type, TextType.LINK)
        self.assertEqual(new_nodes[1].url, "https://www.boot.dev")

    def test_split_nodes_link_empty(self):
        nodes = [TextNode("This is text with no links", TextType.TEXT)]
        new_nodes = split_nodes_link(nodes)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is text with no links")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
    
    def test_split_nodes_link_multiple(self):
        node1 = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)
        node2 = TextNode("This is a test that has no links", TextType.TEXT)
        node3 = TextNode("This is text with a link [to google](https://www.google.com) ", TextType.TEXT)
        node_list = [node1, node2, node3]
        new_nodes = split_nodes_link(node_list)
        self.assertEqual(len(new_nodes), 8)
        self.assertEqual(new_nodes[0].text, "This is text with a link ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "to boot dev")
        self.assertEqual(new_nodes[1].text_type, TextType.LINK)
        self.assertEqual(new_nodes[1].url, "https://www.boot.dev")
        self.assertEqual(new_nodes[2].text, " and ")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[3].text, "to youtube")
        self.assertEqual(new_nodes[3].text_type, TextType.LINK)
        self.assertEqual(new_nodes[3].url, "https://www.youtube.com/@bootdotdev")
        self.assertEqual(new_nodes[4].text, "This is a test that has no links")
        self.assertEqual(new_nodes[4].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[5].text, "This is text with a link ")
        self.assertEqual(new_nodes[5].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[6].text, "to google")
        self.assertEqual(new_nodes[6].text_type, TextType.LINK)
        self.assertEqual(new_nodes[6].url, "https://www.google.com")
        self.assertEqual(new_nodes[7].text, " ")
        self.assertEqual(new_nodes[7].text_type, TextType.TEXT)
        
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

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
