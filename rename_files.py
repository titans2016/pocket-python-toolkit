"""
rename_files.py — Batch rename files in a folder.

Usage:
    python rename_files.py <folder> [--prefix TEXT] [--numbering] [--date]

Examples:
    python rename_files.py ./photos --prefix "vacation_" --numbering
    python rename_files.py ./docs --date
"""

import os
import argparse
from datetime import datetime


def rename_files(folder, prefix="", numbering=False, add_date=False, dry_run=False):
    if not os.path.isdir(folder):
        print(f"Error: '{folder}' is not a valid directory.")
        return

    files = sorted([
        f for f in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, f))
    ])

    if not files:
        print("No files found.")
        return

    renamed = 0
    for i, filename in enumerate(files, start=1):
        name, ext = os.path.splitext(filename)
        new_name = prefix

        if add_date:
            date_str = datetime.now().strftime("%Y-%m-%d")
            new_name += f"{date_str}_"

        if numbering:
            new_name += f"{i:03d}"
        else:
            new_name += name

        new_name += ext
        src = os.path.join(folder, filename)
        dst = os.path.join(folder, new_name)

        if src == dst:
            continue

        print(f"  {filename}  →  {new_name}")
        if not dry_run:
            os.rename(src, dst)
        renamed += 1

    action = "Would rename" if dry_run else "Renamed"
    print(f"\n{action} {renamed} file(s).")


def main():
    parser = argparse.ArgumentParser(description="Batch rename files in a folder.")
    parser.add_argument("folder", help="Target folder path")
    parser.add_argument("--prefix", default="", help="Prefix to add to filenames")
    parser.add_argument("--numbering", action="store_true", help="Replace filename with sequential number")
    parser.add_argument("--date", action="store_true", help="Add today's date as prefix")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without renaming")
    args = parser.parse_args()

    rename_files(
        folder=args.folder,
        prefix=args.prefix,
        numbering=args.numbering,
        add_date=args.date,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
