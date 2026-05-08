
import os
import shutil
import sys

from copystatic import copy_files_recursive
from html_render.generate_page import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    print(f'Building with basepath {basepath}')
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    print("Generating content to public directory...")
    generate_pages_recursive(
        dir_path_content = dir_path_content, 
        template_path = template_path, 
        dest_dir_path = dir_path_public, 
        basepath = basepath
    )

main()