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
