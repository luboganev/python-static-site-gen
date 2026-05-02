from dataclasses import dataclass
from enum import Enum

from domain.textnode import TextNode


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "ulist"
    OLIST = "olist"

class BlockNode:
    """Base class — maybe abstract."""
    pass

@dataclass
class ParagraphBlock(BlockNode):
    children: list[TextNode]

    def __init__(self, children: list[TextNode]):
        self.children = children

@dataclass
class HeadingBlock(BlockNode):
    level: int
    children: list[TextNode]

    def __init__(self, level: int, children: list[TextNode]):
        self.level = level
        self.children = children

@dataclass
class CodeBlock(BlockNode):
    text: str

    def __init__(self, text: str):
        self.text = text

@dataclass
class QuoteBlock(BlockNode):
    children: list[TextNode]

    def __init__(self, children: list[TextNode]):
        self.children = children

@dataclass
class ListBlock(BlockNode):
    ordered: bool
    items: list[list[TextNode]]

    def __init__(self, ordered: bool, items: list[list[TextNode]]):
        self.ordered = ordered
        self.items = items