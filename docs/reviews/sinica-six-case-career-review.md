# Sinica career experience — six-case review draft

Status: DRAFT / user-reviewed conversation notes, not canonical verified facts.
Scope: Academia Sinica, Research Center for Environmental Changes. Do not infer employment dates, exact position, or publication metrics from this draft without separate review.

## Suggested 104 Chinese summary

中央研究院｜研究助理（職稱、任職起訖日期待 canonical evidence review）

負責 Python 資料工程、自動化批次流程、數值模型開發與空間演算法研究，涵蓋 GIS 歷史資料重建、氣象資料處理、森林生物量與水文模擬，以及跨機構研究成果交付。

### 資料工程與自動化
- 以 Python、R、Shell Script、Cron、SCP 建立跨主機資料流程：每日取得中央氣象局 15 天 NetCDF 預報資料，轉換為 ORCHIDEE 模型輸入、執行模擬，再將結果整理成水資源與農業研究團隊所需格式並傳送至合作主機。
- 實作 Log、失敗重試及 Email 通知；使用 NumPy／平行處理改善程式效能，撰寫驗證程式、單元測試與設定檔。
- 主要負責 Python GIS／Raster 批次處理及 1904–2015 年台灣土地覆蓋變遷分析；參與歷史地圖數位化、座標校正、分類標準化，處理數十張歷史地圖與多解析度資料。

### 演算法與科學模型
- 自行設計 Python 土地利用空間配置演算法，使用 3×3 鄰域土地類型權重、歷史轉換機率及政策限制，逐年推估未來約 100 年土地利用分布，支援多種解析度與政策情境。
- 以 Fortran 修改 ORCHIDEE-CAN 颱風／風速／環境干擾相關輸入輸出，使用 Linux／HPC 多核心、多節點進行模擬。
- 整合第四次森林資源調查 3,648 個樣區、30m 樹冠高度資料及 5×5km 網格，進行森林生物量估算與模型驗證。3,648 是觀測樣區數，**不是**模擬網格數。
- 研究性 CNN 衛星影像分類實驗：修改既有 TensorFlow／Keras CNN，使用 Scikit-learn、訓練標籤、超參數與 Confusion Matrix 等驗證裸土／都市分類；**未正式採用或部署**。

### 跨機構交付與國際合作
- 參與中央氣象局、臺灣大學、中原大學 2018–2020 約三年合作；團隊每年完成期中與期末報告（合計六份），個人負責技術圖表、研究方法章節、跨單位資料整合及技術問答。
- 北海道大學：準備教材並向 1–5 名博士生進行一次約 30–60 分鐘線上 GIS／Python 歷史地圖數位化教學。
- 康乃爾大學：參與加州約 2017–2019 年火災事件之森林生物量損失、碳儲存影響模擬；事件名稱與具體數值待查。
- Monash University Malaysia：2020 年與教授研究交流，並獲 Engineering PhD Program **有條件錄取**，未入學；不得寫成已取得 PhD。

### 研究成果
- 2019 Scientific Reports, *Reconstructing Taiwan's land cover changes between 1904 and 2015 from historical maps and satellite images*; DOI 10.1038/s41598-019-40063-1; second author; Google Scholar screenshot shows 89 citations as of 2026-10-15.
- 2022 JGR: Biogeosciences, *Simulation of the Impact of Environmental Disturbances on Forest Biomass in Taiwan*; DOI 10.1029/2021JG006519; second author; Google Scholar screenshot shows 10 citations as of 2026-10-15.
- 2026 Land Use Policy, *From global models to local indicators: Assessing land-use transitions and conflicts*; DOI 10.1016/j.landusepol.2026.107937; third author; Google Scholar screenshot showed no cited-by link on 2026-10-15. Algorithm developed earlier during Sinica tenure; do not claim later manuscript writing.
- At least 99 Google Scholar citations confirmed across first two papers on screenshot date; counts are time-dependent.

## Case inventory and ownership

| Case | Focus | Ownership and boundaries |
| --- | --- | --- |
| 01 | Forest biomass / ORCHIDEE-CAN | Python preprocessing, Fortran I/O modification, HPC simulations and model validation; historical spin-up exact years not confirmed |
| 02 | Historical land cover 1904–2015 | Lead Python automation and change analysis; shared GIS digitization and standardization; CNN was exploratory |
| 03 | Policy-constrained land use algorithm | Personally proposed and implemented main Python algorithm; 3×3 neighborhood, dynamic recalculation, annual maps; 2026 publication postdates team departure |
| 04 | Weather bureau forecast-to-model pipeline | Personally built SCP/Shell/Python/R workflow, postprocessing and inter-institutional transfers; hydrology and agriculture results were team outcomes |
| 05 | International collaboration | Hokkaido teaching, Cornell wildfire modeling, Monash research exchange and conditional PhD offer |
| 06 | Reliability and technical coordination | Cron, logging, retry, email alert, unit/validation tests, data backup, development estimation and technical mentoring; **not** HPC administration |

## Evidence and verification gates

- **User-provided:** Engineering responsibilities, technologies, project collaboration, simulation scale, CNN research status, estimated >=80% processing time reduction in Case 02. The 80% is **not measured/independently verified** and is intentionally excluded from the public resume draft above.
- **Publication citation counts:** User-provided Google Scholar screenshots dated 2026-10-15; recheck before publicizing.
- **PhD:** Official Monash University **Malaysia campus** Engineering PhD conditional admission offer dated 2020-06-04, intended start 2020-08-03; proposed thesis: *The Roles of Terrestrial Water Storages in Shaping the Intensification of Global Hydrologic Cycle*. Offer letter does **not** confirm scholarship. User recalls supervisor's message promising priority nomination for three years' full funding; no verified funding award. Do not publish offer letter, ID, address, birth date, or private communications.
- **Still open:** employment exact dates/title; model validation metrics; Case 02 map counts and precise class schema; fire incident details; automation baseline metrics; funding letter. Keep these out of verified canonical YAML until reviewed.

## Proposed canonical integration (separate follow-up)

After review, map the employment facts into `data/public/experience.yaml`, publication evidence into `data/public/achievements.yaml`, and skills with stable evidence refs. Follow `docs/data-schema.md`; do not place speculative facts into `verified` records. Run ruff, pytest, `career validate`, `career check-privacy`, and review all public claims before merging.
