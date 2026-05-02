import unittest

from domain.textnode import TextNode, TextType
from markdown.block_markdown import _parse_heading, block_to_block_type, markdown_to_blocks
from domain.blocknode import BlockType, HeadingBlock

class TestMarkdownToBlock(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_and_blank_blocks(self):
        md = """
This is **bolded** paragraph







This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

            
            



- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_strip_empty_space(self):
        md = """
This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here           
        This is the same paragraph on a new line            

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

class TestParseToBlockNode(unittest.TestCase):

    def test_heading(self):
        headings = [
            "# this is an h1",
            "## this is an h2",
            "### this is an h3",
            "#### this is an h4",
            "##### this is an h5",
            "###### this is an h6",
        ]
        expected = [
            HeadingBlock(
                level = 1,
                children = [
                    TextNode("this is an h1", text_type = TextType.TEXT)
                ]
            ),
            HeadingBlock(
                level = 2,
                children = [
                    TextNode("this is an h2", text_type = TextType.TEXT)
                ]
            ),
            HeadingBlock(
                level = 3,
                children = [
                    TextNode("this is an h3", text_type = TextType.TEXT)
                ]
            ),
            HeadingBlock(
                level = 4,
                children = [
                    TextNode("this is an h4", text_type = TextType.TEXT)
                ]
            ),
            HeadingBlock(
                level = 5,
                children = [
                    TextNode("this is an h5", text_type = TextType.TEXT)
                ]
            ),
            HeadingBlock(
                level = 6,
                children = [
                    TextNode("this is an h6", text_type = TextType.TEXT)
                ]
            ),
        ]
        for i in range(len(headings)):
            self.assertEqual(
                _parse_heading(headings[i]),
                expected[i],
            )

    def test_quote(self):
        raise NotImplementedError
    
    def test_code(self):
        raise NotImplementedError
    
    def test_ulist(self):
        raise NotImplementedError
    
    def test_olist(self):
        raise NotImplementedError
    
class TestMarkdownToBlockNodes(unittest.TestCase):

    def test_markdown_to_block_nodes(self):
        raise NotImplementedError

if __name__ == "__main__":
    unittest.main()