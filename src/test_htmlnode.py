import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )
    
    def test_empty_dict_props(self):
        """Tests props_to_html when the props dictionary is empty."""
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_single_property(self):
        """Tests output format for a single key-value pair."""
        props = {'href': 'https://www.google.com'}
        node = HTMLNode(props=props)
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_multiple_properties(self):
        """Tests output format for multiple key-value pairs."""
        props = {'href': 'https://www.google.com', 'target': '_blank'}
        node = HTMLNode(props=props)
        self.assertEqual(' href="https://www.google.com" target="_blank"', node.props_to_html())

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )

if __name__ == "__main__":
    unittest.main()