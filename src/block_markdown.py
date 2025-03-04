from enum import Enum
from htmlnode import ParentNode
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
    lines = block.split("\n")
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
    

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        children.append(create_node_block(block))
    return ParentNode("div", children, None)
        

def create_node_block(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return block_to_paragraph(block)
    elif block_type == BlockType.HEADING:
        return block_to_heading(block)
    elif block_type == BlockType.CODE:
        return block_to_code(block)
    elif block_type == BlockType.QUOTE:
        return block_to_quote(block)
    elif block_type == BlockType.UNORDERED_LIST:
        return block_to_unordered_list(block)
    elif block_type == BlockType.ORDERED_LIST:
        return block_to_ordered_list(block)
    raise ValueError(f"Unknown block type: {block_type}")
    

def text_to_children(text):
    text_nodes = text_to_textnode(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def block_to_paragraph(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    return ParentNode(tag = "p", children = text_to_children(paragraph))

def block_to_heading(block):
    level = block.count("#", 0, 6)
    children = text_to_children(block[level+1:])
    return ParentNode(f"h{level}", children)

def block_to_code(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])
    
def block_to_quote(block):
    lines = block.split("\n")
    quote_text = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        line = line.lstrip(">").strip()
        if line != "":
            quote_text.append(line)
    content = " ".join(quote_text)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def block_to_unordered_list(block):
    lines = block.split("\n")
    html_items = []
    for line in lines:
        content = line[2:]
        children = text_to_children(content)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def block_to_ordered_list(block):
    lines = block.split("\n")
    list_text = []
    for line in lines:
        text = line[3:]
        children = text_to_children(text)
        list_text.append(ParentNode("li", children))
    return ParentNode("ol", list_text)



