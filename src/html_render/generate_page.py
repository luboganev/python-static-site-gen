import os

from domain.node_to_html_node import markdown_to_html_node
from markdown.block_markdown import extract_title


def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        template = f.read()

    content = markdown_to_html_node(markdown = markdown).to_html()
    title = extract_title(markdown = markdown)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    with open(dest_path, "w") as f:
        f.write(template)

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        if os.path.isfile(from_path):
            (root, extension) = os.path.splitext(filename)
            if extension == ".md":
                os.makedirs(dest_dir_path, exist_ok=True)
                dest_path = os.path.join(dest_dir_path, f"{root}.html")
                generate_page(
                    from_path = from_path,
                    template_path = template_path,
                    dest_path = dest_path,
                    basepath = basepath
                )
        else:
            dest_path = os.path.join(dest_dir_path, filename)
            generate_pages_recursive(
                dir_path_content = from_path, 
                template_path = template_path, 
                dest_dir_path = dest_path, 
                basepath = basepath
            )