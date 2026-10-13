# Privacy model

Assume the repository and every reachable commit are public forever. Changing visibility later does not remove secrets or personal records from Git history.

## Never commit

- private phone, residential address, identity numbers, or private email;
- salary records, application notes, confidential employer material;
- credentials, API keys, tokens, environment files, or private keys;
- private research or trading strategies;
- generated resumes that may combine otherwise separate facts.

## Scanner behavior

`career check-privacy` scans text files outside `.git/`, `.venv/`, `private/`, and `dist/`. Findings report file, line, and category only; matched values are redacted. It is a defense-in-depth check, not proof that content is appropriate for publication.

The allowlist is exact-value only and is intended for deliberately public contact details. Secret, private-key, and identity-number findings cannot be allowlisted.

## Pre-commit review

Run the scanner, inspect `git status`, inspect `git diff --cached`, and verify that every public career claim is both truthful and appropriately classified. If accidental sensitive data reached Git, stop and rotate affected credentials before rewriting history.
