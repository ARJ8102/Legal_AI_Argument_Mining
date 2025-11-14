import os

IGNORE_DIRS = {".git", "__pycache__", "venv", "env", ".idea", ".vscode"}

project_root = os.getcwd()  # run from your project root

print(f"Project structure for {project_root}:\n")

for item in sorted(os.listdir(project_root)):
    if item in IGNORE_DIRS:
        continue
    path = os.path.join(project_root, item)
    if os.path.isdir(path):
        print(f"[DIR] {item}")
        # List only .py files in this folder
        py_files = [f for f in os.listdir(path) if f.endswith(".py")]
        for f in py_files:
            print(f"    [FILE] {f}")
    elif item.endswith(".py"):
        print(f"[FILE] {item}")
