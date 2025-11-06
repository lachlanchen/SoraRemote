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

## Control server + PWA

Run the Tornado server to expose a REST API and the web controller:

```
python server/app.py
# -> listens on http://0.0.0.0:8791 and serves the PWA at /
```

### Key endpoints

All endpoints operate against the currently attached Chrome (defaults to debugger port `9333`).

- `POST /api/open` `{ url? }`
  - Navigates the attached Chrome tab to the given URL (defaults to Sora Explore).
- `POST /api/attach` `{ path, click_plus? }`
  - Uploads media. Uses DataTransfer injection and clears existing media automatically. `click_plus` defaults to `false` to avoid launching the OS file picker.
- `POST /api/describe` `{ text }`
  - Fills the “Optionally describe your video…” textarea beside the media preview.
- `POST /api/script-updates` `{ text }`
  - Fills the “Describe updates to your script…” composer field.
- `POST /api/storyboard` `{ scenes: ["scene 1", ...], script_updates?: "..." }`
  - Opens the storyboard, fills each scene textarea, and optionally updates the “Describe updates to your script…” field in the storyboard panel.
- `POST /api/storyboard-media` `{ path }`
  - Attaches media to the storyboard-specific plus button (the floating uploader inside the storyboard panel).
- `POST /api/settings` `{ model?, orientation?, duration?, resolution? }`
  - Opens the composer settings menu and selects the requested option(s). Each field is optional and can be sent one at a time. The response echoes the label Sora actually selected.

Use `GET /api/actions` to inspect the current button state (enabled/disabled/displayed) and `POST /api/click` with `{ key: "plus" | "storyboard" | "settings" | "create" | "profile" }` for direct button presses.

### PWA controls

Open `http://0.0.0.0:8791` (or your chosen host) after starting `server/app.py`.

Highlights:

- Upload media via the file picker or by pasting a path, then click **Plus** to send it to Sora without reopening the system file dialog.
- Apply a media description in the “Media description” box — the textarea mirrors the one in the composer.
- Independent buttons for **Set Model**, **Set Orientation**, **Set Duration**, **Set Resolution**, and **Apply Script Updates** make it easy to test controls one at a time. The server uses in-page JavaScript to select the exact radio option and textarea, so no accidental “three dots” menu clicks.
- The live debug log shows every API call and the values returned from Sora (e.g., the selected model or duration).

By default the server reuses Chrome on `--remote-debugging-port 9333` and keeps uploads in `./uploads` unless `SORA_UPLOADS_DIR` is set.
