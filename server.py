# server.py
from fastmcp import FastMCP
import os

mcp = FastMCP("Archaeologist-Tools")

@mcp.tool()
def list_structure(path: str = "."):
    """Lists the directory tree. Use this to get an overview of the project."""
    tree = []
    for root, dirs, files in os.walk(path):
        # Ignore hidden folders like .git or venv
        dirs[:] = [d for d in dirs if not d.startswith(('.', 'venv'))]
        level = root.replace(path, '').count(os.sep)
        indent = ' ' * 4 * level
        tree.append(f"{indent}{os.path.basename(root)}/")
        for f in files:
            if not f.startswith('.'):
                tree.append(f"{indent}    {f}")
    return "\n".join(tree)

@mcp.tool()
def peek_file(file_path: str):
    """Reads the first 50 lines of a file to understand its purpose."""
    try:
        with open(file_path, 'r') as f:
            lines = [next(f) for _ in range(50)]
            return "".join(lines)
    except Exception as e:
        return f"Error reading file: {e}"

if __name__ == "__main__":
    # We run this on a local port so our client can find it
    mcp.run(transport="http", port=8000)