from htmlnode import HTMLNode
import unittest

class TestHTMLNode(unittest.TestCase):
    def test_props_1(self):
        props = {
            "href" : "https://www.bootdev.com",
            "target" : "_blank"
        }
        node = HTMLNode(props=props)
        node_props_html = node.props_to_html()

        expected = ' href="https://www.bootdev.com" target="_blank"'
        
        self.assertEqual(node_props_html, expected)


if __name__ == "__main__":
    unittest.main()