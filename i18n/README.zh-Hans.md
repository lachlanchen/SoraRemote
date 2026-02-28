[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)



# SoraRemote

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20WSL-6c757d)
![Server](https://img.shields.io/badge/Server-Tornado%20API-0EA5E9)
![Frontend](https://img.shields.io/badge/Frontend-PWA-10B981)
![Status](https://img.shields.io/badge/Status-Experimental-F59E0B)

SoraRemote 是一个轻量级的 Python + Selenium 工具包，用于自动化 Sora Web UI。

它支持三种互补工作流：
1. CLI 自动化代理（`agents/sora_agent.py`）：用于提示词输入与 UI 控制操作。
2. CLI 下载器（`agents/sora_download.py`）：用于发现并下载媒体候选项。
3. 本地 Tornado 控制服务 + PWA（`server/app.py` + `pwa/`）：用于 API 驱动与浏览器端控制。

当前 README 内容作为规范化操作指南已被保留，并为了可读性进行了重组。

## ✨ 概览

核心设计：
- 通过 DevTools 远程调试连接到持久化 Chrome 会话（默认端口 `9333`）。
- 复用浏览器配置目录状态，保持登录/会话连续性。
- 自动化关键创作区操作（输入、加号/媒体附加、故事板、设置、创建）。
- 通过 REST + WebSocket 日志暴露同样的操作，供本地 PWA 控制器使用。

### 工作流快照

| 工作流 | 入口 | 主要用途 |
| --- | --- | --- |
| CLI 代理 | `agents/sora_agent.py` | 输入提示词、点击控件、自动化创作流程 |
| CLI 下载器 | `agents/sora_download.py` | 发现可下载媒体并保存到本地 |
| API + PWA | `server/app.py` + `pwa/` | 在浏览器中进行远程控制与可视化编排 |

## ✅ 功能特性

- Chrome 连接/启动流程，支持可复用配置（`--debugger-port`、`--start-chrome`、`--user-data-dir`）。
- 关键控件支持安全点击或强制点击（`plus`、`storyboard`、`settings`、`create`、`profile`）。
- 具备选择器回退行为的提示词输入。
- 通过文件路径 + DataTransfer 注入实现媒体附加。
- 故事板场景填充 + 脚本更新 + 故事板专用媒体附加。
- 模型/方向/时长/分辨率的设置自动化。
- 使用浏览器 Cookie 的独立下载发现与获取流程。
- Tornado REST API 与实时 WebSocket 调试流。
- 可安装的本地 PWA，支持上传、预览与细粒度控制。

## 🗂️ 项目结构

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

## 🧩 前置要求

- Python 3.10+（推荐）。
- 已安装且可运行 Chrome/Chromium。
- 当需要登录或交互式 UI 时，非无头模式（`--no-headless`）需要可用显示环境。
- 可在所连接的 Chrome 配置中访问 Sora 账号。

## 📦 安装

来自规范 README 的现有安装流程：

```bash
conda activate agent
pip install -r requirements.txt
```

`requirements.txt` 中的依赖：

| Package | Version spec |
| --- | --- |
| `selenium` | `>=4.17.2` |
| `tornado` | `>=6.4` |
| `Pillow` | `>=9.4.0` |
| `pillow-heif` | `>=0.16.0` |

## 🚀 使用

### 快速开始（CLI 代理）

快速开始（在受管浏览器中打开 Sora）：

```bash
python agents/sora_agent.py
```

连接带持久会话的 Chrome（推荐用于 Sora）：

```bash
python -m agents.sora_agent --debugger-port 9333 --start-chrome --no-headless --login-timeout 600 --text "A sunset over Tokyo, cinematic."
```

说明：
- 会打开一个位于 Sora 页面上的 Chrome 窗口。若跳转到登录页，请完成登录；脚本会等待后输入你的提示词。
- 若要复用同一登录态，请传入固定配置目录路径：

```bash
python -m agents.sora_agent --debugger-port 9333 --start-chrome --no-headless --user-data-dir "$HOME/chrome_sora_profile_9333"
```

### 关键 CLI 参数（`agents/sora_agent.py`）

- `--url` 目标页面（默认：`https://sora.chatgpt.com/explore`）。
- `--debugger-port` 连接到使用 `--remote-debugging-port=PORT` 启动的现有 Chrome。
- `--start-chrome` 若与 `--debugger-port` 一起设置，会为你启动 Chrome（使用 `--user-data-dir`）。
- `--no-headless` 以可见浏览器运行；登录和 Cloudflare 场景需要此选项。
- `--selector` 用于定位输入框的 CSS（默认匹配 Sora 创作区 textarea）。
- `--text` 要输入到输入框的文本。
- `--chrome-binary` 显式设置 Chrome/Chromium 路径。
- `--action` UI 操作：`list`、`plus`、`storyboard`、`settings`、`create`、`profile`。
- `--force-click` 即使元素显示禁用也执行点击。
- `--login-timeout` 等待手动认证完成的窗口时间。

驱动处理：
- 代理会在启动前从 `PATH` 中移除任何陈旧 `chromedriver`。
- 然后由 Selenium Manager 自动为已安装的 Chrome 解析匹配驱动。

### CLI 示例（UI 控制）

列出并点击常用控件：

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action list --action storyboard --action settings --action plus
```

强制点击 Create video 按钮（即使显示为禁用）：

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action create --force-click
```

打开 profile/settings，并在需要时手动导航：

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action list --action profile
```

如果未检测到 `profile`，通常 `settings` 按钮会打开同一菜单。

### 下载流程

使用封装脚本发现并下载视频：

- 仅演练（只列出候选项）：`./bin/sora_download.sh --dry-run`
- 最多下载 2 个文件到 `./downloads/sora`：`./bin/sora_download.sh --max 2`
- 修改输出目录：`OUT_DIR=$HOME/Videos/sora ./bin/sora_download.sh --max 1`

也可通过 `python -m agents.sora_download ...` 直接调用模块。

## 🌐 控制服务 + PWA

运行 Tornado 服务：

```bash
python server/app.py
# listens on http://0.0.0.0:8791 and serves the PWA at /
```

默认情况下，服务会：
- 复用远程调试端口 `9333` 上的 Chrome。
- 将上传文件存储到 `./uploads`，除非设置了 `SORA_UPLOADS_DIR`。

### 关键端点

所有端点都作用于当前连接的 Chrome（默认调试端口 `9333`）。

| Method | Path | Payload | Description |
| --- | --- | --- | --- |
| `GET` | `/api/status` | none | Returns DevTools readiness state and active port. |
| `POST` | `/api/open` | `{ url? }` | Navigates the attached Chrome tab to the given URL (defaults to Sora Explore). |
| `GET` | `/api/actions` | none | Inspects button/control state (found/displayed/disabled metadata). |
| `POST` | `/api/click` | `{ key, force? }` | Presses one control where `key ∈ {plus, storyboard, settings, create, profile}`. |
| `POST` | `/api/type` | `{ text, selector?, url? }` | Types prompt text into composer selector. |
| `POST` | `/api/compose` | `{ text, click_create? }` | Opens compose page, types text, optionally clicks create. |
| `POST` | `/api/attach` | `{ path, click_plus? }` | Uploads media via DataTransfer injection; clears existing media automatically (`click_plus` defaults to `false`). |
| `POST` | `/api/describe` | `{ text }` | Fills the “Optionally describe your video…” textarea. |
| `POST` | `/api/script-updates` | `{ text }` | Fills the “Describe updates to your script…” field. |
| `POST` | `/api/storyboard` | `{ scenes: ["scene 1", ...], script_updates?: "...", media_path?: "..." }` | Opens storyboard, fills scene textareas, optionally applies script updates and storyboard media. |
| `POST` | `/api/storyboard-media` | `{ path }` | Attaches media to storyboard-specific uploader when storyboard is already visible. |
| `POST` | `/api/storyboard-attach-only` | `{ path }` | Ensures storyboard is open, then attaches media. |
| `POST` | `/api/settings` | `{ model?, orientation?, duration?, resolution? }` | Opens settings and applies selected values; response echoes applied labels. |
| `POST` | `/api/upload` | multipart form data | Saves local file(s) to server upload directory and returns server-side paths. |
| `POST` | `/api/preview` | multipart form data | Converts image to PNG preview (useful for HEIC/HEIF/AVIF fallback in UI). |
| `GET` | `/ws` | WebSocket | Streams action/debug events. |

### PWA 控制

启动 `server/app.py` 后，访问 `http://0.0.0.0:8791`（或你指定的主机）。

现有实现亮点：
- 通过文件选择器上传媒体，或粘贴路径后点击 **Plus** 进行附加，而无需重复打开系统文件对话框。
- 在独立的 “Media description” 输入框中应用媒体描述。
- 为 **Set Model**、**Set Orientation**、**Set Duration**、**Set Resolution** 以及脚本更新提供独立控制。
- 提供故事板控制：场景、脚本更新、打开故事板面板、附加当前故事板路径。
- 实时调试日志显示 API 调用与 Sora 返回值（例如已选模型/时长）。

## ⚙️ 配置

### 环境变量

`server/app.py` 读取：
- `SORA_DEBUGGER_PORT`（默认 `9333`）
- `SORA_USER_DATA_DIR`（默认 `~/chrome_sora_profile_<port>`）
- `SORA_DISPLAY`（可选 X display）
- `SORA_API_PORT`（默认 `8791`）
- `SORA_URL`（默认 `https://sora.chatgpt.com/explore`）
- `SORA_UPLOADS_DIR`（可选：覆盖上传目录）

`agents/sora_agent.py` 还支持：
- `CHROME_BINARY`（当未提供 `--chrome-binary` 时）

封装脚本支持：
- `PORT`、`SORA_PROFILE_DIR`、`TIMEOUT`、`LOGIN_TIMEOUT`（`bin/sora_type.sh`）
- `PORT`、`SORA_PROFILE_DIR`、`OUT_DIR`（`bin/sora_download.sh`）

## 🧪 示例

### 端到端 API 示例（curl）

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

### 通过 API 上传并附加媒体

```bash
# Upload file and get server path
curl -s -X POST http://127.0.0.1:8791/api/upload -F 'file=@/absolute/path/to/input.jpg'

# Then attach using returned path
curl -s -X POST http://127.0.0.1:8791/api/attach \
  -H 'Content-Type: application/json' \
  -d '{"path":"/absolute/or/server-returned/path.jpg","click_plus":false}'
```

## 🛠️ 开发说明

- 当前没有打包模块（不存在 `pyproject.toml`/`setup.py`）。
- 当前仓库快照中没有 CI/测试/lint 流水线。
- `selenium_template` 是指向 `../auto-publish/` 的符号链接；其目标内容位于本仓库外。
- PWA manifest 引用了 `/icons/icon-192.png` 与 `/icons/icon-512.png`；这些图标资源当前未被本仓库跟踪。

## 🧯 故障排查

- Chrome 连接失败：
  - 确保 Chrome 以 `--remote-debugging-port=9333`（或匹配的 `--debugger-port`）启动。
  - 检查 `GET /api/status` 是否返回 `devtools_ready: true`。
- 反复要求登录：
  - 使用持久化 `--user-data-dir`，避免随机配置目录路径。
- Cloudflare/登录流程无法推进：
  - 使用非无头模式（`--no-headless`），并提高 `--login-timeout`。
- 媒体附加无效果：
  - 确认文件路径在服务端机器上存在；不确定时使用 `/api/upload` + 返回路径。
- 故事板媒体附加失败：
  - 尝试 `POST /api/storyboard-attach-only`，或先打开故事板再调用 `/api/storyboard-media`。
- PWA 中分辨率控制不可用：
  - 仅当模型为 `Sora 2 Pro` 时，`High` 分辨率可用。
- chromedriver 版本错误：
  - 从 shell 配置中移除手动固定的 chromedriver；本项目有意由 Selenium Manager 自动选择匹配版本。

## 🧭 路线图

计划中/可能的后续改进：
- 为选择器稳定性与 API 处理器增加自动化测试。
- 增加 lint/format 工具与 CI 工作流。
- 增加受跟踪的 PWA 图标资源并强化离线缓存策略。
- 在 `i18n/` 下添加正式多语言 README 文件。
- 增加打包元数据以简化安装。

## 🤝 贡献

欢迎贡献。

建议流程：
1. Fork 并创建功能分支。
2. 变更范围尽量聚焦；涉及 UI 自动化变更时附带复现/使用说明。
3. 使用真实已连接的 Chrome 会话手动验证流程。
4. 提交 PR 并说明前后行为差异。

如果你修改了选择器或交互逻辑，请附上具体 Sora UI 上下文，以便更容易排查回归。

## ❤️ 支持 / 赞助

来自 `.github/FUNDING.yml` 的资助链接：
- GitHub Sponsors: https://github.com/sponsors/lachlanchen
- 项目链接: https://lazying.art, https://chat.lazying.art, https://onlyideas.art

## 🙏 致谢

- 感谢 Selenium 和 Selenium Manager 提供浏览器自动化与驱动解析能力。
- 感谢 Tornado 提供轻量级异步 HTTP/WebSocket 控制服务。
- 感谢 Pillow 与 `pillow-heif` 提供本地图像转换/预览支持。

## 🧱 已验证可用构建

如果你需要一个可稳定复现、并保证故事板媒体附加端到端可用的基线版本（包括 Open Storyboard / Attach Current Path 按钮与组合 Apply 流程），请检出以下提交：

`c6683ed6d9ee0ac110536352867a26a966e3e275`

## 📄 许可证

当前仓库快照中尚无许可证文件（本草稿检查日期为 **February 28, 2026**）。

假设：在添加许可证前，所有权利由仓库所有者保留。若非如此，请添加 `LICENSE` 文件并更新本节。
