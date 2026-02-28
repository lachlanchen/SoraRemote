[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)



# SoraRemote

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20WSL-6c757d)
![Server](https://img.shields.io/badge/Server-Tornado%20API-0EA5E9)
![Frontend](https://img.shields.io/badge/Frontend-PWA-10B981)
![Status](https://img.shields.io/badge/Status-Experimental-F59E0B)

SoraRemote 是一個輕量級的 Python + Selenium 工具組，用於自動化 Sora 網頁 UI。

它支援三種互補的工作流程：
1. CLI 自動化代理（`agents/sora_agent.py`）：用於輸入提示詞與執行 UI 控制動作。
2. CLI 下載器（`agents/sora_download.py`）：用於探索與下載媒體候選內容。
3. 本機 Tornado 控制伺服器 + PWA（`server/app.py` + `pwa/`）：用於 API 驅動與瀏覽器端控制。

目前 README 內容保留為標準操作指引，並已為了清晰度重新整理。

## ✨ 概覽

核心設計：
- 透過 DevTools 遠端除錯連接到持久化 Chrome 工作階段（預設連接埠 `9333`）。
- 重用瀏覽器設定檔狀態，維持登入/工作階段連續性。
- 自動化主要編輯器操作（輸入、plus/媒體附加、storyboard、settings、create）。
- 透過 REST + WebSocket 日誌對外暴露相同操作，供本機 PWA 控制器使用。

### 工作流程快照

| 工作流程 | 入口點 | 主要用途 |
| --- | --- | --- |
| CLI 代理 | `agents/sora_agent.py` | 輸入提示詞、點擊控制項、自動化 compose 流程 |
| CLI 下載器 | `agents/sora_download.py` | 探索可下載媒體並儲存到本機 |
| API + PWA | `server/app.py` + `pwa/` | 從瀏覽器進行遠端控制與視覺化編排 |

## ✅ 功能

- Chrome 連接/啟動流程與可重用設定檔（`--debugger-port`、`--start-chrome`、`--user-data-dir`）。
- 針對關鍵控制項的安全點擊或強制點擊（`plus`、`storyboard`、`settings`、`create`、`profile`）。
- 提示詞輸入，具備 selector 後備行為。
- 透過檔案路徑與 DataTransfer 注入進行媒體附加。
- Storyboard 場景填入 + script 更新 + storyboard 專用媒體附加。
- 設定自動化（model/orientation/duration/resolution）。
- 使用瀏覽器 cookies 的獨立下載探索 + 取得流程。
- Tornado REST API 與即時 WebSocket 偵錯串流。
- 可安裝的本機 PWA，提供上傳、預覽與細緻控制。

## 🗂️ 專案結構

```text
SoraRemote/
├─ README.md
├─ requirements.txt
├─ .github/
│  └─ FUNDING.yml
├─ agents/
│  ├─ sora_agent.py
│  └─ sora_download.py
├─ server/
│  └─ app.py
├─ pwa/
│  ├─ index.html
│  ├─ app.js
│  ├─ styles.css
│  ├─ manifest.webmanifest
│  └─ sw.js
├─ bin/
│  ├─ sora_type.sh
│  └─ sora_download.sh
├─ i18n/
│  └─ (currently empty)
├─ uploads/
│  └─ .gitkeep
└─ selenium_template -> ../auto-publish/ (symlink)
```

## 🧩 先決條件

- Python 3.10+（建議）。
- 已安裝且可執行的 Chrome/Chromium。
- 在需要登入或互動式 UI 時，非無頭模式（`--no-headless`）所需的顯示環境。
- 已附加 Chrome 設定檔中的 Sora 帳號存取權限。

## 📦 安裝

沿用標準 README 的既有安裝流程：

```bash
conda activate agent
pip install -r requirements.txt
```

`requirements.txt` 中的相依套件：

| 套件 | 版本規格 |
| --- | --- |
| `selenium` | `>=4.17.2` |
| `tornado` | `>=6.4` |
| `Pillow` | `>=9.4.0` |
| `pillow-heif` | `>=0.16.0` |

## 🚀 使用方式

### 快速開始（CLI 代理）

快速開始（在受管理的瀏覽器中開啟 Sora）：

```bash
python agents/sora_agent.py
```

使用持久化工作階段連接 Chrome（Sora 建議）：

```bash
python -m agents.sora_agent --debugger-port 9333 --start-chrome --no-headless --login-timeout 600 --text "A sunset over Tokyo, cinematic."
```

說明：
- 會開啟 Chrome 視窗並進入 Sora 頁面。若被導向登入，完成登入後腳本會等待並輸入你的提示詞。
- 若要重用同一登入狀態，請傳入固定的設定檔路徑：

```bash
python -m agents.sora_agent --debugger-port 9333 --start-chrome --no-headless --user-data-dir "$HOME/chrome_sora_profile_9333"
```

### 主要 CLI 選項（`agents/sora_agent.py`）

- `--url` 目標頁面（預設：`https://sora.chatgpt.com/explore`）。
- `--debugger-port` 連接到已使用 `--remote-debugging-port=PORT` 啟動的 Chrome。
- `--start-chrome` 若與 `--debugger-port` 一起設定，會自動幫你啟動 Chrome（使用 `--user-data-dir`）。
- `--no-headless` 以可見瀏覽器執行；登入與 Cloudflare 流程需要。
- `--selector` 用於定位輸入框的 CSS（預設匹配 Sora composer textarea）。
- `--text` 要輸入到輸入框的內容。
- `--chrome-binary` 明確指定 Chrome/Chromium 路徑。
- `--action` UI 動作：`list`、`plus`、`storyboard`、`settings`、`create`、`profile`。
- `--force-click` 即使元素顯示為停用也強制點擊。
- `--login-timeout` 等待手動驗證完成的時間視窗。

Driver 處理：
- 代理在啟動前會先移除 `PATH` 中可能過時的 `chromedriver`。
- 接著由 Selenium Manager 自動解析與已安裝 Chrome 相符的 driver。

### CLI 範例（UI 控制）

列出並點擊常用控制項：

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action list --action storyboard --action settings --action plus
```

強制點擊 Create video 按鈕（即使停用）：

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action create --force-click
```

開啟個人檔案/設定並在需要時手動導覽：

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action list --action profile
```

若未偵測到 `profile`，通常 `settings` 按鈕會開啟相同選單。

### 下載流程

使用處理腳本探索並下載影片：

- Dry-run（僅列出候選項）：`./bin/sora_download.sh --dry-run`
- 最多下載 2 個檔案到 `./downloads/sora`：`./bin/sora_download.sh --max 2`
- 變更輸出資料夾：`OUT_DIR=$HOME/Videos/sora ./bin/sora_download.sh --max 1`

也可直接以模組方式使用：`python -m agents.sora_download ...`。

## 🌐 控制伺服器 + PWA

執行 Tornado 伺服器：

```bash
python server/app.py
# 監聽 http://0.0.0.0:8791 並在 / 提供 PWA
```

伺服器預設行為：
- 重用遠端除錯連接埠 `9333` 上的 Chrome。
- 上傳檔案儲存在 `./uploads`，除非設定 `SORA_UPLOADS_DIR`。

### 主要端點

所有端點都針對目前附加的 Chrome 運作（預設為除錯連接埠 `9333`）。

| Method | Path | Payload | 說明 |
| --- | --- | --- | --- |
| `GET` | `/api/status` | none | 回傳 DevTools 就緒狀態與目前連接埠。 |
| `POST` | `/api/open` | `{ url? }` | 將附加的 Chrome 分頁導向指定 URL（預設為 Sora Explore）。 |
| `GET` | `/api/actions` | none | 檢查按鈕/控制項狀態（found/displayed/disabled 中繼資料）。 |
| `POST` | `/api/click` | `{ key, force? }` | 點擊單一控制項，其中 `key ∈ {plus, storyboard, settings, create, profile}`。 |
| `POST` | `/api/type` | `{ text, selector?, url? }` | 將提示詞輸入至 composer selector。 |
| `POST` | `/api/compose` | `{ text, click_create? }` | 開啟 compose 頁、輸入文字，並可選擇點擊 create。 |
| `POST` | `/api/attach` | `{ path, click_plus? }` | 透過 DataTransfer 注入上傳媒體；會自動清除既有媒體（`click_plus` 預設為 `false`）。 |
| `POST` | `/api/describe` | `{ text }` | 填入「Optionally describe your video...」文字區。 |
| `POST` | `/api/script-updates` | `{ text }` | 填入「Describe updates to your script...」欄位。 |
| `POST` | `/api/storyboard` | `{ scenes: ["scene 1", ...], script_updates?: "...", media_path?: "..." }` | 開啟 storyboard、填入場景文字區，並可選擇套用 script 更新與 storyboard 媒體。 |
| `POST` | `/api/storyboard-media` | `{ path }` | 當 storyboard 已顯示時，附加媒體到 storyboard 專用上傳器。 |
| `POST` | `/api/storyboard-attach-only` | `{ path }` | 確保 storyboard 已開啟，接著附加媒體。 |
| `POST` | `/api/settings` | `{ model?, orientation?, duration?, resolution? }` | 開啟設定並套用選定值；回應會回傳已套用標籤。 |
| `POST` | `/api/upload` | multipart form data | 將本機檔案儲存到伺服器上傳目錄，並回傳伺服器端路徑。 |
| `POST` | `/api/preview` | multipart form data | 將圖片轉為 PNG 預覽（對 UI 中 HEIC/HEIF/AVIF 後備很有用）。 |
| `GET` | `/ws` | WebSocket | 串流動作/偵錯事件。 |

### PWA 控制項

啟動 `server/app.py` 後，開啟 `http://0.0.0.0:8791`（或你指定的 host）。

現有實作重點：
- 可透過檔案選擇器上傳媒體，或貼上路徑後點擊 **Plus** 進行附加，避免重新開啟系統檔案對話框。
- 可在專用「Media description」欄位套用媒體描述。
- 提供獨立控制：**Set Model**、**Set Orientation**、**Set Duration**、**Set Resolution**，以及 script 更新。
- Storyboard 控制包含場景、script 更新、開啟 storyboard 面板，以及附加目前 storyboard 路徑。
- 即時偵錯日誌會顯示 API 呼叫與 Sora 回傳值（例如所選 model/duration）。

## ⚙️ 設定

### 環境變數

`server/app.py` 會讀取：
- `SORA_DEBUGGER_PORT`（預設 `9333`）
- `SORA_USER_DATA_DIR`（預設 `~/chrome_sora_profile_<port>`）
- `SORA_DISPLAY`（可選 X display）
- `SORA_API_PORT`（預設 `8791`）
- `SORA_URL`（預設 `https://sora.chatgpt.com/explore`）
- `SORA_UPLOADS_DIR`（可選；覆寫上傳目錄）

`agents/sora_agent.py` 也支援：
- `CHROME_BINARY`（若未提供 `--chrome-binary`）

包裝腳本支援：
- `PORT`、`SORA_PROFILE_DIR`、`TIMEOUT`、`LOGIN_TIMEOUT`（`bin/sora_type.sh`）
- `PORT`、`SORA_PROFILE_DIR`、`OUT_DIR`（`bin/sora_download.sh`）

## 🧪 範例

### 端到端 API 範例（curl）

```bash
# 1) Open Sora
curl -s -X POST http://127.0.0.1:8791/api/open -H 'Content-Type: application/json' -d '{}'

# 2) Type prompt
curl -s -X POST http://127.0.0.1:8791/api/type -H 'Content-Type: application/json' -d '{"text":"A cinematic drone shot over snowy mountains."}'

# 3) Set model and duration
curl -s -X POST http://127.0.0.1:8791/api/settings -H 'Content-Type: application/json' -d '{"model":"sora 2 pro"}'
curl -s -X POST http://127.0.0.1:8791/api/settings -H 'Content-Type: application/json' -d '{"duration":15}'

# 4) Click Create
curl -s -X POST http://127.0.0.1:8791/api/click -H 'Content-Type: application/json' -d '{"key":"create"}'
```

### 透過 API 進行媒體上傳 + 附加

```bash
# Upload file and get server path
curl -s -X POST http://127.0.0.1:8791/api/upload -F 'file=@/absolute/path/to/input.jpg'

# Then attach using returned path
curl -s -X POST http://127.0.0.1:8791/api/attach \
  -H 'Content-Type: application/json' \
  -d '{"path":"/absolute/or/server-returned/path.jpg","click_plus":false}'
```

## 🛠️ 開發備註

- 目前尚未封裝為套件模組（不存在 `pyproject.toml`/`setup.py`）。
- 目前這個儲存庫快照尚未包含 CI/測試/lint 流程。
- `selenium_template` 是指向 `../auto-publish/` 的 symlink；其目標內容位於此儲存庫之外。
- PWA manifest 參照 `/icons/icon-192.png` 與 `/icons/icon-512.png`；目前此儲存庫尚未追蹤 icon 資產。

## 🧯 疑難排解

- Chrome 無法連接：
  - 確認 Chrome 是以 `--remote-debugging-port=9333`（或對應的 `--debugger-port`）啟動。
  - 檢查 `GET /api/status` 是否為 `devtools_ready: true`。
- 重複出現登入提示：
  - 使用持久化 `--user-data-dir`，並避免隨機設定檔路徑。
- Cloudflare/登入流程無法前進：
  - 使用非無頭模式（`--no-headless`）並增加 `--login-timeout`。
- 媒體附加沒有作用：
  - 確認檔案路徑存在於伺服器機器上；不確定時請使用 `/api/upload` + 回傳路徑。
- Storyboard 媒體附加失敗：
  - 嘗試 `POST /api/storyboard-attach-only`，或先開啟 storyboard 再呼叫 `/api/storyboard-media`。
- PWA 中無法使用解析度控制：
  - `High` 解析度僅在 model 為 `Sora 2 Pro` 時可用。
- 錯誤 chromedriver 問題：
  - 請從你的 shell 設定中移除手動固定的 chromedriver；本專案刻意讓 Selenium Manager 自動選擇相符版本。

## 🧭 路線圖

規劃中/可能的下一步改進：
- 為 selector 穩定性與 API handlers 新增自動化測試。
- 新增 lint/format 工具與 CI 工作流程。
- 新增並追蹤 PWA icon 資產，並強化離線快取策略。
- 在 `i18n/` 下新增正式的多語 README 檔案。
- 新增封裝中繼資料以簡化安裝。

## 🤝 貢獻

歡迎貢獻。

建議流程：
1. Fork 並建立功能分支。
2. 讓變更範圍保持聚焦，並為 UI 自動化變更附上重現/使用說明。
3. 以實際附加的 Chrome 工作階段手動驗證流程。
4. 建立 PR，提供變更前後行為細節。

若你調整 selector 或互動邏輯，請附上具體 Sora UI 情境，讓回歸問題更容易排查。

## ❤️ 支援 / 贊助

來自 `.github/FUNDING.yml` 的資助連結：
- GitHub Sponsors: https://github.com/sponsors/lachlanchen
- 專案連結：https://lazying.art, https://chat.lazying.art, https://onlyideas.art

## 🙏 致謝

- Selenium 與 Selenium Manager：提供瀏覽器自動化與 driver 解析能力。
- Tornado：提供輕量非同步 HTTP/WebSocket 控制服務。
- Pillow 與 `pillow-heif`：提供本機圖片轉換/預覽支援。

## 🧱 已知穩定版本

若你需要可保證 storyboard 媒體附加端到端可用的穩定基準（包含 Open Storyboard / Attach Current Path 按鈕，以及整合式 Apply 流程），請 checkout 以下 commit：

`c6683ed6d9ee0ac110536352867a26a966e3e275`

## 📄 授權

目前在此儲存庫快照中尚未發現授權檔案（於 **2026 年 2 月 28 日** 在此草稿中檢查）。

假設：在新增授權之前，所有權利仍由儲存庫擁有者保留。若非預期，請新增 `LICENSE` 檔案並更新此章節。
