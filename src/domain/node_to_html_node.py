from domain.blocknode import BlockNode, CodeBlock, HeadingBlock, ListBlock, ParagraphBlock, QuoteBlock
from domain.htmlnode import HTMLNode, LeafNode, ParentNode
from domain.textnode import TextNode, TextType
from markdown.block_markdown import markdown_to_block_nodes

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.IMG:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"invalid text type: {text_node.text_type}")

def _text_nodes_to_html_nodes(text_nodes: list[TextNode]) -> list[HTMLNode]:
    return [text_node_to_html_node(tn) for tn in text_nodes]

def block_nodes_to_html_node(nodes: list[BlockNode]) -> HTMLNode:
    children = [_block_to_html_node(node) for node in nodes]
    return ParentNode(tag="div", children=children)

def _block_to_html_node(node: BlockNode) -> HTMLNode:
    match node:
        case ParagraphBlock():
            return _render_paragraph(node)
        case HeadingBlock():
            return _render_heading(node)
        case CodeBlock():
            return _render_code(node)
        case QuoteBlock():
            return _render_quote(node)
        case ListBlock():
            return _render_list(node)
        case _:
            raise ValueError(f"Unknown block node type: {type(node).__name__}")
        
def _render_paragraph(node: ParagraphBlock) -> ParentNode:
    return ParentNode(tag="p", children=_text_nodes_to_html_nodes(node.children))

def _render_heading(node: HeadingBlock) -> ParentNode:
    return ParentNode(tag=f"h{node.level}", children=_text_nodes_to_html_nodes(node.children))

def _render_code(node: CodeBlock) -> ParentNode:
    text_node = TextNode(node.text + "\n", TextType.TEXT)
    leaf = text_node_to_html_node(text_node)
    return ParentNode(
        tag="pre",
        children=[
            ParentNode(tag="code", children=[leaf]),
        ],
    )

def _render_quote(node: QuoteBlock) -> ParentNode:
    return ParentNode(tag="blockquote", children=_text_nodes_to_html_nodes(node.children))

def _render_list(node: ListBlock) -> ParentNode:
    children = [
        ParentNode(tag="li", children=_text_nodes_to_html_nodes(item))
        for item in node.items
    ]
    return ParentNode(tag="ul" if not node.ordered else "ol", children=children)

def markdown_to_html_node(markdown: str) -> HTMLNode:
    nodes = markdown_to_block_nodes(markdown)
    return block_nodes_to_html_node(nodes)