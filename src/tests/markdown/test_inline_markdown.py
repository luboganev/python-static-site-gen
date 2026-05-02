import unittest

from markdown.inline_markdown import extract_markdown_images, extract_markdown_links, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes
from domain.textnode import TextNode, TextType

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
        self.assertIn("invalid markdown, formatted section not closed", str(ctx.exception))

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

class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

class TestSplitNodesImage(unittest.TestCase):

    def test_pass_on_non_text_nodes(self):
        expected = [
            TextNode(text = "bold block", text_type = TextType.BOLD),
            TextNode(text = "italic block", text_type = TextType.ITALIC),
            TextNode(text = "code block", text_type = TextType.CODE),
            TextNode(text = "link block", text_type = TextType.LINK),
            TextNode(text = "img block", text_type = TextType.IMG),
        ]
        new_nodes = split_nodes_image(old_nodes = expected)
        self.assertEqual(new_nodes, expected)

    def test_multiple_images_single_text_node(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode(text = "This is text with an ", text_type = TextType.TEXT),
                TextNode(text = "image", text_type = TextType.IMG, url = "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(text = " and another ", text_type = TextType.TEXT),
                TextNode(
                    text = "second image", text_type = TextType.IMG, url = "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_multiple_text_nodes_with_single_image(self):
        """Tests processing multiple independent TextNode inputs, each containing images."""

        node1 = TextNode("Start text for Node 1.", text_type = TextType.TEXT)
        node2 = TextNode("Text before image 2. ![img2](url2). Text after.", text_type = TextType.TEXT)

        old_nodes = [node1, node2]
        new_nodes = split_nodes_image(old_nodes)

        expected_output = [
            TextNode(text = "Start text for Node 1.", text_type = TextType.TEXT),
            TextNode(text = "Text before image 2. ", text_type = TextType.TEXT),
            TextNode(text = "img2", text_type = TextType.IMG, url = "url2"),
            TextNode(text = ". Text after.", text_type = TextType.TEXT),
        ]

        self.assertListEqual(expected_output, new_nodes)

    def test_image_at_start(self):
        node = TextNode(
            text = "![Start Pic](http://example.com/start). Followed by some content.", 
            text_type = TextType.TEXT
        )

        new_nodes = split_nodes_image([node])

        expected_output = [
            TextNode(text = "Start Pic", text_type = TextType.IMG, url = "http://example.com/start"),
            TextNode(text = ". Followed by some content.", text_type = TextType.TEXT),
        ]

        self.assertListEqual(expected_output, new_nodes)

    def test_image_at_end(self):
        node = TextNode(
            text = "Some preceding text. Final ![End Pic](http://example.com/end)", 
            text_type = TextType.TEXT
        )

        new_nodes = split_nodes_image([node])

        expected_output = [
            TextNode(text = "Some preceding text. Final ", text_type = TextType.TEXT),
            TextNode(text = "End Pic", text_type = TextType.IMG, url = "http://example.com/end"),
        ]

        self.assertListEqual(expected_output, new_nodes)

class TestSplitNodesLink(unittest.TestCase):

    def test_split_link(self):
        node = TextNode(
            text = "This is text with a [link](https://google.com) and another [second link](https://boot.dev)",
            text_type = TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode(text = "This is text with a ", text_type = TextType.TEXT),
                TextNode(text = "link", text_type = TextType.LINK, url = "https://google.com"),
                TextNode(text = " and another ", text_type = TextType.TEXT),
                TextNode(
                    text = "second link", text_type = TextType.LINK, url = "https://boot.dev"
                ),
            ],
            new_nodes,
        )

    def test_pass_on_non_text_nodes(self):
        expected = [
            TextNode(text = "bold block", text_type = TextType.BOLD),
            TextNode(text = "italic block", text_type = TextType.ITALIC),
            TextNode(text = "code block", text_type = TextType.CODE),
            TextNode(text = "link block", text_type = TextType.LINK),
            TextNode(text = "img block", text_type = TextType.IMG),
        ]
        new_nodes = split_nodes_link(old_nodes = expected)
        self.assertEqual(new_nodes, expected)

    def test_multiple_text_nodes_with_single_link(self):
        node1 = TextNode("Start text for Node 1.", text_type = TextType.TEXT)
        node2 = TextNode("Text before link 2. [Link 3](url3). Text after.", text_type = TextType.TEXT)

        old_nodes = [node1, node2]
        new_nodes = split_nodes_link(old_nodes)

        expected_output = [
            TextNode(text = "Start text for Node 1.", text_type = TextType.TEXT),
            TextNode(text = "Text before link 2. ", text_type = TextType.TEXT),
            TextNode(text = "Link 3", text_type = TextType.LINK, url = "url3"),
            TextNode(text = ". Text after.", text_type = TextType.TEXT),
        ]

        self.assertListEqual(expected_output, new_nodes)

    def test_link_at_start(self):
        node = TextNode(
            text = "[Start Link](http://example.com/start). Followed by some content.",
            text_type = TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        expected_output = [
            TextNode(text = "Start Link", text_type = TextType.LINK, url = "http://example.com/start"),
            TextNode(text = ". Followed by some content.", text_type = TextType.TEXT),
        ]

        self.assertListEqual(expected_output, new_nodes)

    def test_link_at_end(self):
        node = TextNode(
            text = "Some preceding text. Final [End Link](http://example.com/end)",
            text_type = TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        expected_output = [
            TextNode(text = "Some preceding text. Final ", text_type = TextType.TEXT),
            TextNode(text = "End Link", text_type = TextType.LINK, url = "http://example.com/end"),
        ]

        self.assertListEqual(expected_output, new_nodes)

class TestTextToTextNodes(unittest.TestCase):

    def test_all_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMG, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        actual = text_to_textnodes(text = text)

        self.assertListEqual(expected, actual)

if __name__ == "__main__":
    unittest.main()