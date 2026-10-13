# Data schema

## Verification states

- `verified`: supported by reviewed evidence.
- `user_provided`: supplied by the profile owner but not independently verified.
- `unverified`: provisional and excluded by the default resume profiles.

`evidence_url` and `last_reviewed` are optional. Never create placeholder evidence URLs that look real.

## Localization

Every reader-facing claim uses two independently editable fields:

```yaml
text:
  zh-TW: 可人工審查的繁體中文內容
  en: Independently reviewed English content
```

## Stable references

IDs use lowercase kebab-case. Resume configs select `summary_id`, `project_ids`, `achievement_ids`, and experience bullet IDs. Skill `evidence_refs` may point to an employment record, bullet, project, achievement, education record, or summary.

## Dates

Employment and education dates use `YYYY-MM`. Employment sets exactly one of `end_date` or `present: true`. An end date before the start date fails. Overlapping roles are permitted and surfaced as warnings.

## Canonical files

- `profile.yaml`: identity and summaries
- `experience.yaml`: one record per actual role
- `education.yaml`
- `skills.yaml`
- `achievements.yaml`
- `projects.yaml`

Empty sections use `[]`; templates omit empty optional sections cleanly.
