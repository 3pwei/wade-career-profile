from __future__ import annotations

import copy

import pytest
from pydantic import ValidationError

from career_profile.models import CareerProfile, Employment


def test_valid_profile_loads(career_payload: dict[str, object]) -> None:
    profile = CareerProfile.model_validate(career_payload)
    assert profile.identity.professional_name == "Morgan Lin"


def test_invalid_schema_fails(career_payload: dict[str, object]) -> None:
    payload = copy.deepcopy(career_payload)
    del payload["identity"]
    with pytest.raises(ValidationError):
        CareerProfile.model_validate(payload)


def test_invalid_url_fails(career_payload: dict[str, object]) -> None:
    payload = copy.deepcopy(career_payload)
    payload["identity"]["website"] = "not-a-url"
    with pytest.raises(ValidationError, match="website"):
        CareerProfile.model_validate(payload)


def test_invalid_date_range_fails() -> None:
    with pytest.raises(ValidationError, match="end_date must not be earlier"):
        Employment.model_validate(
            {
                "id": "bad-role",
                "employer": "Example",
                "position": {"zh-TW": "工程師", "en": "Engineer"},
                "employment_type": "full-time",
                "start_date": "2024-01",
                "end_date": "2023-12",
                "present": False,
                "technologies": [],
                "bullets": [],
                "verification_status": "verified",
            }
        )


def test_end_date_and_present_are_mutually_exclusive() -> None:
    with pytest.raises(ValidationError, match="exactly one"):
        Employment.model_validate(
            {
                "id": "bad-role",
                "employer": "Example",
                "position": {"zh-TW": "工程師", "en": "Engineer"},
                "employment_type": "full-time",
                "start_date": "2024-01",
                "end_date": "2024-12",
                "present": True,
                "verification_status": "verified",
            }
        )
