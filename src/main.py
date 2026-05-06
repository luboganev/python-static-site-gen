
import os
from shutil import rmtree, copy
from os import path, mkdir, listdir
import shutil

from copystatic import copy_files_recursive
from domain.textnode import TextNode
from domain.textnode import TextType
from html_render.generate_page import generate_page

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"

def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    generate_page(
        from_path = os.path.join(dir_path_content, "index.md"),
        template_path = "template.html",
        dest_path = os.path.join(dir_path_public, "index.html")
    )

main()