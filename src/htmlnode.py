


class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    def props_to_html(self):
        html_string = ""
        for key, value in self.props.items():
            html_string += f' {key}="{value}"'
        return html_string
    def __repr__(self):
        return f"{self.tag}, {self.value}, {self.children}, {self.props}"