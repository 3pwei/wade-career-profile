"""Render Markdown and standalone HTML from a selected resume."""

from __future__ import annotations

import re
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from .errors import RenderError
from .models import Language
from .selector import ResumeSelection

PROFILE_LABELS = {
    "general": "General",
    "backend-engineer": "Backend_Engineer",
    "data-engineer": "Data_Engineer",
    "cloud-platform-engineer": "Cloud_Platform_Engineer",
    "data-analyst": "Data_Analyst",
}


def _environment(template_dir: Path, *, autoescape: bool) -> Environment:
    if not template_dir.is_dir():
        raise RenderError(f"Missing template directory: {template_dir}")
    return Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=autoescape,
        undefined=StrictUndefined,
        keep_trailing_newline=True,
    )


def _context(selection: ResumeSelection) -> dict[str, object]:
    language = selection.language
    return {
        "resume": selection,
        "lang": language,
        "localize": lambda value: value.get(language),
        "category_label": lambda value: value.value.replace("-", " ").title(),
        "date_label": lambda value: value or ("至今" if language == "zh-TW" else "Present"),
        "section_labels": {
            "summary": "專業摘要" if language == "zh-TW" else "Professional Summary",
            "experience": "工作經歷" if language == "zh-TW" else "Experience",
            "skills": "技術能力" if language == "zh-TW" else "Technical Skills",
            "projects": "專案作品" if language == "zh-TW" else "Projects",
            "achievements": "專業成就" if language == "zh-TW" else "Achievements",
            "education": "學歷" if language == "zh-TW" else "Education",
        },
    }


def render_markdown(selection: ResumeSelection, template_dir: Path) -> str:
    path = template_dir / "resume.md.j2"
    if not path.is_file():
        raise RenderError(f"Missing Markdown template: {path}")
    return (
        _environment(template_dir, autoescape=False)
        .get_template(path.name)
        .render(**_context(selection))
    )


def render_html(selection: ResumeSelection, template_dir: Path) -> str:
    template_path = template_dir / "resume.html.j2"
    css_path = template_dir / "styles" / "resume.css"
    missing = [str(path) for path in (template_path, css_path) if not path.is_file()]
    if missing:
        raise RenderError(f"Missing HTML template files: {', '.join(missing)}")
    context = _context(selection)
    context["css"] = css_path.read_text(encoding="utf-8")
    return (
        _environment(template_dir, autoescape=True)
        .get_template(template_path.name)
        .render(**context)
    )


def output_filename(profile_id: str, language: Language, extension: str) -> str:
    if profile_id not in PROFILE_LABELS:
        raise RenderError(f"Unsupported resume profile name: {profile_id}")
    lang_label = "ZH" if language == "zh-TW" else "EN"
    safe_extension = re.sub(r"[^a-z]", "", extension.lower())
    return f"Wade_Huang_{PROFILE_LABELS[profile_id]}_{lang_label}.{safe_extension}"


def write_text_output(content: str, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8", newline="\n")
    return output_path
