[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# SoraRemote

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20WSL-6c757d)
![Server](https://img.shields.io/badge/Server-Tornado%20API-0EA5E9)
![Frontend](https://img.shields.io/badge/Frontend-PWA-10B981)
![Status](https://img.shields.io/badge/Status-Experimental-F59E0B)
![Control%20Modes](https://img.shields.io/badge/Control%20Modes-CLI%20%7C%20REST%20%7C%20PWA-0EA5E9)
![Runtime](https://img.shields.io/badge/Runtime-Linux%20%7C%20macOS%20%7C%20WSL-6B7280)

SoraRemote 是一個輕量級的 Python + Selenium 工具組，用於自動化 Sora 網頁 UI。

它支援同一套自動化流程中的三種互補執行模式：
1. **CLI 自動化代理**（`agents/sora_agent.py`）用於提示詞輸入與 UI 動作。
2. **CLI 下載器**（`agents/sora_download.py`）用於發現並下載媒體候選項目。
3. **Tornado + PWA 控制平面**（`server/app.py` + `pwa/`）用於透過 API 進行瀏覽器編排。

目前保留原始 README 的核心作業指南內容，並重組為更清楚的結構。

## 🚀 快速存取

| 目標 | 入口 | 主要用途 |
| --- | --- | --- |
| 執行腳本化提示詞 | `agents/sora_agent.py` | 透過 CLI 或包裝腳本驅動 compose 操作 |
| 取得已生成媒體 | `agents/sora_download.py` | 發現並將候選項目儲存到本機 |
| 遠端控制 | `server/app.py` + `pwa/` | 透過 REST/WebSocket 與瀏覽器控制面板進行遠端控制 |

## ✨ 概覽

核心設計：
- 透過 DevTools 遠端除錯連線至持久化的 Chrome 工作階段（預設通訊埠 `9333`）。
- 重複使用瀏覽器設定檔狀態，以維持登入/會話連續性。
- 自動化關鍵 composer 動作（輸入、加號/媒體附件、storyboard、設定、建立）。
- 透過 REST + WebSocket 日誌將相同動作暴露給本機 PWA 控制器。

### 工作流程快照

| 工作流程 | 入口 | 主要用途 |
| --- | --- | --- |
| CLI 代理 | `agents/sora_agent.py` | 輸入提示詞、點擊控件、自動化 compose 流程 |
| CLI 下載器 | `agents/sora_download.py` | 發現可下載媒體並儲存為本機檔案 |
| API + PWA | `server/app.py` + `pwa/` | 從瀏覽器進行遠端控制與視覺化編排 |

## ✅ 功能

- 使用可重複利用的設定檔啟動/附著 Chrome 的流程（`--debugger-port`、`--start-chrome`、`--user-data-dir`）。
- 對關鍵控件支援安全點擊或強制點擊（`plus`、`storyboard`、`settings`、`create`、`profile`）。
- 具備 selector fallback 行為的提示詞輸入。
- 透過檔案路徑搭配 DataTransfer 注入進行媒體附件。
- Storyboard 場景填寫 + 腳本更新 + storyboard 專屬媒體附件。
- 模型／方向／時長／解析度的設定自動化。
- 使用瀏覽器 cookies 的獨立下載發現與抓取流程。
- Tornado REST API 與即時 WebSocket 偵錯串流。
- 可安裝的本機 PWA，含上傳、預覽與細粒度控制。

## 🗂️ 專案結構

```text
SoraRemote/
├─ README.md
├─ requirements.txt
├─ .github/
│  └─ FUNDING.yml
├─ agents/
│  ├─ __init__.py
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
│  ├─ README.ar.md
│  ├─ README.de.md
│  ├─ README.es.md
│  ├─ README.fr.md
│  ├─ README.ja.md
│  ├─ README.ko.md
│  ├─ README.ru.md
│  ├─ README.vi.md
│  ├─ README.zh-Hans.md
│  └─ README.zh-Hant.md
├─ uploads/
│  └─ .gitkeep
└─ selenium_template -> ../auto-publish/ (symlink)
```

## 🧩 先決條件

- Python 3.10+（建議）。
- 已安裝並可執行 Chrome/Chromium。
- 在需要登入或互動式 UI 時，非無頭模式（`--no-headless`）需有可用顯示器。
- 在附著的 Chrome 設定檔中有 Sora 帳號存取權。

## 📦 安裝

沿用既有的標準安裝流程：

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

快速啟動（在受控瀏覽器中開啟 Sora）：

```bash
python agents/sora_agent.py
```

使用持久化工作階段附著 Chrome（建議用於 Sora）：

```bash
python -m agents.sora_agent --debugger-port 9333 --start-chrome --no-headless --login-timeout 600 --text "A sunset over Tokyo, cinematic."
```

注意事項：
- 會在 Sora 頁面開啟一個 Chrome 視窗。若被導向登入頁，請先完成登入；腳本會等待並接著輸入你的提示詞。
- 若要重複使用同一個登入狀態，請傳入固定的設定檔路徑：

```bash
python -m agents.sora_agent --debugger-port 9333 --start-chrome --no-headless --user-data-dir "$HOME/chrome_sora_profile_9333"
```

### 主要 CLI 選項（`agents/sora_agent.py`）

- `--url` 目標頁面（預設：`https://sora.chatgpt.com/explore`）。
- `--debugger-port` 附著已用 `--remote-debugging-port=PORT` 啟動的既有 Chrome。
- `--start-chrome` 若與 `--debugger-port` 同時提供，會為你啟動 Chrome（使用 `--user-data-dir`）。
- `--no-headless` 以可見瀏覽器執行；登入與 Cloudflare 流程需要此模式。
- `--selector` 用來定位輸入框的 CSS（預設符合 Sora composer textarea）。
- `--text` 要輸入到輸入框的內容。
- `--chrome-binary` 明確指定 Chrome/Chromium 路徑。
- `--action` UI 行為：`list`、`plus`、`storyboard`、`settings`、`create`、`profile`。
- `--force-click` 即使元素看似停用也會強制點擊。
- `--login-timeout` 等待手動登入完成的時間視窗。

Driver 處理：
- 代理會在啟動前先從 `PATH` 移除任何過期的 `chromedriver`。
- Selenium Manager 會自動為目前安裝的 Chrome 解析對應的驅動程式。

### CLI 範例（UI 控制）

列出並點擊常用控件：

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action list --action storyboard --action settings --action plus
```

強制點擊 Create video 按鈕（即使停用）：

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action create --force-click
```

開啟 profile/settings 並依需求手動導覽：

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action list --action profile
```

若未偵測到 `profile`，`settings` 按鈕通常會開啟同一個選單。

### 下載流程

使用處理腳本探索並下載影片：

- 乾跑（僅列出候選）：`./bin/sora_download.sh --dry-run`
- 最多下載 2 個檔案到 `./downloads/sora`：`./bin/sora_download.sh --max 2`
- 更改輸出資料夾：`OUT_DIR=$HOME/Videos/sora ./bin/sora_download.sh --max 1`

也可直接以模組方式使用：`python -m agents.sora_download ...`。

## 🌐 控制伺服器 + PWA

執行 Tornado 伺服器：

```bash
python server/app.py
# listens on http://0.0.0.0:8791 and serves the PWA at /
```

伺服器預設行為：
- 重複使用通訊埠 `9333` 上的 Chrome。
- 除非設定 `SORA_UPLOADS_DIR`，否則將上傳存放於 `./uploads`。

### 主要端點

所有端點都會對目前已附著的 Chrome 運作（預設除錯通訊埠為 `9333`）。

| 方法 | 路徑 | 請求資料 | 說明 |
| --- | --- | --- | --- |
| `GET` | `/api/status` | none | 回傳 DevTools 準備度狀態與目前通訊埠。 |
| `POST` | `/api/open` | `{ url? }` | 導航已附著的 Chrome 分頁到指定 URL（預設為 Sora Explore）。 |
| `GET` | `/api/actions` | none | 檢查按鈕/控件狀態（found/displayed/disabled 中繼資料）。 |
| `POST` | `/api/click` | `{ key, force? }` | 按下指定控件，`key ∈ {plus, storyboard, settings, create, profile}`。 |
| `POST` | `/api/type` | `{ text, selector?, url? }` | 將提示詞輸入到 composer selector。 |
| `POST` | `/api/compose` | `{ text, click_create? }` | 開啟 compose 頁面、輸入文字，並可選擇點擊 create。 |
| `POST` | `/api/attach` | `{ path, click_plus? }` | 透過 DataTransfer 注入上傳媒體；若已存在媒體會自動清空（`click_plus` 預設為 `false`）。 |
| `POST` | `/api/describe` | `{ text }` | 填寫「Optionally describe your video…」文字區。 |
| `POST` | `/api/script-updates` | `{ text }` | 填寫「Describe updates to your script…」欄位。 |
| `POST` | `/api/storyboard` | `{ scenes: ["scene 1", ...], script_updates?: "...", media_path?: "..." }` | 開啟 storyboard、填寫場景文字區，可選擇套用腳本更新與 storyboard 媒體。 |
| `POST` | `/api/storyboard-media` | `{ path }` | 當 storyboard 已可見時，將媒體附加到 storyboard 專用上傳器。 |
| `POST` | `/api/storyboard-attach-only` | `{ path }` | 確保 storyboard 已開啟後再附加媒體。 |
| `POST` | `/api/settings` | `{ model?, orientation?, duration?, resolution? }` | 開啟設定並套用所選值；回應會回傳已套用的標籤。 |
| `POST` | `/api/upload` | multipart form data | 將本機檔案儲存到伺服器上傳目錄，並回傳伺服器端路徑。 |
| `POST` | `/api/preview` | multipart form data | 將圖片轉為 PNG 預覽（在 UI 中用於 HEIC/HEIF/AVIF fallback）。 |
| `GET` | `/ws` | WebSocket | 串流 action/debug 事件。 |

### PWA 控制

啟動 `server/app.py` 後開啟 `http://0.0.0.0:8791`（或你選擇的主機）。

現有實作重點：
- 透過檔案選擇器上傳媒體或貼上路徑後，點擊 **Plus** 附加，無需再次開啟系統檔案對話框。
- 在專用的「Media description」欄位套用媒體描述。
- 針對 **Set Model**、**Set Orientation**、**Set Duration**、**Set Resolution** 與腳本更新提供獨立控制。
- Storyboard 控制項包含場景、腳本更新、開啟 storyboard 面板與附加目前 storyboard 路徑。
- 即時除錯日誌會顯示 API 呼叫與 Sora 回傳值（例如已選取的模型/時長）。

## ⚙️ 設定

### 環境變數

`server/app.py` 讀取：
- `SORA_DEBUGGER_PORT`（預設 `9333`）
- `SORA_USER_DATA_DIR`（預設 `~/chrome_sora_profile_<port>`）
- `SORA_DISPLAY`（可選的 X display）
- `SORA_API_PORT`（預設 `8791`）
- `SORA_URL`（預設 `https://sora.chatgpt.com/explore`）
- `SORA_UPLOADS_DIR`（可選覆寫上傳目錄）

`agents/sora_agent.py` 也支援：
- `CHROME_BINARY`（若未提供 `--chrome-binary`）

Wrapper 腳本支援：
- `PORT`、`SORA_PROFILE_DIR`、`TIMEOUT`、`LOGIN_TIMEOUT`（`bin/sora_type.sh`）
- `PORT`、`SORA_PROFILE_DIR`、`OUT_DIR`（`bin/sora_download.sh`）

## 🧪 範例

### 端對端 API 範例（curl）

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

### 透過 API 上傳 + 附加媒體

```bash
# Upload file and get server path
curl -s -X POST http://127.0.0.1:8791/api/upload -F 'file=@/absolute/path/to/input.jpg'

# Then attach using returned path
curl -s -X POST http://127.0.0.1:8791/api/attach \
  -H 'Content-Type: application/json' \
  -d '{"path":"/absolute/or/server-returned/path.jpg","click_plus":false}'
```

## 🛠️ 開發備註

- 目前沒有套件化模組（不存在 `pyproject.toml`/`setup.py`）。
- 目前此儲存庫快照中沒有 CI/測試/lint 流程。
- `selenium_template` 是指向 `../auto-publish/` 的 symlink；其目標內容位於本專案外部。
- PWA manifest 參照 `/icons/icon-192.png` 與 `/icons/icon-512.png`，目前本儲存庫未追蹤 icon 資源。

## 🧯 疑難排解

- Chrome 附著失敗：
  - 確保 Chrome 是以 `--remote-debugging-port=9333`（或與 `--debugger-port` 相符）啟動。
  - 檢查 `GET /api/status` 是否回傳 `devtools_ready: true`。
- 重複出現登入提示：
  - 使用持久化 `--user-data-dir`，並避免使用隨機的 profile 路徑。
- Cloudflare/登入流程停滯：
  - 改用非無頭模式（`--no-headless`）並增加 `--login-timeout`。
- 媒體附件沒有反應：
  - 確認檔案路徑存在於伺服器本機；若不確定請使用 `/api/upload` 並使用回傳路徑。
- Storyboard 媒體附件失敗：
  - 嘗試 `POST /api/storyboard-attach-only`，或先開啟 storyboard 再呼叫 `/api/storyboard-media`。
- PWA 中解析度控制無法使用：
  - 僅在模型為 `Sora 2 Pro` 時會啟用 `High` 解析度。
- chromedriver 錯誤：
  - 從 shell 環境中移除手動指定的 chromedriver；本專案刻意讓 Selenium Manager 自動選擇對應版本。

## 🧭 路線圖

預計／可能的下一步改進：
- 為 selector 穩定性與 API handler 加入自動化測試。
- 新增 lint/format 工具與 CI 工作流程。
- 新增並追蹤 PWA icon 資源，並加強離線快取策略。
- 在 `i18n/` 下新增正式的多語 README 檔案。
- 新增打包元資料以簡化安裝。

## 🤝 貢獻

歡迎投稿。

建議流程：
1. Fork 並建立功能分支。
2. 保持變更聚焦，並為 UI 自動化變更補上重現與使用說明。
3. 以真實附著 Chrome 的會話手動驗證流程。
4. 提交 PR 時附上變更前後行為說明。

若你變更了 selector 或互動邏輯，請附上具體的 Sora UI 上下文，讓回歸更容易排查。

## 🙏 致謝

- Selenium 與 Selenium Manager：提供瀏覽器自動化與驅動程式解析。
- Tornado：提供輕量化非同步 HTTP/WebSocket 控制服務。
- Pillow 與 `pillow-heif`：提供本地圖片轉換與預覽支援。

## 🧱 已知穩定版本

如果你需要一個穩定的基準，以保證 storyboard 媒體附件端到端可用（包含 Open Storyboard / Attach Current Path 按鈕與合併 Apply 流程），可參考提交：

`c6683ed6d9ee0ac110536352867a26a966e3e275`

## 📄 授權

此儲存庫快照目前尚未包含授權檔（在本版本草案中檢查於 **February 28, 2026**）。

假設在新增授權前，所有權利仍由本專案擁有者保留。若非預期，請新增 `LICENSE` 檔案並更新此段。


## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |
