"""Deterministic, configuration-driven resume selection."""

from __future__ import annotations

from dataclasses import dataclass

from .models import (
    Achievement,
    CareerBullet,
    CareerProfile,
    Education,
    Employment,
    Identity,
    Language,
    Project,
    ResumeProfile,
    SectionVisibility,
    Skill,
    SkillCategory,
)


@dataclass(frozen=True)
class SelectedEmployment:
    employment: Employment
    bullets: tuple[CareerBullet, ...]


@dataclass(frozen=True)
class ResumeSelection:
    language: Language
    identity: Identity
    headline: str
    summary: str
    employment: tuple[SelectedEmployment, ...]
    skills: tuple[tuple[SkillCategory, tuple[Skill, ...]], ...]
    projects: tuple[Project, ...]
    achievements: tuple[Achievement, ...]
    education: tuple[Education, ...]
    section_order: tuple[str, ...]
    sections: SectionVisibility
    profile_id: str


def select_resume(
    career: CareerProfile, profile: ResumeProfile, language: Language
) -> ResumeSelection:
    allowed = set(profile.allowed_verification_statuses)
    summaries = {item.id: item for item in career.summaries}
    summary = summaries[profile.summary_id]

    employment: list[SelectedEmployment] = []
    requested_roles = set(profile.experience_bullets)
    for role in career.employment:
        if role.id not in requested_roles or role.verification_status not in allowed:
            continue
        wanted = profile.experience_bullets[role.id]
        by_id = {bullet.id: bullet for bullet in role.bullets}
        selected = tuple(
            by_id[bullet_id]
            for bullet_id in wanted
            if by_id[bullet_id].verification_status in allowed
        )
        employment.append(SelectedEmployment(role, selected))

    category_order = {
        category: index for index, category in enumerate(profile.skill_category_order)
    }
    grouped: dict[SkillCategory, list[Skill]] = {
        category: [] for category in profile.skill_category_order
    }
    for skill in career.skills:
        if skill.category in grouped and skill.verification_status in allowed:
            grouped[skill.category].append(skill)
    skill_groups = tuple(
        (category, tuple(sorted(items, key=lambda item: (item.name.casefold(), item.id))))
        for category, items in sorted(grouped.items(), key=lambda pair: category_order[pair[0]])
        if items
    )

    project_by_id = {project.id: project for project in career.projects}
    projects = tuple(
        project_by_id[project_id]
        for project_id in profile.project_ids
        if project_by_id[project_id].verification_status in allowed
    )
    achievement_by_id = {achievement.id: achievement for achievement in career.achievements}
    achievements = tuple(
        achievement_by_id[achievement_id]
        for achievement_id in profile.achievement_ids
        if achievement_by_id[achievement_id].verification_status in allowed
    )
    education = tuple(item for item in career.education if item.verification_status in allowed)

    return ResumeSelection(
        language=language,
        identity=career.identity,
        headline=profile.headline.get(language),
        summary=summary.text.get(language),
        employment=tuple(employment),
        skills=skill_groups,
        projects=projects,
        achievements=achievements,
        education=education,
        section_order=tuple(profile.section_order),
        sections=profile.sections,
        profile_id=profile.id,
    )
