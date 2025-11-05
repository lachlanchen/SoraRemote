import asyncio
import sys
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
)


# Config via env
DEBUGGER_PORT = int(os.environ.get("SORA_DEBUGGER_PORT", "9333"))
USER_DATA_DIR = os.environ.get("SORA_USER_DATA_DIR", os.path.expanduser(f"~/chrome_sora_profile_{DEBUGGER_PORT}"))
DISPLAY = os.environ.get("SORA_DISPLAY", None)
LISTEN_PORT = int(os.environ.get("SORA_API_PORT", "8791"))
DEFAULT_URL = os.environ.get("SORA_URL", "https://sora.chatgpt.com/explore")


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


class WSLogs(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin: str) -> bool:
        return True

    def open(self):
        HUB.add(self)

    def on_close(self):
        HUB.remove(self)


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
        (r"/api/compose", ComposeHandler),
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
