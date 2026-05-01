from textnode import TextNode, TextType
import re


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
    results: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            results.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception("Odd number of delimiters in the text")
        for i in range(len(parts)):
            if len(parts[i]) > 0:
                if i % 2 == 0:
                    results.append(TextNode(text=parts[i], text_type=TextType.TEXT))
                else:
                    results.append(TextNode(text=parts[i], text_type=text_type))
    return results

def extract_markdown_images(text: str):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes: list[TextNode]):
    results: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            results.append(node)
            continue
        images = extract_markdown_images(text = node.text)
        remaining_text = node.text
        for image in images:
            if len(remaining_text) <=0:
                raise Exception("All text consumed, but still but not all expected images processed")
            parts = remaining_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(parts[0]) > 0:
                results.append(TextNode(text=parts[0], text_type=TextType.TEXT))
            results.append(TextNode(text=image[0], text_type=TextType.IMG, url = image[1]))
            remaining_text = parts[1]
        if len(remaining_text) > 0:
            results.append(TextNode(text=remaining_text, text_type=TextType.TEXT))
    return results

def extract_markdown_links(text: str):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_link(old_nodes: list[TextNode]):
    results: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            results.append(node)
            continue
        links = extract_markdown_links(text = node.text)
        remaining_text = node.text
        for image in links:
            if len(remaining_text) <=0:
                raise Exception("All text consumed, but still but not all expected links processed")
            parts = remaining_text.split(f"[{image[0]}]({image[1]})", 1)
            if len(parts[0]) > 0:
                results.append(TextNode(text=parts[0], text_type=TextType.TEXT))
            results.append(TextNode(text=image[0], text_type=TextType.LINK, url = image[1]))
            remaining_text = parts[1]
        if len(remaining_text) > 0:
            results.append(TextNode(text=remaining_text, text_type=TextType.TEXT))
    return results
