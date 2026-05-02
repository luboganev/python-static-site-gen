
from domain.textnode import TextNode
from domain.textnode import TextType

node = TextNode(text="Hello there", text_type=TextType.BOLD, url="https://www.boot.dev")
print(node)