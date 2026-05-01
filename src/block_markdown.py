def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = [x.strip() for x in markdown.split("\n\n")]
    blocks = [x for x in blocks if x]
    return ["\n".join(line.strip() for line in block.split("\n")) for block in blocks]
    