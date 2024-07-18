import re
import unittest
from textnode import TextNode, text_node_to_html_node, extract_markdown_images, extract_markdown_links
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestTextNode(unittest.TestCase):
    def test_image_node(self):
        text_node = TextNode("image.jpg", "image")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.props.get("src"), "image.jpg")
        self.assertEqual(html_node.props.get("alt"), "Image")

    def test_link_node(self):
        text_node = TextNode("Anchor text", "link", "https://example.com")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Anchor text")
        self.assertEqual(html_node.props.get("href"), "https://example.com")

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
        print(node)
        self.assertEqual(repr(node), expected_repr)

        node_without_url = TextNode("Another text node", "italic")
        expected_repr_without_url = "TextNode(Another text node, italic, None)"
        print(node_without_url)
        self.assertEqual(repr(node_without_url), expected_repr_without_url)


class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text_node_to_leaf_node(self):
        # Normal text
        normal_text_node = TextNode("Hello, World!", "text")
        self.assertEqual(
            text_node_to_html_node(normal_text_node), LeafNode(None, "Hello, World!")
        )

        # Bold text
        bold_text_node = TextNode("Hello, Bold World!", "bold")
        self.assertEqual(
            text_node_to_html_node(bold_text_node), LeafNode("b", "Hello, Bold World!")
        )

        # Italic text
        italic_text_node = TextNode("Hello, Italic World!", "italic")
        self.assertEqual(
            text_node_to_html_node(italic_text_node),
            LeafNode("i", "Hello, Italic World!"),
        )

        # Code text
        code_text_node = TextNode("print('Hello, Code World!')", "code")
        self.assertEqual(
            text_node_to_html_node(code_text_node),
            LeafNode("code", "print('Hello, Code World!')"),
        )

        # Link text
        link_text_node = TextNode("Anchor text", "link", "https://example.com")
        self.assertEqual(
            text_node_to_html_node(link_text_node),
            HTMLNode("a", "Anchor text", props={"href": "https://example.com"}),
        )

        # Image text
        image_text_node = TextNode("image.jpg", "image")
        self.assertEqual(
            text_node_to_html_node(image_text_node),
            HTMLNode("img", "", props={"src": "image.jpg", "alt": "Image"}),
        )

class TestMarkdownExtract(unittest.TestCase):
    def test_extract_markdown_images(self):
    # Test case 1: Basic functionality
        text1 = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result1 = extract_markdown_images(text1)
        expected1 = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        assert result1 == expected1, f"Expected {expected1}, got {result1}"

    # Test case 2: No images
        text2 = "This is text with no images."
        result2 = extract_markdown_images(text2)
        expected2 = []
        assert result2 == expected2, f"Expected {expected2}, got {result2}"

    # Test case 3: Edge case with empty alt text
        text3 = "Image with empty alt text ![](https://i.imgur.com/empty.gif)"
        result3 = extract_markdown_images(text3)
        expected3 = [("", "https://i.imgur.com/empty.gif")]
        assert result3 == expected3, f"Expected {expected3}, got {result3}"

        print("All tests for extract_markdown_images passed!")
    

    def test_extract_markdown_links(self):
        # Test case 1: Basic functionality
        text1 = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result1 = extract_markdown_links(text1)
        expected1 = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(result1, expected1, f"Expected {expected1}, got {result1}")

        # Test case 2: No links
        text2 = "This is text with no links."
        result2 = extract_markdown_links(text2)
        expected2 = []
        self.assertEqual(result2, expected2, f"Expected {expected2}, got {result2}")
                # Test case 3: Edge case with empty anchor text and URL
        text3 = "Link with empty anchor text [](<https://empty.link>)"
        result3 = extract_markdown_links(text3)
        expected3 = [("", "https://empty.link")]
        self.assertEqual(result3, expected3, f"Expected {expected3}, got {result3}")

        # Test case 4: Links with complex URLs
        text4 = "Here are [two](https://with-query.com?query=1) [complex](https://example.com/path/to/resource?param1=val1&param2=val2) links"
        result4 = extract_markdown_links(text4)
        expected4 = [("two", "https://with-query.com?query=1"), ("complex", "https://example.com/path/to/resource?param1=val1&param2=val2")]
        self.assertEqual(result4, expected4, f"Expected {expected4}, got {result4}")

        # Test case 5: Edge case with broken links
        text5 = "Link with no actual URL [broken]()"
        result5 = extract_markdown_links(text5)
        expected5 = [("broken", "")]
        self.assertEqual(result5, expected5, f"Expected {expected5}, got {result5}")

if __name__ == "__main__":
    unittest.main()
