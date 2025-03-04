from textnode import *
from htmlnode import *
from block_markdown import markdown_to_html_node
import os
import shutil
import sys

dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"
basepath = sys.argv[0]

def main():
    
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    move_files_from_static_to_public(dir_path_static, dir_path_public)
    
    generate_pages_recursive(dir_path_content, template_path, dir_path_public, basepath)
    
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
            return line[2:]
    if title is None:
        raise ValueError("Title not found in markdown content.")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    from_file = open(from_path, 'r')
    markdown_content = from_file.read()
    from_file.close()   
    
    template_file = open(template_path, 'r')
    template_content = template_file.read()
    template_file.close()

    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    
    title = extract_title(markdown_content)
    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", html_content)
    template_content = template_content.replace('href="/', f'href="{basepath}')
    template_content = template_content.replace('src="/', f'src="{basepath}')

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template_content)
    to_file.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for item in os.listdir(dir_path_content):
        if item.endswith(".md"):
            from_path = os.path.join(dir_path_content, item)
            dest_path = os.path.join(dest_dir_path, item.replace(".md", ".html"))
            generate_page(from_path, template_path, dest_path, basepath)
        elif os.path.isdir(os.path.join(dir_path_content, item)):
            new_dir_path_content = os.path.join(dir_path_content, item)
            new_dest_dir_path = os.path.join(dest_dir_path, item)
            generate_pages_recursive(new_dir_path_content, template_path, new_dest_dir_path, basepath)
        else:
            print(f"Skipping {item}, not a markdown file or directory.")

main()

