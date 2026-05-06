import re

from domain.blocknode import BlockNode, BlockType, CodeBlock, HeadingBlock, ListBlock, ParagraphBlock, QuoteBlock
from domain.textnode import TextNode
from markdown.inline_markdown import text_to_textnodes


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = [x.strip() for x in markdown.split("\n\n")]
    blocks = [x for x in blocks if x]
    return ["\n".join(line.strip() for line in block.split("\n")) for block in blocks]
    
def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH

def markdown_to_block_nodes(markdown: str) -> list[BlockNode]:
    nodes = []
    for raw in markdown_to_blocks(markdown):
        block_type = block_to_block_type(raw)
        nodes.append(_build_block_node(raw, block_type))
    return nodes

def _build_block_node(raw: str, block_type: BlockType) -> BlockNode:
    match block_type:
        case BlockType.PARAGRAPH:
            return _parse_paragraph(text = raw)
        case BlockType.HEADING:
            return _parse_heading(text = raw)
        case BlockType.CODE:
            return _parse_code(text = raw)
        case BlockType.QUOTE:
            return _parse_quote(text = raw)
        case BlockType.ULIST:
            return _parse_list(text = raw, ordered = False)
        case BlockType.OLIST:
            return _parse_list(text = raw, ordered = True)
        case _:
            raise ValueError(f"Unknown block type: {block_type}")
        
def _parse_paragraph(text: str) -> ParagraphBlock:
    flattened = " ".join(text.split("\n"))
    return ParagraphBlock(children=text_to_textnodes(flattened))
        
def _parse_heading(text: str) -> HeadingBlock:
    level = 0
    for char in text:
        if char == "#":
            level += 1
        else:
            break
    text = text[level + 1 :]
    return HeadingBlock(
        level = level,
        children = text_to_textnodes(text = text)
    )

def _parse_code(text: str) -> CodeBlock:
    code_text = (
        text
        .removeprefix("```\n")
        .removesuffix("```") # empty block will have only a single \n
        .removesuffix("\n")
    )
    return CodeBlock(text = code_text)

def _parse_quote(text: str) -> QuoteBlock:
    lines = [x.removeprefix('>').removeprefix(' ') for x in text.split("\n")]
    final_text_nodes: list['TextNode'] = []
    for line in lines:
        final_text_nodes.extend(text_to_textnodes(text = line))
    return QuoteBlock(children = final_text_nodes)

def _parse_list(text: str, ordered: bool) -> ListBlock:
    items = []
    for line in text.split("\n"):
        stripped = _strip_list_marker(line, ordered)
        if not stripped:
            continue
        items.append(text_to_textnodes(stripped))
    return ListBlock(ordered=ordered, items=items)

_ORDERED_PREFIX = re.compile(r"^\d+\. ?")

def _strip_list_marker(line: str, ordered: bool) -> str:
    if ordered:
        return _ORDERED_PREFIX.sub("", line, count=1)
    else:
       return line.removeprefix("-").removeprefix(" ") 