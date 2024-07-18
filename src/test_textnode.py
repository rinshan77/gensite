import unittest
from textnode import TextNode, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestTextNode(unittest.TestCase):
    def test_image_node(self):
        text_node = TextNode("image.jpg", "image")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.props.get('src'), "image.jpg")
        self.assertEqual(html_node.props.get('alt'), "Image")
    
    def test_link_node(self):
        text_node = TextNode("Anchor text", "link", "https://example.com")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Anchor text")
        self.assertEqual(html_node.props.get('href'), "https://example.com")

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
    
    def test_text_node_to_leaf_node(self):
        # Normal text
        normal_text_node = TextNode("Hello, World!", "text")
        self.assertEqual(text_node_to_html_node(normal_text_node), LeafNode(None, "Hello, World!"))

        # Bold text
        bold_text_node = TextNode("Hello, Bold World!", "bold")
        self.assertEqual(text_node_to_html_node(bold_text_node), LeafNode("b", "Hello, Bold World!"))

        # Italic text
        italic_text_node = TextNode("Hello, Italic World!", "italic")
        self.assertEqual(text_node_to_html_node(italic_text_node), LeafNode("i", "Hello, Italic World!"))

        # Code text
        code_text_node = TextNode("print('Hello, Code World!')", "code")
        self.assertEqual(text_node_to_html_node(code_text_node), LeafNode("code", "print('Hello, Code World!')"))

        # Link text
        link_text_node = TextNode("Anchor text", "link", "https://example.com")
        self.assertEqual(
            text_node_to_html_node(link_text_node),
            HTMLNode("a", "Anchor text", props={"href": "https://example.com"})
        )

        # Image text
        image_text_node = TextNode("image.jpg", "image")
        self.assertEqual(
            text_node_to_html_node(image_text_node),
            HTMLNode("img", "", props={"src": "image.jpg", "alt": "Image"})
        )

        
if __name__ == "__main__":
    unittest.main()
