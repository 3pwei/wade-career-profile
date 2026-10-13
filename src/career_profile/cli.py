"""Typer command-line interface."""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from .errors import CareerProfileError, PdfEnvironmentError, ValidationError
from .loader import discover_profiles, load_career_profile, load_resume_profile
from .models import Language
from .pdf import pdf_page_count, render_pdf
from .privacy import assert_repository_safe
from .renderer import (
    output_filename,
    render_html,
    render_markdown,
    write_text_output,
)
from .selector import select_resume
from .validator import validate_profile

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA_DIR = ROOT / "data" / "public"
DEFAULT_CONFIG_DIR = ROOT / "configs"
DEFAULT_TEMPLATE_DIR = ROOT / "templates"
DEFAULT_OUTPUT_DIR = ROOT / "dist"

app = typer.Typer(
    name="career",
    help="Validate career data and build privacy-conscious resume variants.",
    no_args_is_help=True,
)
console = Console()


class OutputFormat(StrEnum):
    MARKDOWN = "markdown"
    HTML = "html"
    PDF = "pdf"


def _language(value: str) -> Language:
    if value not in {"zh-TW", "en"}:
        raise typer.BadParameter("must be one of: zh-TW, en")
    return value  # type: ignore[return-value]


def _profile_path(profile_id: str, config_dir: Path) -> Path:
    profiles = discover_profiles(config_dir)
    if profile_id not in profiles:
        available = ", ".join(profiles)
        raise ValidationError(
            f"Unsupported resume profile '{profile_id}'. Available profiles: {available}"
        )
    return profiles[profile_id]


def _build_one(
    profile_id: str,
    language: Language,
    output_format: OutputFormat,
    data_dir: Path,
    output_dir: Path,
    config_dir: Path,
    template_dir: Path,
) -> Path:
    career = load_career_profile(data_dir)
    resume_profile = load_resume_profile(_profile_path(profile_id, config_dir))
    report = validate_profile(career, resume_profile)
    for warning in report.warnings:
        console.print(f"[yellow]Warning:[/yellow] {warning}")
    selected = select_resume(career, resume_profile, language)
    destination = output_dir / profile_id

    if output_format == OutputFormat.MARKDOWN:
        path = destination / output_filename(profile_id, language, "md")
        return write_text_output(render_markdown(selected, template_dir), path)
    html_path = destination / output_filename(profile_id, language, "html")
    write_text_output(render_html(selected, template_dir), html_path)
    if output_format == OutputFormat.HTML:
        return html_path
    pdf_path = destination / output_filename(profile_id, language, "pdf")
    render_pdf(html_path, pdf_path, require_cjk=language == "zh-TW")
    pages = pdf_page_count(pdf_path)
    if pages and pages > 2:
        console.print(
            f"[yellow]Warning:[/yellow] PDF has {pages} pages. Prioritize content instead of "
            "shrinking typography."
        )
    return pdf_path


@app.command("validate")
def validate_command(
    data_dir: Annotated[Path, typer.Option(help="Canonical YAML directory or monolithic file.")] = (
        DEFAULT_DATA_DIR
    ),
    config_dir: Annotated[Path, typer.Option(help="Resume profile configuration directory.")] = (
        DEFAULT_CONFIG_DIR
    ),
) -> None:
    """Validate canonical data and every configured resume profile."""
    try:
        career = load_career_profile(data_dir)
        all_warnings: set[str] = set()
        for profile_id, path in discover_profiles(config_dir).items():
            profile = load_resume_profile(path)
            if profile.id != profile_id:
                raise ValidationError(
                    f"Profile filename '{profile_id}' does not match declared id '{profile.id}'"
                )
            all_warnings.update(validate_profile(career, profile).warnings)
        console.print("[green]Career data and resume profiles are valid.[/green]")
        for warning in sorted(all_warnings):
            console.print(f"[yellow]Warning:[/yellow] {warning}")
    except CareerProfileError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(1) from exc


@app.command("list-profiles")
def list_profiles(
    config_dir: Annotated[Path, typer.Option(help="Resume profile configuration directory.")] = (
        DEFAULT_CONFIG_DIR
    ),
) -> None:
    """List available profile IDs in deterministic order."""
    try:
        for profile_id in discover_profiles(config_dir):
            console.print(profile_id)
    except CareerProfileError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(1) from exc


@app.command("build")
def build_command(
    profile: Annotated[str, typer.Option(help="Resume profile ID.")],
    lang: Annotated[str, typer.Option(help="Output language: en or zh-TW.")],
    output_format: Annotated[
        OutputFormat, typer.Option("--format", help="Output format: markdown, html, or pdf.")
    ],
    data_dir: Annotated[Path, typer.Option(help="Canonical YAML directory or monolithic file.")] = (
        DEFAULT_DATA_DIR
    ),
    output_dir: Annotated[Path, typer.Option(help="Generated output directory.")] = (
        DEFAULT_OUTPUT_DIR
    ),
    config_dir: Annotated[Path, typer.Option(help="Resume profile configuration directory.")] = (
        DEFAULT_CONFIG_DIR
    ),
    template_dir: Annotated[Path, typer.Option(help="Template directory.")] = DEFAULT_TEMPLATE_DIR,
) -> None:
    """Build one resume variant without changing source YAML."""
    try:
        path = _build_one(
            profile,
            _language(lang),
            output_format,
            data_dir,
            output_dir,
            config_dir,
            template_dir,
        )
        console.print(f"[green]Built:[/green] {path}")
    except (CareerProfileError, PdfEnvironmentError) as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(1) from exc


@app.command("build-all")
def build_all(
    data_dir: Annotated[Path, typer.Option(help="Canonical YAML directory or monolithic file.")] = (
        DEFAULT_DATA_DIR
    ),
    output_dir: Annotated[Path, typer.Option(help="Generated output directory.")] = (
        DEFAULT_OUTPUT_DIR
    ),
    config_dir: Annotated[Path, typer.Option(help="Resume profile configuration directory.")] = (
        DEFAULT_CONFIG_DIR
    ),
    template_dir: Annotated[Path, typer.Option(help="Template directory.")] = DEFAULT_TEMPLATE_DIR,
    include_pdf: Annotated[
        bool, typer.Option("--pdf/--no-pdf", help="Include local PDF generation.")
    ] = True,
) -> None:
    """Build every profile, language, and supported format."""
    formats = [OutputFormat.MARKDOWN, OutputFormat.HTML]
    if include_pdf:
        formats.append(OutputFormat.PDF)
    try:
        for profile_id in discover_profiles(config_dir):
            for language in ("en", "zh-TW"):
                for output_format in formats:
                    path = _build_one(
                        profile_id,
                        _language(language),
                        output_format,
                        data_dir,
                        output_dir,
                        config_dir,
                        template_dir,
                    )
                    console.print(f"[green]Built:[/green] {path}")
    except CareerProfileError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(1) from exc


@app.command("check-privacy")
def check_privacy(
    repository_root: Annotated[
        Path, typer.Option(help="Repository tree to scan; private/ and dist/ are excluded.")
    ] = ROOT,
    allowlist: Annotated[
        Path | None, typer.Option(help="Optional exact-value public contact allowlist.")
    ] = None,
) -> None:
    """Fail on clear sensitive values while redacting every diagnostic."""
    try:
        resolved_allowlist = allowlist or repository_root / "privacy-allowlist.yaml"
        assert_repository_safe(repository_root, resolved_allowlist)
        console.print("[green]Privacy check passed.[/green]")
    except CareerProfileError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(1) from exc


if __name__ == "__main__":
    app()
