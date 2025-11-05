import asyncio
import sys
import io
import base64
import json
import os
import signal
from typing import Any, Dict, List, Optional

import tornado.ioloop
import tornado.web
import tornado.websocket

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from agents.sora_agent import (
    build_chrome_attached,
    start_chrome_with_debug,
    wait_for_devtools,
    devtools_ready,
    wait_for_page_loaded,
    wait_for_quiet_resources,
    wait_for_selector_visible,
    type_into_selector,
    find_page_controls,
    element_disabled_state,
    click_safely,
    attach_media_by_path,
    fill_storyboard,
    apply_settings,
)

# Optional image preview support (HEIC/HEIF)
try:
    import pillow_heif  # type: ignore
    pillow_heif.register_heif_opener()
except Exception:
    pillow_heif = None
try:
    from PIL import Image  # type: ignore
except Exception:
    Image = None


# Config via env
DEBUGGER_PORT = int(os.environ.get("SORA_DEBUGGER_PORT", "9333"))
USER_DATA_DIR = os.environ.get("SORA_USER_DATA_DIR", os.path.expanduser(f"~/chrome_sora_profile_{DEBUGGER_PORT}"))
DISPLAY = os.environ.get("SORA_DISPLAY", None)
LISTEN_PORT = int(os.environ.get("SORA_API_PORT", "8791"))
DEFAULT_URL = os.environ.get("SORA_URL", "https://sora.chatgpt.com/explore")
UPLOADS_DIR = os.environ.get("SORA_UPLOADS_DIR")  # Optional override (e.g., $HOME/Downloads)


# Simple broadcast hub for live logs to PWA
class LogHub:
    def __init__(self):
        self._clients: List[tornado.websocket.WebSocketHandler] = []

    def add(self, client: tornado.websocket.WebSocketHandler):
        self._clients.append(client)

    def remove(self, client: tornado.websocket.WebSocketHandler):
        try:
            self._clients.remove(client)
        except ValueError:
            pass

    async def emit(self, event: str, data: Dict[str, Any]):
        msg = json.dumps({"event": event, "data": data})
        dead = []
        for c in self._clients:
            try:
                await c.write_message(msg)
            except Exception:
                dead.append(c)
        for d in dead:
            self.remove(d)


HUB = LogHub()
ACTION_LOCK = asyncio.Lock()


class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "content-type")

    def options(self, *args, **kwargs):
        self.set_status(204)
        self.finish()


class StatusHandler(BaseHandler):
    async def get(self):
        ready = devtools_ready(DEBUGGER_PORT)
        await HUB.emit("status", {"ready": ready})
        self.write(json.dumps({"ok": True, "devtools_ready": ready, "port": DEBUGGER_PORT}))


async def _ensure_chrome_open(url: str) -> None:
    if not devtools_ready(DEBUGGER_PORT):
        _ = start_chrome_with_debug(
            port=DEBUGGER_PORT,
            url=url,
            user_data_dir=USER_DATA_DIR,
            chrome_binary=None,
            display=DISPLAY,
        )
        ok = await asyncio.get_event_loop().run_in_executor(None, wait_for_devtools, DEBUGGER_PORT, 30)  # type: ignore[arg-type]
        if not ok:
            raise RuntimeError("DevTools endpoint not ready; Chrome may have failed to start.")


class OpenHandler(BaseHandler):
    async def post(self):
        body = json.loads(self.request.body or b"{}")
        url = body.get("url") or DEFAULT_URL
        await HUB.emit("open", {"url": url})
        async with ACTION_LOCK:
            await _ensure_chrome_open(url)
            # Drive navigation
            def _open():
                with build_chrome_attached(DEBUGGER_PORT, chrome_binary=None) as d:
                    d.get(url)
                    wait_for_page_loaded(d, timeout=30)
                    try:
                        wait_for_quiet_resources(d, stable_secs=1.5, timeout=30)
                    except Exception:
                        pass
            await asyncio.get_event_loop().run_in_executor(None, _open)
        self.write(json.dumps({"ok": True, "url": url}))


class ActionsHandler(BaseHandler):
    async def get(self):
        async with ACTION_LOCK:
            await _ensure_chrome_open(DEFAULT_URL)
            def _list():
                with build_chrome_attached(DEBUGGER_PORT, chrome_binary=None) as d:
                    ctrls = find_page_controls(d, timeout=10)
                    out: Dict[str, Any] = {}
                    for k, el in ctrls.items():
                        if el is None:
                            out[k] = None
                        else:
                            st = element_disabled_state(el)
                            out[k] = st
                    return out
            result = await asyncio.get_event_loop().run_in_executor(None, _list)
        await HUB.emit("actions", result)
        self.write(json.dumps({"ok": True, "actions": result}))


class ClickHandler(BaseHandler):
    async def post(self):
        body = json.loads(self.request.body or b"{}")
        key = body.get("key")
        force = bool(body.get("force"))
        if key not in {"plus", "storyboard", "settings", "create", "profile"}:
            self.set_status(400)
            return self.finish(json.dumps({"ok": False, "error": "invalid key"}))
        await HUB.emit("click", {"key": key, "force": force})
        async with ACTION_LOCK:
            await _ensure_chrome_open(DEFAULT_URL)
            def _click():
                with build_chrome_attached(DEBUGGER_PORT, chrome_binary=None) as d:
                    ctrls = find_page_controls(d, timeout=10)
                    el = ctrls.get(key)
                    ok = click_safely(d, el, force=force)
                    return bool(ok)
            ok = await asyncio.get_event_loop().run_in_executor(None, _click)
        self.write(json.dumps({"ok": ok, "key": key}))


class TypeHandler(BaseHandler):
    async def post(self):
        body = json.loads(self.request.body or b"{}")
        text = body.get("text") or ""
        selector = body.get("selector") or 'textarea[placeholder="Describe your video..."]'
        open_url = body.get("url") or DEFAULT_URL
        await HUB.emit("type", {"selector": selector, "len": len(text)})
        async with ACTION_LOCK:
            await _ensure_chrome_open(open_url)
            def _type():
                with build_chrome_attached(DEBUGGER_PORT, chrome_binary=None) as d:
                    d.get(open_url)
                    wait_for_page_loaded(d, timeout=30)
                    try:
                        wait_for_quiet_resources(d, stable_secs=1.5, timeout=30)
                    except Exception:
                        pass
                    wait_for_selector_visible(d, selector, timeout=30)
                    type_into_selector(d, selector, text, timeout=30)
                    return True
            ok = await asyncio.get_event_loop().run_in_executor(None, _type)
        self.write(json.dumps({"ok": ok}))


class ComposeHandler(BaseHandler):
    async def post(self):
        body = json.loads(self.request.body or b"{}")
        text = body.get("text") or ""
        click_create = bool(body.get("click_create", False))
        selector = 'textarea[placeholder="Describe your video..."]'
        await HUB.emit("compose", {"click_create": click_create, "len": len(text)})
        async with ACTION_LOCK:
            await _ensure_chrome_open(DEFAULT_URL)
            def _compose():
                with build_chrome_attached(DEBUGGER_PORT, chrome_binary=None) as d:
                    d.get(DEFAULT_URL)
                    wait_for_page_loaded(d, timeout=30)
                    try:
                        wait_for_quiet_resources(d, stable_secs=1.5, timeout=30)
                    except Exception:
                        pass
                    type_into_selector(d, selector, text, timeout=30)
                    if click_create:
                        ctrls = find_page_controls(d, timeout=10)
                        _ = click_safely(d, ctrls.get("create"), force=False)
                    return True
            ok = await asyncio.get_event_loop().run_in_executor(None, _compose)
        self.write(json.dumps({"ok": ok}))


class AttachHandler(BaseHandler):
    async def post(self):
        body = json.loads(self.request.body or b"{}")
        path = body.get("path")
        click_plus = bool(body.get("click_plus", True))
        if not path:
            self.set_status(400)
            return self.finish(json.dumps({"ok": False, "error": "path required"}))
        await HUB.emit("attach", {"path": path, "click_plus": click_plus})
        async with ACTION_LOCK:
            await _ensure_chrome_open(DEFAULT_URL)
            def _attach():
                with build_chrome_attached(DEBUGGER_PORT, chrome_binary=None) as d:
                    try:
                        current = d.current_url or ""
                    except Exception:
                        current = ""
                    normalized_current = current.rstrip("/")
                    normalized_target = DEFAULT_URL.rstrip("/")
                    if not normalized_current.startswith(normalized_target):
                        d.get(DEFAULT_URL)
                    wait_for_page_loaded(d, timeout=30)
                    try:
                        wait_for_quiet_resources(d, stable_secs=1.0, timeout=20)
                    except Exception:
                        pass
                    return attach_media_by_path(d, path, click_plus=click_plus, timeout=20)
            ok = await asyncio.get_event_loop().run_in_executor(None, _attach)
        await HUB.emit("attach_result", {"ok": bool(ok)})
        self.write(json.dumps({"ok": bool(ok)}))


class StoryboardHandler(BaseHandler):
    async def post(self):
        body = json.loads(self.request.body or b"{}")
        scenes = body.get("scenes") or []
        if not isinstance(scenes, list):
            self.set_status(400)
            return self.finish(json.dumps({"ok": False, "error": "scenes must be a list"}))
        await HUB.emit("storyboard", {"count": len(scenes)})
        async with ACTION_LOCK:
            await _ensure_chrome_open(DEFAULT_URL)
            def _fill():
                with build_chrome_attached(DEBUGGER_PORT, chrome_binary=None) as d:
                    d.get(DEFAULT_URL)
                    wait_for_page_loaded(d, timeout=30)
                    try:
                        wait_for_quiet_resources(d, stable_secs=1.0, timeout=20)
                    except Exception:
                        pass
                    return fill_storyboard(d, scenes, ensure_storyboard=True, timeout=30)
            filled = await asyncio.get_event_loop().run_in_executor(None, _fill)
        self.write(json.dumps({"ok": True, "filled": int(filled)}))


class SettingsHandler(BaseHandler):
    async def post(self):
        body = json.loads(self.request.body or b"{}")
        orientation = body.get("orientation")
        duration = body.get("duration")
        model = body.get("model")
        await HUB.emit("settings", {"orientation": orientation, "duration": duration})
        async with ACTION_LOCK:
            await _ensure_chrome_open(DEFAULT_URL)
            def _apply():
                with build_chrome_attached(DEBUGGER_PORT, chrome_binary=None) as d:
                    d.get(DEFAULT_URL)
                    wait_for_page_loaded(d, timeout=30)
                    try:
                        wait_for_quiet_resources(d, stable_secs=1.0, timeout=20)
                    except Exception:
                        pass
                    return apply_settings(d, orientation=orientation, duration=duration, model=model, timeout=20)
            res = await asyncio.get_event_loop().run_in_executor(None, _apply)
        self.write(json.dumps({"ok": True, "applied": res}))


class WSLogs(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin: str) -> bool:
        return True

    def open(self):
        HUB.add(self)

    def on_close(self):
        HUB.remove(self)


class UploadHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "POST,OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "content-type")

    def options(self, *args, **kwargs):
        self.set_status(204)
        self.finish()

    def post(self):
        if UPLOADS_DIR:
            upload_dir = os.path.expanduser(UPLOADS_DIR)
        else:
            upload_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        saved = []
        try:
            for field, files in (self.request.files or {}).items():
                for f in files:
                    filename = f.get('filename') or 'upload.bin'
                    # Simple unique name
                    base, ext = os.path.splitext(filename)
                    out = os.path.join(upload_dir, f"{base}_{int(tornado.ioloop.IOLoop.current().time()*1000)}{ext}")
                    with open(out, 'wb') as w:
                        w.write(f['body'])
                    saved.append(out)
        except Exception as e:
            self.set_status(500)
            return self.finish(json.dumps({"ok": False, "error": str(e)}))
        self.set_header("Content-Type", "application/json")
        self.finish(json.dumps({"ok": True, "paths": saved}))


class PreviewHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "POST,OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "content-type")

    def options(self, *args, **kwargs):
        self.set_status(204)
        self.finish()

    def post(self):
        if Image is None:
            self.set_status(500)
            return self.finish(json.dumps({"ok": False, "error": "Pillow not installed"}))
        files = (self.request.files or {}).get('file') or []
        if not files:
            self.set_status(400)
            return self.finish(json.dumps({"ok": False, "error": "file required"}))
        f = files[0]
        body = f.get('body') or b''
        try:
            im = Image.open(io.BytesIO(body))
            # Convert to RGB if needed
            if im.mode not in ('RGB', 'RGBA'):
                im = im.convert('RGB')
            # Downsize for preview
            im.thumbnail((1024, 1024))
            out = io.BytesIO()
            im.save(out, format='PNG', optimize=True)
            b64 = base64.b64encode(out.getvalue()).decode('ascii')
            data_url = f"data:image/png;base64,{b64}"
            self.set_header("Content-Type", "application/json")
            return self.finish(json.dumps({"ok": True, "data_url": data_url}))
        except Exception as e:
            self.set_status(500)
            return self.finish(json.dumps({"ok": False, "error": str(e)}))


class SPAHandler(tornado.web.StaticFileHandler):
    def parse_url_path(self, url_path: str) -> str:
        if not url_path or url_path == "/":
            return "index.html"
        return url_path


def make_app() -> tornado.web.Application:
    cwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pwa_root = os.path.join(cwd, "pwa")
    os.makedirs(pwa_root, exist_ok=True)
    routes = [
        (r"/api/status", StatusHandler),
        (r"/api/open", OpenHandler),
        (r"/api/actions", ActionsHandler),
        (r"/api/click", ClickHandler),
        (r"/api/type", TypeHandler),
        (r"/api/attach", AttachHandler),
        (r"/api/storyboard", StoryboardHandler),
        (r"/api/settings", SettingsHandler),
        (r"/api/compose", ComposeHandler),
        (r"/api/upload", UploadHandler),
        (r"/api/preview", PreviewHandler),
        (r"/ws", WSLogs),
        (r"/(.*)", SPAHandler, {"path": pwa_root, "default_filename": "index.html"}),
    ]
    return tornado.web.Application(routes, debug=True)


def main():
    app = make_app()
    app.listen(LISTEN_PORT, address="0.0.0.0")
    print(f"Sora control server listening on http://0.0.0.0:{LISTEN_PORT}")
    print(f"PWA available at / (connects to this server)")
    loop = tornado.ioloop.IOLoop.current()

    def _sigterm(*_):
        print("Shutting down...")
        loop.stop()

    signal.signal(signal.SIGTERM, _sigterm)
    signal.signal(signal.SIGINT, _sigterm)
    loop.start()


if __name__ == "__main__":
    main()
