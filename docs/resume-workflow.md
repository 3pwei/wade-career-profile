# Resume workflow

1. Record incomplete facts in ignored local files under `private/`.
2. Verify dates, wording, evidence, and whether the fact is safe to publish.
3. Add one canonical record to `data/public/` with a stable ID and honest verification status.
4. Reference the ID from one or more files in `configs/`; do not copy the fact.
5. Run validation, privacy scan, tests, and English／Traditional Chinese builds.
6. For PDF, inspect the actual pages and confirm selectable text, links, spacing, clipping, and page breaks.
7. Review the exact staged diff before commit and open a PR. Never merge automatically.

Generated files belong in `dist/` and are ignored. Builds never modify YAML input.
