import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_print(self):
        node = HTMLNode("a", "b", "c", "d")
        print(node)

    def test_constructor(self):
        node = HTMLNode(tag="p", value="Hello", children=[], props={"class": "text"})
        print(node)
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"class": "text"})

    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.example.com", "target": "_blank"})
        self.assertEqual(
            node.props_to_html(), 'href="https://www.example.com" target="_blank"'
        )

    def test_repr(self):
        node = HTMLNode(
            tag="a", value="Link", children=[], props={"href": "https://example.com"}
        )
        repr_str = repr(node)
        expected_repr = "HTMLNode(tag='a', value='Link', children=[], props={'href': 'https://example.com'})"
        self.assertEqual(repr_str, expected_repr)

    def test_empty_children_defaults(self):
        node = HTMLNode(tag="div")
        self.assertEqual(node.children, [])

    def test_empty_props_defaults(self):
        node = HTMLNode(tag="img")
        self.assertEqual(node.props, {})


class TestLeafNode(unittest.TestCase):
    def test_leaf_node_no_tag_returns_value(self):
        node = LeafNode(tag=None, value="Just text")
        result = node.to_html()
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_node_with_tag_renders_correct_html(self):
        node = LeafNode(tag="p", value="This is a paragraph.")
        result = node.to_html()
        print(result)
        self.assertEqual(node.to_html(), "<p>This is a paragraph.</p>")

    def test_leaf_node_with_tag_and_props_renders_correct_html(self):
        node = LeafNode(
            tag="a", value="Click me!", props={"href": "https://www.google.com"}
        )
        result = node.to_html()

        print("Generated HTML:", result)

        expected_html = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(result, expected_html)

    def test_leaf_node_empty_props(self):
        node = LeafNode(tag="div", value="Content")
        result = node.to_html()
        print(result)
        self.assertEqual(node.to_html(), "<div>Content</div>")

    def test_leaf_node_repr(self):
        node = LeafNode(tag="a", value="Link", props={"href": "https://example.com"})
        expected_repr = "HTMLNode(tag='a', value='Link', children=[], props={'href': 'https://example.com'})"
        result = node.to_html()
        print(result)
        print(node)
        self.assertEqual(repr(node), expected_repr)

    def test_leaf_node_no_tag_renders_value(self):
        node = LeafNode(tag=None, value="Just text", props=None)
        result = node.to_html()

        print("Generated HTML without tag:", result)

        expected_html = "Just text"
        self.assertEqual(result, expected_html)


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_invalid_tag(self):
        with self.assertRaises(ValueError) as cm:
            ParentNode(None, [LeafNode("b", "Bold text")])
        self.assertEqual(str(cm.exception), "Needs tag value.")

    def test_no_children(self):
        with self.assertRaises(ValueError) as cm:
            ParentNode("p", [])
        self.assertEqual(str(cm.exception), "Needs children value.")

    def test_nested_nodes(self):
        nested_node = ParentNode(
            "div",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                    ],
                ),
                LeafNode("i", "Italic text"),
            ],
        )
        self.assertEqual(
            nested_node.to_html(),
            "<div><p><b>Bold text</b>Normal text</p><i>Italic text</i></div>",
        )


if __name__ == "__main__":
    unittest.main()
