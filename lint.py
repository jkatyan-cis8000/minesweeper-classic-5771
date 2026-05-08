#!/usr/bin/env python3
"""Lint.py - Enforces layer dependencies for Minesweeper."""

import ast
import sys
from pathlib import Path


# Layer order (imports must go forward, never backward or sideways)
LAYER_ORDER = ["types", "config", "repo", "service", "runtime", "ui", "providers", "utils"]

# Standard library modules (allowed in all layers)
STDLIB_MODULES = {
    "abc", "ast", "asyncio", "base64", "bisect", "builtins", "calendar", "cmath",
    "collections", "contextlib", "copy", "dataclasses", "datetime", "decimal",
    "enum", "functools", "gc", "gzip", "hashlib", "heapq", "hmac", "html",
    "http", "importlib", "inspect", "itertools", "json", "logging", "math",
    "os", "pathlib", "pickle", "platform", "pprint", "queue", "random", "re",
    "shutil", "socket", "smtplib", "sqlite3", "ssl", "statistics", "string",
    "struct", "sys", "time", "timeit", "traceback", "types", "typing", "unicodedata",
    "unittest", "uuid", "warnings", "weakref", "xml", "zipfile"
}

# Valid imports per layer (internal src/ modules only)
VALID_IMPORTS = {
    "types": [],
    "config": ["types"],
    "repo": ["types", "config"],
    "service": ["types", "config", "repo"],
    "runtime": ["types", "config", "repo", "service", "ui"],
    "ui": ["types", "config", "repo", "service"],
    "providers": LAYER_ORDER[:-1],  # Can import from all layers
    "utils": [],  # Leaf layer, no internal imports
}


def get_layer_from_path(filepath: Path) -> str:
    """Extract the layer name from a file path."""
    src = Path("src")
    try:
        rel_path = filepath.relative_to(src)
        parts = rel_path.parts
        if parts:
            return parts[0]
    except ValueError:
        pass
    return ""


def get_imported_modules(tree: ast.Module) -> list[str]:
    """Extract all imported module names from an AST (internal only)."""
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module:
                # Skip relative imports (they are internal and allowed)
                if node.level == 0:
                    # Absolute import - get top-level module
                    top_level = node.module.split(".")[0]
                    imports.append(top_level)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                # Only track internal src/ imports
                if alias.name.startswith("src"):
                    imports.append(alias.name.split(".")[0])
    return imports


def is_stdlib_module(module_name: str) -> bool:
    """Check if a module is part of the Python standard library."""
    return module_name in STDLIB_MODULES


def check_file(filepath: Path) -> list[str]:
    """Check a single file for layer violations."""
    errors = []
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return [f"{filepath}: Error reading file: {e}"]
    
    # Skip empty files
    if not content.strip():
        return errors
    
    try:
        tree = ast.parse(content, filename=str(filepath))
    except SyntaxError as e:
        return [f"{filepath}:{e.lineno}: Syntax error: {e.msg}"]
    
    # Get the layer of this file
    layer = get_layer_from_path(filepath)
    if not layer or layer not in LAYER_ORDER:
        return errors  # Skip files outside src/
    
    # Get imports from this file
    imports = get_imported_modules(tree)
    
    # Check each import
    for imp in imports:
        # Skip standard library modules
        if is_stdlib_module(imp):
            continue
        
        # Only check internal src/ imports
        if imp == "src" or imp.startswith("src."):
            # Extract the actual layer from the import
            if imp == "src":
                # This shouldn't happen for valid imports
                continue
            imp_layer = imp.split(".")[0]
            if imp_layer not in LAYER_ORDER:
                continue  # Unknown internal module
            
            # Check if import is valid
            if imp_layer not in VALID_IMPORTS.get(layer, []):
                errors.append(
                    f"{filepath}: Import violation: '{layer}' layer imports '{imp_layer}' layer. "
                    f"Valid imports for '{layer}': {VALID_IMPORTS.get(layer, [])}"
                )
    
    # Check line count
    line_count = len(content.splitlines())
    if line_count > 300:
        errors.append(
            f"{filepath}: File exceeds 300 lines ({line_count} lines)"
        )
    
    return errors


def main():
    """Main linting function."""
    errors = []
    src_dir = Path("src")
    
    if not src_dir.exists():
        print("Error: src/ directory not found")
        sys.exit(1)
    
    # Find all Python files
    for py_file in src_dir.rglob("*.py"):
        file_errors = check_file(py_file)
        errors.extend(file_errors)
    
    if errors:
        print("Linting failed:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    
    print("Linting passed!")
    sys.exit(0)


if __name__ == "__main__":
    main()
