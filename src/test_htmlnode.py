from htmlnode import HTMLNode, LeafNode, ParentNode
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

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Best programming course", {"href": "https://www.bootdev.com"})
        expected = ('<a href="https://www.bootdev.com">Best programming course</a>')
        self.assertEqual(node.to_html(), expected)

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    unittest.main()