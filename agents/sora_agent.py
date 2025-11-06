import argparse
import os
import sys
import time
import json
import subprocess
import shutil
import base64
import mimetypes
import re
import urllib.request
import urllib.error
from contextlib import contextmanager

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from typing import List, Tuple

try:
    import pillow_heif  # type: ignore
    pillow_heif.register_heif_opener()
except Exception:
    pillow_heif = None
try:
    from PIL import Image  # type: ignore
except Exception:
    Image = None


def _strip_conflicting_chromedriver_from_path() -> None:
    """
    Remove any PATH entries that contain a 'chromedriver' binary to avoid
    Selenium picking an incompatible driver from PATH. This lets Selenium Manager
    resolve and download a matching driver instead.
    """
    path_env = os.environ.get("PATH", "")
    if not path_env:
        return
    parts = path_env.split(os.pathsep)
    kept: list[str] = []
    for p in parts:
        try:
            if os.path.isfile(os.path.join(p, "chromedriver")) or os.path.isfile(os.path.join(p, "chromedriver.exe")):
                # Skip this PATH entry
                continue
        except Exception:
            # If anything odd, keep the entry
            pass
        kept.append(p)
    os.environ["PATH"] = os.pathsep.join(kept)

@contextmanager
def build_chrome(headless: bool = False, chrome_binary: str | None = None):
    """
    Create a Chrome WebDriver using Selenium Manager (no manual driver needed).
    - Defaults to headless when no DISPLAY is available.
    - Closes the driver on exit.
    """
    options = ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1600,1000")

    # Allow overriding Chrome/Chromium binary via arg/env.
    if chrome_binary:
        options.binary_location = chrome_binary
    elif os.environ.get("CHROME_BINARY"):
        options.binary_location = os.environ["CHROME_BINARY"]

    # Ensure PATH doesn't force an incompatible chromedriver
    _strip_conflicting_chromedriver_from_path()

    # Rely on Selenium Manager to fetch the right driver
    try:
        options.set_capability('strictFileInteractability', False)
    except Exception:
        pass
    driver = webdriver.Chrome(options=options)
    try:
        yield driver
    finally:
        try:
            driver.quit()
        except Exception:
            pass


@contextmanager
def build_chrome_attached(debugger_port: int, chrome_binary: str | None = None):
    """
    Attach to an existing Chrome instance via --remote-debugging-port.
    Relies on Selenium Manager to pick a matching ChromeDriver.
    """
    options = ChromeOptions()
    if chrome_binary:
        options.binary_location = chrome_binary
    elif os.environ.get("CHROME_BINARY"):
        options.binary_location = os.environ["CHROME_BINARY"]

    options.add_experimental_option("debuggerAddress", f"127.0.0.1:{debugger_port}")

    _strip_conflicting_chromedriver_from_path()

    try:
        options.set_capability('strictFileInteractability', False)
    except Exception:
        pass
    driver = webdriver.Chrome(options=options)
    try:
        yield driver
    finally:
        try:
            driver.quit()
        except Exception:
            pass


def _http_get(url: str, timeout: float = 2.0) -> tuple[int, bytes]:
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return resp.getcode(), resp.read()
    except urllib.error.URLError:
        return 0, b""
    except Exception:
        return 0, b""


def devtools_ready(port: int) -> bool:
    code, body = _http_get(f"http://127.0.0.1:{port}/json/version", timeout=1.5)
    if code != 200:
        return False
    try:
        data = json.loads(body.decode("utf-8", errors="ignore"))
        return bool(data.get("Browser"))
    except Exception:
        return False


def wait_for_devtools(port: int, timeout: int = 20) -> bool:
    start = time.time()
    while time.time() - start < timeout:
        if devtools_ready(port):
            return True
        time.sleep(0.5)
    return False


def resolve_chrome_binary(explicit: str | None) -> str | None:
    if explicit and os.path.exists(explicit):
        return explicit
    if os.environ.get("CHROME_BINARY") and os.path.exists(os.environ["CHROME_BINARY"]):
        return os.environ["CHROME_BINARY"]
    for name in ("google-chrome", "google-chrome-stable", "chromium-browser", "chromium"):
        path = shutil.which(name)
        if path:
            return path
    return None


def start_chrome_with_debug(port: int, url: str, user_data_dir: str | None, chrome_binary: str | None, display: str | None = None) -> subprocess.Popen:
    binary = resolve_chrome_binary(chrome_binary)
    if not binary:
        raise RuntimeError("Could not find Chrome/Chromium binary. Set --chrome-binary or CHROME_BINARY.")

    if not user_data_dir:
        user_data_dir = os.path.join(os.path.expanduser("~"), f"chrome_sora_profile_{port}")
    os.makedirs(user_data_dir, exist_ok=True)

    cmd = [
        binary,
        f"--remote-debugging-port={port}",
        f"--user-data-dir={user_data_dir}",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-popup-blocking",
        url,
    ]

    env = os.environ.copy()
    if display:
        env["DISPLAY"] = display

    # Start visible Chrome; let calling code wait for devtools
    return subprocess.Popen(cmd, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def wait_for_page_loaded(driver, timeout: int = 30):
    """Wait for document.readyState === 'complete'."""
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )


def wait_for_quiet_resources(driver, stable_secs: float = 1.5, timeout: int = 30) -> bool:
    """Wait until no new performance resource entries appear for stable_secs.
    Avoids navigating while the SPA is still hydrating.
    """
    start = time.time()
    last_len = -1
    stable_for = 0.0
    while time.time() - start < timeout:
        try:
            curr_len = driver.execute_script(
                "return performance.getEntriesByType('resource').length;"
            )
        except Exception:
            curr_len = None

        if curr_len is not None and curr_len == last_len:
            time.sleep(0.25)
            stable_for += 0.25
            if stable_for >= stable_secs:
                return True
        else:
            last_len = curr_len
            stable_for = 0.0
            time.sleep(0.25)
    return False


def wait_for_selector_visible(driver, selector: str, timeout: int = 30):
    """Wait until the selector resolves to a displayed element with size."""
    def _visible(d):
        try:
            el = d.find_element(By.CSS_SELECTOR, selector)
            if not el.is_displayed():
                return False
            rect = d.execute_script(
                "const r=arguments[0].getBoundingClientRect(); return {w:r.width,h:r.height};",
                el,
            )
            return rect and rect.get("w", 0) > 0 and rect.get("h", 0) > 0
        except Exception:
            return False

    WebDriverWait(driver, timeout).until(_visible)


def wait_for_xpath_clickable(driver, xpath: str, timeout: int = 30):
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )


def find_page_controls(driver, timeout: int = 10):
    """Discover key controls on the Sora page and return them.

    Returns a mapping with optional WebElements:
      - plus: media attach button
      - storyboard: storyboard button
      - settings: settings gear button
      - create: create video button (may be disabled)
      - profile: user profile/account button (best-effort)
    """
    controls: dict[str, object] = {"plus": None, "storyboard": None, "settings": None, "create": None, "profile": None}

    x_plus = "//button[.//span[contains(@class,'sr-only') and normalize-space()='Attach media']]"
    x_story = "//button[normalize-space()='Storyboard']"
    x_settings = "//button[@aria-label='Settings' and (.//span[contains(normalize-space(),'Sora') or contains(normalize-space(),'Pro') or contains(normalize-space(),'Model')])]"
    x_create = "//button[.//span[contains(@class,'sr-only') and normalize-space()='Create video']]"
    # Multiple fallbacks for profile control
    x_profile_variants = [
        "//button[@aria-label='Profile']",
        "//button[contains(@aria-label,'account') or contains(@aria-label,'Account')]",
        "//button[.//img[contains(@alt,'avatar') or contains(@src,'avatar')]]",
        "//img[contains(@alt,'avatar') or contains(@src,'avatar')]/ancestor::button[1]",
    ]

    for key, xp in (("plus", x_plus), ("storyboard", x_story), ("settings", x_settings), ("create", x_create)):
        try:
            el = driver.find_element(By.XPATH, xp)
            controls[key] = el
        except Exception:
            controls[key] = None

    # Resolve profile via first matching variant
    for xp in x_profile_variants:
        try:
            controls["profile"] = driver.find_element(By.XPATH, xp)
            break
        except Exception:
            continue

    return controls


def element_disabled_state(el) -> dict:
    state = {}
    try:
        state["disabled"] = el.get_attribute("disabled") is not None
    except Exception:
        state["disabled"] = False
    for attr in ("aria-disabled", "data-disabled"):
        try:
            val = el.get_attribute(attr)
        except Exception:
            val = None
        state[attr] = val
    try:
        state["displayed"] = el.is_displayed()
    except Exception:
        state["displayed"] = False
    return state


def click_safely(driver, el, force: bool = False) -> bool:
    if el is None:
        return False
    try:
        driver.execute_script("arguments[0].scrollIntoView({block:'center',inline:'center'});", el)
    except Exception:
        pass
    st = element_disabled_state(el)
    if (st.get("disabled") or st.get("aria-disabled") == "true" or st.get("data-disabled") == "true") and not force:
        print("Button appears disabled; skipping click (use --force-click to override).")
        return False
    try:
        el.click()
        return True
    except Exception:
        try:
            driver.execute_script("arguments[0].click();", el)
            return True
        except Exception:
            return False


def find_file_inputs(driver):
    try:
        return driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
    except Exception:
        return []


def list_file_inputs_with_meta(driver) -> List[Tuple[object, bool, str]]:
    metas: List[Tuple[object, bool, str]] = []
    for el in find_file_inputs(driver):
        try:
            disabled = el.get_attribute("disabled") is not None
        except Exception:
            disabled = False
        try:
            accept = el.get_attribute("accept") or ""
        except Exception:
            accept = ""
        metas.append((el, disabled, accept))
    return metas


def reveal_input_file(driver, el):
    try:
        driver.execute_script(
            "arguments[0].style.display='block'; arguments[0].style.visibility='visible'; arguments[0].removeAttribute('hidden');",
            el,
        )
    except Exception:
        pass


def _accept_allows_path(accept: str, path: str) -> bool:
    if not accept:
        return True
    ext = os.path.splitext(path)[1].lower().lstrip('.')
    mime_map = {
        'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'png': 'image/png', 'webp': 'image/webp',
        'heic': 'image/heic', 'heif': 'image/heif', 'avif': 'image/avif',
        'mp4': 'video/mp4', 'webm': 'video/webm', 'mov': 'video/quicktime', 'qt': 'video/quicktime'
    }
    file_mime = mime_map.get(ext, '')
    parts = [p.strip().lower() for p in accept.split(',') if p.strip()]
    if not parts:
        return True
    if file_mime and file_mime in parts:
        return True
    if any(p.startswith('image/') for p in parts) and ext in ('jpg','jpeg','png','webp','heic','heif','avif'):
        return True
    if any(p.startswith('video/') for p in parts) and ext in ('mp4','webm','mov','qt'):
        return True
    return any(ext and ext in p for p in parts)


def _convert_image_if_needed(path: str, accept: str) -> str:
    try:
        if _accept_allows_path(accept, path):
            return path
        if Image is None:
            return path
        # Choose best format based on accept list
        parts = [p.strip().lower() for p in accept.split(',') if p.strip()]
        fmt, out_ext = ('PNG', 'png')
        if 'image/jpeg' in parts:
            fmt, out_ext = ('JPEG', 'jpg')
        im = Image.open(path)
        if im.mode not in ('RGB', 'RGBA'):
            im = im.convert('RGB')
        out_dir = os.path.join(os.getcwd(), 'uploads', 'converted')
        os.makedirs(out_dir, exist_ok=True)
        base = os.path.splitext(os.path.basename(path))[0]
        out_path = os.path.join(out_dir, f"{base}_converted.{out_ext}")
        im.save(out_path, format=fmt, optimize=True)
        return out_path
    except Exception:
        return path


def attach_media_by_path(driver, path: str, click_plus: bool = True, timeout: int = 20, clear_before: bool = True) -> bool:
    if not os.path.isabs(path):
        # Normalize to absolute path within server
        path = os.path.abspath(path)
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    if clear_before:
        try:
            rem = driver.find_element(By.XPATH, "//button[.//span[contains(@class,'sr-only') and normalize-space()='Remove media']]")
            try:
                rem.click()
            except Exception:
                driver.execute_script("arguments[0].click();", rem)
            # Wait briefly for input to re-enable
            time.sleep(0.6)
        except Exception:
            pass

    ctrls = find_page_controls(driver, timeout=10)
    plus_el = ctrls.get("plus")
    if click_plus and plus_el is not None:
        _ = click_safely(driver, plus_el, force=False)
        time.sleep(0.5)

    # Wait for an enabled input[type=file] whose accept matches the file
    end = time.time() + timeout
    target = None
    accept = ""
    while time.time() < end and target is None:
        # If we know the plus button, try the first following input near it
        if plus_el is not None:
            try:
                near = driver.find_element(By.XPATH, "//button[.//span[contains(@class,'sr-only') and normalize-space()='Attach media']]/following::input[@type='file'][1]")
                if near.get_attribute('disabled') is None:
                    acc = (near.get_attribute('accept') or '').strip()
                    if not acc or _accept_allows_path(acc, path):
                        target, accept = near, acc
                        break
            except Exception:
                pass

        metas = list_file_inputs_with_meta(driver)
        # Prefer inputs with accept that explicitly allow the file
        candidates: List[Tuple[object, str]] = []
        fallbacks: List[Tuple[object, str]] = []
        for el, disabled, acc in metas:
            if disabled:
                continue
            a = acc or ""
            if a:
                if _accept_allows_path(a, path):
                    candidates.append((el, a))
            else:
                # Inputs without accept can work but may be decoys
                fallbacks.append((el, a))
        if candidates:
            target, accept = candidates[0]
            break
        if fallbacks:
            target, accept = fallbacks[0]
            break
        time.sleep(0.2)

    if target is None:
        # Try a generic injection off-screen (won't flash in UI)
        try:
            driver.execute_script(
                "var i=document.createElement('input');"
                "i.type='file'; i.id='sora_injected_file';"
                "i.setAttribute('tabindex','-1'); i.setAttribute('aria-hidden','true');"
                "i.style.position='fixed'; i.style.left='-10000px'; i.style.top='-10000px';"
                "i.style.width='1px'; i.style.height='1px'; i.style.opacity='0';"
                "i.style.pointerEvents='none';"
                "document.body.appendChild(i);",
            )
            target = driver.find_element(By.ID, 'sora_injected_file')
            accept = ""
        except Exception:
            pass

    if target is None:
        return False

    attach_path = _convert_image_if_needed(path, accept)

    payload_cache: dict[str, str] | None = None

    def _ensure_payload() -> dict[str, str] | None:
        nonlocal payload_cache
        if payload_cache is not None:
            return payload_cache
        try:
            with open(attach_path, 'rb') as fh:
                data_b64 = base64.b64encode(fh.read()).decode('ascii')
            name = os.path.basename(attach_path)
            mime = mimetypes.guess_type(attach_path)[0] or 'application/octet-stream'
            payload_cache = {'b64': data_b64, 'name': name, 'mime': mime}
            return payload_cache
        except Exception:
            return None

    def _inject_file_via_js(el) -> bool:
        payload = _ensure_payload()
        if not payload:
            return False
        try:
            return bool(
                driver.execute_async_script(
                    """
                    const el = arguments[0];
                    const b64 = arguments[1];
                    const name = arguments[2];
                    const mime = arguments[3];
                    const done = arguments[arguments.length - 1];
                    try {
                        if (typeof window.DataTransfer === 'undefined') {
                            done(false);
                            return;
                        }
                        const binary = atob(b64);
                        const len = binary.length;
                        const bytes = new Uint8Array(len);
                        for (let i = 0; i < len; ++i) {
                            bytes[i] = binary.charCodeAt(i);
                        }
                        const file = new File([bytes], name, { type: mime || 'application/octet-stream' });
                        const dt = new DataTransfer();
                        dt.items.add(file);
                        const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'files').set;
                        setter.call(el, dt.files);
                        el.dispatchEvent(new Event('change', { bubbles: true }));
                        done(true);
                    } catch (err) {
                        console.error('inject error', err);
                        done(false);
                    }
                    """,
                    el,
                    payload['b64'],
                    payload['name'],
                    payload['mime'],
                )
            )
        except Exception:
            return False

    def _set_file(el) -> bool:
        if _inject_file_via_js(el):
            return True
        try:
            reveal_input_file(driver, el)
            el.send_keys(attach_path)
            try:
                driver.execute_script("arguments[0].dispatchEvent(new Event('change', {bubbles:true}));", el)
            except Exception:
                pass
            return True
        except Exception:
            return False

    if not _set_file(target):
        return False

    # Wait for UI confirmation (Remove media button appears)
    def _has_remove():
        try:
            driver.find_element(By.XPATH, "//button[.//span[contains(@class,'sr-only') and normalize-space()='Remove media']]")
            return True
        except Exception:
            return False
    def _files_selected(el) -> bool:
        try:
            return bool(driver.execute_script("return arguments[0].files && arguments[0].files.length > 0;", el))
        except Exception:
            return False

    end_confirm = time.time() + 8.0
    while time.time() < end_confirm:
        if _has_remove() or _files_selected(target):
            return True
        time.sleep(0.3)

    # Retry once via explicit plus->nearest input path if confirmation not seen
    try:
        if plus_el is not None:
            _ = click_safely(driver, plus_el, force=False)
            time.sleep(0.4)
            near = driver.find_element(By.XPATH, "//button[.//span[contains(@class,'sr-only') and normalize-space()='Attach media']]/following::input[@type='file'][1]")
            if near.get_attribute('disabled') is None:
                if not _set_file(near):
                    return False
                end_confirm = time.time() + 6.0
                while time.time() < end_confirm:
                    if _has_remove() or _files_selected(near):
                        return True
                    time.sleep(0.3)
    except Exception:
        pass

    # Last resort: return False to signal UI likely showed an error
    return False


def fill_storyboard(driver, scenes: list[str], ensure_storyboard: bool = True, timeout: int = 30) -> int:
    """Fill storyboard textareas with provided scenes. Returns number filled."""
    if ensure_storyboard:
        ctrls = find_page_controls(driver, timeout=10)
        _ = click_safely(driver, ctrls.get("storyboard"), force=False)
        time.sleep(0.3)

    def _find_scene_textareas():
        try:
            return driver.find_elements(By.CSS_SELECTOR, "textarea[placeholder='Describe this scene… who, where, what happens?']")
        except Exception:
            return []

    # Ensure enough textareas by clicking an add-scene button if present
    def _add_scene_button():
        x = "//button[contains(@class,'border-dashed') and .//div[contains(normalize-space(),'Describe this scene')]]"
        try:
            return driver.find_element(By.XPATH, x)
        except Exception:
            return None

    filled = 0
    for idx, text in enumerate(scenes):
        # Grow scenes if needed
        start = time.time()
        while True:
            areas = _find_scene_textareas()
            if len(areas) > idx:
                break
            add_btn = _add_scene_button()
            if add_btn is not None:
                try:
                    add_btn.click()
                except Exception:
                    try:
                        driver.execute_script("arguments[0].click();", add_btn)
                    except Exception:
                        pass
            if time.time() - start > timeout:
                break
            time.sleep(0.4)

        areas = _find_scene_textareas()
        if len(areas) <= idx:
            break

        el = areas[idx]
        try:
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        except Exception:
            pass
        try:
            el.click()
        except Exception:
            try:
                driver.execute_script("arguments[0].click();", el)
            except Exception:
                pass
        try:
            el.send_keys(Keys.CONTROL, 'a')
            el.send_keys(text)
        except Exception:
            pass
        try:
            driver.execute_script(
                "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input', {bubbles:true}));",
                el,
                text,
            )
        except Exception:
            pass
        filled += 1

    return filled


def apply_settings(
    driver,
    orientation: str | None = None,
    duration: int | None = None,
    model: str | None = None,
    resolution: str | None = None,
    timeout: int = 20,
) -> dict:
    """Apply settings like orientation and duration via the settings menu.
    Returns a dict of attempted values.
    """
    result = {"orientation": None, "duration": None, "model": None, "resolution": None}
    ctrls = find_page_controls(driver, timeout=10)
    settings_btn = ctrls.get("settings")

    if settings_btn is None:
        # Fallback: prefer visible settings button near composer summary
        try:
            candidates = driver.find_elements(By.XPATH, "//button[@aria-label='Settings']")
        except Exception:
            candidates = []
        for cand in candidates:
            try:
                if not cand.is_displayed():
                    continue
            except Exception:
                continue
            try:
                text = cand.text.strip()
            except Exception:
                text = ""
            if any(token.lower() in text.lower() for token in ("sora", "portrait", "landscape", "model")):
                settings_btn = cand
                break
        if settings_btn is None:
            settings_btn = ctrls.get("settings")

    def is_menu_open() -> bool:
        try:
            driver.find_element(By.XPATH, "//div[@role='menu' and contains(@class,'popover')]")
            return True
        except Exception:
            return False

    def ensure_menu_open() -> bool:
        if is_menu_open():
            return True
        if settings_btn is None:
            return False
        clicked = click_safely(driver, settings_btn, force=False)
        if not clicked:
            try:
                driver.execute_script("arguments[0].click();", settings_btn)
            except Exception:
                pass
        time.sleep(0.2)
        return is_menu_open()


    def select_menu_option(section_labels: list[str], option_labels: list[str]) -> str | None:
        if not ensure_menu_open():
            return None

        section_labels_norm = [str(l).strip().lower() for l in section_labels if str(l).strip()]
        option_labels_norm = [str(l).strip().lower() for l in option_labels if str(l).strip()]
        if not section_labels_norm or not option_labels_norm:
            return None

        script = """
        const sections = arguments[0];
        const options = arguments[1];
        const done = arguments[arguments.length - 1];

        const norm = (str) => (str || '').replace(/\\s+/g, ' ').trim().toLowerCase();

        function openMenus() {
            return Array.from(document.querySelectorAll('div[role="menu"]'))
                .filter(el => norm(el.getAttribute('data-state')) === 'open');
        }

        function clickEl(el) {
            if (!el) return;
            el.dispatchEvent(new PointerEvent('pointerdown', {bubbles: true, composed: true}));
            el.dispatchEvent(new PointerEvent('pointerup', {bubbles: true, composed: true}));
            el.click();
        }

        const menus = openMenus();
        if (!menus.length) {
            done(null);
            return;
        }

        const primary = menus[menus.length - 1];
        const parents = Array.from(primary.querySelectorAll('div[role="menuitem"]'));
        const parent = parents.find(el => sections.some(label => norm(el.innerText).includes(label)));
        if (!parent) {
            done(null);
            return;
        }

        clickEl(parent);

        setTimeout(() => {
            const menusAfter = openMenus();
            let submenu = menusAfter.find(el => !primary.contains(el) || el !== primary);
            if (!submenu) {
                submenu = primary;
            }
            const radios = Array.from(submenu.querySelectorAll('div[role="menuitemradio"]'));
            const target = radios.find(el => options.some(label => {
                const txt = norm(el.innerText);
                return txt === label || txt.includes(label);
            }));
            if (!target) {
                done(null);
                return;
            }
            clickEl(target);
            setTimeout(() => {
                done({ label: target.innerText.trim() });
            }, 150);
        }, 160);
        """;

        try:
            result_js = driver.execute_async_script(script, section_labels_norm, option_labels_norm)
        except Exception:
            result_js = None

        if isinstance(result_js, dict) and result_js.get('label'):
            return result_js['label']
        return None

    if orientation:
        opt = 'portrait' if str(orientation).lower().startswith('p') else 'landscape'
        selected = select_menu_option(['orientation'], [opt])
        if selected:
            result["orientation"] = selected

    if duration is not None:
        seconds = int(duration)
        labels = [
            f"{seconds} seconds",
            f"{seconds}s",
            f"{seconds} sec",
            f"{seconds} second",
        ]
        selected = select_menu_option(['duration', 'length'], labels)
        if selected:
            match = re.search(r"(\d+)", selected)
            if match:
                result["duration"] = int(match.group(1))
            else:
                result["duration"] = selected

    if model:
        # Accept values like 'sora 2 pro', 'pro', 'sora 2'
        m = str(model).strip().lower()
        if 'pro' in m:
            want = 'sora 2 pro'
        else:
            want = 'sora 2'
        selected = select_menu_option(['model'], [want])
        if selected:
            result["model"] = selected

    if resolution:
        res = str(resolution).strip().lower()
        labels = [res]
        if res.startswith('high'):
            labels.extend(['high quality', 'high'])
        elif res.startswith('standard'):
            labels.extend(['standard'])
        selected = select_menu_option(['quality', 'resolution'], labels)
        if selected:
            result["resolution"] = selected

    # Close menu if still open (best-effort)
    if is_menu_open():
        try:
            body = driver.find_element(By.TAG_NAME, 'body')
            body.send_keys(Keys.ESCAPE)
        except Exception:
            try:
                driver.execute_script("document.activeElement && document.activeElement.blur && document.activeElement.blur();")
            except Exception:
                pass

    return result


def wait_for_any_text(driver, timeout: int = 30):
    """
    As a generic signal the page rendered, wait for any non-empty body text.
    This is resilient when we don't know page internals.
    """
    WebDriverWait(driver, timeout).until(
        lambda d: bool(d.find_element(By.TAG_NAME, "body").text.strip())
    )


def open_url(url: str, headless: bool, timeout: int, chrome_binary: str | None):
    with build_chrome(headless=headless, chrome_binary=chrome_binary) as driver:
        driver.get(url)
        wait_for_page_loaded(driver, timeout=timeout)
        # Try a light-weight render check; ignore failures silently
        try:
            wait_for_any_text(driver, timeout=max(5, timeout // 3))
        except Exception:
            pass

        title = driver.title
        current_url = driver.current_url
        print(f"Page loaded: '{title}' @ {current_url}")

        return title, current_url


def open_url_attached(url: str, debugger_port: int, timeout: int, chrome_binary: str | None):
    with build_chrome_attached(debugger_port=debugger_port, chrome_binary=chrome_binary) as driver:
        driver.get(url)
        wait_for_page_loaded(driver, timeout=timeout)
        try:
            wait_for_quiet_resources(driver, stable_secs=1.5, timeout=max(5, timeout // 2))
        except Exception:
            pass
        try:
            wait_for_any_text(driver, timeout=max(5, timeout // 3))
        except Exception:
            pass
        return driver.title, driver.current_url


def type_into_selector(driver, selector: str, text: str, timeout: int = 30):
    wait_for_selector_visible(driver, selector, timeout=timeout)
    el = driver.find_element(By.CSS_SELECTOR, selector)

    # Bring into view and focus
    try:
        driver.execute_script("arguments[0].scrollIntoView({block:'center',inline:'center'});", el)
    except Exception:
        pass
    try:
        el.click()
    except Exception:
        # Fallback JS click
        try:
            driver.execute_script("arguments[0].click();", el)
        except Exception:
            pass

    # Clear then type via keys
    try:
        el.send_keys(Keys.CONTROL, "a")
        el.send_keys(text)
    except Exception:
        pass

    # Ensure frameworks receive input event
    try:
        driver.execute_script(
            "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input', {bubbles:true}));",
            el,
            text,
        )
    except Exception:
        pass


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Selenium agent to open a URL (Sora example)")
    parser.add_argument(
        "--url",
        default="https://sora.chatgpt.com/explore",
        help="URL to open. Defaults to Sora Explore.",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Force headless mode (useful on servers).",
    )
    parser.add_argument(
        "--no-headless",
        action="store_true",
        help="Force non-headless mode (requires a display).",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Max seconds to wait for page load.",
    )
    parser.add_argument(
        "--chrome-binary",
        default=None,
        help="Path to Chrome/Chromium binary (or set CHROME_BINARY).",
    )
    parser.add_argument(
        "--debugger-port",
        type=int,
        default=None,
        help="Attach to an existing Chrome launched with --remote-debugging-port=PORT.",
    )
    parser.add_argument(
        "--start-chrome",
        action="store_true",
        help="If set with --debugger-port, start Chrome with that port and a user-data-dir if not already running.",
    )
    parser.add_argument(
        "--user-data-dir",
        default=None,
        help="User data dir for Chrome when using --start-chrome.",
    )
    parser.add_argument(
        "--display",
        default=None,
        help="DISPLAY to use when starting Chrome (e.g., :0 or :1).",
    )
    parser.add_argument(
        "--selector",
        default='textarea[placeholder="Describe your video..."]',
        help="CSS selector of the input to type into.",
    )
    parser.add_argument(
        "--text",
        default="A serene mountain landscape at sunrise.",
        help="Text to type into the target input.",
    )
    parser.add_argument(
        "--login-timeout",
        type=int,
        default=300,
        help="Seconds to wait for manual login when redirected to /login.",
    )
    parser.add_argument(
        "--action",
        action="append",
        choices=["list", "plus", "storyboard", "settings", "create", "profile"],
        help="Action(s) to perform: list presence or click a button.",
    )
    parser.add_argument(
        "--force-click",
        action="store_true",
        help="Force click even if a button looks disabled.",
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    # Default behavior: headless when no DISPLAY set. Allow explicit override.
    default_headless = not bool(os.environ.get("DISPLAY"))
    if args.headless:
        headless = True
    elif args.no_headless:
        headless = False
    else:
        headless = default_headless

    if args.debugger_port:
        if args.start_chrome and not devtools_ready(args.debugger_port):
            print(f"Starting Chrome with --remote-debugging-port={args.debugger_port}...")
            _ = start_chrome_with_debug(
                port=args.debugger_port,
                url=args.url,
                user_data_dir=args.user_data_dir,
                chrome_binary=args.chrome_binary,
                display=args.display,
            )
            if not wait_for_devtools(args.debugger_port, timeout=30):
                raise SystemExit("DevTools endpoint not ready; Chrome may have failed to start.")

        print(
            f"Attaching to Chrome on :{args.debugger_port} and opening: {args.url}"
        )
        title, current_url = open_url_attached(args.url, args.debugger_port, args.timeout, args.chrome_binary)

        # After load, attempt to type (handle login redirect gracefully)
        with build_chrome_attached(debugger_port=args.debugger_port, chrome_binary=args.chrome_binary) as driver:
            if "/login" in driver.current_url:
                print("Detected login page; waiting for you to complete login...")
                end = time.time() + max(10, args.login_timeout)
                last_url = driver.current_url
                while time.time() < end:
                    time.sleep(2)
                    try:
                        if "/login" not in driver.current_url:
                            break
                    except Exception:
                        pass
                print(f"Continuing. Current URL: {driver.current_url}")

            # Ensure target page is open
            if driver.current_url.rstrip('/') != args.url.rstrip('/'):
                try:
                    driver.get(args.url)
                except Exception:
                    pass

            # If actions are specified, perform them; otherwise type.
            if args.action:
                controls = find_page_controls(driver, timeout=10)
                if "list" in args.action:
                    for k, el in controls.items():
                        if el is None:
                            print(f"control:{k}: not found")
                            continue
                        st = element_disabled_state(el)
                        print(
                            f"control:{k}: found displayed={st.get('displayed')} disabled={st.get('disabled')} aria-disabled={st.get('aria-disabled')} data-disabled={st.get('data-disabled')}"
                        )
                for click_key in [a for a in args.action if a in ("plus", "storyboard", "settings", "create")]:
                    el = controls.get(click_key)
                    ok = click_safely(driver, el, force=args.force_click)
                    print(f"clicked:{click_key}: {ok}")
            else:
                tried = []
                for sel in [args.selector, 'textarea', 'div[contenteditable="true"]']:
                    try:
                        type_into_selector(driver, sel, args.text, timeout=max(10, args.timeout // 2))
                        print(f"Typed into selector: {sel}")
                        break
                    except Exception as e:
                        tried.append((sel, str(e)))
                else:
                    print("Failed to find a suitable input. Tried:")
                    for sel, err in tried:
                        print(f" - {sel}: {err}")

        print(f"Page loaded: '{title}' @ {current_url}")
        print("Done.")
        return 0
    else:
        print(
            f"Launching Chrome (headless={headless}) to open: {args.url} (timeout={args.timeout}s)"
        )
        title, current_url = open_url(
            args.url,
            headless=headless,
            timeout=args.timeout,
            chrome_binary=args.chrome_binary,
        )
        print(f"Page loaded: '{title}' @ {current_url}")
        print("Done.")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
