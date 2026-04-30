"""Google search scraper package.

A free self-hosted alternative to SerpAPI.
Scrape Google search results directly with no API keys,
no rate limits, and no subscription fees.
"""

from .scraper import search

__all__ = ["search"]
__version__ = "1.0.0"
