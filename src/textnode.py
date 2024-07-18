import re
from htmlnode import HTMLNode, LeafNode, ParentNode


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node):
    text_type_map = {
        "text": None,
        "bold": "b",
        "italic": "i",
        "code": "code",
        "link": "a",
        "image": "img",
    }

    tag = text_type_map.get(text_node.text_type)
    if tag is None and text_node.text_type != "text":
        raise ValueError("Invalid text type")

    if tag == "a":
        if text_node.url:
            return LeafNode(tag, text_node.text, {"href": text_node.url})
        else:
            raise ValueError("URL required for link text type")
    elif tag == "img":
        return LeafNode(tag, "", {"src": text_node.text, "alt": "Image"})
    else:
        return LeafNode(tag, text_node.text)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == "text":
            parts = node.text.split(delimiter)

            # Handle unbalanced delimiters
            if len(parts) % 2 == 0:
                raise ValueError(f"Unbalanced delimiter '{delimiter}' in text.")

            # Alternate between text_type_text and the provided text_type
            for i, part in enumerate(parts):
                if i % 2 == 0:
                    new_nodes.append(TextNode(part, "text"))
                else:
                    new_nodes.append(TextNode(part, text_type))
        else:
            # If not a "text" type node, add it unchanged
            new_nodes.append(node)

    return new_nodes
    

def extract_markdown_links(text):
    # Updated regex to match URLs with or without angle brackets
    pattern = r'\[(.*?)\]\(<(.*?)>\)|\[(.*?)\]\((.*?)\)'
    
    matches = re.findall(pattern, text)
    
    result = []
    for match in matches:
        if match[1]:  # Angle bracket case
            url = match[1].strip('<>')  # Clean angle brackets
            result.append((match[0], url))
        else:         # Parentheses case
            result.append((match[2], match[3]))

    return result


def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches
