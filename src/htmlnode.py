class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}
    
    def to_html(self):
        raise NotImplementedError("Subclasses should implement this method.")
    
    def props_to_html(self):
        return " ".join([f'{key}="{value}"' for key, value in self.props.items()])

    def __repr__(self):
        return f"HTMLNode(tag={self.tag!r}, value={self.value!r}, children={self.children!r}, props={self.props!r})"

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, [], props)
        if not value:
            raise ValueError("LeafNode must have a non-empty value.")

    def to_html(self):
        if not self.value:
            raise ValueError("LeafNode must have a non-empty value.")
        
        if not self.tag:
            return self.value
    

        props_str = self.props_to_html()
        props_str = f" {props_str}" if props_str else ""
        
        return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"
    


