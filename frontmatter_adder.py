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

def get_frontmatter(path: str):

    frontmatter_str = ""

    with open(path, "r", encoding="utf-8") as f:
        if f.readline() == "---\n":
            line = f.readline()
            while line != "---\n":
                frontmatter_str += line
                line = f.readline()

    return yaml.safe_load(frontmatter_str)

if __name__ == "__main__":
    # vault_dir = sys.argv[1]
    # if not os.path.isdir(vault_dir):
    #     print("This is not a dir")
    #     exit(-1)
    # print("--------------")
    
    # files = list_dir_recursive(vault_dir)

    # for file in files:
    #     created, updated = timestamp_strs(file)

    #     print(file, end="")
    #     print(f", Frontmatter: {has_frontmatter(file)}")

    # print(f"\n{len(files)} notes total")

    file_path = "D:\\notes\\Windows\\Add to PATH.md"
    
    frontmatter = get_frontmatter(file_path)
    print(f"{frontmatter}\n")

    created, updated = get_timestamps(file_path)
    frontmatter["updated"] = updated
    frontmatter["created"] = created
    print(f"{frontmatter}\n")
    
    print(yaml.dump(frontmatter))

