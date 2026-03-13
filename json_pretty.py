"""
json_pretty.py — Pretty-print and validate a JSON file.

Usage:
    python json_pretty.py <file> [--indent N] [--sort-keys] [--output FILE]

Examples:
    python json_pretty.py data.json
    python json_pretty.py data.json --sort-keys --output clean.json
"""

import json
import argparse
import sys
import os


def pretty_print(filepath, indent=2, sort_keys=False, output=None):
    if not os.path.isfile(filepath):
        print(f"Error: File '{filepath}' not found.")
        sys.exit(1)

    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        sys.exit(1)

    formatted = json.dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(formatted + "\n")
        print(f"✅ Saved to: {output}")
    else:
        print(formatted)

    # Stats
    size_before = len(raw.encode("utf-8"))
    size_after = len(formatted.encode("utf-8"))

    def count_items(obj):
        if isinstance(obj, dict):
            return len(obj), sum(count_items(v)[0] + count_items(v)[1] for v in obj.values()), 0
        elif isinstance(obj, list):
            return 0, 0, len(obj)
        return 0, 0, 0

    print(f"\n📊 Stats:", file=sys.stderr)
    print(f"   Keys (top level): {len(data) if isinstance(data, dict) else 'N/A'}", file=sys.stderr)
    print(f"   Size before:      {size_before:,} bytes", file=sys.stderr)
    print(f"   Size after:       {size_after:,} bytes", file=sys.stderr)
    print(f"   Type:             {type(data).__name__}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Pretty-print and validate a JSON file.")
    parser.add_argument("file", help="Path to the JSON file")
    parser.add_argument("--indent", type=int, default=2, help="Indentation spaces (default: 2)")
    parser.add_argument("--sort-keys", action="store_true", help="Sort keys alphabetically")
    parser.add_argument("--output", help="Save output to a file instead of printing")
    args = parser.parse_args()

    pretty_print(args.file, indent=args.indent, sort_keys=args.sort_keys, output=args.output)


if __name__ == "__main__":
    main()
