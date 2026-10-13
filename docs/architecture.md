# Architecture

## Design goals

The system favors a small local pipeline: canonical YAML, strict Pydantic models, explicit cross-file validation, deterministic selection, and presentation-only templates. It intentionally has no server, database, authentication layer, or network dependency at runtime.

## Data flow

1. `loader.py` reads either the split `data/public/` layout or one monolithic synthetic example.
2. `models.py` validates shape, URLs, localized text, status values, and date ranges.
3. `validator.py` enforces unique IDs and valid cross-file references. Overlapping jobs generate warnings, not errors.
4. `selector.py` uses a profile config to select canonical records in declared order and filters disallowed verification statuses.
5. `renderer.py` renders Jinja templates. `pdf.py` prints the generated HTML with local Chromium.
6. `privacy.py` scans public repository text and redacts detected values from diagnostics.

The selector does not calculate total years of experience. This avoids double-counting concurrent roles and prevents inferred claims.

## Future database integration

Models and loader are separated, so another repository implementation can produce the same `CareerProfile` object later. YAML remains authoritative in phase one; no speculative repository abstraction is introduced yet.
