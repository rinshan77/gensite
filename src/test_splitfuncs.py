import unittest
from textnode import TextNode
from splitfuncs import split_nodes_link, split_nodes_image, split_nodes_delimiter, markdown_to_blocks, block_to_block_type
from test_htmlnode import HTMLNode, LeafNode, ParentNode


class TestSplitNodes(unittest.TestCase):

    def test_split_nodes_link(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", "text")
        new_nodes = split_nodes_link([node])
        expected_nodes = [
            TextNode("This is text with a link ", "text"),
            TextNode("to boot dev", "link", "https://www.boot.dev"),
            TextNode(" and ", "text"),
            TextNode("to youtube", "link", "https://www.youtube.com/@bootdotdev")
        ]
        self.assertEqual(new_nodes, expected_nodes, f"Expected {expected_nodes}, got {new_nodes}")

        # Test case 2: No links in text
        node = TextNode("This is text with no links", "text")
        new_nodes = split_nodes_link([node])
        expected_nodes = [node]
        self.assertEqual(new_nodes, expected_nodes, f"Expected {expected_nodes}, got {new_nodes}")

        # Test case 3: Multiple links and text
        node = TextNode("Check [Google](https://www.google.com) and [GitHub](https://github.com)", "text")
        new_nodes = split_nodes_link([node])
        expected_nodes = [
            TextNode("Check ", "text"),
            TextNode("Google", "link", "https://www.google.com"),
            TextNode(" and ", "text"),
            TextNode("GitHub", "link", "https://github.com")
        ]
        self.assertEqual(new_nodes, expected_nodes, f"Expected {expected_nodes}, got {new_nodes}")

        # Test case 4: Edge case with empty text
        node = TextNode("", "text")
        new_nodes = split_nodes_link([node])
        expected_nodes = [node]
        self.assertEqual(new_nodes, expected_nodes, f"Expected {expected_nodes}, got {new_nodes}")

        # Test case 5: Text node with no links but other text types
        node = TextNode("Just some bold text", "bold")
        new_nodes = split_nodes_link([node])
        expected_nodes = [node]
        self.assertEqual(new_nodes, expected_nodes, f"Expected {expected_nodes}, got {new_nodes}")

    def test_split_nodes_image(self):
        # Test case 1: Basic functionality
        node = TextNode(
            "This is text with an image ![banner](https://www.example.com/banner.jpg) and more text",
            "text"
        )
        new_nodes = split_nodes_image([node])
        expected_nodes = [
            TextNode("This is text with an image ", "text"),
            TextNode("banner", "image", "https://www.example.com/banner.jpg"),
            TextNode(" and more text", "text")
        ]
        self.assertEqual(new_nodes, expected_nodes, f"Expected {expected_nodes}, got {new_nodes}")

        # Test case 2: No images in text
        node = TextNode("This is text with no images", "text")
        new_nodes = split_nodes_image([node])
        expected_nodes = [node]
        self.assertEqual(new_nodes, expected_nodes, f"Expected {expected_nodes}, got {new_nodes}")

        # Test case 3: Multiple images and text
        node = TextNode("Here is ![image1](https://example.com/img1.jpg) and ![image2](https://example.com/img2.jpg)", "text")
        new_nodes = split_nodes_image([node])
        expected_nodes = [
            TextNode("Here is ", "text"),
            TextNode("image1", "image", "https://example.com/img1.jpg"),
            TextNode(" and ", "text"),
            TextNode("image2", "image", "https://example.com/img2.jpg")
        ]
        self.assertEqual(new_nodes, expected_nodes, f"Expected {expected_nodes}, got {new_nodes}")

        # Test case 4: Edge case with empty text
        node = TextNode("", "text")
        new_nodes = split_nodes_image([node])
        expected_nodes = [node]
        self.assertEqual(new_nodes, expected_nodes, f"Expected {expected_nodes}, got {new_nodes}")

        # Test case 5: Text node with no images but other text types
        node = TextNode("Just some italic text", "italic")
        new_nodes = split_nodes_image([node])
        expected_nodes = [node]
        self.assertEqual(new_nodes, expected_nodes, f"Expected {expected_nodes}, got {new_nodes}")

class TestMarkdownToBlocks(unittest.TestCase):

    def test_basic_functionality(self):
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        
        expected_blocks = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        ]
        
        self.assertEqual(markdown_to_blocks(markdown), expected_blocks)

    def test_leading_and_trailing_whitespace(self):
        markdown = """   # Heading with leading whitespace   

   Paragraph with leading and trailing whitespace    
"""
        expected_blocks = [
            "# Heading with leading whitespace",
            "Paragraph with leading and trailing whitespace"
        ]
        
        self.assertEqual(markdown_to_blocks(markdown), expected_blocks)

    def test_excessive_newlines(self):
        markdown = """# Heading

Paragraph


"""
        expected_blocks = [
            "# Heading",
            "Paragraph"
        ]
        
        self.assertEqual(markdown_to_blocks(markdown), expected_blocks)

    def test_empty_string(self):
        markdown = ""
        expected_blocks = []
        self.assertEqual(markdown_to_blocks(markdown), expected_blocks)

    def test_multiple_consecutive_newlines(self):
        markdown = """# Heading



Paragraph with multiple new lines after it before this line."""
        
        expected_blocks = [
            "# Heading",
            "Paragraph with multiple new lines after it before this line."
        ]
        
        self.assertEqual(markdown_to_blocks(markdown), expected_blocks)

    def test_no_blocks(self):
        markdown = """


"""
        expected_blocks = []
        self.assertEqual(markdown_to_blocks(markdown), expected_blocks)

class TestBlockToBlockType(unittest.TestCase):

    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading"), "heading")
        self.assertEqual(block_to_block_type("## Subheading"), "heading")
        self.assertEqual(block_to_block_type("### Another Subheading"), "heading")

    def test_code(self):
        self.assertEqual(block_to_block_type("```\ncode block\n```"), "code")
        self.assertEqual(block_to_block_type("```\nmultiline\ncode\nblock\n```"), "code")

    def test_quote(self):
        self.assertEqual(block_to_block_type("> This is a quote"), "quote")
        self.assertEqual(block_to_block_type("> This is a multiline\n> quote block"), "quote")

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("* Item 1\n* Item 2\n* Item 3"), "unordered_list")
        self.assertEqual(block_to_block_type("- Item 1\n- Item 2\n- Item 3"), "unordered_list")
    
    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. Item 1\n2. Item 2\n3. Item 3"), "ordered_list")
        self.assertEqual(block_to_block_type("1. First item\n2. Second item\n3. Third item"), "ordered_list")

    def test_paragraph(self):
        self.assertEqual(block_to_block_type("This is just a regular paragraph of text."), "paragraph")
        self.assertEqual(block_to_block_type("Another line of regular text."), "paragraph")

    def test_mixed_content(self):
        # Should return paragraph as it doesn't match any specific block types
        self.assertEqual(block_to_block_type("#Not actually a heading"), "paragraph")
        self.assertEqual(block_to_block_type("1.This doesn't meet the ordered list format"), "paragraph")


if __name__ == "__main__":
    unittest.main()