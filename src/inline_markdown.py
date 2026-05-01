from textnode import TextNode, TextType
import re

def extract_markdown_images(text: str):
    """Extracts image tokens: (alt_text, url)"""
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str):
    """Extracts link tokens: (text, url)"""
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_tokens(old_nodes: list[TextNode], tokenizer_strategy):
    """
    Splits a list of TextNodes by iterating over tokens identified by the 
    tokenizer_strategy.

    Args:
        old_nodes: The input list of nodes.
        tokenizer_strategy: A callable that takes (text, text_type) and returns 
                             a sequence of structured token data.

    Returns:
        A list of TextNode objects.
    """
    results: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            results.append(node)
            continue

        # Use the provided strategy to get all tokens in order
        tokens = tokenizer_strategy(node.text, node.text_type)
        remaining_text = node.text

        for token in tokens:
            if not remaining_text:
                raise Exception("All text consumed, but still expected tokens remain")

            # Determine the string pattern of the current token (e.g., [link](url))
            token_pattern = token['pattern'] 

            parts = remaining_text.split(token_pattern, 1)
            prefix_text = parts[0]
            remaining_text = parts[1]

            # Append the prefix text if it exists
            if len(prefix_text) > 0:
                results.append(TextNode(text=prefix_text, text_type=TextType.TEXT))

            # Append the token node itself
            token_node = TextNode(
                text=token['display'],
                text_type=token['target_type'],
                **token.get('extras', {}) # Handles url, etc.
            )
            results.append(token_node)

        # Append any remaining text after the last token
        if len(remaining_text) > 0:
            results.append(TextNode(text=remaining_text, text_type=TextType.TEXT))

    return results

def split_nodes_image(old_nodes: list[TextNode]):
    """Splits nodes based on image tokens using the generic token splitter."""
    
    def image_tokenizer(text: str, text_type: TextType):
        images = extract_markdown_images(text=text)
        token_list = []
        for alt_text, url in images:
            # The pattern used for splitting must match the source string exactly
            pattern = f"![{alt_text}]({url})" 
            
            token_list.append({
                'display': alt_text,
                'target_type': TextType.IMG,
                'extras': {'url': url},
                'pattern': pattern
            })
        return token_list

    return split_nodes_tokens(old_nodes, image_tokenizer)


def split_nodes_link(old_nodes: list[TextNode]):
    """Splits nodes based on link tokens using the generic token splitter."""
    
    def link_tokenizer(text: str, text_type: TextType):
        links = extract_markdown_links(text=text)
        token_list = []
        for text_content, url in links:
            # The pattern used for splitting must match the source string exactly
            pattern = f"[{text_content}]({url})"
            
            token_list.append({
                'display': text_content,
                'target_type': TextType.LINK,
                'extras': {'url': url},
                'pattern': pattern
            })
        return token_list

    return split_nodes_tokens(old_nodes, link_tokenizer)


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
    results: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            results.append(node)
            continue
        delimiter_count = node.text.count(delimiter)
        if delimiter_count % 2 != 0:
             raise Exception("Odd number of delimiters in the text")

        parts = node.text.split(delimiter)
        
        # The original logic relies on parts[i] being non-empty to process, 
        # but we must ensure it handles cases where split results are empty strings
        for i in range(len(parts)):
            part_text = parts[i]

            if len(part_text) > 0 or (len(parts) == 1 and not delimiter_count): # Handle the case where there are no delimiters at all
                # Even index means text block (before/between delimiters)
                if i % 2 == 0:
                    results.append(TextNode(text=part_text, text_type=TextType.TEXT))
                # Odd index means the delimited block content (e.g., code block)
                else:
                    results.append(TextNode(text=part_text, text_type=text_type))

    return results

