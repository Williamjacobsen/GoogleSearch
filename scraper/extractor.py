"""Google result extraction logic."""

from .config import FALLBACK_SELECTORS, SNIPPET_SELECTORS

_EXTRACT_JS = f"""
() => {{
    const items = [];
    const seenUrls = new Set();

    document.querySelectorAll("h3").forEach(h3 => {{
        // --- URL ---
        let url = "";
        const linkA = h3.closest("a[href]")
            || (h3.parentElement && h3.parentElement.closest("a[href]"));
        if (linkA) url = linkA.href;

        if (!url
            || url.includes("google.com/search")
            || url.includes("google.com/webhp"))
            return;
        if (seenUrls.has(url)) return;
        seenUrls.add(url);

        // --- Title ---
        const title = h3.innerText;
        if (!title) return;

        // --- Snippet ---
        let snippet = "";
        let container = h3;
        for (let i = 0; i < 7; i++) {{
            container = container.parentElement;
            if (!container) break;

            // Primary selectors
            const descEls = container.querySelectorAll("{SNIPPET_SELECTORS}");
            for (const el of descEls) {{
                let text = el.innerText.trim();
                if (text && text !== title && text.length > 15
                    && !text.includes("https://")) {{
                    text = text.replace(/\\s*Read more\\s*$/i, "").trim();
                    snippet = text;
                    break;
                }}
            }}
            if (snippet) break;

            // Fallback selectors
            const fallbackEls = container.querySelectorAll("{FALLBACK_SELECTORS}");
            for (const el of fallbackEls) {{
                const text = el.innerText.trim();
                if (text && text.length > 20) {{
                    const lines = text.split("\\n").filter(l => l.trim());
                    const cleanLines = lines.filter(l =>
                        l.trim() !== title &&
                        !l.includes("https://") &&
                        !l.includes("www.") &&
                        l.length > 10
                    );
                    if (cleanLines.length > 0) {{
                        snippet = cleanLines.join(" ").substring(0, 300);
                        break;
                    }}
                }}
            }}
            if (snippet) break;
        }}

        items.push({{ title: title, url: url, snippet: snippet }});
    }});
    return items;
}}
"""


def extract_results(page) -> list:
    """Run the JS extractor and return structured results."""
    return page.evaluate(_EXTRACT_JS)
