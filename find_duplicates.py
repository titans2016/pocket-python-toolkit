"""
find_duplicates.py — Find duplicate files in a folder by comparing MD5 checksums.

Usage:
    python find_duplicates.py <folder> [--delete]

Examples:
    python find_duplicates.py ./downloads
    python find_duplicates.py ./photos --delete
"""

import os
import hashlib
import argparse
from collections import defaultdict


def md5(filepath, chunk_size=8192):
    h = hashlib.md5()
    with open(filepath, "rb") as f:
        while chunk := f.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()


def find_duplicates(folder):
    hashes = defaultdict(list)

    for dirpath, _, filenames in os.walk(folder):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                file_hash = md5(filepath)
                hashes[file_hash].append(filepath)
            except (OSError, PermissionError) as e:
                print(f"  Skipping {filepath}: {e}")

    duplicates = {h: paths for h, paths in hashes.items() if len(paths) > 1}
    return duplicates


def main():
    parser = argparse.ArgumentParser(description="Find duplicate files by MD5 checksum.")
    parser.add_argument("folder", help="Folder to scan")
    parser.add_argument("--delete", action="store_true", help="Delete duplicates (keeps first file)")
    args = parser.parse_args()

    print(f"Scanning: {args.folder}\n")
    duplicates = find_duplicates(args.folder)

    if not duplicates:
        print("No duplicates found.")
        return

    total = 0
    for file_hash, paths in duplicates.items():
        print(f"Hash: {file_hash}")
        for i, path in enumerate(paths):
            size = os.path.getsize(path)
            marker = "  [KEEP]  " if i == 0 else "  [DUP]   "
            print(f"{marker}{path}  ({size:,} bytes)")
            if args.delete and i > 0:
                os.remove(path)
                print(f"           → Deleted.")
                total += 1
        print()

    if args.delete:
        print(f"Deleted {total} duplicate(s).")
    else:
        print(f"Found {len(duplicates)} group(s) of duplicates. Use --delete to remove them.")


if __name__ == "__main__":
    main()
