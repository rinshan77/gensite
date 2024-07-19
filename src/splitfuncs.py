import re
from htmlnode import HTMLNode, LeafNode, ParentNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    from textnode import TextNode
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

def split_nodes_image(old_nodes):
    from textnode import TextNode, extract_markdown_images
    new_nodes = []

    for node in old_nodes:
        if node.text_type == "text":
            current_text = node.text
            images = extract_markdown_images(current_text)
            
            if not images:
                # No images found, just append the original node
                new_nodes.append(node)
                continue

            # Split the text around each image
            for image_alt, image_url in images:
                parts = current_text.split(f"![{image_alt}]({image_url})", 1)
                if parts[0]:
                    new_nodes.append(TextNode(parts[0], "text"))
                new_nodes.append(TextNode(image_alt, "image", image_url))
                current_text = parts[1]

            # Append any remaining text after the last image
            if current_text:
                new_nodes.append(TextNode(current_text, "text"))
        else:
            new_nodes.append(node)

    return new_nodes


def split_nodes_link(old_nodes):
    from textnode import TextNode, extract_markdown_links
    new_nodes = []

    for node in old_nodes:
        if node.text_type == "text":
            current_text = node.text
            links = extract_markdown_links(current_text)
            
            if not links:
                # No links found, just append the original node
                new_nodes.append(node)
                continue

            # Split the text around each link
            for link_text, link_url in links:
                parts = current_text.split(f"[{link_text}]({link_url})", 1)
                if parts[0]:
                    new_nodes.append(TextNode(parts[0], "text"))
                new_nodes.append(TextNode(link_text, "link", link_url))
                current_text = parts[1]

            # Append any remaining text after the last link
            if current_text:
                new_nodes.append(TextNode(current_text, "text"))
        else:
            new_nodes.append(node)

    return new_nodes

def markdown_to_blocks(markdown):
    # Split the markdown text by double newlines
    blocks = markdown.split('\n\n')
    # Strip leading and trailing whitespace from each block
    blocks = [block.strip() for block in blocks]
    # Remove any empty blocks
    blocks = [block for block in blocks if block]
    return blocks

def block_to_block_type(block):
    # Check for heading
    if block.startswith("# ") or any(block.startswith(f"{'#' * i} ") for i in range(1, 7)):
        return "heading"
    
    # Check for code block
    if block.startswith("```") and block.endswith("```"):
        return "code"
    
    # Check for quote
    if all(line.startswith("> ") for line in block.split('\n')):
        return "quote"

    # Check for unordered list
    if all(line.startswith("* ") or line.startswith("- ") for line in block.split('\n')):
        return "unordered_list"

    # Check for ordered list
    lines = block.split('\n')
    if all(line.split(". ", 1)[0].isdigit() and int(line.split(". ", 1)[0]) == idx + 1 
           for idx, line in enumerate(lines)):
        return "ordered_list"

    return "paragraph"
