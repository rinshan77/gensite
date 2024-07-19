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


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    root = HTMLNode("div")

    for block in blocks:
        block_type = block_to_block_type(block)
        block_node = create_block_node(block, block_type)
        root.children.append(block_node)

    return root


def create_block_node(block, block_type):
    if block_type == "heading":
        return create_heading_node(block)
    elif block_type == "code":
        return create_code_node(block)
    elif block_type == "quote":
        return create_quote_node(block)
    elif block_type == "unordered_list":
        return create_unordered_list_node(block)
    elif block_type == "ordered_list":
        return create_ordered_list_node(block)
    elif block_type == "paragraph":
        return create_paragraph_node(block)
    else:
        raise ValueError(f"Unknown block type: {block_type}")


def create_heading_node(block):
    level = block.count("#")
    text = block[level + 1 :]
    heading_node = HTMLNode(f"h{level}", children=text_to_children(text))
    return heading_node


def create_code_node(block):
    # First remove the triple backticks and then strip the newlines
    code_text = block.strip("`").strip("\n")
    pre_node = HTMLNode("pre")
    code_node = HTMLNode("code", children=[code_text])
    pre_node.children.append(code_node)
    return pre_node


def create_quote_node(block):
    lines = block.split("\n")
    quote_text = "\n".join([line[2:] for line in lines])
    blockquote_node = HTMLNode("blockquote", children=text_to_children(quote_text))
    return blockquote_node


def create_unordered_list_node(block):
    lines = block.split("\n")
    ul_node = HTMLNode("ul")
    for line in lines:
        li_text = line[2:]  # Remove the '* ' or '- ' prefix
        li_node = HTMLNode("li", children=text_to_children(li_text))
        ul_node.children.append(li_node)
    return ul_node


def create_ordered_list_node(block):
    lines = block.split("\n")
    ol_node = HTMLNode("ol")
    for line in lines:
        li_text = line.split(". ", 1)[1]  # Get text after the 'number. ' prefix
        li_node = HTMLNode("li", children=text_to_children(li_text))
        ol_node.children.append(li_node)
    return ol_node


def create_paragraph_node(block):
    p_node = HTMLNode("p", children=text_to_children(block))
    return p_node


def text_to_children(text):
    return [HTMLNode("span", children=[text])]
