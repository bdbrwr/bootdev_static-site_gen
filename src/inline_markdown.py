from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        sections = node.text.split(delimiter)
        if len(sections) %2 == 0:
            raise ValueError("Formatted section not closed")
        for i, v in enumerate(sections):
            if v == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(v, TextType.TEXT))
            else:
                new_nodes.append(TextNode(v, text_type))

    return new_nodes