#!/usr/bin/env python3
"""CLI entry point for the Google search scraper."""

import argparse

from scraper import search


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scrape Google search results. "
                    "A free self-hosted alternative to SerpAPI."
    )
    parser.add_argument("query", help="Search query")
    parser.add_argument(
        "-n", "--num",
        type=int,
        default=10,
        help="Number of results (default: 10)",
    )
    args = parser.parse_args()

    search(args.query, max_results=args.num)


if __name__ == "__main__":
    main()
