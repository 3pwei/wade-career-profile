from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
import yaml

from career_profile.models import CareerProfile, ResumeProfile


@pytest.fixture
def career_payload() -> dict[str, Any]:
    verification = {"verification_status": "verified", "evidence_url": None, "last_reviewed": None}
    local = lambda zh, en: {"zh-TW": zh, "en": en}  # noqa: E731
    return {
        "identity": {
            "full_name": "Morgan Lin",
            "professional_name": "Morgan Lin",
            "headline": local("測試工程師", "Test Engineer"),
            "location": local("測試城市", "Test City"),
            "website": "https://example.com",
            "github": "https://github.com/example",
            "linkedin": None,
            "private_contact": None,
        },
        "summaries": [
            {"id": "general", "text": local("中文摘要", "English summary"), **verification}
        ],
        "employment": [
            {
                "id": "example-role",
                "employer": "Example Works",
                "position": local("軟體工程師", "Software Engineer"),
                "employment_type": "full-time",
                "start_date": "2022-01",
                "end_date": "2023-12",
                "present": False,
                "location": None,
                "technologies": ["Python"],
                "bullets": [
                    {
                        "id": "built-api",
                        "kind": "responsibility",
                        "text": local("建立合成測試 API。", "Built a synthetic test API."),
                        "relevance_tags": ["backend"],
                        "quantified_impact": None,
                        **verification,
                    }
                ],
                **verification,
            }
        ],
        "education": [],
        "skills": [
            {
                "id": "python",
                "name": "Python",
                "category": "programming-languages",
                "evidence_refs": ["example-role"],
                "proficiency": None,
                **verification,
            }
        ],
        "achievements": [],
        "projects": [
            {
                "id": "example-project",
                "name": "Synthetic Project",
                "domain": local("測試", "Testing"),
                "summary": local("只供測試。", "For testing only."),
                "repository_url": "https://github.com/example/synthetic-project",
                "demo_url": None,
                "technologies": ["Python"],
                "architecture_highlights": [],
                "responsibilities": [],
                "engineering_challenges": [],
                "verified_outcomes": [],
                "visibility": "public",
                "relevance_tags": ["backend"],
                **verification,
            }
        ],
    }


@pytest.fixture
def career(career_payload: dict[str, Any]) -> CareerProfile:
    return CareerProfile.model_validate(career_payload)


@pytest.fixture
def resume_profile() -> ResumeProfile:
    return ResumeProfile.model_validate(
        {
            "id": "general",
            "headline": {"zh-TW": "測試工程師", "en": "Test Engineer"},
            "summary_id": "general",
            "skill_category_order": ["programming-languages"],
            "project_ids": ["example-project"],
            "achievement_ids": [],
            "experience_bullets": {"example-role": ["built-api"]},
            "section_order": ["summary", "experience", "skills", "projects", "education"],
            "sections": {
                "experience": True,
                "education": True,
                "skills": True,
                "projects": True,
                "achievements": True,
            },
            "allowed_verification_statuses": ["verified", "user_provided"],
        }
    )


@pytest.fixture
def data_dir(tmp_path: Path, career_payload: dict[str, Any]) -> Path:
    mapping = {
        "profile.yaml": {
            "identity": career_payload["identity"],
            "summaries": career_payload["summaries"],
        },
        "experience.yaml": {"employment": career_payload["employment"]},
        "education.yaml": {"education": career_payload["education"]},
        "skills.yaml": {"skills": career_payload["skills"]},
        "achievements.yaml": {"achievements": career_payload["achievements"]},
        "projects.yaml": {"projects": career_payload["projects"]},
    }
    for filename, document in mapping.items():
        (tmp_path / filename).write_text(
            yaml.safe_dump(document, allow_unicode=True, sort_keys=False), encoding="utf-8"
        )
    return tmp_path


@pytest.fixture
def config_dir(tmp_path: Path, resume_profile: ResumeProfile) -> Path:
    path = tmp_path / "configs"
    path.mkdir()
    (path / "general.yaml").write_text(
        yaml.safe_dump(
            resume_profile.model_dump(by_alias=True, mode="json"),
            allow_unicode=True,
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    return path
