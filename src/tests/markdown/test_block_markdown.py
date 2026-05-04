import unittest

from domain.textnode import TextNode, TextType
from markdown.block_markdown import _parse_code, _parse_heading, _parse_quote, block_to_block_type, markdown_to_blocks
from domain.blocknode import BlockType, CodeBlock, HeadingBlock, QuoteBlock

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
    
    def test_code(self):
        cases = [
            (
                "basic single line",
                "```\nprint('hello')\n```",
                CodeBlock(text="print('hello')"),
            ),
            (
                "last newline preserved",
                "```\nprint('hello')\n\n```",
                CodeBlock(text="print('hello')\n"),
            ),
            (
                "multi line",
                "```\nline one\nline two\nline three\n```",
                CodeBlock(text="line one\nline two\nline three"),
            ),
            (
                "empty block",
                "```\n```",
                CodeBlock(text=""),
            ),
            (
                "bold syntax stays literal",
                "```\n**not bold**\n```",
                CodeBlock(text="**not bold**"),
            ),
            (
                "italic, code, link syntax stay literal",
                "```\n_italic_ `code` [link](url)\n```",
                CodeBlock(text="_italic_ `code` [link](url)"),
            ),
            (
                "heading syntax stays literal",
                "```\n# not a heading\n```",
                CodeBlock(text="# not a heading"),
            ),
            (
                "leading indentation preserved",
                "```\n    indented four\n        indented eight\n```",
                CodeBlock(text="    indented four\n        indented eight"),
            ),
            (
                "blank lines inside preserved",
                "```\nfirst\n\nthird\n```",
                CodeBlock(text="first\n\nthird"),
            ),
            (
                "trailing whitespace on lines preserved",
                "```\ntrailing spaces   \nnext line\n```",
                CodeBlock(text="trailing spaces   \nnext line"),
            ),
            (
                "inline backticks survive",
                "```\nuse `print()` to output\n```",
                CodeBlock(text="use `print()` to output"),
            ),
            (
                "kitchen sink of markdown syntax",
                "```\n# Header\n**bold** and _italic_\n- list item\n> quote\n```",
                CodeBlock(text="# Header\n**bold** and _italic_\n- list item\n> quote"),
            ),
        ]

        for name, raw, expected in cases:
            with self.subTest(name=name):
                self.assertEqual(_parse_code(raw), expected)

    def test_quote(self):
        cases = [
            (
                "single line quote",
                "> hello world",
                QuoteBlock(children=[
                    TextNode("hello world", TextType.TEXT),
                ]),
            ),
            (
                "multi line quote",
                "> first line\n> second line\n> third line",
                QuoteBlock(children=[
                    TextNode("first line", TextType.TEXT),
                    TextNode("second line", TextType.TEXT),
                    TextNode("third line", TextType.TEXT),
                ]),
            ),
            (
                "quote with inline bold on single line",
                "> this is **bold** text",
                QuoteBlock(children=[
                    TextNode("this is ", TextType.TEXT),
                    TextNode("bold", TextType.BOLD),
                    TextNode(" text", TextType.TEXT),
                ]),
            ),
            (
                "each line parses inline independently",
                "> **bold one**\n> _italic two_",
                QuoteBlock(children=[
                    TextNode("bold one", TextType.BOLD),
                    TextNode("italic two", TextType.ITALIC),
                ]),
            ),
            (
                "marker without space is tolerated",
                ">no space after marker",
                QuoteBlock(children=[
                    TextNode("no space after marker", TextType.TEXT),
                ]),
            ),
            (
                "empty quote line in middle skipped",
                "> first\n>\n> third",
                QuoteBlock(children=[
                    TextNode("first", TextType.TEXT),
                    TextNode("third", TextType.TEXT),
                ]),
            ),
        ]

        for name, raw, expected in cases:
            with self.subTest(name=name):
                self.assertEqual(_parse_quote(raw), expected)
    
    def test_ulist(self):
        raise NotImplementedError
    
    def test_olist(self):
        raise NotImplementedError
    
class TestMarkdownToBlockNodes(unittest.TestCase):

    def test_markdown_to_block_nodes(self):
        raise NotImplementedError

if __name__ == "__main__":
    unittest.main()