# Development

## Setup and checks

```bash
uv sync --frozen --extra dev
uv run ruff check .
uv run ruff format --check .
uv run pytest
uv run career validate
uv run career check-privacy
```

To regenerate the lockfile after an intentional dependency change, run `uv lock`, review the diff, then repeat every check.

## Pull request policy

Work on a feature branch. Do not commit directly to `master`, enable auto-merge, deploy, publish artifacts, or merge without explicit authorization. Before opening a PR, review all staged paths and the exact staged diff for accidental disclosure.

## PDF smoke test

Install local Chromium and Noto CJK fonts as documented in the README. The test suite skips the PDF smoke test when Chromium is unavailable; a skip must be reported as `NOT VERIFIED`, not a pass.
