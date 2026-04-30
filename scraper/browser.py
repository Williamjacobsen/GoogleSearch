"""Browser setup and stealth injection."""

from playwright.sync_api import BrowserContext, Page

from .config import CHROME_ARGS, LOCALE, STEALTH_JS, USER_AGENT, VIEWPORT


def launch_browser(playwright):
    """Launch headed Chromium with anti-detection args."""
    return playwright.chromium.launch(headless=False, args=CHROME_ARGS)


def new_context(browser) -> BrowserContext:
    """Create a context with fake fingerprint."""
    return browser.new_context(
        user_agent=USER_AGENT,
        viewport=VIEWPORT,
        locale=LOCALE,
    )


def inject_stealth(context: BrowserContext, page: Page) -> None:
    """Inject CDP anti-detection script before navigation."""
    cdp = context.new_cdp_session(page)
    cdp.send("Page.addScriptToEvaluateOnNewDocument", {"source": STEALTH_JS})
