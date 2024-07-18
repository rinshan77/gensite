import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_print(self):
        node = HTMLNode("a", "b", "c", "d")
        print(node)
        
    def test_constructor(self):
        node = HTMLNode(tag="p", value="Hello", children=[], props={"class": "text"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"class": "text"})

    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.example.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), 'href="https://www.example.com" target="_blank"')

    def test_repr(self):
        node = HTMLNode(tag="a", value="Link", children=[], props={"href": "https://example.com"})
        repr_str = repr(node)
        expected_repr = "HTMLNode(tag='a', value='Link', children=[], props={'href': 'https://example.com'})"
        self.assertEqual(repr_str, expected_repr)
        
    def test_empty_children_defaults(self):
        node = HTMLNode(tag="div")
        self.assertEqual(node.children, [])
        
    def test_empty_props_defaults(self):
        node = HTMLNode(tag="img")
        self.assertEqual(node.props, {})

if __name__ == "__main__":
    unittest.main()