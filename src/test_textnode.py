import unittest
from textnode import TextNode, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_text_node(self):
        text_node = TextNode("Simple text", "text")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.value, "Simple text")

    def test_bold_node(self):
        text_node = TextNode("Bold text", "bold")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.value, "Bold text")

    def test_italic_node(self):
        text_node = TextNode("Italic text", "italic")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.value, "Italic text")

    def test_link_node(self):
        text_node = TextNode(("Anchor text", "https://example.com"), "link")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.value, "Anchor text")
        self.assertEqual(html_node.props['href'], "https://example.com")

    def test_image_node(self):
        text_node = TextNode(("image.jpg", "Alt text"), "image")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.props['src'], "image.jpg")
        self.assertEqual(html_node.props['alt'], "Alt text")

    def test_code_node(self):
        text_node = TextNode("Code text", "code")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.value, "Code text")

    def test_invalid_node(self):
        text_node = TextNode("Invalid text", "unknown")
        with self.assertRaises(ValueError):
            text_node_to_html_node(text_node)

    def test_repr(self):
        node = TextNode("This is a text node", "bold", "https://www.boot.dev")
        expected_repr = "TextNode(This is a text node, bold, https://www.boot.dev)"
        self.assertEqual(repr(node), expected_repr)

        node_without_url = TextNode("Another text node", "italic")
        expected_repr_without_url = "TextNode(Another text node, italic, None)"
        self.assertEqual(repr(node_without_url), expected_repr_without_url)

class TestTextNodeToHtmlNode(unittest.TestCase):
    
    def test_text_node(self):
        text_node = TextNode("Simple text", "text")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.value, "Simple text")

    def test_bold_node(self):
        text_node = TextNode("Bold text", "bold")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.value, "Bold text")

    def test_italic_node(self):
        text_node = TextNode("Italic text", "italic")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.value, "Italic text")

    def test_link_node(self):
        text_node = TextNode(("Anchor text", "https://example.com"), "link")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.value, "Anchor text")
        self.assertEqual(html_node.props['href'], "https://example.com")

    def test_image_node(self):
        text_node = TextNode(("image.jpg", "Alt text"), "image")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.props['src'], "image.jpg")
        self.assertEqual(html_node.props['alt'], "Alt text")

    def test_code_node(self):
        text_node = TextNode("Code text", "code")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.value, "Code text")

    def test_invalid_text_node(self):
        text_node = TextNode("Invalid text", "unknown")
        with self.assertRaises(ValueError):
            text_node_to_html_node(text_node)
        
if __name__ == "__main__":
    unittest.main()
