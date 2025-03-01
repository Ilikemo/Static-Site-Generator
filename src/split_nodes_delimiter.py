from textnode import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if not node.text:
            pass
        elif node.text_type == TextType.TEXT:
            text_list = node.text.split(delimiter)
            for i in range(len(text_list)):
                if i % 2 == 0:
                    new_nodes.append(TextNode(text_list[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(text_list[i], text_type))
        else:
            new_nodes.append(node)
    return new_nodes
