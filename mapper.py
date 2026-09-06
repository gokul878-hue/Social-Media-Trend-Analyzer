#!/usr/bin/env python3
"""Hadoop Streaming mapper for keyword and hashtag frequency counts."""

import csv
import re
import sys

STOP_WORDS = {
    "a", "about", "after", "all", "also", "an", "and", "are", "as", "at",
    "be", "because", "been", "but", "by", "can", "could", "do", "for", "from",
    "get", "has", "have", "how", "i", "in", "into", "is", "it", "its", "just",
    "more", "new", "not", "of", "on", "or", "our", "out", "so", "than", "that",
    "the", "their", "they", "this", "to", "today", "using", "was", "we", "what",
    "when", "which", "who", "will", "with", "you", "your"
}

HASHTAG_RE = re.compile(r"(?<!\w)#[A-Za-z0-9_]+")
URL_RE = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
MENTION_RE = re.compile(r"(?<!\w)@[A-Za-z0-9_]+")
WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9']{2,}")


def extract_text(line):
    """Return the text column from CSV, or the whole line for plain text input."""
    try:
        row = next(csv.reader([line]))
    except csv.Error:
        return None

    if not row:
        return None

    if row[0].strip().lower() == "post_id":
        return None

    return row[-1].strip()


def main():
    for raw_line in sys.stdin:
        text = extract_text(raw_line.strip())
        if not text:
            continue

        for hashtag in HASHTAG_RE.findall(text):
            print(f"H:{hashtag.casefold()}\t1")

        cleaned = URL_RE.sub(" ", text)
        cleaned = MENTION_RE.sub(" ", cleaned)
        cleaned = HASHTAG_RE.sub(" ", cleaned)

        for match in WORD_RE.findall(cleaned.casefold()):
            word = match.strip("'")
            if word and word not in STOP_WORDS:
                print(f"K:{word}\t1")


if __name__ == "__main__":
    main()
