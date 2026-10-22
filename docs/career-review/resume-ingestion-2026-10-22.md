# Backend and Cloud / Data Platform resume ingestion

Review date: 2026-10-22. Source baseline: `54e597e9a2f4105e6a6fc13940876bd33d3e6726`.

This is a manual editorial and disclosure review of the merged case notes, not independent
verification of employment or outcomes. Every newly ingested employment bullet remains
`user_provided`. A `last_reviewed` date records this review, not employer confirmation.
The `evidence_url` values point to the pinned owner-recollection documents as provenance;
they are not independently reviewed code, logs, personnel records or measurement reports.

## Promotion boundary

The current request authorizes integrating suitable content. This promotion uses generalized
engineering responsibilities and qualitative outcomes already described in the review notes.
It omits customer and internal service names, deployment topology, source code, raw payloads,
operational scale and restricted quantitative results. This editorial decision does not certify
employer approval or waive confidentiality obligations. No such approval evidence was available.
The source notes remain review-only: only the specific wording in canonical YAML is promoted.

## Selected facts and attribution

| Canonical bullet ID | Source case | Attribution / limit | Resume selection |
| --- | --- | --- | --- |
| `ensense-forwarder-refactoring` | EnSense 01 / 10 | Owner led design and built core/generator; teammates contributed modules. Independent processes, not a multi-tenant service. | Both |
| `ensense-django-api` | EnSense 06 | Individual query/export API contributions within a team system. No streaming, pagination/index ownership or throughput claims. | Backend |
| `ensense-time-boundary-fix` | EnSense 02 | Reproduced boundary defect and deployed tested correction. No exactly-once guarantee or measured incident reduction. | Backend |
| `ensense-data-replay` | EnSense 03 | Built replay using shared modules; failures logged for later replay. Delivery and deduplication guarantees unresolved. | Backend |
| `ensense-python-monitoring` | EnSense 04 | Personally designed Python/Cron checks and notification state. No ownership of the team's MQTT web dashboard or automatic remediation. | Cloud / Data Platform |
| `ensense-ec2-delivery` | EnSense 09 | Code review and manual EC2 delivery/recovery checks. No employer CI/CD, zero downtime or automatic rollback claim. | Both |
| `ensense-data-quality` | EnSense 07 | Data cleaning, reconciliation and analytical review. Does not claim sole report-automation authorship. | Cloud / Data Platform |
| `wiwynn-api-batching` | Wiwynn 01 | Maintained existing integration and changed calls to batches. No APIM architecture ownership. | Backend |
| `wiwynn-etl-operations` | Wiwynn 04 | ADF/Databricks development, production investigation, fixes and backfill. No SLA/MTTR or platform-scale claim. | Both |
| `wiwynn-inspection-automation` | Wiwynn 11 | Collaborative cross-tool API inspections. Implementation language, API names and individual task split not established. | Both |
| `wiwynn-kafka-ingestion` | Wiwynn 08 | Python batch consumption and Delta writes. No OOM diagnosis, offset policy, exactly-once or measured throughput claim. | Backend |
| `wiwynn-databricks-migration` | Wiwynn 03 | Team migration; owner rewrote and validated part of the logic and supported cutover. No solo or whole-platform delivery claim. | Cloud / Data Platform |
| `wiwynn-data-validation` | Wiwynn 05 / 10 | SIT/UAT scenarios, source/target checks and upstream BI repairs. No Power BI authoring or autonomous test-framework claim. | Cloud / Data Platform |

Official EnSense title stays Cloud Engineer; functional leadership is expressed through project
ownership, not an invented HR title. WITS remains the single employer record with the existing
Wiwynn assignment dates. Confirmed canonical dates take precedence over stale date TODOs in the
earlier notes. Earlier Sinica/NTU timeline entries are preserved; no new research facts are inferred.

## Quantitative review: NOT VERIFIED for public use

| Claim family | Review result | Decision / evidence needed |
| --- | --- | --- |
| Wiwynn inspection duration | The source arithmetic is correct: `(before - after) / before`; workflow inspection time, not incident recovery. The outcome belongs to the collaborating team. | Hold numbers outside canonical YAML and generated submission resumes. Need timing definition, supporting record and disclosure clearance. |
| EnSense Forwarder LOC | The source bounds imply a line-count reduction above ninety percent, but compare different architectural scopes. This is not a performance/productivity percentage. | Hold LOC and percentage. Need comparable file scope, counting method and disclosure clearance. |
| EnSense monitoring effort / scale | Half-day has no established duration; converting it to hours and a precise percentage would add an assumption. Scope is approximate. | Hold scope, timing and derived percentages pending evidence and clearance. |
| EnSense report effort | Before manual preparation and after output review are different activities; individual automation authorship is unresolved. | Hold efficiency and monthly-savings claims. |
| Wiwynn API, Delta and platform counts | Exact request counts, timing and platform scale remain subject to the source restrictions; team scope is not individual output. | Hold restricted figures; no recovery from memory outside the pinned SSOT. |

Private review candidates can retain source-recalled numbers with explicit qualifications, but are
not canonical inputs, are not evidence of clearance, and must not be committed or sent as resumes.
Missing evidence or clearance must not be treated as passing merely because a PR was merged or a
privacy scanner found no secrets. No new claim was upgraded to `verified`.

## Variant behavior and reproduction

Both configurations explicitly select stable experience IDs; an empty `experience_bullets` map
previously selected no employment at all. The Backend version emphasizes DRF APIs, Node.js modularity,
batch ingestion, defect diagnosis and replay. The Cloud / Data Platform version emphasizes Azure/AWS
operations, monitoring, ETL migration and data validation. Two relevant side projects per variant
support the employment record. Employment appears newest first without duplicating canonical facts.

```bash
uv run career validate
uv run career check-privacy
uv run ruff check .
uv run ruff format --check .
uv run pytest
uv run career build-all --no-pdf
uv run career build --profile backend-engineer --lang zh-TW --format pdf
uv run career build --profile cloud-platform-engineer --lang zh-TW --format pdf
```

Generated resumes remain ignored under `dist/`. No generated resume or private review attachment
belongs in the public Git history. Review the concrete PR before any merge or external publication.
