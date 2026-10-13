from __future__ import annotations

from pathlib import Path

import pytest

from career_profile.errors import RenderError
from career_profile.models import CareerProfile, ResumeProfile
from career_profile.renderer import output_filename, render_html, render_markdown
from career_profile.selector import select_resume

TEMPLATES = Path(__file__).resolve().parents[1] / "templates"


def test_english_markdown_and_html_render(
    career: CareerProfile, resume_profile: ResumeProfile
) -> None:
    selection = select_resume(career, resume_profile, "en")
    markdown = render_markdown(selection, TEMPLATES)
    html = render_html(selection, TEMPLATES)
    assert "English summary" in markdown
    assert "Built a synthetic test API" in html
    assert "<!doctype html>" in html


def test_traditional_chinese_markdown_and_html_render(
    career: CareerProfile, resume_profile: ResumeProfile
) -> None:
    selection = select_resume(career, resume_profile, "zh-TW")
    assert "中文摘要" in render_markdown(selection, TEMPLATES)
    html = render_html(selection, TEMPLATES)
    assert 'lang="zh-TW"' in html
    assert "建立合成測試 API" in html


def test_expected_output_filename() -> None:
    assert output_filename("backend-engineer", "en", "pdf") == (
        "Wade_Huang_Backend_Engineer_EN.pdf"
    )


def test_empty_optional_sections_are_omitted(
    career: CareerProfile, resume_profile: ResumeProfile
) -> None:
    empty = career.model_copy(update={"employment": [], "projects": [], "education": []})
    profile = resume_profile.model_copy(update={"experience_bullets": {}, "project_ids": []})
    html = render_html(select_resume(empty, profile, "en"), TEMPLATES)
    assert "Professional Summary" in html
    assert "<h2>Experience</h2>" not in html
    assert "<h2>Projects</h2>" not in html


def test_missing_template_files_fail_actionably(
    career: CareerProfile, resume_profile: ResumeProfile, tmp_path: Path
) -> None:
    selection = select_resume(career, resume_profile, "en")
    with pytest.raises(RenderError, match="Missing HTML template files"):
        render_html(selection, tmp_path)


def test_markdown_is_not_html_escaped(career: CareerProfile, resume_profile: ResumeProfile) -> None:
    summaries = [
        item.model_copy(
            update={"text": type(item.text).model_validate({"zh-TW": "研發", "en": "R&D"})}
        )
        for item in career.summaries
    ]
    updated = career.model_copy(update={"summaries": summaries})
    selection = select_resume(updated, resume_profile, "en")
    assert "R&D" in render_markdown(selection, TEMPLATES)
    assert "R&amp;D" in render_html(selection, TEMPLATES)
