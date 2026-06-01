"""
Automated File Organizer by Extension with Conflict Resolution
Scans a directory, groups files by extension, moves them to categorized subfolders,
generates a report, skips hidden files, and handles duplicate filenames.
"""

import os
import shutil
import json
from datetime import datetime
from collections import defaultdict

CATEGORY_MAP = {
    'Images':     ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg', '.ico', '.tiff'],
    'Videos':     ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v'],
    'Audio':      ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'],
    'Documents':  ['.pdf', '.docx', '.doc', '.pptx', '.xlsx', '.odt', '.txt', '.rtf'],
    'Code':       ['.py', '.js', '.ts', '.html', '.css', '.java', '.cpp', '.c', '.go', '.rs'],
    'Data':       ['.json', '.csv', '.xml', '.yaml', '.yml', '.sql', '.db'],
    'Archives':   ['.zip', '.tar', '.gz', '.bz2', '.rar', '.7z', '.xz'],
    'Executables':['.exe', '.msi', '.deb', '.rpm', '.sh', '.bat', '.cmd'],
    'Fonts':      ['.ttf', '.otf', '.woff', '.woff2'],
    'Ebooks':     ['.epub', '.mobi', '.azw', '.fb2'],
}

def get_category(ext):
    ext = ext.lower()
    for cat, exts in CATEGORY_MAP.items():
        if ext in exts:
            return cat
    return 'Miscellaneous'


def resolve_conflict(dest_path):
    """If destination exists, append a counter to make it unique."""
    if not os.path.exists(dest_path):
        return dest_path
    base, ext = os.path.splitext(dest_path)
    counter = 1
    while True:
        new_path = f"{base}_({counter}){ext}"
        if not os.path.exists(new_path):
            return new_path
        counter += 1


def is_hidden(filename):
    return filename.startswith('.')


def scan_directory(source_dir):
    """Scan directory and return file info list."""
    if not os.path.isdir(source_dir):
        raise NotADirectoryError(f"'{source_dir}' is not a valid directory.")
    files = []
    for entry in os.scandir(source_dir):
        if entry.is_file() and not is_hidden(entry.name):
            _, ext = os.path.splitext(entry.name)
            files.append({
                'name': entry.name,
                'path': entry.path,
                'ext': ext.lower() if ext else '.noext',
                'size': entry.stat().st_size,
                'category': get_category(ext.lower() if ext else '.noext'),
            })
    return files


def organize(source_dir, dry_run=False):
    """Organize files into category subdirectories."""
    files = scan_directory(source_dir)
    report = defaultdict(lambda: {'count': 0, 'size': 0, 'files': []})
    conflicts_resolved = 0
    skipped = 0

    print(f"\n  {'─'*60}")
    print(f"  {'DRY RUN MODE' if dry_run else 'ORGANIZER'} — Source: {source_dir}")
    print(f"  Files found: {len(files)}")
    print(f"  {'─'*60}\n")

    for f in files:
        cat = f['category']
        cat_dir = os.path.join(source_dir, cat)
        dest = os.path.join(cat_dir, f['name'])

        # Check if file is already in correct category folder
        if os.path.dirname(f['path']) == cat_dir:
            skipped += 1
            continue

        resolved = resolve_conflict(dest)
        was_conflict = resolved != dest

        if was_conflict:
            conflicts_resolved += 1

        action = "MOVE" if not was_conflict else "MOVE (conflict resolved)"
        print(f"  [{action}] {f['name']} → {cat}/{os.path.basename(resolved)}")

        if not dry_run:
            os.makedirs(cat_dir, exist_ok=True)
            shutil.move(f['path'], resolved)

        report[cat]['count'] += 1
        report[cat]['size'] += f['size']
        report[cat]['files'].append(f['name'])

    return dict(report), conflicts_resolved, skipped, len(files)


def print_report(report, conflicts, skipped, total):
    print(f"\n  {'═'*60}")
    print(f"  FILE ORGANIZATION REPORT — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  {'═'*60}")
    print(f"  {'Category':<20} {'Files':>7}  {'Size':>12}")
    print(f"  {'─'*45}")
    grand_total_files = 0
    grand_total_size = 0
    for cat in sorted(report):
        count = report[cat]['count']
        size = report[cat]['size']
        grand_total_files += count
        grand_total_size += size
        print(f"  {cat:<20} {count:>7}  {format_size(size):>12}")
    print(f"  {'─'*45}")
    print(f"  {'TOTAL':<20} {grand_total_files:>7}  {format_size(grand_total_size):>12}")
    print(f"\n  Conflicts resolved : {conflicts}")
    print(f"  Files skipped      : {skipped}")
    print(f"  Total scanned      : {total}")
    print(f"  {'═'*60}\n")
    return report


def format_size(size_bytes):
    for unit in ('B', 'KB', 'MB', 'GB'):
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def create_demo_directory(path="demo_files"):
    """Create a demo directory with sample files for testing."""
    os.makedirs(path, exist_ok=True)
    demo_files = [
        "photo1.jpg", "photo2.png", "movie.mp4", "song.mp3",
        "document.pdf", "report.docx", "data.csv", "script.py",
        "archive.zip", "notes.txt", "presentation.pptx", "style.css",
        "app.js", ".hidden_file", "backup.tar.gz", "font.ttf",
    ]
    for name in demo_files:
        open(os.path.join(path, name), 'w').close()
    print(f"  Created demo directory '{path}' with {len(demo_files)} sample files.")
    return path


def main():
    print("╔══════════════════════════════════════════╗")
    print("║   File Organizer v1.0                    ║")
    print("╚══════════════════════════════════════════╝")

    source = input("\n  Enter directory to organize (or 'd' for demo): ").strip()

    if source.lower() == 'd':
        source = create_demo_directory("demo_organized_files")
        dry = True
    else:
        dry_input = input("  Dry run (no actual moves)? (y/n): ").strip().lower()
        dry = dry_input == 'y'

    try:
        report, conflicts, skipped, total = organize(source, dry_run=dry)
        print_report(report, conflicts, skipped, total)
        if dry:
            print("  ℹ  Dry run complete. No files were actually moved.")
    except (NotADirectoryError, PermissionError) as e:
        print(f"  ✗ Error: {e}")


if __name__ == "__main__":
    main()
