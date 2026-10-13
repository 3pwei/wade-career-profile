from career_profile.models import CareerProfile, ResumeProfile
from career_profile.selector import select_resume


def test_selection_is_deterministic(career: CareerProfile, resume_profile: ResumeProfile) -> None:
    first = select_resume(career, resume_profile, "en")
    second = select_resume(career, resume_profile, "en")
    assert first == second
    assert [item.name for item in first.skills[0][1]] == ["Python"]
    assert first.employment[0].bullets[0].id == "built-api"


def test_language_selects_independent_text(
    career: CareerProfile, resume_profile: ResumeProfile
) -> None:
    english = select_resume(career, resume_profile, "en")
    chinese = select_resume(career, resume_profile, "zh-TW")
    assert english.summary == "English summary"
    assert chinese.summary == "中文摘要"
