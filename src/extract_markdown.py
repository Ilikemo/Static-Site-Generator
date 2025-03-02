import re
from textnode import *


def extract_markdown_images(text):
    return (re.findall(r"!\[(.*?)\]\((.*?)\)", text))

def extract_markdown_links(text):
    return (re.findall(r"\[(.*?)\]\((.*?)\)", text))


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if not node.text:
            pass
        elif node.text_type == TextType.TEXT:
            image_list = extract_markdown_images(node.text)
            if image_list:
                text = node.text
                for i in range(len(image_list)):
                    sections = text.split(f"![{image_list[i][0]}]({image_list[i][1]})")
                    if sections[0]:
                        new_nodes.append(TextNode(sections[0], TextType.TEXT))
                    new_nodes.append(TextNode(image_list[i][0], TextType.IMAGE, image_list[i][1]))
                    if i == len(image_list) - 1:
                        if sections[1]:
                            new_nodes.append(TextNode(sections[1], TextType.TEXT))
                    text = str(sections[1])
                    
            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if not node.text:
            pass
        elif node.text_type == TextType.TEXT:
            link_list = extract_markdown_links(node.text)
            if link_list:
                text = node.text
                for i in range(len(link_list)):
                    sections = text.split(f"[{link_list[i][0]}]({link_list[i][1]})")
                    if sections[0]:    
                        new_nodes.append(TextNode(sections[0], TextType.TEXT))
                    new_nodes.append(TextNode(link_list[i][0], TextType.LINK, link_list[i][1]))
                    if i == len(link_list) - 1:
                        if sections[1]:
                            new_nodes.append(TextNode(sections[1], TextType.TEXT))
                    text = str(sections[1])
            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)
    return new_nodes