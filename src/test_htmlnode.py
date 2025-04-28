from htmlnode import HTMLNode
import unittest

class TestHTMLNode(unittest.TestCase):
    def test_props_1(self):
        props = {
            "href" : "https://www.bootdev.com",
            "target" : "_blank"
        }
        node = HTMLNode(props=props)
        actual = node.props_to_html()

        expected = ' href="https://www.bootdev.com" target="_blank"'
        
        self.assertEqual(actual, expected)

    def test_error(self):
        # Learning Note: This is the sintax to check for a speicific error type. Could also generally check with Exception

        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr(self):
        node = HTMLNode("a")

        actual = repr(node)
        expected = "HTMLNode(self.tag='a', self.value=None, self.children=None, self.props=None)"
        
        # Learning Note: repr uses single quotes for strings by default. There's a workaround with calling repr on the element itself, but I didn't implement this here.

        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()