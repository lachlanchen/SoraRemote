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

SoraRemote 是一个轻量级的 Python + Selenium 工具包，用于自动化 Sora Web UI。

它支持一个自动化工作流中的三种互补执行模式：
1. **CLI 自动化代理**（`agents/sora_agent.py`）用于提示词输入和 UI 操作。
2. **CLI 下载器**（`agents/sora_download.py`）用于发现并下载媒体候选项。
3. **Tornado + PWA 控制平面**（`server/app.py` + `pwa/`）用于基于 API 的浏览器编排。

当前 README 的内容保持为规范操作指引并已重构为更清晰结构。

## 🚀 快速访问

| 目标 | 入口 | 主要用途 |
| --- | --- | --- |
| 运行脚本化提示词 | `agents/sora_agent.py` | 通过 CLI 或包装脚本驱动 compose 操作 |
| 获取已生成媒体 | `agents/sora_download.py` | 发现并本地保存候选文件 |
| 远程控制 | `server/app.py` + `pwa/` | 通过 REST/WebSocket + 浏览器控制面板进行远程控制 |

## ✨ 概览

核心设计：
- 通过 DevTools 远程调试（默认端口 `9333`）连接到持久化 Chrome 会话。
- 复用浏览器配置文件状态以保持登录/会话连续性。
- 自动执行关键创作动作（输入、加号/媒体附加、故事板、设置、创建）。
- 通过 REST + WebSocket 日志把这些动作暴露给本地 PWA 控制器。

### 工作流快照

| 工作流 | 入口 | 主要用途 |
| --- | --- | --- |
| CLI 代理 | `agents/sora_agent.py` | 输入提示词、点击控件、自动化 compose 流程 |
| CLI 下载器 | `agents/sora_download.py` | 发现可下载媒体并本地保存文件 |
| API + PWA | `server/app.py` + `pwa/` | 从浏览器远程控制并进行可视化编排 |

## ✅ 功能

- 支持带可复用配置的 Chrome 附加/启动流程（`--debugger-port`、`--start-chrome`、`--user-data-dir`）。
- 关键控件支持安全点击或强制点击（`plus`、`storyboard`、`settings`、`create`、`profile`）。
- 具备选择器回退行为的提示词输入。
- 通过文件路径和 DataTransfer 注入进行媒体附加。
- 故事板场景填写 + 脚本更新 + 故事板专属媒体附加。
- 模型/方向/时长/分辨率设置自动化。
- 使用浏览器 Cookie 的独立下载发现与抓取流程。
- Tornado REST API 与实时 WebSocket 调试流。
- 可安装的本地 PWA，支持上传、预览和细粒度控制。

## 🗂️ 项目结构

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

## 🧩 先决条件

- Python 3.10+（推荐）。
- 已安装并可运行 Chrome/Chromium。
- 非无头场景（`--no-headless`）需要可用显示器用于登录或交互式 UI。
- 在附加 Chrome 配置中具备 Sora 账号登录状态。

## 📦 安装

按该仓库既有流程安装：

```bash
conda activate agent
pip install -r requirements.txt
```

`requirements.txt` 中的依赖：

| 包 | 版本说明 |
| --- | --- |
| `selenium` | `>=4.17.2` |
| `tornado` | `>=6.4` |
| `Pillow` | `>=9.4.0` |
| `pillow-heif` | `>=0.16.0` |

## 🚀 使用

### 快速开始（CLI 代理）

快速启动（在受管浏览器中打开 Sora）：

```bash
python agents/sora_agent.py
```

使用持久化会话附加 Chrome（推荐用于 Sora）：

```bash
python -m agents.sora_agent --debugger-port 9333 --start-chrome --no-headless --login-timeout 600 --text "A sunset over Tokyo, cinematic."
```

说明：
- 会在 Sora 页面打开一个 Chrome 窗口。若被重定向到登录页请先登录；脚本会等待并随后输入你的提示词。
- 要复用同一登录态，请传入固定的配置路径：

```bash
python -m agents.sora_agent --debugger-port 9333 --start-chrome --no-headless --user-data-dir "$HOME/chrome_sora_profile_9333"
```

### 关键 CLI 选项（`agents/sora_agent.py`）

- `--url` 目标页面（默认：`https://sora.chatgpt.com/explore`）。
- `--debugger-port` 连接到一个通过 `--remote-debugging-port=PORT` 启动的现有 Chrome。
- `--start-chrome` 若与 `--debugger-port` 同时设置，会为你启动 Chrome（使用 `--user-data-dir`）。
- `--no-headless` 以可见浏览器运行；登录和 Cloudflare 场景需要该模式。
- `--selector` 定位输入框的 CSS（默认匹配 Sora compose textarea）。
- `--text` 要输入到输入框的文本。
- `--chrome-binary` 显式设置 Chrome/Chromium 路径。
- `--action` UI 操作：`list`、`plus`、`storyboard`、`settings`、`create`、`profile`。
- `--force-click` 即使元素看起来禁用也会执行点击。
- `--login-timeout` 手动完成登录的等待时长。

驱动处理：
- 代理会在启动前从 `PATH` 中移除任何过期的 `chromedriver`。
- Selenium Manager 会自动为当前已安装的 Chrome 解析匹配驱动。

### CLI 示例（UI 控制）

列出并点击常用控件：

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action list --action storyboard --action settings --action plus
```

强制点击 Create video 按钮（即使处于禁用状态）：

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action create --force-click
```

打开 profile/settings 并按需手动导航：

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action list --action profile
```

如果未检测到 `profile`，通常 `settings` 按钮会打开同一菜单。

### 下载流程

使用处理脚本发现并下载视频：

- 试运行（仅列出候选项）：`./bin/sora_download.sh --dry-run`
- 最多下载 2 个文件到 `./downloads/sora`：`./bin/sora_download.sh --max 2`
- 更改输出文件夹：`OUT_DIR=$HOME/Videos/sora ./bin/sora_download.sh --max 1`

也可直接通过 `python -m agents.sora_download ...` 直接调用模块。

## 🌐 控制服务器 + PWA

运行 Tornado 服务：

```bash
python server/app.py
# listens on http://0.0.0.0:8791 and serves the PWA at /
```

服务默认行为：
- 重用调试端口为 `9333` 的 Chrome。
- 将上传文件保存到 `./uploads`，除非设置了 `SORA_UPLOADS_DIR`。

### 关键端点

所有端点均操作当前已附加的 Chrome（默认调试端口 `9333`）。

| 方法 | 路径 | 载荷 | 描述 |
| --- | --- | --- | --- |
| `GET` | `/api/status` | none | 返回 DevTools 就绪状态和当前端口。 |
| `POST` | `/api/open` | `{ url? }` | 将已附加的 Chrome 标签页导航到给定 URL（默认指向 Sora Explore）。 |
| `GET` | `/api/actions` | none | 检查按钮/控件状态（found/displayed/disabled 元数据）。 |
| `POST` | `/api/click` | `{ key, force? }` | 按下一个控件，其中 `key ∈ {plus, storyboard, settings, create, profile}`。 |
| `POST` | `/api/type` | `{ text, selector?, url? }` | 在 composer 选择器中输入提示词。 |
| `POST` | `/api/compose` | `{ text, click_create? }` | 打开 compose 页面并输入文本，可选点击 create。 |
| `POST` | `/api/attach` | `{ path, click_plus? }` | 通过 DataTransfer 注入上传媒体；会自动清空已有媒体（`click_plus` 默认 `false`）。 |
| `POST` | `/api/describe` | `{ text }` | 填写“Optionally describe your video…”文本框。 |
| `POST` | `/api/script-updates` | `{ text }` | 填写“Describe updates to your script…”字段。 |
| `POST` | `/api/storyboard` | `{ scenes: ["scene 1", ...], script_updates?: "...", media_path?: "..." }` | 打开故事板，填写场景文本框，可选应用脚本更新和故事板媒体。 |
| `POST` | `/api/storyboard-media` | `{ path }` | 当故事板已可见时，将媒体附加到故事板专用上传控件。 |
| `POST` | `/api/storyboard-attach-only` | `{ path }` | 确保故事板已打开后再附加媒体。 |
| `POST` | `/api/settings` | `{ model?, orientation?, duration?, resolution? }` | 打开设置并应用选定值；响应会回显已应用标签。 |
| `POST` | `/api/upload` | multipart form data | 将本地文件保存到服务端上传目录并返回服务端路径。 |
| `POST` | `/api/preview` | multipart form data | 将图片转换为 PNG 预览（在 UI 中用于 HEIC/HEIF/AVIF 降级场景）。 |
| `GET` | `/ws` | WebSocket | 推送 action/debug 事件流。 |

### PWA 控制

启动 `server/app.py` 后打开 `http://0.0.0.0:8791`（或你选择的主机）。

来自现有实现的要点：
- 通过文件选择器上传媒体或粘贴路径后点击 **Plus** 附加，无需重复打开系统文件对话框。
- 在专用“Media description”框中应用媒体描述。
- 为 **Set Model**、**Set Orientation**、**Set Duration**、**Set Resolution** 以及脚本更新提供独立控制。
- 提供故事板控制：场景、脚本更新、打开故事板面板、附加当前故事板路径。
- 实时调试日志展示 API 调用和 Sora 返回值（例如已选择的模型/时长）。

## ⚙️ 配置

### 环境变量

`server/app.py` 读取：
- `SORA_DEBUGGER_PORT`（默认 `9333`）
- `SORA_USER_DATA_DIR`（默认 `~/chrome_sora_profile_<port>`）
- `SORA_DISPLAY`（可选 X display）
- `SORA_API_PORT`（默认 `8791`）
- `SORA_URL`（默认 `https://sora.chatgpt.com/explore`）
- `SORA_UPLOADS_DIR`（可选上传目录覆盖）

`agents/sora_agent.py` 也支持：
- `CHROME_BINARY`（未提供 `--chrome-binary` 时）

包装脚本支持：
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

### 通过 API 上传 + 附加媒体

```bash
# Upload file and get server path
curl -s -X POST http://127.0.0.1:8791/api/upload -F 'file=@/absolute/path/to/input.jpg'

# Then attach using returned path
curl -s -X POST http://127.0.0.1:8791/api/attach \
  -H 'Content-Type: application/json' \
  -d '{"path":"/absolute/or/server-returned/path.jpg","click_plus":false}'
```

## 🛠️ 开发说明

- 当前不含打包模块（缺少 `pyproject.toml`/`setup.py`）。
- 当前仓库快照中不含 CI/测试/lint 流程。
- `selenium_template` 是到 `../auto-publish/` 的符号链接；其目标内容位于仓库外。
- PWA manifest 引用了 `/icons/icon-192.png` 和 `/icons/icon-512.png`；当前未在本仓库中跟踪图标资源。

## 🧯 故障排查

- Chrome 附加失败：
  - 确保 Chrome 已通过 `--remote-debugging-port=9333`（或与 `--debugger-port` 匹配）启动。
  - 检查 `GET /api/status` 是否返回 `devtools_ready: true`。
- 重复出现登录提示：
  - 使用持久化 `--user-data-dir`，并避免随机 profile 路径。
- Cloudflare 或登录流程卡住：
  - 使用非无头模式（`--no-headless`）并提高 `--login-timeout`。
- 媒体附加无效：
  - 确认文件路径在服务端机器上存在；若不确定请使用 `/api/upload` 和返回路径。
- 故事板媒体附加失败：
  - 尝试 `POST /api/storyboard-attach-only`，或先打开故事板再调用 `/api/storyboard-media`。
- PWA 中分辨率控制不可用：
  - 仅当模型为 `Sora 2 Pro` 时，`High` 分辨率才会启用。
- chromedriver 版本错误：
  - 移除 shell 环境里手动固定的 chromedriver，本项目故意由 Selenium Manager 自动选择匹配版本。

## 🧭 路线图

计划/预期的后续改进：
- 为选择器稳定性与 API 处理器补充自动化测试。
- 添加 lint/format 工具与 CI 工作流。
- 补充受追踪的 PWA 图标资源并增强离线缓存策略。
- 在 `i18n/` 下补充正式多语言 README 文件。
- 增加打包元数据以简化安装。

## 🤝 贡献

欢迎提交贡献。

建议流程：
1. Fork 并创建功能分支。
2. 保持变更范围集中，并为 UI 自动化变更补充复现/使用说明。
3. 在真实已连接的 Chrome 会话下手动验证流程。
4. 提交 PR 时说明前后行为变化。

如果你修改了选择器或交互逻辑，请包含具体 Sora UI 的上下文信息，以便更轻松地排查回归。

## 🙏 致谢

- Selenium 与 Selenium Manager：浏览器自动化与驱动解析。
- Tornado：轻量级异步 HTTP/WebSocket 控制服务。
- Pillow 与 `pillow-heif`：本地图像转换与预览支持。

## 🧱 已验证构建

如果你需要一个稳定的基线版本，能保证故事板媒体附加端到端可用（包括 Open Storyboard / Attach Current Path 按钮和组合 Apply 流程），请查看提交：

`c6683ed6d9ee0ac110536352867a26a966e3e275`

## 📄 许可证

当前仓库快照中尚未包含许可证文件（此版本草稿检查时间为 **February 28, 2026**）。

默认假设在添加许可证前所有权利仍归仓库所有者所有；若这不符合你的意图，请添加 `LICENSE` 文件并更新此段。


## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |
