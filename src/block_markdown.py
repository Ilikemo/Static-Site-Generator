from enum import Enum
from htmlnode import *
from textnode import *
from inline_markdown import *
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(block):
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        return BlockType.QUOTE
    if block.startswith("- "):
        return BlockType.UNORDERED_LIST
    if re.match(r"^\d+\.", block):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
    

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        block_nodes.append(create_node_block(block, block_type))
    return HTMLNode(tag = "div", children = block_nodes)
        

def create_node_block(block, block_type):
    if block_type == BlockType.PARAGRAPH:
        children = text_to_children(block)
        return HTMLNode(tag = "p", children = children)
    elif block_type == BlockType.HEADING:
        level = block.count("#")
        chidren = text_to_children(block[level+1:])
        return HTMLNode(tag = f"h{level}", children = children)
    elif block_type == BlockType.CODE:
        lines = block.split("\n")
        code = "\n".join(lines[1:-1]).strip("\n ")
        return HTMLNode(tag = "pre", children = HTMLNode(tag = "code", value = code))
    elif block_type == BlockType.QUOTE:
        lines = block.split("\n")
        quote_text = []
        for line in lines:
            if line.startswith("> "):
                quote_text.append(line[2:])
            elif line.startswith(">"):
                quote_text.append(line[1:])
        content = "\n".join(quote_text)
        children = text_to_children(content)
        return HTMLNode(tag = "blockquote", children = children)
    elif block_type == BlockType.UNORDERED_LIST:
        lines = block.split("\n")
        list_text = []
        for line in lines:
            list_text.append(line[2:])
        content = "\n".join(list_text)
        children = text_to_children(content)
        return HTMLNode(tag = "ul", children = children)
    elif block_type == BlockType.ORDERED_LIST:
        lines = block.split("\n")
        list_text = []
        for line in lines:
            if not line.strip():
                continue
            content = line.strip()
            period_index = content.find(".")
            if period_index != -1:
                item_text = content[period_index + 1:].strip()
                item_children = text_to_children(item_text)
                list_text.append(HTMLNode(tag = "li", children = item_children))
        return HTMLNode(tag = "ol", children = list_text)
    

def text_to_children(text):
    text_nodes = text_to_textnode(text)
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    return html_nodes