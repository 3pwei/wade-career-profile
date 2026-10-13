"""Pydantic models for canonical career data and resume profiles."""

from __future__ import annotations

from datetime import date
from enum import StrEnum
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, model_validator

StableId = Annotated[str, Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")]
YearMonth = Annotated[str, Field(pattern=r"^\d{4}-(?:0[1-9]|1[0-2])$")]
Language = Literal["zh-TW", "en"]


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True, str_strip_whitespace=True)


class VerificationStatus(StrEnum):
    VERIFIED = "verified"
    USER_PROVIDED = "user_provided"
    UNVERIFIED = "unverified"


class Verification(StrictModel):
    verification_status: VerificationStatus
    evidence_url: HttpUrl | None = None
    last_reviewed: date | None = None


class LocalizedText(StrictModel):
    zh_tw: str = Field(alias="zh-TW", min_length=1)
    en: str = Field(min_length=1)

    def get(self, language: Language) -> str:
        return self.zh_tw if language == "zh-TW" else self.en


class PrivateContact(StrictModel):
    email: str | None = None
    phone: str | None = None
    address: str | None = None


class Identity(StrictModel):
    full_name: str
    professional_name: str
    headline: LocalizedText
    location: LocalizedText
    website: HttpUrl | None = None
    github: HttpUrl | None = None
    linkedin: HttpUrl | None = None
    private_contact: PrivateContact | None = None


class Summary(Verification):
    id: StableId
    text: LocalizedText


class CareerBullet(Verification):
    id: StableId
    kind: Literal["responsibility", "achievement"]
    text: LocalizedText
    relevance_tags: list[StableId] = Field(default_factory=list)
    quantified_impact: LocalizedText | None = None


class Employment(Verification):
    id: StableId
    employer: str
    position: LocalizedText
    employment_type: str
    start_date: YearMonth
    end_date: YearMonth | None = None
    present: bool = False
    location: LocalizedText | None = None
    technologies: list[str] = Field(default_factory=list)
    bullets: list[CareerBullet] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_dates(self) -> Employment:
        if self.present == (self.end_date is not None):
            raise ValueError("exactly one of present=true or end_date must be set")
        if self.end_date and self.end_date < self.start_date:
            raise ValueError("end_date must not be earlier than start_date")
        return self


class Education(Verification):
    id: StableId
    institution: str
    degree: LocalizedText
    field_of_study: LocalizedText
    start_date: YearMonth
    end_date: YearMonth | None = None
    research_focus: LocalizedText | None = None
    achievements: list[LocalizedText] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_dates(self) -> Education:
        if self.end_date and self.end_date < self.start_date:
            raise ValueError("end_date must not be earlier than start_date")
        return self


class SkillCategory(StrEnum):
    PROGRAMMING = "programming-languages"
    BACKEND = "backend-engineering"
    DATA_ENGINEERING = "data-engineering"
    CLOUD = "cloud-platforms"
    DEVOPS = "devops-ci-cd"
    DATABASES = "databases"
    ANALYTICS = "data-analytics"
    AUTOMATION = "automation"
    RELIABILITY = "monitoring-reliability"
    OTHER = "other-relevant-skills"


class Skill(Verification):
    id: StableId
    name: str
    category: SkillCategory
    evidence_refs: list[StableId] = Field(default_factory=list)
    proficiency: LocalizedText | None = None


class Project(Verification):
    id: StableId
    name: str
    domain: LocalizedText
    summary: LocalizedText
    repository_url: HttpUrl | None = None
    demo_url: HttpUrl | None = None
    technologies: list[str] = Field(default_factory=list)
    architecture_highlights: list[LocalizedText] = Field(default_factory=list)
    responsibilities: list[LocalizedText] = Field(default_factory=list)
    engineering_challenges: list[LocalizedText] = Field(default_factory=list)
    verified_outcomes: list[LocalizedText] = Field(default_factory=list)
    visibility: Literal["public", "private"]
    relevance_tags: list[StableId] = Field(default_factory=list)


class Achievement(Verification):
    id: StableId
    type: Literal[
        "publication",
        "research",
        "engineering-improvement",
        "certification",
        "award",
        "business-outcome",
    ]
    title: LocalizedText
    description: LocalizedText | None = None
    relevance_tags: list[StableId] = Field(default_factory=list)


class CareerProfile(StrictModel):
    identity: Identity
    summaries: list[Summary]
    employment: list[Employment]
    education: list[Education]
    skills: list[Skill]
    achievements: list[Achievement]
    projects: list[Project]


class SectionVisibility(StrictModel):
    experience: bool = True
    education: bool = True
    skills: bool = True
    projects: bool = True
    achievements: bool = True


class ResumeProfile(StrictModel):
    id: StableId
    headline: LocalizedText
    summary_id: StableId
    skill_category_order: list[SkillCategory]
    project_ids: list[StableId]
    achievement_ids: list[StableId] = Field(default_factory=list)
    experience_bullets: dict[StableId, list[StableId]] = Field(default_factory=dict)
    section_order: list[
        Literal["summary", "experience", "skills", "projects", "achievements", "education"]
    ]
    sections: SectionVisibility = Field(default_factory=SectionVisibility)
    allowed_verification_statuses: list[VerificationStatus] = Field(
        default_factory=lambda: [VerificationStatus.VERIFIED, VerificationStatus.USER_PROVIDED]
    )

    @model_validator(mode="after")
    def validate_ordering(self) -> ResumeProfile:
        unique_lists = {
            "skill_category_order": self.skill_category_order,
            "project_ids": self.project_ids,
            "achievement_ids": self.achievement_ids,
            "section_order": self.section_order,
            "allowed_verification_statuses": self.allowed_verification_statuses,
        }
        for label, values in unique_lists.items():
            if len(values) != len(set(values)):
                raise ValueError(f"{label} must not contain duplicates")
        if "summary" not in self.section_order:
            raise ValueError("section_order must include summary")
        return self
