from __future__ import annotations

import shutil
from pathlib import Path

import pytest
from pypdf import PdfReader

from career_profile.errors import PdfEnvironmentError
from career_profile.models import CareerProfile, ResumeProfile
from career_profile.pdf import render_pdf
from career_profile.renderer import render_html
from career_profile.selector import select_resume

TEMPLATES = Path(__file__).resolve().parents[1] / "templates"


@pytest.mark.skipif(shutil.which("fc-match") is None, reason="fontconfig is unavailable")
def test_pdf_smoke_when_chromium_is_available(
    career: CareerProfile, resume_profile: ResumeProfile, tmp_path: Path
) -> None:
    selection = select_resume(career, resume_profile, "en")
    html_path = tmp_path / "resume.html"
    html_path.write_text(render_html(selection, TEMPLATES), encoding="utf-8")
    try:
        pdf_path = render_pdf(html_path, tmp_path / "resume.pdf", require_cjk=False)
    except PdfEnvironmentError:
        pytest.skip("Playwright Chromium is not installed")
    assert pdf_path.read_bytes().startswith(b"%PDF")
    first_bytes = pdf_path.read_bytes()
    second_path = render_pdf(html_path, tmp_path / "resume-second.pdf", require_cjk=False)
    assert second_path.read_bytes() == first_bytes
    reader = PdfReader(pdf_path)
    links = [
        annotation.get_object().get("/A", {}).get("/URI")
        for page in reader.pages
        for annotation in page.get("/Annots", [])
    ]
    assert "https://example.com/" in links
    if pdftotext := shutil.which("pdftotext"):
        extracted = tmp_path / "resume.txt"
        assert shutil.which("pdftotext") == pdftotext
        import subprocess

        subprocess.run([pdftotext, str(pdf_path), str(extracted)], check=True)
        assert "Morgan Lin" in extracted.read_text(encoding="utf-8")
