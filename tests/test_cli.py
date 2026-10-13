from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from career_profile.cli import app

runner = CliRunner()
TEMPLATES = Path(__file__).resolve().parents[1] / "templates"


def test_cli_help_works() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "check-privacy" in result.stdout


def test_cli_builds_markdown_with_expected_name(
    data_dir: Path, config_dir: Path, tmp_path: Path
) -> None:
    output_dir = tmp_path / "output"
    result = runner.invoke(
        app,
        [
            "build",
            "--profile",
            "general",
            "--lang",
            "en",
            "--format",
            "markdown",
            "--data-dir",
            str(data_dir),
            "--config-dir",
            str(config_dir),
            "--template-dir",
            str(TEMPLATES),
            "--output-dir",
            str(output_dir),
        ],
    )
    assert result.exit_code == 0, result.stdout
    expected = output_dir / "general" / "Wade_Huang_General_EN.md"
    assert expected.is_file()
    assert "English summary" in expected.read_text(encoding="utf-8")


def test_cli_rejects_unsupported_language(data_dir: Path, config_dir: Path, tmp_path: Path) -> None:
    result = runner.invoke(
        app,
        [
            "build",
            "--profile",
            "general",
            "--lang",
            "fr",
            "--format",
            "html",
            "--data-dir",
            str(data_dir),
            "--config-dir",
            str(config_dir),
            "--template-dir",
            str(TEMPLATES),
            "--output-dir",
            str(tmp_path / "out"),
        ],
    )
    assert result.exit_code != 0
    assert "must be one of" in result.stderr


def test_cli_validation_failure_returns_nonzero(tmp_path: Path, config_dir: Path) -> None:
    broken = tmp_path / "broken"
    broken.mkdir()
    (broken / "profile.yaml").write_text("identity: {}\n", encoding="utf-8")
    result = runner.invoke(
        app,
        ["validate", "--data-dir", str(broken), "--config-dir", str(config_dir)],
    )
    assert result.exit_code == 1
    assert "Missing top-level key" in result.stdout


def test_cli_rejects_unsupported_profile(data_dir: Path, config_dir: Path, tmp_path: Path) -> None:
    result = runner.invoke(
        app,
        [
            "build",
            "--profile",
            "unknown-profile",
            "--lang",
            "en",
            "--format",
            "markdown",
            "--data-dir",
            str(data_dir),
            "--config-dir",
            str(config_dir),
            "--template-dir",
            str(TEMPLATES),
            "--output-dir",
            str(tmp_path / "out"),
        ],
    )
    assert result.exit_code == 1
    assert "Unsupported resume profile" in result.stdout
