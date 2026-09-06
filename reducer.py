#!/usr/bin/env python3
"""Hadoop Streaming reducer that totals counts for each emitted key."""

import sys


def main():
    current_key = None
    current_total = 0

    for raw_line in sys.stdin:
        line = raw_line.rstrip("\n")
        try:
            key, raw_count = line.rsplit("\t", 1)
            count = int(raw_count)
        except (ValueError, TypeError):
            continue

        if key == current_key:
            current_total += count
            continue

        if current_key is not None:
            print(f"{current_key}\t{current_total}")

        current_key = key
        current_total = count

    if current_key is not None:
        print(f"{current_key}\t{current_total}")


if __name__ == "__main__":
    main()
