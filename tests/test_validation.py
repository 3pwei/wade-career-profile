from __future__ import annotations

import copy

import pytest

from career_profile.errors import ValidationError
from career_profile.models import CareerProfile, ResumeProfile
from career_profile.validator import validate_profile


def test_duplicate_ids_fail(career_payload: dict[str, object]) -> None:
    payload = copy.deepcopy(career_payload)
    payload["skills"].append(copy.deepcopy(payload["skills"][0]))
    with pytest.raises(ValidationError, match="Duplicate skills IDs"):
        validate_profile(CareerProfile.model_validate(payload))


def test_missing_project_reference_fails(
    career: CareerProfile, resume_profile: ResumeProfile
) -> None:
    broken = resume_profile.model_copy(update={"project_ids": ["missing-project"]})
    with pytest.raises(ValidationError, match="missing projects"):
        validate_profile(career, broken)


def test_broken_skill_evidence_reference_fails(career_payload: dict[str, object]) -> None:
    payload = copy.deepcopy(career_payload)
    payload["skills"][0]["evidence_refs"] = ["missing-evidence"]
    with pytest.raises(ValidationError, match="broken evidence refs"):
        validate_profile(CareerProfile.model_validate(payload))


def test_overlap_warns_but_does_not_fail(career_payload: dict[str, object]) -> None:
    payload = copy.deepcopy(career_payload)
    second = copy.deepcopy(payload["employment"][0])
    second["id"] = "overlapping-role"
    second["start_date"] = "2023-06"
    second["end_date"] = "2024-06"
    second["bullets"] = []
    payload["employment"].append(second)
    report = validate_profile(CareerProfile.model_validate(payload))
    assert report.warnings
    assert "allowed" in report.warnings[0]


def test_bullet_ids_are_unique_across_employment(career_payload: dict[str, object]) -> None:
    payload = copy.deepcopy(career_payload)
    second = copy.deepcopy(payload["employment"][0])
    second["id"] = "second-role"
    second["start_date"] = "2024-01"
    second["end_date"] = "2024-12"
    payload["employment"].append(second)
    with pytest.raises(ValidationError, match="across employment"):
        validate_profile(CareerProfile.model_validate(payload))
