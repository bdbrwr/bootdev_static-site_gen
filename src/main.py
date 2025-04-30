from textnode import TextNode
from copystatic import copy_files_recursive

import os
import shutil

dir_path_static = "./static"
dir_path_public = "./public"

def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    
    print("Copying static files to puclic directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

if __name__ == "__main__":
    main()