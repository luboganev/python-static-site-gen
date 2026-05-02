from enum import Enum

from domain.textnode import TextNode


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "ulist"
    OLIST = "olist"

class BlockNode():
    def __init__(self, text: str, block_type: BlockType):
        self.text = text
        self.block_type = block_type

    def __eq__(self, value):
        if self.text != value.text: return False
        if self.block_type != value.block_type: return False
        return True
    
    def __repr__(self):
        return f"BlockNode({self.text}, {self.block_type.value})"