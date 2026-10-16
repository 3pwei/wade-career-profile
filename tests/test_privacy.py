from __future__ import annotations

from pathlib import Path

import pytest

from career_profile.errors import PrivacyError
from career_profile.privacy import assert_public_tree_safe, load_allowlist, scan_text


def test_sensitive_value_is_redacted() -> None:
    unsafe = "api" + "_key = " + "synthetic-secret-value"
    findings = scan_text(unsafe, Path("fixture.yaml"))
    assert findings
    diagnostic = findings[0].diagnostic()
    assert "synthetic-secret-value" not in diagnostic
    assert "[REDACTED secret]" in diagnostic


def test_public_tree_rejects_unsafe_fixture(tmp_path: Path) -> None:
    unsafe = "api" + "_key: " + "synthetic-secret-value"
    (tmp_path / "unsafe.yaml").write_text(unsafe, encoding="utf-8")
    with pytest.raises(PrivacyError, match="Public privacy check failed"):
        assert_public_tree_safe(tmp_path)


def test_contact_allowlist_is_exact(tmp_path: Path) -> None:
    allowlist = tmp_path / "allowlist.yaml"
    public_email = "public" + "@" + "example.test"
    allowlist.write_text(f"allowed_public_contact_values:\n  - {public_email}\n", encoding="utf-8")
    assert load_allowlist(allowlist) == {public_email}
    assert not scan_text(public_email, Path("profile.yaml"), {public_email})


def test_secret_cannot_be_allowlisted(tmp_path: Path) -> None:
    allowlist = tmp_path / "allowlist.yaml"
    unsafe = "api" + "_key=" + "synthetic-secret-value"
    allowlist.write_text(f"allowed_public_contact_values:\n  - '{unsafe}'\n", encoding="utf-8")
    with pytest.raises(PrivacyError, match="cannot permit"):
        load_allowlist(allowlist)



def test_doi_not_mistaken_for_taiwan_phone() -> None:
    sample = "Publication DOI 10.1038/s41598-019-40063-1; second author."
    assert not scan_text(sample, Path("publications.md"))


def test_actual_phone_on_same_line_as_doi_still_detected() -> None:
    sample = "DOI 10.1038/s41598-019-40063-1; contact 0912-345-678"
    findings = scan_text(sample, Path("publications.md"))
    assert any(finding.category == "phone" for finding in findings)
    assert "0912" not in findings[0].diagnostic()


def test_other_sensitive_patterns_not_exempt_inside_doi_line() -> None:
    sample = "DOI 10.1038/s41598-019-40063-1; api_key=synthetic-secret-value"
    findings = scan_text(sample, Path("publications.md"))
    assert any(finding.category == "secret" for finding in findings)
