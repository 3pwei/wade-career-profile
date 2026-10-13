# AGENTS.md

These instructions apply to the entire repository.

## Mission

Maintain a truthful, privacy-conscious, reproducible career profile and resume system. YAML under
`data/` is the canonical source; resume variants may select facts but must not rewrite them.

## Coding conventions

- Use Python 3.12+, type hints, small focused modules, and explicit error handling.
- Keep dependencies minimal and pinned in `pyproject.toml` and `uv.lock`.
- Run `ruff check .`, `ruff format --check .`, and `pytest` before proposing changes.
- Preserve deterministic ordering and output names. Never mutate source YAML during a build.

## Data integrity

- Use stable IDs and references. Do not copy employment records into variant configuration.
- Never fabricate career claims, dates, qualifications, evidence URLs, metrics, or years of
  experience.
- Treat `user_provided` as distinct from independently `verified`.
- Allow legitimate overlapping roles, but warn about overlaps and never naively sum their durations.
- Mark incomplete facts as TODOs in ignored local files under `private/`, not in public claims.

## Privacy

- Assume the repository and its full Git history are public.
- Never commit private contact details, residential addresses, identity numbers, salaries,
  credentials, confidential employer material, application notes, or private strategy details.
- Use synthetic fixtures in tests. Redact sensitive values from diagnostics.
- Before every commit, inspect the exact staged diff and run `career check-privacy`.
- An allowlist may cover intentionally public contact details only. It must never allow secrets or
  identity numbers.

## Pull requests

- Do not commit directly to `master` after repository initialization.
- Use a feature branch, open a PR, and wait for explicit authorization before merging.
- Do not enable auto-merge, deploy production systems, publish resumes, or create releases.
- Report unverified acceptance criteria as `NOT VERIFIED`, never as passing.
