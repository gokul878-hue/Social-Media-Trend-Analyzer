#!/usr/bin/env python3
"""Rank Hadoop output and create Top 10 keyword and hashtag charts."""

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="results/trend_counts.tsv")
    parser.add_argument("--top", type=int, default=10)
    parser.add_argument("--output-dir", default="results")
    return parser.parse_args()


def read_counts(path):
    keywords = []
    hashtags = []

    with Path(path).open(encoding="utf-8") as handle:
        for raw_line in handle:
            try:
                key, raw_count = raw_line.rstrip("\n").rsplit("\t", 1)
                count = int(raw_count)
            except ValueError:
                continue

            if key.startswith("K:"):
                keywords.append((key[2:], count))
            elif key.startswith("H:"):
                hashtags.append((key[2:], count))

    order = lambda item: (-item[1], item[0])
    return sorted(keywords, key=order), sorted(hashtags, key=order)


def save_chart(items, title, xlabel, destination, color):
    labels = [label for label, _ in reversed(items)]
    values = [count for _, count in reversed(items)]

    fig, axis = plt.subplots(figsize=(10, 6))
    bars = axis.barh(labels, values, color=color)
    axis.set_title(title, fontsize=16, fontweight="bold")
    axis.set_xlabel(xlabel)
    axis.grid(axis="x", linestyle="--", alpha=0.35)
    axis.bar_label(bars, padding=4)
    fig.tight_layout()
    fig.savefig(destination, dpi=180)
    plt.close(fig)


def format_section(title, items):
    lines = [title, "-" * len(title)]
    lines.extend(f"{rank:>2}. {label:<24} {count:>8}" for rank, (label, count) in enumerate(items, 1))
    return "\n".join(lines)


def main():
    args = parse_args()
    if args.top < 1:
        raise SystemExit("--top must be at least 1")

    keywords, hashtags = read_counts(args.input)
    top_keywords = keywords[: args.top]
    top_hashtags = hashtags[: args.top]

    if not top_keywords or not top_hashtags:
        raise SystemExit("The Hadoop results did not contain both keywords and hashtags.")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    report = (
        format_section(f"Top {args.top} Keywords", top_keywords)
        + "\n\n"
        + format_section(f"Top {args.top} Hashtags", top_hashtags)
        + "\n"
    )
    print(report)
    (output_dir / "top_trends.txt").write_text(report, encoding="utf-8")

    save_chart(
        top_keywords,
        f"Top {args.top} Trending Keywords",
        "Frequency",
        output_dir / "top_keywords.png",
        "#2563eb",
    )
    save_chart(
        top_hashtags,
        f"Top {args.top} Trending Hashtags",
        "Frequency",
        output_dir / "top_hashtags.png",
        "#7c3aed",
    )
    print(f"Charts and report saved in {output_dir}/")


if __name__ == "__main__":
    main()
