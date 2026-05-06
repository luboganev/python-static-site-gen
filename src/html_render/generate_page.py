import os

from domain.node_to_html_node import markdown_to_html_node
from markdown.block_markdown import extract_title


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        template = f.read()

    content = markdown_to_html_node(markdown = markdown).to_html()
    title = extract_title(markdown = markdown)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content)
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    with open(dest_path, "w") as f:
        f.write(template)
