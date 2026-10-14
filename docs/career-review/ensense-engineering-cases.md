# EnSense — engineering experience review (Cases 01–10)

> **Review-only / user_provided / publication approval required.** Owner-recalled facts, not independently verified. This file is **not canonical career YAML**, is not an automatically generated resume, and must not be promoted without checking employer confidentiality, dates/title, evidence and publication suitability. No private logs, customer payloads, code, addresses, credentials or exact deployment infrastructure are included.

## Context and evidence conventions

- Work context: EnSense (廣域科技), IoT environmental-sensor platforms. **Official employment and separation-certificate title: Cloud Engineer (雲端工程師)**, per owner recollection of separation documentation; exact dates and document evidence await canonical review. **Do not label the official position Team Lead, Supervisor or RD Manager.**
- Core platform reported by owner: sensors send measurements to MongoDB / AWS S3; Node.js Forwarders on AWS EC2 read, calibrate and deliver payloads to clients via HTTPS / MQTT. S3 and MongoDB are distinct services, **not one combined database**.
- Role breadth: hands-on Node.js/Python engineering, AWS EC2 operations, data processing and analytical modeling, deployment ownership, and **ongoing sub-team leadership duties while holding the official Cloud Engineer title**. Approximately one month after joining, the RD Manager asked the owner to lead 1–2 other engineers; this continued until departure, not merely a short trial.
- Unless explicitly qualified as confirmed, figures are owner estimates. Keep team scope and individual authorship separate. Projects/customers are generalized here for public review.

## Case inventory

| ID | Topic | Review status |
|---|---|---|
| 01 | Node.js Forwarder refactoring and generator | Core recalled details complete |
| 02 | Hour-boundary duplicate forwarding incident | Root cause and remediation complete |
| 03 | Historical data recovery / replay | Core complete; performance details outstanding |
| 04 | Python monitoring, alerts and EC2 operations | Core complete; MQTT dashboard split and disk follow-up incomplete |
| 05 | Sensor calibration and O3 diurnal model | Core complete; historical metrics unavailable |
| 06 | Django historical-data API and exports | Core complete; quantitative performance unavailable |
| 07 | Data quality and monthly acceptance analytics | Core complete; authorship split to review |
| 08 | Visualization | **Absorbed into 04 / 05 / 07**, not a separate contribution |
| 09 | Git review and production deployment | Core complete; no CI/CD claim |
| 10 | Technical leadership and Forwarder migration | Core complete; management-only metrics unavailable |

### 01 — Configuration-driven Node.js Forwarder refactoring

**User-recalled problem:** Each customer/project originally had a separate Forwarder; inherited code contained >5,000 lines and was difficult to maintain.

**Individual contributions:** Proactively redesigned shared Node.js modules covering MongoDB/S3 data retrieval, calibration, JSON/payload conversion, HTTPS, MQTT, scheduling, and logging/error handling. Built a template directory with one JSON config and a manually invoked `.sh` script that selects/assembles modules to **generate a project-specific independent Node.js Forwarder**; each project keeps a separate runtime process. Core architecture and generator were personally developed; teammates contributed some modules.

**Reported outcomes:** Shared main program **plus all common modules below 500 lines** versus inherited >5,000 lines (owner-reported approximate code-size comparison, >90% fewer lines; not a productivity percentage). New project generation takes minutes after configuration. Existing project Forwarders were migrated incrementally to the new design. A shared-module fix requires regeneration/redeployment of affected artifacts.

**Evidence limits:** No source code/LOC report independently reviewed; "minutes" is qualitative; never claim single multi-tenant process, auto CI/CD generation or universal 90% performance improvement.

### 02 — Duplicate data at hour boundary

**Incident:** Only the reading at the exact hour was forwarded twice.

**Diagnosis:** Reproduced in test, compared MongoDB/S3 originals, Forwarder logs, payloads and timestamps; isolated overlapping inclusive time-range end condition. **Remediation:** left-closed/right-open interval `[startTime,endTime)` with end-exclusive comparison. Tested consecutive ranges, the hour-boundary reading, record counts and timestamps; deployed production fix. Owner reports no recurrence afterwards.

**Evidence limits:** Illustrative interval representation, not exact historical source code; impacted customer count and duplicate-volume unknown.

### 03 — Data recovery / replay

**Individual contributions:** Built a replay tool from the same project configuration, calibration and transmission modules as the normal Forwarder, replacing the input retrieval function for recovery. Separate HTTPS and MQTT delivery-status logs; failed events used to query MongoDB/S3 again. Supports user-selected time windows, complete-window or missing-only replay, splitting by record count and time window, and parallel replay via **multiple processes**. Further failures are logged for subsequent replay. When downstream systems could not handle large catch-up deliveries, added packaged CSV output as alternate handoff.

**Evidence limits:** Record ID/timestamp was used to identify duplicates but exact deduplication location is forgotten. "Non-200" does not prove non-delivery, nor prove exactly-once delivery. No throughput, concurrency cap, API rate-limit or elapsed-time improvement verified.

### 04 — Monitoring, alerting and production operations

**Individual contributions:** Designed Python monitoring scripts running on AWS EC2 Cron and combined scheduled checks with human inspection. Resource checks: CPU and memory every 10 minutes; disk daily. Sensor data completeness checked hourly, using cumulative records received since start of day divided by expected `60 × elapsed hours` for one-minute readings; reset daily, summarized by project. Results and notification state retained using daily Google Sheets. Sheet indicators: green >=90%, yellow >=80% and <90%, red <80%. LINE notification when completeness <80%; email list of disconnected devices checked hourly using latest-timestamp timeout and one notification per device per day, reset by a new daily Sheet.

**Related team component:** Forwarder also published monitoring data to an internal real-time MQTT dashboard. Dashboard was developed collaboratively; the profile owner's exact UI/frontend versus integration ownership remains unresolved. Keep separate from owner's Python / Google Sheets analytical dashboard.

**Operational incident:** Production disk filled and logging failed after a periodic human log-archive/transfer maintenance task was missed. Owner cleared stale logs/unneeded files; further multiple improvements recalled but not itemized. Do not claim automated log rotation or automatic remediation.

**Reported scale / impact:** Approximately 40 projects, >1,000 devices. Daily manual inspection fell from ~half-day (~4h assumed) to ~30 min; estimated ~87.5% time reduction **conditional on four-hour definition of half-day**. Earlier alert detection, retained history, fewer repeated emails and fewer customer-first reports are reported, not independently measured.

### 05 — Sensor calibration research and O3 diurnal model

**Scope:** Participated in calibration for PM2.5/PM10, CO/CO2, VOC/TVOC, NH3, temperature/humidity and other gases. Used Python (Pandas, NumPy, SciPy, scikit-learn, Matplotlib/Seaborn), linear/polynomial fitting, moving average, environmental compensation and outlier controls according to sensor/project needs; Node.js calibration integration and JSON configuration.

**O3 representative case:** Studied ambient ozone diurnal behavior. Retrieved sunrise/sunset or daylight-cycle information from a government environmental data source, aligned cycles across dates, included raw O3 readings, hour/time and temperature/humidity and diurnal features in a polynomial regression. Used scikit-learn `PolynomialFeatures` with **degree 4 or greater** (exact degree/features unknown) and government station O3 as target reference. Validated across dates, seasons and devices, comparing Bias and diurnal curves; owner reports lower Bias and trends closer to the station. Recomputed coefficients through Python scripts, submitted for colleague/manager review and integrated the reviewed model into production Node.js Forwarders.

**Evidence limits:** Exact R²/Bias before and after cannot be recovered; no asserted numeric improvement or regulation-grade accuracy. R² is a used evaluation measure but no documented numerical O3 delta. Do not conflate ambient photochemistry with direct sunlight damage to the sensor or assume exact polynomial formula.

### 06 — Django REST API, historical queries and export

**Context:** Collaborated on an environmental monitoring data center serving a limited set of government/customer users (customer name intentionally omitted pending disclosure review). Deployed Python Django REST Framework behind uWSGI and Nginx on AWS EC2. Developed historical queries by device ID and start/end timestamp, with MongoDB read queries and AWS S3 historical/export storage; built CSV/Excel downloads **in Python memory** with timestamp/device/measurement columns, date/time-zone conversion and export field formatting. Used DRF Authentication/Permission API-key/token mechanisms, Views/ViewSets, status/error handling and API documentation.

**Verification:** Postman manual tests, invalid device IDs/time ranges/tokens, MongoDB result reconciliation, export correctness and large historic downloads. Team-developed system; individual contributed both query and export APIs.

**Evidence limits:** Query limits, pagination and indexes were described collectively but not individually confirmed; no endpoint count, exact query performance, streaming, async export or sole authentication architecture ownership claim.

### 07 — Data quality and monthly customer acceptance reports

**Individual activities:** Designed outlier cleaning (IQR/Z-score, moving average/adjacent-value changes, physically plausible ranges), normalized UTC/Taiwan timezone, timestamp format, gas units (ppm/ppb) and device fields. Used Python/Pandas/NumPy, MongoDB aggregation, Node.js transformation, shell automation and Google Sheets as applicable. For monthly customer acceptance, aligned sensors and national-station readings at hourly average granularity; generated R², Bias, hourly/daily summaries and time-series graphics with Python/Jupyter, using contract/customer acceptance thresholds. Main personal review role was checking analytical results and diagnosing mismatched periods, missing intervals, outliers, formula issues, then checking corrected calibration parameters; do **not** claim sole drafting/delivery of all final reports.

**Reported impact:** >20 projects per month; per-project report preparation formerly 60–90 minutes manually, afterwards approximately 15 minutes to review generated output: **75%–83.3% less processing time**, or 4–6× comparison of processing duration. Data processing jobs typically hundreds to thousands of readings. At a hypothetical 20 projects/month this implies 15–25 hours saved, **not an observed monthly total**.

**Evidence limits:** Automated report creation was described; exact division of script authorship versus team review still requires confirmation. Do not count this efficiency gain again under monitoring Case 04.

### 08 — Visualization (absorbed; no standalone claim)

Google Sheets completeness chart/colors belong to 04; O3 trend comparisons to 05; R²/Bias/time-series charts and monthly reporting to 07. MQTT dashboard was team developed, personal responsibilities unresolved. No substantiated independent web dashboard, Plotly, Grafana, Tableau or Power BI creation case at EnSense.

### 09 — SDLC, Git review and production releases

**Individual responsibilities:** Git code review, merges and conflict resolution; reviewed readability, calibration/data logic, configuration, deployment settings, logging and error handling. Built **separate Shell deployment scripts** (distinct from the generator's `.sh`), manually used SSH, Git pull and systemd to update/restart Node.js Forwarders on EC2. Validated process, logs, MongoDB/S3 inputs, calibrated payloads, HTTPS responses, MQTT Subscriber output and sustained forwarding. Rollback by Git checkout/reset or previous config regeneration, followed by manual recovery verification. Real deployment issues included bad config and anomalous readings after new calibration logic.

**Evidence limits:** Deployments are on-demand and predominantly manual, **not a complete CI/CD pipeline**; no automatic rollback, zero-downtime claims, verified MTTR or deployment efficiency metrics.

### 10 — Cloud Engineer with ongoing sub-team technical leadership

**Official title versus duties:** The personnel/separation-certificate title remained **Cloud Engineer** throughout employment; no formal promotion or title change is evidenced. Approximately one month after hire, the RD Manager assigned the owner to lead a sub-team of **1–2 other engineers**, continuously until departure. These are sustained **functional team-lead responsibilities**, not proof of an official Team Lead/Supervisor job title.

**Organization and reporting:** The RD Manager led the RD department. Within the cloud engineering function, the owner led one sub-team and **reported directly to the RD Manager**. A separate, parallel AWS S3-focused sub-team of approximately **three people** had another lead who also reported directly to the same manager. The owner was **not the only team lead** and did **not** manage the other S3 sub-team or the entire RD organization. “Forwarder/data sub-team” is a functional description, not a verified formal team name.

**Actual leadership duties:** Assigned work and priorities, guided engineers, reviewed/merged code, made architecture and technology choices within the owner's scope, decided production release timing, estimated delivery schedules, coordinated other functions and assisted with **annual performance appraisals** (not claimed as sole final evaluator). Work tracking via GitLab Issues, Notion, Excel/Sheets. PM or management typically owned primary client contact; owner provided technical support.

**Representative project:** Proactively proposed and led Forwarder redesign end-to-end: audited inherited code, set modular/config/generator architecture, wrote core modules, delegated other modules/tests, reviewed code, established acceptance checks, coordinated existing-service support and staged deployments, and ultimately migrated all existing Forwarder projects. Worked with teammates on legacy code understanding, coached via reviews, prepared JSON examples, retained rollback procedures, established ongoing review/merge and change-testing norms, and assigned shared-module maintainers.

**Evidence limits:** Exact number of migrated Forwarders unknown; do not equate with ~40 monitored projects. Case 01 LOC reduction is a **single engineering outcome**, not an additional management KPI. No separate team productivity or on-time delivery rate measured. Sub-team leadership was persistent **without an HR title change**; the second S3 sub-team and RD Manager are organizational context, **not** the owner's direct reports. Exact start/end of delegated lead duties is approximate.

## Reported numeric evidence ledger

| Metric | Reported value | Attribution / qualification |
|---|---|---|
| Inherited vs shared Forwarder LOC | >5,000 vs <500 | 01, owner recall, different architecture scope; >90% line-count change only |
| Generate new Forwarder | Minutes after config | 01, qualitative approximation |
| Monitoring scope | ~40 projects / >1,000 sensors | 04, approximate scope |
| Daily manual checks | Half day -> 30 min | 04, 87.5% estimated only if half-day = 4 hours |
| Monthly acceptance volume | >20 projects | 07, approximate |
| Per-project report effort | 60–90 -> 15 min | 07, 75–83.3% range; review time vs former manual creation |
| Sub-team direct reports | 1–2 other engineers | 10, delegated ongoing lead responsibilities; official title remains Cloud Engineer |
| O3 improvement | Bias lower, cycle shape closer to reference | 05, numerical values unavailable |
| Duplicate forwarding defect | Fixed, no later recurrence recalled | 02, no affected volume |
| Migration | All existing Forwarder projects progressively migrated | 10, exact count unknown |

## Required publication/evidence review before canonical ingestion

1. Verify Cloud Engineer title against separation certificate and employment dates against HR material; do not promote delegated lead duties into an official Team Lead title.
2. Review whether client or project names, scale, equipment architecture, source details and metrics are employer-confidential even if paraphrased.
3. Verify code size comparison, monitoring scale/time baseline and report before/after time definitions before public quantified claims.
4. Recover, where possible, O3 Bias/R² measurements; otherwise use qualitative wording only.
5. Confirm replay duplicate handling, MQTT dashboard ownership, post-disk-incident controls, API query optimizations and Jupyter automation authorship before attaching specific claims.
6. Keep `user_provided` distinct from independently verified facts. Do not invent metrics/years. Only after explicit approval, map safe facts to bilingual canonical YAML and run `career validate`, `career check-privacy`, tests and output review.

**Status:** Review document only. No `data/public/*`, profile variants, generated resumes or deployment assets modified.
