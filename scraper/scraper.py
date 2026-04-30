"""Main scraper orchestration."""

from playwright.sync_api import sync_playwright

from .browser import inject_stealth, launch_browser, new_context
from .config import (
    CONSENT_BUTTONS,
    CONSENT_DELAY,
    CONSENT_TIMEOUT,
    NAV_TIMEOUT,
    OUTPUT_HTML,
    OUTPUT_SCREENSHOT,
    RESULT_TIMEOUT,
    SCROLL_DELAY,
)
from .display import VirtualDisplay
from .extractor import extract_results
from .utils import sleep_random


def _dismiss_consent(page) -> None:
    """Click away Google's cookie consent popup if it appears."""
    for name in CONSENT_BUTTONS:
        btn = page.get_by_role("button", name=name)
        if btn.count() > 0 and btn.is_visible(timeout=CONSENT_TIMEOUT):
            print(f"Consent popup — clicking '{name}'...")
            btn.click(timeout=10_000)
            sleep_random(*CONSENT_DELAY)
            return


def _navigate_to_results(page, query: str) -> None:
    """Go to the Google search results page."""
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}&hl=en&gl=us"
    print(f"Navigating to {url}")
    page.goto(url, wait_until="domcontentloaded", timeout=NAV_TIMEOUT)
    sleep_random(1, 2)


def _wait_for_results(page) -> bool:
    """Wait for result headings to appear."""
    print("Waiting for search results...")
    try:
        page.wait_for_selector("h3", timeout=RESULT_TIMEOUT)
        return True
    except Exception:
        print("No results found. Taking screenshot...")
        page.screenshot(path=OUTPUT_SCREENSHOT)
        return False


def _scroll(page) -> None:
    """Scroll down like a human."""
    sleep_random(*SCROLL_DELAY)
    page.evaluate("window.scrollBy(0, 700)")


def _print_results(results: list, query: str) -> None:
    """Pretty-print results to stdout."""
    print(f"\n{'=' * 60}")
    print(f"Results for: {query}")
    print(f"{'=' * 60}")
    for i, r in enumerate(results, 1):
        desc = r.get("snippet", "")
        desc_line = f"\n   {desc[:180]}" if desc else "\n   (no description)"
        print(f"\n{i}. {r['title']}")
        print(f"   {r['url']}{desc_line}")


def _save_html(page) -> None:
    """Write the raw results HTML to disk."""
    html = page.content()
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)


def search(query: str, max_results: int = 10) -> list:
    """Search Google and return structured results.

    Args:
        query: Search query string.
        max_results: Maximum number of results to return.

    Returns:
        List of dicts with keys: title, url, snippet.
    """
    with VirtualDisplay():
        with sync_playwright() as p:
            browser = launch_browser(p)
            context = new_context(browser)
            page = context.new_page()
            inject_stealth(context, page)

            # Establish session
            print("Visiting google.com...")
            page.goto("https://www.google.com/", wait_until="domcontentloaded", timeout=20_000)
            sleep_random(1, 2)

            # Dismiss consent
            _dismiss_consent(page)

            # Search
            _navigate_to_results(page, query)

            if not _wait_for_results(page):
                browser.close()
                return []

            _scroll(page)
            results = extract_results(page)
            results = results[:max_results]

            _print_results(results, query)
            _save_html(page)

            browser.close()
            return results
