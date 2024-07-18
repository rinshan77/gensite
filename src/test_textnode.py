import unittest
from textnode import TextNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node1, node2)

    def test_not_equal_different_text(self):
        node1 = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a different text node", "bold")
        self.assertNotEqual(node1, node2)

    def test_not_equal(self):
        node1 = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a different text node", "bold")
        self.assertFalse(node1.__eq__ (node2))

    def test_not_equal_different_text_type(self):
        node1 = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italic")
        self.assertNotEqual(node1, node2)

    def test_not_equal_different_url(self):
        node1 = TextNode("This is a text node", "bold", "http://example.com")
        node2 = TextNode("This is a text node", "bold", "http://different.com")
        self.assertNotEqual(node1, node2)

    def test_eq_with_none_url(self):
        node1 = TextNode("This is a text node", "bold", None)
        node2 = TextNode("This is a text node", "bold", None)
        self.assertEqual(node1, node2)

    def test_eq_mixed_none_url(self):
        node1 = TextNode("This is a text node", "bold", None)
        node2 = TextNode("This is a text node", "bold", "http://example.com")
        self.assertNotEqual(node1, node2)

    def test_repr(self):
        node = TextNode("This is a text node", "bold", "https://www.boot.dev")
        expected_repr = "TextNode(This is a text node, bold, https://www.boot.dev)"
        self.assertEqual(repr(node), expected_repr)

        node_without_url = TextNode("Another text node", "italic")
        expected_repr_without_url = "TextNode(Another text node, italic, None)"
        self.assertEqual(repr(node_without_url), expected_repr_without_url)

if __name__ == "__main__":
    unittest.main()
