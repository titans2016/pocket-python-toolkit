"""
text_stats.py — Analyze a text file: word count, line count, top words, etc.

Usage:
    python text_stats.py <file> [--top N]

Examples:
    python text_stats.py essay.txt
    python text_stats.py notes.txt --top 20
"""

import re
import argparse
from collections import Counter

STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to",
    "for", "of", "with", "by", "from", "is", "was", "are", "were",
    "be", "been", "being", "have", "has", "had", "do", "does", "did",
    "will", "would", "could", "should", "may", "might", "it", "its",
    "this", "that", "these", "those", "i", "you", "he", "she", "we",
    "they", "not", "as", "if", "so", "up", "out", "about", "into",
}


def analyze(filepath, top_n=10):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    lines = text.splitlines()
    words = re.findall(r"\b[a-zA-Z']+\b", text.lower())
    chars = len(text)
    chars_no_spaces = len(text.replace(" ", "").replace("\n", ""))
    sentences = len(re.findall(r"[.!?]+", text))

    filtered_words = [w for w in words if w not in STOPWORDS and len(w) > 2]
    top_words = Counter(filtered_words).most_common(top_n)

    print(f"\n📄 File: {filepath}")
    print("─" * 40)
    print(f"  Lines:              {len(lines):>8,}")
    print(f"  Words:              {len(words):>8,}")
    print(f"  Characters:         {chars:>8,}")
    print(f"  Chars (no spaces):  {chars_no_spaces:>8,}")
    print(f"  Sentences (approx): {sentences:>8,}")

    if words:
        avg = len(words) / max(sentences, 1)
        print(f"  Avg words/sentence: {avg:>8.1f}")

    print(f"\n🔤 Top {top_n} words (excluding stopwords):")
    for i, (word, count) in enumerate(top_words, 1):
        bar = "█" * min(count, 30)
        print(f"  {i:>2}. {word:<20} {count:>5}  {bar}")


def main():
    parser = argparse.ArgumentParser(description="Analyze a text file.")
    parser.add_argument("file", help="Path to the text file")
    parser.add_argument("--top", type=int, default=10, help="Number of top words to show (default: 10)")
    args = parser.parse_args()

    analyze(args.file, top_n=args.top)


if __name__ == "__main__":
    main()
