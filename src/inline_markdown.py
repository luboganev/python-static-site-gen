from textnode import TextNode, TextType
import re

def extract_markdown_images(text: str):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def _split_nodes_by_extractor(old_nodes, extractor, formatter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        matches = extractor(old_node.text)
        if len(matches) == 0:
            new_nodes.append(old_node)
            continue
        remaining = old_node.text
        for match in matches:
            delimiter = formatter(match)
            sections = remaining.split(delimiter, 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(match[0], text_type, match[1]))
            remaining = sections[1] if len(sections) > 1 else ""
        if remaining != "":
            new_nodes.append(TextNode(remaining, TextType.TEXT))
    return new_nodes


def split_nodes_image(old_nodes):
    return _split_nodes_by_extractor(
        old_nodes,
        extract_markdown_images,
        lambda m: f"![{m[0]}]({m[1]})",
        TextType.IMG,
    )


def split_nodes_link(old_nodes):
    return _split_nodes_by_extractor(
        old_nodes,
        extract_markdown_links,
        lambda m: f"[{m[0]}]({m[1]})",
        TextType.LINK,
    )

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

