import os

IGNORE_DIRS = {'.git', '.github', '.idea', '__pycache__', '.venv', 'env', 'venv', '.pytest_cache'}
IGNORE_FILES = {'.gitignore', '.dockerignore'}
MAX_DEPTH = 2  # cambia a 3 si quieres ver un nivel más dentro

def print_tree(path='.', prefix='', depth=0):
    if depth > MAX_DEPTH:
        return
    items = sorted(os.listdir(path))
    for index, item in enumerate(items):
        full_path = os.path.join(path, item)
        if item in IGNORE_DIRS or item in IGNORE_FILES:
            continue
        connector = "└── " if index == len(items) - 1 else "├── "
        print(prefix + connector + item)
        if os.path.isdir(full_path):
            new_prefix = prefix + ("    " if index == len(items) - 1 else "│   ")
            print_tree(full_path, new_prefix, depth + 1)

if __name__ == "__main__":
    print("vitalapp-devops")
    print_tree(".")
