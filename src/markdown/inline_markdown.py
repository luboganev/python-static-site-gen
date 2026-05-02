from typing import Callable
from domain.textnode import TextNode, TextType
import re

def extract_markdown_images(text: str) -> tuple[str, str]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str) -> tuple[str, str]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def _split_nodes_by_extractor(
        old_nodes: list['TextNode'], 
        extractor: Callable[[str], tuple[str, str]], 
        formatter: Callable[[tuple[str, str]], str], 
        text_type: 'TextType') -> list['TextNode']:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        matches = extractor(old_node.text)
        if len(matches) == 0:
            # If no matches, keep the original text node
            new_nodes.append(old_node)
            continue
        remaining = old_node.text
        for match in matches:
            delimiter = formatter(match)
            sections = remaining.split(delimiter, 1)
            if sections[0] != "":
                new_nodes.append(TextNode(text=sections[0], text_type=TextType.TEXT))
            # Using keyword arguments for the token node: match[0]=text, text_type=type, match[1]=url (or other data)
            new_nodes.append(TextNode(text=match[0], text_type=text_type, url=match[1])) 
            remaining = sections[1] if len(sections) > 1 else ""
        if remaining != "":
            new_nodes.append(TextNode(text=remaining, text_type=TextType.TEXT))
    return new_nodes


def split_nodes_image(old_nodes: list['TextNode']) -> list['TextNode']:
    return _split_nodes_by_extractor(
        old_nodes,
        extract_markdown_images,
        lambda m: f"![{m[0]}]({m[1]})",
        TextType.IMG,
    )


def split_nodes_link(old_nodes: list['TextNode']) -> list['TextNode']:
    return _split_nodes_by_extractor(
        old_nodes,
        extract_markdown_links,
        lambda m: f"[{m[0]}]({m[1]})",
        TextType.LINK,
    )

def split_nodes_delimiter(old_nodes: list['TextNode'], delimiter: str, text_type: 'TextType') -> list['TextNode']:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes: list['TextNode'] = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(text=sections[i], text_type=TextType.TEXT))
            else:
                split_nodes.append(TextNode(text=sections[i], text_type=text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def text_to_textnodes(text: str) -> list['TextNode']:
    nodes = [TextNode(text = text, text_type = TextType.TEXT)]
    nodes = split_nodes_delimiter(old_nodes = nodes, delimiter = "`", text_type = TextType.CODE)
    nodes = split_nodes_delimiter(old_nodes = nodes, delimiter = "**", text_type = TextType.BOLD)
    nodes = split_nodes_delimiter(old_nodes = nodes, delimiter = "_", text_type = TextType.ITALIC)
    nodes = split_nodes_image(old_nodes = nodes)
    nodes = split_nodes_link(old_nodes = nodes)
    return nodes
    