from textnode import *
from htmlnode import *
from block_markdown import markdown_to_html_node
import os
import shutil

def main():
    move_files_from_static_to_public('static', 'public')
    generate_page(open('content/index.md'), open('template.html'), open('public/index.html'))
    
def move_files_from_static_to_public(source_dir, destination_dir):
    abs_destination_dir = os.path.abspath(destination_dir)
    if os.path.abspath(source_dir) == os.path.abspath(destination_dir):
        raise ValueError("Source and destination directories must be different.")
    if os.path.abspath(destination_dir).startswith(os.path.abspath(source_dir)):
        raise ValueError("Destination directory must not be inside the source directory.")
    if abs_destination_dir.endswith('/src') or abs_destination_dir == 'src':
        raise ValueError("Destination directory must not be inside the src directory.")
    if abs_destination_dir == os.path.abspath('src'):
        raise ValueError("Cannot use src as destination directory.")
    if os.path.exists(destination_dir):
        shutil.rmtree(destination_dir)
    os.mkdir(destination_dir)
    print(f"Copying files from {source_dir} to {destination_dir}")
    source_content = os.listdir(source_dir)
    for item in source_content:
        item_path = os.path.join(source_dir, item)
        if os.path.isfile(item_path):
            shutil.copy(item_path, destination_dir)
        elif os.path.isdir(item_path):
            move_files_from_static_to_public(item_path, os.path.join(destination_dir, item))
            
def extract_title(markdown):
    title = None
    for line in markdown.split('\n'):
        line.strip()
        if line.startswith("# "):
            title = line[2:]
            break
    if title is None:
        raise ValueError("Title not found in markdown content.")
    return title

def generate_page(from_path, template_path, dest_path):
    print(f"Gnerating page from {from_path} to {dest_path} using {template_path}")
    markdown_content = from_path.read()
    template_content = template_path.read()
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    title = extract_title(markdown_content)
    template_content = template_content.replace("{{title}}", title)
    template_content = template_content.replace("{{content}}", html_content)
    dest_path.write(template_content)


main()

