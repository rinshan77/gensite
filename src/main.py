import re
import os
import shutil

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


#def main():
#    dummy = TextNode("This is a text node", "bold", "https://www.boot.dev")
#    print(dummy)
#    leaf1 = LeafNode(tag="b", value="Bold text", props={"class": "bold-class"})
#    leaf2 = LeafNode(tag="i", value="Italic text", props={"id": "italic-id"})
#    leaf3 = LeafNode(tag="code", value="Code text", props={"style": "color: red;"})
#    parent_node = ParentNode(
#        tag="div", children=[leaf1, leaf2, leaf3], props={"class": "parent-div"}
#    )
#    print(parent_node.to_html())
#
#    text_type_text = "text"
#    text_type_code = "code"
#    text_type_bold = "bold"
#    text_type_italic = "italic"
#    node = TextNode("This is text with a `code block` word", text_type_text)
#    new_nodes = split_nodes_delimiter([node], "`", text_type_code)
#    for n in new_nodes:
#        print(n)
#    node_italics = TextNode("This is *italic* and this is not", text_type_text)
#    new_nodes_italics = split_nodes_delimiter([node_italics], "*", text_type_italic)
#    for n in new_nodes_italics:
#        print(n)
#    node_bold = TextNode("This is **bold** and this is not", text_type_text)
#    new_nodes_bold = split_nodes_delimiter([node_bold], "**", text_type_bold)
#    for n in new_nodes_bold:
#        print(n)
#
#    complex_node = TextNode(
#        "This is *italic* and **bold** with `code` text", text_type_text
#    )
#    nodes_after_code = split_nodes_delimiter([complex_node], "`", text_type_code)
#    nodes_after_bold = split_nodes_delimiter(nodes_after_code, "**", text_type_bold)
#    final_nodes = split_nodes_delimiter(nodes_after_bold, "*", text_type_italic)
#   for n in final_nodes:
#        print(n)
#    try:
#        unbalanced_node = TextNode("This `is unbalanced", text_type_text)
#        split_nodes_delimiter([unbalanced_node], "`", text_type_code)
#    except ValueError as e:
#        print(e)
#    plain_node = TextNode("This has no special delimiters", text_type_text)
#    plain_result = split_nodes_delimiter([plain_node], "`", text_type_code)
#    for n in plain_result:
#        print(n)
#    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
#    print(extract_markdown_images(text))
#    text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
#    print(extract_markdown_links(text))


def copy_static_to_public(src, dst):
    if not os.path.exists(dst):
        os.makedirs(dst)
    
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)
        
        if os.path.isdir(src_path):
            print(f"Copying directory: {src_path} to {dst_path}")
            copy_static_to_public(src_path, dst_path)
        else:
            print(f"Copying file: {src_path} to {dst_path}")
            shutil.copy(src_path, dst_path)

def extract_title(markdown):
    lines = markdown.split('\n')
    for line in lines:
        if line.startswith('# '):
            return line[2:].strip()
    raise Exception("No H1 header found")

def generate_page(from_path, template_path, dest_path):
    # Print the paths being used for the page generation
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read the markdown file
    with open(from_path, 'r') as f:
        markdown_content = f.read()

    # Read the template file
    with open(template_path, 'r') as f:
        template_content = f.read()

    # Convert markdown to HTML
    html_content = markdown_to_html_node(markdown_content).to_html()
    print(f"HTML Content: {html_content}")  # Debugging line, to ensure it has the desired HTML output

    # Extract the title from the markdown
    title = extract_title(markdown_content)
    print(f"Title: {title}")  # Debugging line, to ensure the title extraction works

    # Replace placeholders in the template
    final_content = template_content.replace('{{ Title }}', title)
    final_content = final_content.replace('{{ Content }}', html_content)
    print(f"Final Content: {final_content}")  # Debugging line, to verify the final content correctness

    # Write the final HTML to the destination
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(final_content)

    print(f"Page generated successfully at {dest_path}")


from markdown import markdown as md

def markdown_to_html_node(markdown):
    class HTMLNode:
        def __init__(self, content):
            self.content = md(content)
        
        def to_html(self):
            return self.content
            
    return HTMLNode(markdown)


def main():
    # Step 1: Delete everything in the `public` directory
    public_dir = 'public'
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    os.makedirs(public_dir)

    # Step 2: Copy all static files from `static` to `public`
    static_dir = 'static'
    if os.path.exists(static_dir):
        shutil.copytree(static_dir, public_dir, dirs_exist_ok=True)

    # Step 3: Generate a page from `content/index.md` using `template.html` and write it to `public/index.html`
    content_path = 'content/index.md'
    template_path = 'template.html'
    output_path = os.path.join(public_dir, 'index.html')

    generate_page(content_path, template_path, output_path)

if __name__ == "__main__":
    main()

