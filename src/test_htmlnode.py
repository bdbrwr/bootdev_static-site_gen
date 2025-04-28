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
    
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")



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
    
    def test_to_html_with_multiple_children(self):
        child_node1 = LeafNode("span", "child1")
        child_node2 = LeafNode("span", "child2")
        parent_node = ParentNode("div", [child_node1]+[child_node2])
        self.assertEqual(parent_node.to_html(), "<div><span>child1</span><span>child2</span></div>")

    def test_to_html_with_grandgrandchildren(self):
        grandgrandchild_node = LeafNode("b", "grandgrandchild")
        grandchild_node = ParentNode("p", [grandgrandchild_node])
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><p><b>grandgrandchild</b></p></span></div>",
        )

    def test_to_html_with_multiple_children_to_grandchildren(self):
        grandchild_node1 = LeafNode("b", "grandchild1")
        grandchild_node2 = LeafNode("b", "grandchild2")
        child_node1 = ParentNode("span", [grandchild_node1])
        child_node2 = ParentNode("span", [grandchild_node2])
        parent_node = ParentNode("div", [child_node1]+[child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild1</b></span><span><b>grandchild2</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )


if __name__ == "__main__":
    unittest.main()