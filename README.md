**Selenium Agent (Sora Example)**

- Activate conda env: `conda activate agent`
- Install deps: `pip install -r requirements.txt`

Quick start (opens Sora in a managed browser):
- `python agents/sora_agent.py`

Attach to Chrome with persistent session (recommended for Sora):
- Start and attach using remote debugging on port 9333, open visible Chrome, and wait for login:
  `python -m agents.sora_agent --debugger-port 9333 --start-chrome --no-headless --login-timeout 600 --text "A sunset over Tokyo, cinematic."`
  - A Chrome window opens on the Sora page. If you are redirected to login, sign in; the script waits and then types your prompt.
  - To reuse the same login, pass a fixed profile path: `--user-data-dir "$HOME/chrome_sora_profile_9333"` (created automatically on first run).

Key options:
- `--url` target page (default: `https://sora.chatgpt.com/explore`).
- `--debugger-port` attach to an existing Chrome started with `--remote-debugging-port=PORT`.
- `--start-chrome` if set with `--debugger-port`, launches Chrome for you (with a `--user-data-dir`).
- `--no-headless` to run a visible browser; needed for login and Cloudflare.
- `--selector` CSS to locate the input (default matches the Sora composer textarea).
- `--text` what to type into the input.
- `--chrome-binary` set a Chrome/Chromium path explicitly.
- `--action` UI actions: `list`, `plus`, `storyboard`, `settings`, `create`. You can pass multiple `--action` flags to list and/or click these buttons. Use `--force-click` to click disabled buttons.

Driver handling:

Examples (UI controls):
- List and click common controls:
  `python -m agents.sora_agent --debugger-port 9333 --no-headless --action list --action storyboard --action settings --action plus`
- Force-click the Create video button (even if disabled):
  `python -m agents.sora_agent --debugger-port 9333 --no-headless --action create --force-click`

Downloads and profile
- Open profile/settings and navigate manually if needed:
  `python -m agents.sora_agent --debugger-port 9333 --no-headless --action list --action profile`
  (If `profile` is not detected, the `settings` button typically opens the same menu.)
- Discover and download videos with a separate handler:
  - Dry-run (list candidates only): `./bin/sora_download.sh --dry-run`
  - Download up to 2 files to `./downloads/sora`: `./bin/sora_download.sh --max 2`
  - Change output folder: `OUT_DIR=$HOME/Videos/sora ./bin/sora_download.sh --max 1`
- The agent removes any stale `chromedriver` from PATH before launching, letting Selenium Manager download a matching driver for your installed Chrome automatically.
