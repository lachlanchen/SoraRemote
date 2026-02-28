[English](README.md) · [العربية](i18n/README.ar.md) · [Español](i18n/README.es.md) · [Français](i18n/README.fr.md) · [日本語](i18n/README.ja.md) · [한국어](i18n/README.ko.md) · [Tiếng Việt](i18n/README.vi.md) · [中文 (简体)](i18n/README.zh-Hans.md) · [中文（繁體）](i18n/README.zh-Hant.md) · [Deutsch](i18n/README.de.md) · [Русский](i18n/README.ru.md)


[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# SoraRemote

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20WSL-6c757d)
![Server](https://img.shields.io/badge/Server-Tornado%20API-0EA5E9)
![Frontend](https://img.shields.io/badge/Frontend-PWA-10B981)
![Status](https://img.shields.io/badge/Status-Experimental-F59E0B)
![Control%20Modes](https://img.shields.io/badge/Control%20Modes-CLI%20%7C%20REST%20%7C%20PWA-0EA5E9)
![Runtime](https://img.shields.io/badge/Runtime-Linux%20%7C%20macOS%20%7C%20WSL-6B7280)

SoraRemote is a lightweight Python + Selenium toolkit for automating the Sora web UI.

It supports three complementary execution modes for one automation workflow:
1. **CLI automation agent** (`agents/sora_agent.py`) for prompt typing and UI actions.
2. **CLI downloader** (`agents/sora_download.py`) for discovering and downloading media candidates.
3. **Tornado + PWA control plane** (`server/app.py` + `pwa/`) for API-driven browser orchestration.

The current README content is preserved as canonical operational guidance and reorganized for clarity.

## 🚀 Quick Access

| Goal | Entry point | Primary use |
| --- | --- | --- |
| Run scripted prompts | `agents/sora_agent.py` | Drive composer actions from CLI or wrapper script |
| Fetch generated media | `agents/sora_download.py` | Discover and save candidates locally |
| Remote control | `server/app.py` + `pwa/` | REST/WebSocket + browser dashboard control |

## ✨ Overview

Core design:
- Attach to a persistent Chrome session via DevTools remote debugging (default port `9333`).
- Reuse browser profile state to keep login/session continuity.
- Automate key composer actions (type, plus/media attach, storyboard, settings, create).
- Expose the same actions over REST + WebSocket logs for a local PWA controller.

### Workflow snapshot

| Workflow | Entry point | Primary use |
| --- | --- | --- |
| CLI Agent | `agents/sora_agent.py` | Type prompts, click controls, automate compose flow |
| CLI Downloader | `agents/sora_download.py` | Discover downloadable media and save files locally |
| API + PWA | `server/app.py` + `pwa/` | Remote control and visual orchestration from browser |

## ✅ Features

- Chrome attach/start flow with reusable profile (`--debugger-port`, `--start-chrome`, `--user-data-dir`).
- Safe or forced clicks for key controls (`plus`, `storyboard`, `settings`, `create`, `profile`).
- Prompt typing with selector fallback behavior.
- Media attachment via file path with DataTransfer injection.
- Storyboard scene filling + script updates + storyboard-specific media attach.
- Settings automation for model/orientation/duration/resolution.
- Separate download discovery + fetch flow using browser cookies.
- Tornado REST API and live WebSocket debug stream.
- Installable local PWA with upload, preview, and granular controls.

## 🗂️ Project Structure

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

## 🧩 Prerequisites

- Python 3.10+ (recommended).
- Chrome/Chromium installed and runnable.
- A display for non-headless usage (`--no-headless`) when login or interactive UI is required.
- Sora account access in the attached Chrome profile.

## 📦 Installation

Existing setup flow from the canonical README:

```bash
conda activate agent
pip install -r requirements.txt
```

Dependencies in `requirements.txt`:

| Package | Version spec |
| --- | --- |
| `selenium` | `>=4.17.2` |
| `tornado` | `>=6.4` |
| `Pillow` | `>=9.4.0` |
| `pillow-heif` | `>=0.16.0` |

## 🚀 Usage

### Quick start (CLI agent)

Quick start (opens Sora in a managed browser):

```bash
python agents/sora_agent.py
```

Attach to Chrome with persistent session (recommended for Sora):

```bash
python -m agents.sora_agent --debugger-port 9333 --start-chrome --no-headless --login-timeout 600 --text "A sunset over Tokyo, cinematic."
```

Notes:
- A Chrome window opens on the Sora page. If redirected to login, sign in; the script waits and then types your prompt.
- To reuse the same login, pass a fixed profile path:

```bash
python -m agents.sora_agent --debugger-port 9333 --start-chrome --no-headless --user-data-dir "$HOME/chrome_sora_profile_9333"
```

### Key CLI options (`agents/sora_agent.py`)

- `--url` target page (default: `https://sora.chatgpt.com/explore`).
- `--debugger-port` attach to an existing Chrome started with `--remote-debugging-port=PORT`.
- `--start-chrome` if set with `--debugger-port`, launches Chrome for you (with a `--user-data-dir`).
- `--no-headless` to run a visible browser; needed for login and Cloudflare.
- `--selector` CSS to locate the input (default matches the Sora composer textarea).
- `--text` what to type into the input.
- `--chrome-binary` set a Chrome/Chromium path explicitly.
- `--action` UI actions: `list`, `plus`, `storyboard`, `settings`, `create`, `profile`.
- `--force-click` clicks even if an element appears disabled.
- `--login-timeout` wait window for manual auth completion.

Driver handling:
- The agent removes any stale `chromedriver` from `PATH` before launch.
- Selenium Manager then resolves a matching driver for the installed Chrome automatically.

### CLI examples (UI controls)

List and click common controls:

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action list --action storyboard --action settings --action plus
```

Force-click the Create video button (even if disabled):

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action create --force-click
```

Open profile/settings and navigate manually if needed:

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action list --action profile
```

If `profile` is not detected, the `settings` button typically opens the same menu.

### Downloader flow

Discover and download videos with the handler script:

- Dry-run (list candidates only): `./bin/sora_download.sh --dry-run`
- Download up to 2 files to `./downloads/sora`: `./bin/sora_download.sh --max 2`
- Change output folder: `OUT_DIR=$HOME/Videos/sora ./bin/sora_download.sh --max 1`

Direct module usage is also available via `python -m agents.sora_download ...`.

## 🌐 Control Server + PWA

Run the Tornado server:

```bash
python server/app.py
# listens on http://0.0.0.0:8791 and serves the PWA at /
```

By default the server:
- Reuses Chrome on remote debugging port `9333`.
- Stores uploads in `./uploads` unless `SORA_UPLOADS_DIR` is set.

### Key endpoints

All endpoints operate against the currently attached Chrome (defaults to debugger port `9333`).

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

### PWA controls

Open `http://0.0.0.0:8791` (or your chosen host) after starting `server/app.py`.

Highlights from existing implementation:
- Upload media via file picker or by pasting a path, then click **Plus** to attach without re-opening system file dialogs.
- Apply media description in the dedicated “Media description” box.
- Independent controls for **Set Model**, **Set Orientation**, **Set Duration**, **Set Resolution**, and script updates.
- Storyboard controls for scenes, script updates, storyboard panel open, and attach current storyboard path.
- Live debug log showing API calls and Sora-returned values (for example selected model/duration).

## ⚙️ Configuration

### Environment variables

`server/app.py` reads:
- `SORA_DEBUGGER_PORT` (default `9333`)
- `SORA_USER_DATA_DIR` (default `~/chrome_sora_profile_<port>`)
- `SORA_DISPLAY` (optional X display)
- `SORA_API_PORT` (default `8791`)
- `SORA_URL` (default `https://sora.chatgpt.com/explore`)
- `SORA_UPLOADS_DIR` (optional upload directory override)

`agents/sora_agent.py` also supports:
- `CHROME_BINARY` (if `--chrome-binary` is not provided)

Wrapper scripts support:
- `PORT`, `SORA_PROFILE_DIR`, `TIMEOUT`, `LOGIN_TIMEOUT` (`bin/sora_type.sh`)
- `PORT`, `SORA_PROFILE_DIR`, `OUT_DIR` (`bin/sora_download.sh`)

## 🧪 Examples

### End-to-end API example (curl)

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

### Media upload + attach via API

```bash
# Upload file and get server path
curl -s -X POST http://127.0.0.1:8791/api/upload -F 'file=@/absolute/path/to/input.jpg'

# Then attach using returned path
curl -s -X POST http://127.0.0.1:8791/api/attach \
  -H 'Content-Type: application/json' \
  -d '{"path":"/absolute/or/server-returned/path.jpg","click_plus":false}'
```

## 🛠️ Development Notes

- There is currently no packaged module (`pyproject.toml`/`setup.py` not present).
- There is currently no CI/test/lint pipeline in this repository snapshot.
- `selenium_template` is a symlink to `../auto-publish/`; its target content is outside this repo.
- PWA manifest references `/icons/icon-192.png` and `/icons/icon-512.png`; icon assets are not currently tracked in this repository.

## 🧯 Troubleshooting

- Chrome fails to attach:
  - Ensure Chrome was started with `--remote-debugging-port=9333` (or matching `--debugger-port`).
  - Check `GET /api/status` for `devtools_ready: true`.
- Repeated login prompts:
  - Use a persistent `--user-data-dir` and avoid random profile paths.
- Cloudflare/login flow not progressing:
  - Run non-headless (`--no-headless`) and increase `--login-timeout`.
- Media attach does nothing:
  - Confirm file path exists on the server machine and use `/api/upload` + returned path if unsure.
- Storyboard media attach fails:
  - Try `POST /api/storyboard-attach-only` or open storyboard first, then `/api/storyboard-media`.
- Resolution control unavailable in PWA:
  - `High` resolution is only enabled when model is `Sora 2 Pro`.
- Wrong chromedriver issues:
  - Remove manually pinned chromedriver from your shell profile; this project intentionally lets Selenium Manager choose matching versions.

## 🧭 Roadmap

Planned/likely next improvements:
- Add automated tests for selector stability and API handlers.
- Add lint/format tooling and CI workflows.
- Add tracked PWA icon assets and stronger offline caching strategy.
- Add formal multilingual README files under `i18n/`.
- Add packaging metadata for easier installation.

## 🤝 Contributing

Contributions are welcome.

Suggested process:
1. Fork and create a feature branch.
2. Keep changes scoped and include reproduction/usage notes for UI automation changes.
3. Validate flows manually with a real attached Chrome session.
4. Open a PR with before/after behavior details.

If you change selectors or interaction logic, include concrete Sora UI context so regressions are easier to triage.

## 🙏 Acknowledgements

- Selenium and Selenium Manager for browser automation and driver resolution.
- Tornado for the lightweight async HTTP/WebSocket control service.
- Pillow and `pillow-heif` for local image conversion/preview support.

## 🧱 Known Good Build

If you need a stable baseline that guarantees storyboard media attachment works end-to-end (including the Open Storyboard / Attach Current Path buttons and the combined Apply flow), check out commit:

`c6683ed6d9ee0ac110536352867a26a966e3e275`

## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |

## 📄 License

No license file is currently present in this repository snapshot (checked in this draft on **February 28, 2026**).

Assumption: all rights remain with the repository owner until a license is added. If this is not intended, add a `LICENSE` file and update this section.
