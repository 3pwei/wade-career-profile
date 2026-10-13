"""Load canonical YAML files without mutating their contents."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError as PydanticValidationError

from .errors import DataLoadError
from .models import CareerProfile, ResumeProfile

DATA_FILES = {
    "identity": ("profile.yaml", "identity"),
    "summaries": ("profile.yaml", "summaries"),
    "employment": ("experience.yaml", "employment"),
    "education": ("education.yaml", "education"),
    "skills": ("skills.yaml", "skills"),
    "achievements": ("achievements.yaml", "achievements"),
    "projects": ("projects.yaml", "projects"),
}


def _read_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise DataLoadError(f"Missing YAML file: {path}")
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise DataLoadError(f"Cannot read YAML file {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise DataLoadError(f"Expected a YAML mapping in {path}")
    return value


def load_career_profile(data_dir: Path) -> CareerProfile:
    if data_dir.is_file():
        document = _read_yaml(data_dir)
        try:
            return CareerProfile.model_validate(document)
        except PydanticValidationError as exc:
            raise DataLoadError(f"Career data validation failed in {data_dir}:\n{exc}") from exc
    cache: dict[Path, dict[str, Any]] = {}
    payload: dict[str, Any] = {}
    for model_field, (filename, yaml_key) in DATA_FILES.items():
        path = data_dir / filename
        if path not in cache:
            cache[path] = _read_yaml(path)
        document = cache[path]
        if yaml_key not in document:
            raise DataLoadError(f"Missing top-level key '{yaml_key}' in {path}")
        payload[model_field] = document[yaml_key]
    try:
        return CareerProfile.model_validate(payload)
    except PydanticValidationError as exc:
        raise DataLoadError(f"Career data validation failed:\n{exc}") from exc


def load_resume_profile(config_path: Path) -> ResumeProfile:
    try:
        return ResumeProfile.model_validate(_read_yaml(config_path))
    except PydanticValidationError as exc:
        raise DataLoadError(f"Resume profile validation failed in {config_path}:\n{exc}") from exc


def discover_profiles(config_dir: Path) -> dict[str, Path]:
    if not config_dir.is_dir():
        raise DataLoadError(f"Missing profile configuration directory: {config_dir}")
    profiles = {path.stem: path for path in sorted(config_dir.glob("*.yaml"))}
    if not profiles:
        raise DataLoadError(f"No resume profiles found in {config_dir}")
    return profiles
