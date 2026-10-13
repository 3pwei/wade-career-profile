"""Cross-file integrity validation and non-fatal chronology warnings."""

from __future__ import annotations

from dataclasses import dataclass

from .errors import ValidationError
from .models import CareerProfile, ResumeProfile


@dataclass(frozen=True)
class ValidationReport:
    warnings: tuple[str, ...] = ()


def _duplicates(values: list[str]) -> list[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return sorted(duplicates)


def _employment_overlap_warnings(profile: CareerProfile) -> list[str]:
    warnings: list[str] = []
    dated = sorted(profile.employment, key=lambda item: item.start_date)
    for index, left in enumerate(dated):
        left_end = left.end_date or "9999-12"
        for right in dated[index + 1 :]:
            right_end = right.end_date or "9999-12"
            if right.start_date <= left_end and left.start_date <= right_end:
                warnings.append(
                    f"Employment periods overlap: '{left.id}' and '{right.id}'. "
                    "This is allowed; review it for accuracy."
                )
    return warnings


def validate_profile(
    profile: CareerProfile, resume_profile: ResumeProfile | None = None
) -> ValidationReport:
    errors: list[str] = []

    collections = {
        "summaries": [item.id for item in profile.summaries],
        "employment": [item.id for item in profile.employment],
        "education": [item.id for item in profile.education],
        "skills": [item.id for item in profile.skills],
        "achievements": [item.id for item in profile.achievements],
        "projects": [item.id for item in profile.projects],
    }
    for label, identifiers in collections.items():
        duplicate_ids = _duplicates(identifiers)
        if duplicate_ids:
            errors.append(f"Duplicate {label} IDs: {', '.join(duplicate_ids)}")

    bullet_ids: list[str] = []
    for employment in profile.employment:
        bullet_ids.extend(bullet.id for bullet in employment.bullets)
        duplicates = _duplicates([bullet.id for bullet in employment.bullets])
        if duplicates:
            errors.append(f"Duplicate bullet IDs in '{employment.id}': {', '.join(duplicates)}")
    duplicate_bullet_ids = _duplicates(bullet_ids)
    if duplicate_bullet_ids:
        errors.append(f"Duplicate bullet IDs across employment: {', '.join(duplicate_bullet_ids)}")

    evidence_targets = set().union(*[set(values) for values in collections.values()], bullet_ids)
    for skill in profile.skills:
        missing = sorted(set(skill.evidence_refs) - evidence_targets)
        if missing:
            errors.append(f"Skill '{skill.id}' has broken evidence refs: {', '.join(missing)}")

    if resume_profile:
        summary_ids = set(collections["summaries"])
        project_ids = set(collections["projects"])
        achievement_ids = set(collections["achievements"])
        employment_by_id = {item.id: item for item in profile.employment}

        if resume_profile.summary_id not in summary_ids:
            errors.append(f"Profile references missing summary '{resume_profile.summary_id}'")
        missing_projects = sorted(set(resume_profile.project_ids) - project_ids)
        if missing_projects:
            errors.append(f"Profile references missing projects: {', '.join(missing_projects)}")
        missing_achievements = sorted(set(resume_profile.achievement_ids) - achievement_ids)
        if missing_achievements:
            errors.append(
                f"Profile references missing achievements: {', '.join(missing_achievements)}"
            )
        for employment_id, selected_bullets in resume_profile.experience_bullets.items():
            employment = employment_by_id.get(employment_id)
            if not employment:
                errors.append(f"Profile references missing employment '{employment_id}'")
                continue
            available = {bullet.id for bullet in employment.bullets}
            missing_bullets = sorted(set(selected_bullets) - available)
            if missing_bullets:
                errors.append(
                    f"Profile references missing bullets in '{employment_id}': "
                    f"{', '.join(missing_bullets)}"
                )

    if errors:
        raise ValidationError("Cross-file validation failed:\n- " + "\n- ".join(errors))
    return ValidationReport(tuple(_employment_overlap_warnings(profile)))
