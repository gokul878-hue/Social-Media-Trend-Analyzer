#!/usr/bin/env python3
"""Generate a deterministic synthetic social-media dataset for Hadoop testing."""

import argparse
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

TOPICS = [
    {
        "name": "artificial intelligence",
        "weight": 28,
        "phrases": [
            "Artificial intelligence is transforming modern technology",
            "Machine learning models are improving business decisions",
            "Generative AI is changing software development",
            "AI analytics helps teams understand complex data",
        ],
        "hashtags": ["#AI", "#MachineLearning", "#ArtificialIntelligence"],
    },
    {
        "name": "python",
        "weight": 19,
        "phrases": [
            "Python makes data analysis and automation easier",
            "Developers use Python for machine learning projects",
            "Python programming remains popular among students",
            "Learning Python opens opportunities in data science",
        ],
        "hashtags": ["#Python", "#Programming", "#DataScience"],
    },
    {
        "name": "big data",
        "weight": 16,
        "phrases": [
            "Big data platforms process millions of records",
            "Hadoop enables distributed storage and parallel processing",
            "MapReduce divides large analytics jobs across machines",
            "Organizations use big data to discover useful patterns",
        ],
        "hashtags": ["#BigData", "#Hadoop", "#MapReduce"],
    },
    {
        "name": "cloud computing",
        "weight": 12,
        "phrases": [
            "Cloud computing helps applications scale efficiently",
            "Businesses are moving data workloads to the cloud",
            "Cloud platforms provide flexible computing resources",
            "Modern applications rely on distributed cloud services",
        ],
        "hashtags": ["#CloudComputing", "#Cloud", "#Technology"],
    },
    {
        "name": "cybersecurity",
        "weight": 10,
        "phrases": [
            "Cybersecurity awareness protects users from online attacks",
            "Network security is essential for digital services",
            "Strong authentication improves information security",
            "Security teams monitor systems for suspicious activity",
        ],
        "hashtags": ["#CyberSecurity", "#NetworkSecurity", "#Security"],
    },
    {
        "name": "internet of things",
        "weight": 7,
        "phrases": [
            "Internet of Things devices create real-time sensor data",
            "Smart devices improve automation in modern cities",
            "IoT analytics supports efficient resource management",
            "Connected sensors are changing industrial systems",
        ],
        "hashtags": ["#IoT", "#SmartDevices", "#Innovation"],
    },
    {
        "name": "data analytics",
        "weight": 5,
        "phrases": [
            "Data analytics turns raw information into useful insights",
            "Visualization makes analytics results easier to understand",
            "Businesses use analytics to make evidence-based decisions",
            "Data science combines statistics programming and domain knowledge",
        ],
        "hashtags": ["#Analytics", "#Data", "#Visualization"],
    },
    {
        "name": "blockchain",
        "weight": 3,
        "phrases": [
            "Blockchain provides a distributed record of transactions",
            "Developers explore blockchain for secure digital applications",
            "Distributed ledger technology continues to evolve",
            "Blockchain research examines trust and transparency",
        ],
        "hashtags": ["#Blockchain", "#Web3", "#Technology"],
    },
]

PLATFORMS = ["X", "Reddit", "LinkedIn", "Mastodon"]
ENDINGS = [
    "What do you think?",
    "This trend is worth watching.",
    "The future looks interesting.",
    "Students are discussing this topic.",
    "More research is needed.",
    "Teams are experimenting with new ideas.",
]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=50000)
    parser.add_argument("--output", default="data/generated_posts.csv")
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def main():
    args = parse_args()
    if args.count < 1:
        raise SystemExit("--count must be at least 1")

    random.seed(args.seed)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    weights = [topic["weight"] for topic in TOPICS]
    start_time = datetime(2026, 1, 1, 8, 0, 0)

    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["post_id", "platform", "created_at", "text"])

        for post_id in range(1, args.count + 1):
            topic = random.choices(TOPICS, weights=weights, k=1)[0]
            phrase = random.choice(topic["phrases"])
            hashtags = random.sample(
                topic["hashtags"], k=random.choices([1, 2], weights=[65, 35], k=1)[0]
            )
            text = f"{phrase}. {random.choice(ENDINGS)} {' '.join(hashtags)}"
            timestamp = start_time + timedelta(seconds=post_id * 17)
            writer.writerow(
                [post_id, random.choice(PLATFORMS), timestamp.isoformat(), text]
            )

    print(f"Generated {args.count:,} posts in {output_path}")


if __name__ == "__main__":
    main()
