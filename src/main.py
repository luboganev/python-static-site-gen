
from textnode import TextNode
from textnode import TextType

node = TextNode(text="Hello there", text_type=TextType.BOLD, url="https://www.boot.dev")
print(node)