import sys
import os
import pathlib
import datetime
from typing import Tuple

def list_dir_recursive(path: str):
    
    files = []
    dirs = []
    
    contents = os.listdir(path)

    for item in contents:
        # Skip hidden items and dotfiles
        if item[0] == ".":
            continue

        item_path = os.path.join(path, item)
        
        # Put dirs in dirs list
        if os.path.isdir(item_path):
            dirs.append(item_path)
        else:
            # Only look for markdown files
            if pathlib.Path(item_path).suffix == ".md":
                files.append(item_path)

    for dir in dirs:
        dir_files = list_dir_recursive(dir)
        for dir_file in dir_files:
            files.append(dir_file)

    return files

def timestamp_strs(path: str):
    created_timestamp = pathlib.Path(path).stat().st_ctime
    updated_timestamp = pathlib.Path(path).stat().st_mtime

    created_dt = datetime.datetime.fromtimestamp(created_timestamp)
    updated_dt = datetime.datetime.fromtimestamp(updated_timestamp)

    created_formatted = created_dt.strftime("%Y-%m-%d")
    updated_formatted = updated_dt.strftime("%Y-%m-%d")

    return created_formatted, updated_formatted

if __name__ == "__main__":
    vault_dir = sys.argv[1]
    if not os.path.isdir(vault_dir):
        print("This is not a dir")
        exit(-1)
    print("--------------")
    
    files = list_dir_recursive(vault_dir)

    for file in files:
        created, updated = timestamp_strs(file)

        print(f"{file}, Created: {created}, Updated: {updated}")

    print(f"\n{len(files)} notes total")