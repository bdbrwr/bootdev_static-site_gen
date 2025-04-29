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


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        matches = extract_markdown_images(node.text)
        if len(matches) == 0:
            new_nodes.append(node)
            continue

        remaining_text = node.text
        current_nodes = []

        for image_alt, image_url in matches:
            parts = remaining_text.split(f"![{image_alt}]({image_url})", 1)
            
            if parts[0] != "":
                current_nodes.append(TextNode(parts[0], TextType.TEXT))
            current_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))

            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""
        
        if remaining_text != "":
            current_nodes.append(TextNode(remaining_text, TextType.TEXT))

        new_nodes.extend(current_nodes)

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        matches = extract_markdown_links(node.text)
        if len(matches) == 0:
            new_nodes.append(node)
            continue

        remaining_text = node.text
        current_nodes = []

        for link_text, link_url in matches:
            parts = remaining_text.split(f"[{link_text}]({link_url})", 1)
            
            if parts[0] != "":
                current_nodes.append(TextNode(parts[0], TextType.TEXT))
            current_nodes.append(TextNode(link_text, TextType.LINK, link_url))

            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""
        
        if remaining_text != "":
            current_nodes.append(TextNode(remaining_text, TextType.TEXT))

        new_nodes.extend(current_nodes)

    return new_nodes