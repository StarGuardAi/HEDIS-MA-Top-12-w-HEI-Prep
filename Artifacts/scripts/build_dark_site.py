#!/usr/bin/env python3
"""
Build lightweight dark-themed static pages for recruiter-friendly assets.

Generates HTML files in an output directory (default: public/) for:
- Streamlit external link landing
- Influencer & Talent Partner Kit
- Demo Launch Guide

Intended to be quick to run (<1s) and dependency-light. Uses Python-Markdown if
available, otherwise falls back to pre-formatted text.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable, Optional


try:
    import markdown  # type: ignore

    def _render_markdown(text: str) -> str:
        """Render Markdown to HTML using python-markdown if available."""
        return markdown.markdown(text, extensions=["tables", "fenced_code"])

except ImportError:  # pragma: no cover - fallback path
    markdown = None

    def _render_markdown(text: str) -> str:
        """Fallback renderer when python-markdown is unavailable."""
        escaped = (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        return f"<pre>{escaped}</pre>"


DARK_CSS = """
body {
    background: #0f172a;
    color: #f8fafc;
    font-family: 'Inter', 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
    margin: 0;
    padding: 2rem;
    line-height: 1.6;
}
a {
    color: #38bdf8;
    text-decoration: none;
}
a:hover {
    color: #f472b6;
    text-decoration: underline;
}
.container {
    max-width: 960px;
    margin: 0 auto;
}
code, pre {
    background: #1e293b;
    padding: 0.2rem 0.4rem;
    border-radius: 4px;
}
table {
    width: 100%;
    border-collapse: collapse;
    margin: 1rem 0;
}
th, td {
    border: 1px solid #1e293b;
    padding: 0.6rem;
}
th {
    background: #1e293b;
}
.button {
    display: inline-block;
    margin: 0.4rem 0.6rem 0.4rem 0;
    padding: 0.6rem 1rem;
    background: #38bdf8;
    color: #0f172a;
    border-radius: 6px;
    font-weight: 600;
}
.button:hover {
    background: #0ea5e9;
    color: #0f172a;
}
.card {
    background: #111c3a;
    padding: 1.2rem;
    border-radius: 10px;
    margin: 1rem 0;
    box-shadow: 0 20px 25px -15px rgba(56, 189, 248, 0.35);
}
"""


def _build_html(title: str, body_html: str) -> str:
    """Wrap body content with a dark-themed HTML shell."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <style>{DARK_CSS}</style>
</head>
<body>
  <div class="container">
    <h1>{title}</h1>
    {body_html}
    <footer style="margin-top: 3rem; opacity: 0.7;">
      <p>Generated automatically from the HEDIS MA portfolio repo.</p>
    </footer>
  </div>
</body>
</html>"""


def _write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _load_markdown(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Markdown source not found: {path}")
    return path.read_text(encoding="utf-8")


def build_pages(output_dir: Path) -> Iterable[Path]:
    """Build all static pages. Returns iterable of generated file paths."""
    generated: list[Path] = []

    output_dir = output_dir.resolve()

    # Page 1: Streamlit landing info
    streamlit_body = """
<div class="card">
  <h2>Interactive Demo (Dark Mode)</h2>
  <p>The Streamlit application is hosted with a dark theme at the link below. You can
  share this directly with influencers, recruiters, and hiring managers.</p>
  <a class="button" href="https://hedis-ma-top-12-w-hei-prep.streamlit.app/" target="_blank">Launch Streamlit Demo</a>
  <a class="button" href="http://71.162.0.66:8502" target="_blank">Live External Link</a>
</div>

<div class="card">
  <h2>Suggested Talking Points</h2>
  <ul>
    <li>Full Medicare Advantage Stars narrative in under five minutes.</li>
    <li>Financial, operational, predictive, and equity analytics in one experience.</li>
    <li>Ready-to-send recruiter copy: emphasize 60–90 day deployment.</li>
  </ul>
  <p style="margin-top: 1rem;">
    <strong>Need a curated tour?</strong> Email <a href="mailto:reichert.starguardai@gmail.com">reichert.starguardai@gmail.com</a>
    to schedule a live walkthrough tailored to your stakeholders.
  </p>
</div>
"""
    streamlit_html = _build_html("Streamlit Demo Access", streamlit_body)
    streamlit_path = output_dir / "index.html"
    _write_file(streamlit_path, streamlit_html)
    generated.append(streamlit_path)

    # Page 2: Influencer kit (converted markdown)
    influencer_md = _load_markdown(Path("docs/influencer_portal.md"))
    influencer_html = _build_html(
        "Influencer & Talent Partner Kit",
        _render_markdown(influencer_md),
    )
    influencer_path = output_dir / "influencer_portal.html"
    _write_file(influencer_path, influencer_html)
    generated.append(influencer_path)

    # Page 3: Demo launch guide
    launch_md = _load_markdown(Path("docs/DEMO_LAUNCH_GUIDE.md"))
    launch_html = _build_html(
        "Demo Launch Guide",
        _render_markdown(launch_md),
    )
    launch_path = output_dir / "demo_launch_guide.html"
    _write_file(launch_path, launch_html)
    generated.append(launch_path)

    return generated


def parse_args(argv: Optional[Iterable[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build dark-themed static assets.")
    parser.add_argument(
        "--output",
        "-o",
        default="public",
        help="Output directory for generated HTML files (default: public/).",
    )
    return parser.parse_args(argv)


def main(argv: Optional[Iterable[str]] = None) -> int:
    args = parse_args(argv)
    output_dir = Path(args.output).resolve()

    generated = build_pages(output_dir)
    rel_paths = ", ".join(str(path.relative_to(Path.cwd())) if path.is_relative_to(Path.cwd()) else str(path) for path in generated)
    if markdown is None:
        print("Generated pages (fallback renderer):", rel_paths)
        print("Install 'markdown' package for richer formatting (pip install markdown).")
    else:
        print("Generated pages:", rel_paths)
    return 0


if __name__ == "__main__":
    sys.exit(main())

