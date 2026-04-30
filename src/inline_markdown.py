from textnode import TextNode, TextType


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
