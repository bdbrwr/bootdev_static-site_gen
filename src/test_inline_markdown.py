import unittest
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links
)

from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_multiple_nodes(self):
        nodes = [
            TextNode("Bold ", TextType.BOLD),
            TextNode("Text with *Italics* in there", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("Bold ", TextType.BOLD),
                TextNode("Text with ", TextType.TEXT),
                TextNode("Italics", TextType.ITALIC),
                TextNode(" in there", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_even_more_multiple_nodes(self):
        nodes = [
            TextNode("Bold ", TextType.BOLD),
            TextNode("Text with *Italics* in there", TextType.TEXT),
            TextNode("And some code", TextType.CODE),
            TextNode("closing with more *Italics*", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("Bold ", TextType.BOLD),
                TextNode("Text with ", TextType.TEXT),
                TextNode("Italics", TextType.ITALIC),
                TextNode(" in there", TextType.TEXT),
                TextNode("And some code", TextType.CODE),
                TextNode("closing with more ", TextType.TEXT),
                TextNode("Italics", TextType.ITALIC)
            ],
            new_nodes,
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


    def test_extract_markdown_link(self):
        matches = extract_markdown_links(
            "This is a text with a [link](https://www.boot.dev)"
        )
        self.assertListEqual([("link", "https://www.boot.dev")], matches)
    

    def test_no_link_from_img(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)


    def test_extract_markdown_multiple_link(self):
        matches = extract_markdown_links(
            "This is a text with a [link](https://www.boot.dev) and [instagram](instagram.com/@bootdev)"
        )
        self.assertListEqual([("link", "https://www.boot.dev"), ("instagram", "instagram.com/@bootdev")], matches)
    
    
    def test_extraction_link_image_combined(self):
        text = "This is a text with a [link](https://www.boot.dev) and the ![logo](favicon.png) from their [instagram](instagram.com/@bootdev)"
        links = extract_markdown_links(text)
        images = extract_markdown_images(text)
        combined = links + images
        self.assertListEqual([("link", "https://www.boot.dev"), ("instagram", "instagram.com/@bootdev"), ("logo", "favicon.png")], combined)




if __name__ == "__main__":
    unittest.main()
