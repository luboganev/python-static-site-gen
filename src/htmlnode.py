class HTMLNode():
    def __init__(self, tag: str = None, value: str =    None, children: list["HTMLNode"] = None, props: dict = None):
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
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"