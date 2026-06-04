"""
Recursive Directory Tree Printer with File Size and Extension Filter
Traverses directory tree, displays structure with indentation, file sizes,
and optional extension filtering.
"""

import os
import sys
from collections import defaultdict


def format_size(size_bytes):
    """Convert bytes to human-readable format."""
    if size_bytes == 0:
        return "0 B"
    for unit in ('B', 'KB', 'MB', 'GB', 'TB'):
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} PB"


def should_show(name, extensions):
    """Check if file matches extension filter."""
    if not extensions:
        return True
    _, ext = os.path.splitext(name)
    return ext.lower() in [e.lower() if e.startswith('.') else f'.{e.lower()}' for e in extensions]


def tree(
    path,
    prefix="",
    show_hidden=False,
    extensions=None,
    max_depth=None,
    _depth=0,
    _stats=None,
    _show_size=True,
):
    """Recursively print directory tree."""
    if _stats is None:
        _stats = {'dirs': 0, 'files': 0, 'total_size': 0, 'ext_counts': defaultdict(int)}

    if max_depth is not None and _depth > max_depth:
        return _stats

    try:
        entries = sorted(os.scandir(path), key=lambda e: (not e.is_dir(), e.name.lower()))
    except PermissionError:
        print(f"{prefix}  [Permission Denied]")
        return _stats

    visible = []
    for entry in entries:
        if not show_hidden and entry.name.startswith('.'):
            continue
        if entry.is_file() and not should_show(entry.name, extensions):
            continue
        visible.append(entry)

    for i, entry in enumerate(visible):
        is_last = (i == len(visible) - 1)
        connector = '└── ' if is_last else '├── '
        extension = '    ' if is_last else '│   '

        if entry.is_dir():
            _stats['dirs'] += 1
            print(f"{prefix}{connector}📁 {entry.name}/")
            tree(
                entry.path, prefix + extension,
                show_hidden, extensions, max_depth,
                _depth + 1, _stats, _show_size
            )
        else:
            try:
                size = entry.stat().st_size
            except OSError:
                size = 0
            _stats['files'] += 1
            _stats['total_size'] += size
            _, ext = os.path.splitext(entry.name)
            _stats['ext_counts'][ext.lower() or '.noext'] += 1

            size_str = f"  ({format_size(size)})" if _show_size else ""
            print(f"{prefix}{connector}📄 {entry.name}{size_str}")

    return _stats


def print_tree(path, extensions=None, show_hidden=False, max_depth=None, show_size=True):
    if not os.path.exists(path):
        print(f"  ✗ Path not found: '{path}'")
        return
    if not os.path.isdir(path):
        print(f"  ✗ '{path}' is not a directory.")
        return

    abs_path = os.path.abspath(path)
    print(f"\n  📂 {abs_path}")
    if extensions:
        print(f"     Filter: {extensions}")
    print()

    stats = tree(abs_path, prefix="  ", show_hidden=show_hidden,
                 extensions=extensions, max_depth=max_depth,
                 _show_size=show_size)

    print(f"\n  {'─'*45}")
    print(f"  Directories : {stats['dirs']}")
    print(f"  Files       : {stats['files']}")
    print(f"  Total Size  : {format_size(stats['total_size'])}")

    if stats['ext_counts']:
        print(f"\n  Extension Breakdown:")
        for ext, count in sorted(stats['ext_counts'].items(), key=lambda x: -x[1]):
            bar = '▇' * min(20, count)
            print(f"    {ext or '.noext':<12} {count:>4}  {bar}")
    print(f"  {'─'*45}\n")


def create_demo_tree(base="demo_tree"):
    """Create a sample directory structure for demonstration."""
    structure = {
        '': [],
        'src': ['main.py', 'utils.py', 'config.py'],
        'src/models': ['user.py', 'product.py'],
        'src/views': ['home.html', 'about.html', 'style.css'],
        'data': ['users.csv', 'products.json', 'backup.sql'],
        'docs': ['README.md', 'API.md', 'CHANGELOG.md'],
        'tests': ['test_main.py', 'test_utils.py'],
        'assets': ['logo.png', 'icon.svg', 'font.ttf'],
        '.git': ['config', 'HEAD'],
    }
    for dir_path, files in structure.items():
        full_dir = os.path.join(base, dir_path)
        os.makedirs(full_dir, exist_ok=True)
        for filename in files:
            filepath = os.path.join(full_dir, filename)
            with open(filepath, 'w') as f:
                f.write(f"# {filename}\n" * 5)
    return base


def main():
    print("╔══════════════════════════════════════════╗")
    print("║   Directory Tree Printer v1.0            ║")
    print("╚══════════════════════════════════════════╝")

    print("\n  Creating demo tree structure...")
    demo_path = create_demo_tree("demo_tree")

    print("\n  Full tree (with hidden files):")
    print_tree(demo_path, show_hidden=True)

    print("\n  Python files only:")
    print_tree(demo_path, extensions=['.py'])

    print("\n  Web files only (.html, .css, .js):")
    print_tree(demo_path, extensions=['.html', '.css', '.js'])

    print("\n  Max depth 1:")
    print_tree(demo_path, max_depth=1)

    # Interactive
    path = input("  Enter a path to explore (or Enter to skip): ").strip()
    if path:
        ext_input = input("  Filter extensions (e.g. .py .txt, or Enter for all): ").strip()
        exts = ext_input.split() if ext_input else None
        print_tree(path, extensions=exts, show_hidden=False)

    # Cleanup demo
    import shutil
    shutil.rmtree(demo_path, ignore_errors=True)
    print("  Demo tree cleaned up.")


if __name__ == "__main__":
    main()
