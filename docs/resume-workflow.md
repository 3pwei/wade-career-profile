# Resume workflow

1. Record incomplete facts in ignored local files under `private/`.
2. Verify dates, wording, evidence, and whether the fact is safe to publish.
3. Add one canonical record to `data/public/` with a stable ID and honest verification status.
4. Reference the ID from one or more files in `configs/`; do not copy the fact.
5. Run validation, privacy scan, tests, and English／Traditional Chinese builds.
6. For PDF, inspect the actual pages and confirm selectable text, links, spacing, clipping, and page breaks.
7. Review the exact staged diff before commit and open a PR. Never merge automatically.

Generated files belong in `dist/` and are ignored. Builds never modify YAML input.

## Reviewed experience promoted on 2026-10-22

The owner authorized promotion of reviewed work experience into canonical bilingual data.
`experience.yaml` now includes Sinica analysis/modeling/data workflows, EnSense engineering
and delegated leadership, and Wiwynn integration/operations cases. All remain
`user_provided`, not independently `verified`. The five role configs explicitly select
bullets, and employment is stored in reverse chronology. The WITS assignment dates remain
separate from the employer dates; the existing leave/exit record is retained in canonical
data but is not selected for resumes.

Sources: `docs/career-review/ensense-engineering-cases.md`,
`docs/career-review/wiwynn-consolidated-eight-cases.md`, and
`docs/reviews/sinica-six-case-career-review.md`. These are historical review notes;
canonical YAML is now authoritative for the promoted wording.

Wiwynn's three-person Azure inspection automation retains the owner-confirmed
3-hour to 30-minute comparison. EnSense retains its separate half-day to 30-minute
monitoring comparison, without converting half-day into an assumed percentage.
Uncleared Wiwynn platform-wide/private metrics and uncertain Elasticsearch incident
details are not promoted. Logging remains explicitly a PoC. ITRI employment remains
excluded pending date confirmation. Education and publication records are outside this change.

Synthetic CLI examples must use `--config-dir examples/configs` with
`--data-dir examples/sample-profile.yaml`; production configs reference real employment IDs.
CI checks all real Markdown/HTML outputs for the four included employers.
