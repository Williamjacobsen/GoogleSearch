"""Configuration constants for the scraper."""

# Browser args to hide automation
CHROME_ARGS = [
    "--no-sandbox",
    "--disable-blink-features=AutomationControlled",
    "--disable-infobars",
    "--window-size=1366,768",
]

# Fake browser fingerprint
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/135.0.0.0 Safari/537.36"
)

VIEWPORT = {"width": 1366, "height": 768}

LOCALE = "en-US"

# CDP script injected before any page JS runs
STEALTH_JS = """
Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
delete navigator.__proto__.webdriver;
window.chrome = { runtime: {} };
Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
"""

# Google result description selectors (most reliable first)
SNIPPET_SELECTORS = ".VwiC3b, .yXK7lf, .IsZvec, .st, .s3v94d, .aC3Re, .lEBKkf"
FALLBACK_SELECTORS = ".kb0PBd, .N54PNb"

# Consent button names to try
CONSENT_BUTTONS = ["Reject all", "Accept all"]

# Timing
MIN_DELAY = 0.8
MAX_DELAY = 3.0
SCROLL_DELAY = (1.5, 3.0)
CONSENT_DELAY = (2, 4)

# Timeouts (ms)
NAV_TIMEOUT = 40_000
CONSENT_TIMEOUT = 2_000
RESULT_TIMEOUT = 15_000

# Output
OUTPUT_HTML = "google_results.html"
OUTPUT_SCREENSHOT = "google_failure.png"

# Xvfb
XVFB_DISPLAY = ":99"
XVFB_RESOLUTION = "1366x768x24"
