from textnode import TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode


def main():
    dummy = TextNode("This is a text node", "bold", "https://www.boot.dev")
    print(dummy)


if __name__ == "__main__":
    main()
