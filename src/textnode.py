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
        # Assuming text_node.text is a tuple (anchor_text, href)
        return LeafNode(tag, text_node.text[0], {"href": text_node.text[1]})
    elif tag == "img":
        # Assuming text_node.text is a tuple (src, alt)
        return LeafNode(tag, "", {"src": text_node.text[0], "alt": text_node.text[1]})
    else:
        return LeafNode(tag, text_node.text)