import unittest
from textnode import TextNode
from splitfuncs import split_nodes_link, split_nodes_image, split_nodes_delimiter
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

if __name__ == "__main__":
    unittest.main()