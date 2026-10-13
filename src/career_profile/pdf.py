"""Local HTML-to-PDF rendering with explicit environment checks."""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter

from .errors import PdfEnvironmentError


def _has_cjk_font() -> bool:
    fc_match = shutil.which("fc-match")
    if not fc_match:
        return False
    result = subprocess.run(
        [fc_match, "Noto Sans CJK TC"],
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    return result.returncode == 0 and "Noto" in result.stdout


def _normalize_pdf(source: Path, destination: Path) -> None:
    """Remove volatile Chromium metadata while retaining text and annotations."""
    reader = PdfReader(source)
    writer = PdfWriter()
    writer.append_pages_from_reader(reader)
    title = reader.metadata.title if reader.metadata else None
    writer.add_metadata(
        {
            "/Title": title or "Resume",
            "/Creator": "wade-career-profile",
            "/Producer": "pypdf",
        }
    )
    with tempfile.NamedTemporaryFile(
        mode="w+b", suffix=".pdf", dir=destination.parent, delete=False
    ) as stream:
        normalized_path = Path(stream.name)
        writer.write(stream)
    os.replace(normalized_path, destination)


def render_pdf(html_path: Path, pdf_path: Path, *, require_cjk: bool = True) -> Path:
    if require_cjk and not _has_cjk_font():
        raise PdfEnvironmentError(
            "Traditional Chinese PDF support requires a local Noto Sans CJK TC font. "
            "On Ubuntu run: sudo apt-get install fonts-noto-cjk. Fonts are never downloaded "
            "at runtime by this project."
        )
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w+b", suffix=".chromium.pdf", dir=pdf_path.parent, delete=False
    ) as stream:
        chromium_path = Path(stream.name)
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            try:
                page = browser.new_page()
                page.goto(html_path.resolve().as_uri(), wait_until="networkidle")
                page.emulate_media(media="print")
                page.pdf(
                    path=str(chromium_path),
                    format="A4",
                    print_background=True,
                    prefer_css_page_size=True,
                    margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
                )
            finally:
                browser.close()
        _normalize_pdf(chromium_path, pdf_path)
    except PlaywrightError as exc:
        raise PdfEnvironmentError(
            "Chromium is unavailable. Install it once with 'uv run playwright install chromium'. "
            "Markdown and HTML generation remain available."
        ) from exc
    finally:
        chromium_path.unlink(missing_ok=True)
    return pdf_path


def pdf_page_count(pdf_path: Path) -> int | None:
    try:
        return len(PdfReader(pdf_path).pages)
    except (OSError, ValueError):
        return None
