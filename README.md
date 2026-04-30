# Google Search Scraper

A free self-hosted alternative to SerpAPI. Scrape Google search results directly with no API keys, no rate limits, and no subscription fees.

## Why not SerpAPI?

| | SerpAPI | This scraper |
|---|---|---|
| **Cost** | $50-300+/month | Free |
| **Rate limits** | Yes | No |
| **API keys** | Required | None |
| **Data privacy** | Queries sent to 3rd party | Stay on your machine |
| **Customization** | Limited | Full source code |

## Features

- **Stealth mode** — bypasses Google's headless-detection and bot-protection
- **Headless-server support** — auto-starts Xvfb when no DISPLAY is available
- **Structured output** — each result includes title, URL, and description
- **Configurable result count** — `max_results` parameter
- **Saves full HTML** — writes `google_results.html` for further parsing
- **CLI + Python API** — use from command line or import as a module

## Requirements

- Python 3.10+
- Playwright
- Xvfb (optional — only for headless servers without a display)

## Installation

```bash
# Clone or download the repo, then:
pip install playwright
playwright install chromium

# Optional: system dependencies for headless servers
# Ubuntu/Debian:  sudo apt-get install -y xvfb
# Fedora/RHEL:    sudo dnf install -y xorg-x11-server-Xvfb
```

## Usage

### Command line

```bash
python main.py "python programming"
python main.py "machine learning" -n 5
```

### Python API

```python
from scraper import search

results = search("python programming", max_results=5)

for r in results:
    print(r["title"])
    print(r["url"])
    print(r["snippet"])
```

## Example output

```bash
$ python main.py "python programming" -n 3

============================================================
Results for: python programming
============================================================

1. Welcome to Python.org
   https://www.python.org/
   The official home of the Python Programming Language.

2. Python (programming language)
   https://en.wikipedia.org/wiki/Python_(programming_language)
   Python is a high-level, general-purpose programming language...

3. Introduction to Python
   https://www.w3schools.com/python/python_intro.asp
   Python is a popular programming language. It was created by Guido van Rossum...
```

## Return format

```python
[
    {
        "title": "Welcome to Python.org",
        "url": "https://www.python.org/",
        "snippet": "The official home of the Python Programming Language."
    }
]
```

## How stealth works

1. **Headed Chrome** — Google detects headless Chrome; a real windowed browser avoids that
2. **CDP script injection** — removes `navigator.webdriver`, fakes `window.chrome`, plugins, and languages before any page JS runs
3. **Chrome flags** — `--disable-blink-features=AutomationControlled` hides automation traces
4. **Consent dismissal** — auto-clicks cookie consent buttons
5. **Human-like delays** — randomized sleeps between actions
6. **Virtual display (Xvfb)** — starts a virtual display on headless servers so headed Chrome can run

## Project structure

```
.
├── main.py              # CLI entry point
├── scraper/
│   ├── __init__.py      # Public API (search)
│   ├── browser.py       # Browser launch & stealth injection
│   ├── config.py        # Constants & selectors
│   ├── display.py       # Xvfb virtual display manager
│   ├── extractor.py     # DOM extraction logic
│   ├── scraper.py       # Main orchestration
│   └── utils.py         # Helpers
├── google_results.html  # Last search results (raw HTML)
└── google_failure.png   # Screenshot on failure
```

## Troubleshooting

| Problem | Solution |
|---|---|
| "No results found" | Check `google_failure.png` or `google_results.html` to see what page loaded. Google may have changed their DOM. |
| Browser launch fails | Install Xvfb if running on a headless server without a display. |
| Captcha / "sorry" page | Your IP may be flagged by Google. This script handles *browser-level* detection, not *IP-level* blocks. Try a different network or proxy. |
| Empty snippets | Google sometimes serves results without descriptions. The extractor will return `(no description)` for those. |
| Consent popup keeps appearing | The script auto-clicks "Reject all" or "Accept all". If your region uses different button text, add it to `scraper/config.py`. |
