# Wade Career Profile

以 YAML 為 Single Source of Truth（SSOT）的個人職涯資料與履歷產生器。專案支援繁體中文與英文、五種 job-targeted resume profiles、Markdown／HTML／PDF 輸出、資料一致性檢查、privacy scan 與 CI。

本專案是個人工程工具，不是 SaaS。第一階段刻意不使用 web server、database、Docker、LLM API 或付費服務。

## 架構

```text
data/public YAML ──> Pydantic models ──> cross-file validator
                                      └─> profile selector ──> Jinja templates
                                                               ├─> Markdown
                                                               ├─> HTML
                                                               └─> Playwright PDF
```

- `data/public/`：可公開 canonical facts；`user_provided` 不等同獨立驗證。
- `private/`：本機 TODO 與私有資料，Git 預設忽略。
- `configs/`：只放 stable ID、排序與 section visibility，不複製職涯事實。
- `templates/`：單一 ATS-friendly A4 template。
- `src/career_profile/`：loader、validator、selector、renderer、privacy 與 CLI。
- `examples/sample-profile.yaml`：完全 synthetic 的 CI／操作範例。

詳細設計見 [Architecture](docs/architecture.md) 與 [Data Schema](docs/data-schema.md)。

## 安裝

需求：Python 3.12+ 與 [uv](https://docs.astral.sh/uv/)。

```bash
uv sync --frozen --extra dev
uv run career --help
```

`uv.lock` 是 reproducible install 的依據；更新 dependency 後必須一併提交 lockfile。

## Quick start

```bash
uv run career validate
uv run career list-profiles
uv run career check-privacy

uv run career build --profile backend-engineer --lang en --format markdown
uv run career build --profile data-engineer --lang zh-TW --format html
uv run career build --profile general --lang en --format pdf
uv run career build-all --no-pdf
```

自訂資料或輸出位置：

```bash
uv run career build \
  --profile general \
  --lang zh-TW \
  --format html \
  --data-dir ./data/public \
  --output-dir ./dist
```

輸出命名固定，例如：

```text
dist/backend-engineer/Wade_Huang_Backend_Engineer_EN.pdf
dist/data-engineer/Wade_Huang_Data_Engineer_ZH.html
```

## Supported profiles

- `general`
- `backend-engineer`
- `data-engineer`
- `cloud-platform-engineer`
- `data-analyst`

Variant 只能選擇、排序或隱藏 canonical facts，不能改寫任職紀錄或把未驗證 claim 升級。

## 編輯資料

1. 先在 ignored 的 `private/` 建立本機 TODO，例如 `private/profile.todo.yaml`。
2. 補齊 exact employer、title、dates、education 與 evidence；未知欄位保持 TODO，不猜測。
3. 通過人工 review 後，才把適合公開的 fact 移到 `data/public/`。
4. 保留 stable ID；resume configs 只引用 ID。
5. 執行 `career validate` 與 `career check-privacy`。

繁中與英文文案各自維護，不以盲目翻譯覆蓋另一語言。資料範例及欄位說明見 [Data Schema](docs/data-schema.md)。

## PDF generation

PDF 由本機 Playwright／Chromium 將 HTML 印成 A4，文字可選取、連結可點擊。專案不會在 runtime 下載 font。

Ubuntu：

```bash
sudo apt-get update
sudo apt-get install fonts-noto-cjk
uv run playwright install chromium
```

若缺少 CJK font 或 Chromium，CLI 會回傳 nonzero exit code 與可執行的安裝提示；Markdown／HTML 不受影響。產生 PDF 後應實際檢查 page count、clipping、overlap、link 與 selectable text。超過兩頁時應優先刪減內容，不縮小到難以閱讀。

## Privacy

Repository visibility 不能取代 file-level safety。`private/`、`dist/`、`.env*`、keys 與 temporary files 預設忽略；scanner 的 diagnostics 只顯示 category，不回印命中的 value。

`privacy-allowlist.yaml` 只接受刻意公開 contact value 的 exact match。Secrets、private keys 與 identity numbers 永遠不能 allowlist。提交前流程見 [Privacy](docs/privacy.md)。

## Testing

```bash
uv run ruff check .
uv run ruff format --check .
uv run pytest
uv run career validate
uv run career check-privacy
```

CI 僅執行本機、read-only validation 與 synthetic Markdown／HTML build；不 deploy、不 publish resume、不上傳 private artifacts。

## Roadmap

- 逐筆 review 真實 employment、education、publication 與 quantified impact。
- 以 evidence review 將適當 claim 從 `user_provided` 升級為 `verified`。
- 加入 PDF visual regression／page overflow gate。
- 未來以 read-only export 方式整合 milespapa.com；不讓網站成為第二份資料來源。
