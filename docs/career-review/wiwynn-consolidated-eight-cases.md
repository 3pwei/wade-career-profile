# Wiwynn assignment — consolidated engineering experience (10 cases)

> **Draft / user_provided / publication review required.** This is a non-canonical, public-safe review document for future Career Profile ingestion. Do not automatically include it in resume generation. Detailed employer-internal metrics, client feedback, customer communications, personal HR history, source code and infrastructure specifics must remain outside this public repository pending confidentiality review.

## Employment presentation (pending personnel document review)

- Formal employer: WITS (employer formerly referred to as 緯創軟體; the profile owner reports a 2026-06 rename to 緯致科技). **Legal entity and rename details await documentation.**
- Formal position: 高級軟體工程師 / Senior Software Engineer.
- Assignment: Wiwynn (緯穎科技), Cloud Data Engineer / 雲端資料工程師.
- Arrangement: dispatched/on-site assignment; **one employment, not two concurrent jobs**.
- Start date: TBD. Public-facing employment end date and any absences are **not included in this review note**.
- Exact dates, employer legal naming, evidence, and disclosure approval remain pending before canonical `data/public/experience.yaml` update.

## Responsibilities and cases

### 01 — API integration and batching (Cerberus)

**Confirmed recalled work:** Maintained existing Azure Logic Apps workflows; modified SQL queries/writes and calls to multiple read/write APIs in an Azure API Management environment. Used Recurrence, Condition, For each, Parse JSON, SQL Connector, Run History and SQL debugging. Improved from individual record calls to batches with a limit of 1,000 records.

**Candidate 104 wording:** 使用 Azure Logic Apps、Azure API Management（APIM）與 SQL Script 維護跨系統資料同步工作流程，透過 Condition、For each、Parse JSON、SQL Connector 處理排程、資料讀寫與故障排查；將逐筆 API 呼叫改善為批次處理，減少大量資料同步的請求負擔。

**Evidence boundary:** Exact before/after request counts, customer-facing internal service names, and release details require confidentiality review before publication. Did not claim designing the APIM gateway or retry policy.

### 02 — PySpark / Delta Lake processing performance

**Confirmed recalled work:** Azure Databricks / PySpark; obtained the most recent Delta Table version and pinned the source snapshot with Delta Time Travel / `versionAsOf` or `timestampAsOf`. Addressed a slow processing/write workflow.

**Candidate 104 wording:** 使用 Azure Databricks、PySpark 與 Delta Lake Time Travel 固定來源資料版本（Snapshot），改善 Delta Table 資料處理與寫入流程的執行穩定性及耗時。

**Evidence boundary:** Source snapshot strategy is confirmed; exact elapsed-time comparisons remain owner-recalled and require publication review. Do not infer Delta writer throughput increase or make unverified causal claims.

### 03 — Azure Synapse to Databricks migration

**Confirmed recalled work:** Worked as one member of the team migrating existing ETL pipelines, including some Stored Procedure / T-SQL logic to Spark SQL, PySpark and Databricks notebooks. Performed row-count, business-key/SEQN, aggregations, SQL logic, watermark/incremental and ADF/Notebook log validation. Participated in production cutover, retirement of previous processing flows and post-cutover support.

**Candidate 104 wording:** 參與 Azure Synapse 既有 ETL／Stored Procedure 流程移轉至 Azure Databricks，負責部分 Spark SQL／PySpark 程式改寫、資料比對及增量邏輯驗證，並參與 Production Cutover 與上線後異常排查。

**Evidence boundary:** The platform-wide pipeline count is team scope, **not individual output**. Do not equate total ETL pipelines with distinct Stored Procedures or claim solo migration ownership.

### 04 — CDP platform production ETL operations

**Confirmed recalled work:** Developed/modified Azure Data Factory pipelines, activities, datasets, triggers, dependencies and Databricks notebook parameter passing. Used ADF Monitor, job logs, alerts and SQL/PySpark fixes for production incidents. Checked upstream availability, reran tasks, performed selective backfill by date or SEQN, validated STG/ODS/TGT and downstream data, and coordinated cross-team recovery.

**Candidate 104 wording:** 使用 Azure Data Factory（ADF）、Azure Databricks、Python／PySpark 與 SQL 開發及維護企業 CDP ETL，執行排程管理、Production Monitoring、Incident Troubleshooting、Pipeline Rerun、Backfill 及來源到目標資料驗證。

**Evidence boundary:** Platform-wide record volume and pipeline counts were owner estimates; no verified MTTR, SLA or individual pipeline count. No public numeric operational claim without clearance.

### 05 — Data quality, SIT and UAT

**Confirmed recalled work:** Designed test scenarios and selected representative data using SQL; reconciled source and target row counts, keys and fields; built parameterized SQL/Python/PySpark assisted checks for tables, device identifiers and date ranges; integrated validation into ADF/Databricks workflows; human-reviewed results. Participated in SIT/UAT and reported successful acceptance.

**Candidate 104 wording:** 設計資料整合 SIT／UAT Test Case 與 Test Scenario，透過 SQL、Python／PySpark 進行參數化的資料完整性與一致性檢查，整合至 ADF／Databricks Pipeline，並配合人工審查、異常修正及驗收。

**Evidence boundary:** Do not claim fully autonomous test framework, 100% coverage or universal CI/CD quality gates. Detailed internal sample/combinations count requires clearance.

### 06 — Shared Databricks logging OOP PoC

**Confirmed recalled work:** Prototyped refactoring existing Python logging functions into a class, encapsulating logger initialization/configuration and offering a candidate shared library for different notebooks. Demonstrated the proof of concept to supervisor, receiving positive feedback.

**Candidate 104 wording:** 主動以 Python OOP 將既有 Databricks Logging Functions 重構為 Class Methods，封裝 Logger 初始化及設定，製作共用 Logging Library PoC，評估程式碼重用與維護性改善。

**Evidence boundary:** **PoC only, not deployed to production.** Existing log functionality was not newly invented; no measured productivity improvement.

### 07 — QMS delivery and technical coordination

**Confirmed recalled work:** Weekly meetings with the lead PM; clarified client requirements and business rules; proposed schedules/work arrangements for PM or supervisor approval; tracked development; explained ETL/SQL approaches to PM; executed functional and data validation; supported handover. Team achievement and customer appreciation were recalled by the owner but are not reproduced here.

**Candidate 104 wording:** 擔任企業品質管理資料整合專案技術協作窗口，每週與主要 PM 釐清需求與交付內容，提出開發時程並協調確認、追蹤進度、說明 SQL／ETL 處理邏輯，執行功能與資料驗證，協助跨團隊交付。

**Evidence boundary:** No sole PM/personnel management claim; no internal monthly rating, client email content, workload-share figure or leave/exit reason on this public branch.

### 08 — Python Kafka Consumer batch ingestion

**Confirmed recalled work:** Python Kafka consumer under large message volume had memory/execution-resource pressure and processing stalls; changed the workflow to batch-consume **up to 1,000 messages**, and batch-write them to Delta Tables.

**Candidate 104 wording:** 使用 Python 優化 Kafka Consumer 的大量訊息處理流程，針對記憶體與執行資源壓力改採每批最多 1,000 筆的 Batch Consumption，並批次寫入 Delta Table，改善資料匯入流程的卡頓問題。

**Evidence boundary:** Actual client library and offset/commit method unknown; no OOM confirmation, exact-once guarantee, or independently measured throughput improvement.

### 09 — Elasticsearch maintenance (implementation details pending)

**User-confirmed scope:** Participated in maintenance of existing Elasticsearch Index / Mapping in the Wiwynn work context. The precise production changes, symptoms, failure cause, fix, deployment and outcome are **not remembered** and cannot currently be substantiated.

**Separate historical learning/test records (not attributed to the production maintenance case):** In 2024-12, explored Python Elasticsearch Client `es.index()` and `es.search()` using synthetic documents; Query DSL `match_all` / `match` examples were discussed. Index, Mapping, Shard and Replica concepts were discussed in 2025-01. These do not prove use of specific APIs, reindexing, or other features in the actual maintenance incident.

**Conservative candidate 104 wording:** **Elasticsearch / Index & Mapping Maintenance：** 參與企業資料平台既有 Elasticsearch Index 與 Mapping 維護，具備相關資料索引及查詢概念；另曾使用 Python Elasticsearch Client 測試文件寫入與查詢功能。

**Keywords:** Elasticsearch, Index, Mapping, Python, Elasticsearch Python Client. Additional keywords such as Reindex, Mapping Migration, Index Tuning, Kibana, Query DSL in production or Databricks–Elasticsearch production integration must not be attached to the maintenance claim without evidence.

**Evidence boundary:** Claim status `user_provided`; technical specifics `unverified`. No independently reviewed incident logs, code diff, affected fields or measured outcomes. Do not state that the profile owner changed field types, rebuilt indexes, resolved a particular production defect, or improved search speed. A separate Kibana certificate discussion is not evidence of an Elasticsearch fix.

### 10 — Power BI reporting integration and production data troubleshooting

**User-confirmed responsibilities:** Assisted with Power BI report data connections; supported reports that presented processed or calculated results stored in Azure Databricks Delta Tables. During rotating operational duty, checked that reports displayed correctly. The types of incidents handled included **incorrect report figures, missing records and data that had not updated**.

**Troubleshooting scope:** These incidents are consistent with upstream data freshness, missing or inconsistent data, or report-facing data issues, but the actual root cause and corrective action of any specific incident have **not yet been recalled**. Do not state that a refresh job, DAX expression, source connector, SQL query, Delta transformation or report measure was fixed unless individually confirmed.

**Historical technical context:** Previous career discussions named Power BI as a downstream consumer of Databricks / Delta data. Other discussions of ReportingDB, Fabric SQL Endpoint and Direct Lake were technical exploration, not proof of those connection modes in production.

**Candidate 104 wording (zh-TW):** **Power BI / BI Data Integration & Troubleshooting：** 協助企業 Power BI 報表資料串接，將 Azure Databricks／Delta Table 計算結果提供 BI 報表呈現；參與例行值班檢查報表資料是否正常更新，並針對報表數值異常、資料缺漏與未更新等問題進行調查，協助維持下游資料呈現品質。

**Candidate English wording:** **Power BI / BI Data Integration & Troubleshooting:** Supported enterprise Power BI data connections and reporting of calculated results from Azure Databricks Delta Tables. Performed routine report checks and investigated incorrect figures, missing data and stale report data.

**Keywords:** Power BI, Azure Databricks, Delta Lake, Delta Table, SQL, BI Integration, Data Reporting, Data Validation, Data Freshness, Troubleshooting, Production Monitoring.

**Evidence boundary:** User-provided scope, without a verified incident-specific root cause or fix. No claim of DAX, Power Query, Semantic Model, Refresh API, DirectQuery/Direct Lake, RLS, dashboard design ownership or measurable defect reduction.

## Enterprise SDLC responsibilities (cross-cutting)

- **SA:** Projects requiring fresh system analysis were less common because much work involved existing systems; **led SA and requirements/business-rule analysis when needed**. Infrequency is not lack of ownership.
- **SD:** System design documents, data flow and mapping design.
- **DEV:** SQL, Python/PySpark, ADF and Databricks.
- **UT:** Unit testing and logic verification.
- **SIT:** Integration test design and execution.
- **UAT:** Acceptance support, bug fixes and re-validation.
- **QAS:** Test-environment deployment and quality validation (confirm exact internal acronym).
- **MTP:** Production rollout, post-deployment checks and handover.

**Candidate 104 SDLC wording:** 參與企業資料工程專案 SA、SD、DEV、UT、SIT、UAT、QAS、MTP 全流程；在需要 SA 的專案主導需求分析，並負責系統設計、SQL／Python／PySpark／ADF／Databricks 開發、測試驗證、正式部署與交接。

## Proposed prioritization

For Data Engineer roles: QMS coordination, CDP production operations, Delta performance, migration, Kafka, API batching, data quality, Elasticsearch maintenance (scope under review), OOP PoC (short note). For Backend positions, emphasize API batching, Python Kafka, Python OOP PoC with its limitation and production troubleshooting; do not misrepresent data engineering as extensive enterprise backend service ownership.

## Follow-up review checklist

1. Review employer's legal name, date changes and official title from HR documentation.
2. Confirm suitable publication of project/product identifiers and all quantitative results before promotion to public resume files.
3. Verify each impact number's measurement context, team versus individual attribution, and exact units.
4. Confirm which technologies belonged to each case; avoid transferring techniques between unrelated engagements.
5. Convert cleared facts into canonical bilingual YAML using the existing data schema; keep raw employer-private evidence outside Git.
6. Run `career validate`, `career check-privacy`, relevant tests, and review generated 104/PDF output before any merge.
