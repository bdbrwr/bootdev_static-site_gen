from textnode import TextNode
from copystatic import copy_files_recursive
from generate_page import generate_pages_recursive
import sys
import os
import shutil

basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
dir_path_template = "./template.html"

def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    
    print("Copying static files to puclic directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    print("Generating pages...")
    generate_pages_recursive(dir_path_content, dir_path_template, dir_path_public, basepath)

if __name__ == "__main__":
    main()