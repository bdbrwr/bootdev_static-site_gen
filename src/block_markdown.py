from enum import Enum
import re
from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in blocks if block.strip() != ""]
    return blocks


def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].endswith("```"):
        return BlockType.CODE
    
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    
    return BlockType.PARAGRAPH


def list_node_to_html(block, type):
    lines = block.split("\n")
    if type == "ul":
        return f'<ul>{"".join([f"<li>{str[2:]}</li>" for str in lines])}</ul>'
    if type == "ol":
        return f'<ol>{"".join([f"<li>{str.split(".", maxsplit=1)[-1].strip()}</li>" for str in lines])}</ol>'


def heading_to_html_node(block):
    heading_number = len(block)-len(block.lstrip("#"))
    if heading_number > 6:
        raise ValueError(f"Invalid heading level: {heading_number}")
    heading_tag = f"h{heading_number}"
    text = block[heading_number:].strip()
    children = text_to_children(text)
    return ParentNode(heading_tag, children)


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def code_to_html_node(block):
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def quote_to_html_node(block):
    lines = [a[1:].strip() for a in block.split("\n")]
    text = " ".join(lines)
    chidlren = text_to_children(text)
    return ParentNode("blockquote", chidlren)   


def ulist_to_html_node(block):
    lines = block.split("\n")
    html_items = []
    for line in lines:
        text = line[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def olist_to_html_node(block):
    lines = block.split("\n")
    html_items = []
    for line in lines:
        text = line.split(".", maxsplit=1)[-1].strip()
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_type == BlockType.ULIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.OLIST:
        return olist_to_html_node(block)


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    content_html = []
    for block in blocks:
        content_html.append(block_to_html_node(block))
    return ParentNode("div", content_html)



def text_to_children(text):
    textnodes = text_to_textnodes(text)
    children = []
    for textnode in textnodes:
        html_node = text_node_to_html_node(textnode)
        children.append(html_node)
    return children
    