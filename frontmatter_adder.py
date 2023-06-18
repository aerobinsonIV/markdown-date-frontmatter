import sys
import os
import pathlib
import datetime
import yaml

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

def get_timestamps(path: str):
    created_timestamp = pathlib.Path(path).stat().st_ctime
    updated_timestamp = pathlib.Path(path).stat().st_mtime

    created_dt = datetime.datetime.fromtimestamp(created_timestamp)
    updated_dt = datetime.datetime.fromtimestamp(updated_timestamp)

    # return created_dt, updated_dt

    created_formatted = created_dt.strftime("%Y-%m-%d")
    updated_formatted = updated_dt.strftime("%Y-%m-%d")

    return created_formatted, updated_formatted

def parse_file(path: str):

    frontmatter_str = ""

    with open(path, "r", encoding="utf-8") as f:
        if f.readline() == "---\n":
            line = f.readline()
            while line != "---\n":
                frontmatter_str += line
                line = f.readline()

        remainder = f.read()
    if len(frontmatter_str) == 0:
        empty_dict = {}
        return empty_dict, remainder
    else:
        return yaml.safe_load(frontmatter_str), remainder

def write_file(path: str, frontmatter_str: str, body_str: str):
    with open(path, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write(frontmatter_str)
        f.write("---\n")
        f.write(body_str)

if __name__ == "__main__":
    vault_dir = sys.argv[1]
    if not os.path.isdir(vault_dir):
        print("This is not a dir")
        exit(-1)
    print("--------------")
    
    files = list_dir_recursive(vault_dir)

    for file in files:
        print(f"Processing {file}")
    
        frontmatter_dict, body = parse_file(file)

        created, updated = get_timestamps(file)
        frontmatter_dict["updated"] = updated
        
        # If a note already has creation date info, prioritize that over file metadata
        if "created" not in frontmatter_dict.keys():
            frontmatter_dict["created"] = created
        
        new_frontmatter_str = yaml.dump(frontmatter_dict)

        write_file(file, new_frontmatter_str.replace("'", ""), body)

    print(f"\n{len(files)} notes total processed")

