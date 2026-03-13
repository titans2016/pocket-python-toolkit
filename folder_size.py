"""
folder_size.py — Show size of each subfolder, sorted largest first.

Usage:
    python folder_size.py <folder> [--depth N]

Examples:
    python folder_size.py /home/user/documents
    python folder_size.py . --depth 2
"""

import os
import argparse


def human_readable(size_bytes):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} PB"


def get_folder_size(path):
    total = 0
    try:
        for dirpath, _, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                try:
                    total += os.path.getsize(fp)
                except OSError:
                    pass
    except PermissionError:
        pass
    return total


def scan_folder(root, depth=1, current_depth=0, indent=""):
    if current_depth > depth:
        return

    try:
        entries = sorted(os.scandir(root), key=lambda e: e.name)
    except PermissionError:
        return

    items = []
    for entry in entries:
        if entry.is_dir(follow_symlinks=False):
            size = get_folder_size(entry.path)
            items.append((entry.name, entry.path, size))

    items.sort(key=lambda x: x[2], reverse=True)

    for name, path, size in items:
        print(f"{indent}{human_readable(size):>10}  {name}/")
        if current_depth < depth:
            scan_folder(path, depth, current_depth + 1, indent + "  ")


def main():
    parser = argparse.ArgumentParser(description="Show subfolder sizes sorted by size.")
    parser.add_argument("folder", help="Root folder to scan")
    parser.add_argument("--depth", type=int, default=1, help="Depth of subfolders to show (default: 1)")
    args = parser.parse_args()

    if not os.path.isdir(args.folder):
        print(f"Error: '{args.folder}' is not a valid directory.")
        return

    root_size = get_folder_size(args.folder)
    print(f"\n📁 {os.path.abspath(args.folder)}")
    print(f"   Total size: {human_readable(root_size)}\n")
    scan_folder(args.folder, depth=args.depth)


if __name__ == "__main__":
    main()
