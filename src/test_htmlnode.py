from htmlnode import *
import unittest

class TestHTMLNode(unittest.TestCase):
    def setUp(self):
        self.node = HTMLNode(tag="div", value="Hello, World!", children=None, props={"class": "container", "id": "main"})
    def test_init(self):
        self.assertEqual(self.node.tag, "div")
        self.assertEqual(self.node.value, "Hello, World!")
        self.assertIsNone(self.node.children)
        self.assertEqual(self.node.props, {"class": "container", "id": "main"})
    def test_repr(self):
        self.assertEqual(self.node.__repr__(), "HTMLNode(div, Hello, World!, children: None, {'class': 'container', 'id': 'main'})")
    def test_props_to_html(self):
        self.assertEqual(self.node.props_to_html(), ' class="container" id="main"')

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_leaf_to_html_props(self):
        node = LeafNode("h1", "Hello, world!", props={"class": "header"})
        node2 = LeafNode("h1", "Hello, world!")
        self.assertNotEqual(node, node2)
    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    
    def test_to_html_with_grandchildren1(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_with_grandchildren2(self):
        grandchild_node = LeafNode("b", "grandchild")
        grandchild_node2 = LeafNode("b", "grandchild2")
        child_node = ParentNode("span", [grandchild_node, grandchild_node2])
        child_node2 = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node, child_node2])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b><b>grandchild2</b></span><span>child</span></div>")

if __name__ == "__main__":
    unittest.main()