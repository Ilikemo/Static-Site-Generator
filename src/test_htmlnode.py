from htmlnode import HTMLNode
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
        self.assertEqual(self.node.__repr__(), "div, Hello, World!, None, {'class': 'container', 'id': 'main'}")
    def test_props_to_html(self):
        self.assertEqual(self.node.props_to_html(), ' class="container" id="main"')



if __name__ == "__main__":
    unittest.main()