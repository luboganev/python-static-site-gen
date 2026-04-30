import unittest

from inline_markdown import split_nodes_delimiter
from textnode import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_block_inside(self):
        node = TextNode(text = "This is text with a `code block` word", text_type = TextType.TEXT)
        expected = [
            TextNode(text = "This is text with a ", text_type = TextType.TEXT),
            TextNode(text = "code block", text_type = TextType.CODE),
            TextNode(text = " word", text_type = TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(old_nodes = [node], delimiter = "`", text_type = TextType.CODE)
        self.assertEqual(new_nodes, expected)

    def test_block_at_start(self):
        node = TextNode(text = "`code block` word", text_type = TextType.TEXT)
        expected = [
            TextNode(text = "code block", text_type = TextType.CODE),
            TextNode(text = " word", text_type = TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(old_nodes = [node], delimiter = "`", text_type = TextType.CODE)
        self.assertEqual(new_nodes, expected)
    
    def test_block_at_end(self):
        node = TextNode(text = "This is text with a `code block`", text_type = TextType.TEXT)
        expected = [
            TextNode(text = "This is text with a ", text_type = TextType.TEXT),
            TextNode(text = "code block", text_type = TextType.CODE),
        ]
        new_nodes = split_nodes_delimiter(old_nodes = [node], delimiter = "`", text_type = TextType.CODE)
        self.assertEqual(new_nodes, expected)

    def test_open_block_inside(self):
        node = TextNode(text = "This is text with a `code block word", text_type = TextType.TEXT)
        with self.assertRaises(Exception) as ctx:
            split_nodes_delimiter(old_nodes = [node], delimiter = "`", text_type = TextType.CODE)
        self.assertIn("Odd number of delimiters in the text", str(ctx.exception))

    def test_pass_on_non_text_nodes(self):
        expected = [
            TextNode(text = "bold block", text_type = TextType.BOLD),
            TextNode(text = "italic block", text_type = TextType.ITALIC),
            TextNode(text = "code block", text_type = TextType.CODE),
            TextNode(text = "link block", text_type = TextType.LINK),
            TextNode(text = "img block", text_type = TextType.IMG),
        ]
        new_nodes = split_nodes_delimiter(old_nodes = expected, delimiter = "`", text_type = TextType.CODE)
        self.assertEqual(new_nodes, expected)

if __name__ == "__main__":
    unittest.main()