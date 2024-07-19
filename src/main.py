import re
from textnode import (
    TextNode,
    text_node_to_html_node,
    extract_markdown_images,
    extract_markdown_links,
    text_to_textnodes,
)
from splitfuncs import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    markdown_to_blocks,
    block_to_block_type,
)
from htmlnode import HTMLNode, LeafNode, ParentNode
from blocktypes import markdown_to_html_node, create_block_node


def main():
    dummy = TextNode("This is a text node", "bold", "https://www.boot.dev")
    print(dummy)
    leaf1 = LeafNode(tag="b", value="Bold text", props={"class": "bold-class"})
    leaf2 = LeafNode(tag="i", value="Italic text", props={"id": "italic-id"})
    leaf3 = LeafNode(tag="code", value="Code text", props={"style": "color: red;"})
    parent_node = ParentNode(
        tag="div", children=[leaf1, leaf2, leaf3], props={"class": "parent-div"}
    )
    print(parent_node.to_html())

    text_type_text = "text"
    text_type_code = "code"
    text_type_bold = "bold"
    text_type_italic = "italic"
    node = TextNode("This is text with a `code block` word", text_type_text)
    new_nodes = split_nodes_delimiter([node], "`", text_type_code)
    for n in new_nodes:
        print(n)
    node_italics = TextNode("This is *italic* and this is not", text_type_text)
    new_nodes_italics = split_nodes_delimiter([node_italics], "*", text_type_italic)
    for n in new_nodes_italics:
        print(n)
    node_bold = TextNode("This is **bold** and this is not", text_type_text)
    new_nodes_bold = split_nodes_delimiter([node_bold], "**", text_type_bold)
    for n in new_nodes_bold:
        print(n)

    complex_node = TextNode(
        "This is *italic* and **bold** with `code` text", text_type_text
    )
    nodes_after_code = split_nodes_delimiter([complex_node], "`", text_type_code)
    nodes_after_bold = split_nodes_delimiter(nodes_after_code, "**", text_type_bold)
    final_nodes = split_nodes_delimiter(nodes_after_bold, "*", text_type_italic)
    for n in final_nodes:
        print(n)
    try:
        unbalanced_node = TextNode("This `is unbalanced", text_type_text)
        split_nodes_delimiter([unbalanced_node], "`", text_type_code)
    except ValueError as e:
        print(e)
    plain_node = TextNode("This has no special delimiters", text_type_text)
    plain_result = split_nodes_delimiter([plain_node], "`", text_type_code)
    for n in plain_result:
        print(n)
    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    print(extract_markdown_images(text))
    text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    print(extract_markdown_links(text))


if __name__ == "__main__":
    main()
