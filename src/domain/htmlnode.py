
from dataclasses import dataclass


@dataclass
class HTMLNode():
    def __init__(self, tag: str = None, value: str = None, children: list["HTMLNode"] = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None or len(self.props) == 0:
            return ""
        attributes = [f'{k}="{v}"' for k, v in self.props.items()]
        return " " + " ".join(attributes)

@dataclass
class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict = None):
        super().__init__(tag = tag, value = value, props = props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("Unexpected None value! All LeafNode instances must have a value!")
        if self.tag is None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

@dataclass     
class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list["HTMLNode"], props: dict = None):
        super().__init__(tag = tag, children = children, props = props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("Unexpected None tag! All ParentNode instances must have a tag!")
        if self.children is None:
            raise ValueError("Unexpected None children! All ParentNode instances must have children!")
        else:
            children_string = "".join([child.to_html() for child in self.children])
            return f"<{self.tag}{self.props_to_html()}>{children_string}</{self.tag}>"
        