import unittest
from blocktypes import markdown_to_html_node
from htmlnode import HTMLNode


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_heading(self):
        markdown = "# Heading"
        html_node = markdown_to_html_node(markdown)
        expected = HTMLNode(
            "div",
            children=[
                HTMLNode("h1", children=[HTMLNode("span", children=["Heading"])])
            ],
        )
        self.assertEqual(html_node, expected)

    def test_code(self):
        markdown = "```\ncode block\n```"
        html_node = markdown_to_html_node(markdown)
        expected = HTMLNode(
            "div",
            children=[
                HTMLNode("pre", children=[HTMLNode("code", children=["code block"])])
            ],
        )
        self.assertEqual(html_node, expected)

    def test_quote(self):
        markdown = "> This is a quote"
        html_node = markdown_to_html_node(markdown)
        expected = HTMLNode(
            "div",
            children=[
                HTMLNode(
                    "blockquote",
                    children=[HTMLNode("span", children=["This is a quote"])],
                )
            ],
        )
        self.assertEqual(html_node, expected)

    def test_unordered_list(self):
        markdown = "* Item 1\n* Item 2\n* Item 3"
        html_node = markdown_to_html_node(markdown)
        expected = HTMLNode(
            "div",
            children=[
                HTMLNode(
                    "ul",
                    children=[
                        HTMLNode(
                            "li", children=[HTMLNode("span", children=["Item 1"])]
                        ),
                        HTMLNode(
                            "li", children=[HTMLNode("span", children=["Item 2"])]
                        ),
                        HTMLNode(
                            "li", children=[HTMLNode("span", children=["Item 3"])]
                        ),
                    ],
                )
            ],
        )
        self.assertEqual(html_node, expected)

    def test_ordered_list(self):
        markdown = "1. Item 1\n2. Item 2\n3. Item 3"
        html_node = markdown_to_html_node(markdown)
        expected = HTMLNode(
            "div",
            children=[
                HTMLNode(
                    "ol",
                    children=[
                        HTMLNode(
                            "li", children=[HTMLNode("span", children=["Item 1"])]
                        ),
                        HTMLNode(
                            "li", children=[HTMLNode("span", children=["Item 2"])]
                        ),
                        HTMLNode(
                            "li", children=[HTMLNode("span", children=["Item 3"])]
                        ),
                    ],
                )
            ],
        )
        self.assertEqual(html_node, expected)

    def test_paragraph(self):
        markdown = "This is a paragraph."
        html_node = markdown_to_html_node(markdown)
        expected = HTMLNode(
            "div",
            children=[
                HTMLNode(
                    "p", children=[HTMLNode("span", children=["This is a paragraph."])]
                )
            ],
        )
        self.assertEqual(html_node, expected)


if __name__ == "__main__":
    unittest.main()
