from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        sections = node.text.split(delimiter)
        split_nodes = []
        if len(sections) %2 == 0:
            raise ValueError("Formatted section not closed")
        for i, v in enumerate(sections):
            if v == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(v, TextType.TEXT))
            else:
                split_nodes.append(TextNode(v, text_type))

        new_nodes.extend(split_nodes)

    return new_nodes

def extract_markdown_images(text):
    pattern = re.compile(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)")
    matches = pattern.findall(text)
    return matches


def extract_markdown_links(text):
    pattern = re.compile(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)")
    matches = pattern.findall(text)
    return matches