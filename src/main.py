from textnode import TextNode
from copystatic import copy_files_recursive
from generate_page import generate_pages_recursive

import os
import shutil

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
dir_path_template = "./template.html"

def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    
    print("Copying static files to puclic directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    print("Generating pages...")
    generate_pages_recursive(dir_path_content, dir_path_template, dir_path_public)

if __name__ == "__main__":
    main()