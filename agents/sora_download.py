import argparse
import os
import time
import shutil
import urllib.request
import urllib.error
from urllib.parse import urlparse

from selenium.webdriver.common.by import By

from agents.sora_agent import (
    build_chrome_attached,
    start_chrome_with_debug,
    wait_for_devtools,
    devtools_ready,
    wait_for_page_loaded,
    wait_for_quiet_resources,
    wait_for_selector_visible,
)


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def sanitize_filename(name: str) -> str:
    bad = '<>:"/\\|?*\n\r\t'
    for ch in bad:
        name = name.replace(ch, '_')
    return name[:200]


def cookies_for_domain(driver, url: str) -> str:
    """Build a Cookie header string for the target URL's domain."""
    parsed = urlparse(url)
    domain = parsed.hostname or ''
    jar = []
    try:
        for c in driver.get_cookies():
            cdom = c.get('domain', '')
            if cdom.startswith('.'):
                cdom = cdom[1:]
            if domain.endswith(cdom):
                jar.append(f"{c['name']}={c['value']}")
    except Exception:
        pass
    return '; '.join(jar)


def http_download(url: str, out_path: str, driver=None, timeout: int = 120) -> bool:
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome Safari',
        'Accept': '*/*',
    }
    if driver is not None:
        ck = cookies_for_domain(driver, url)
        if ck:
            headers['Cookie'] = ck

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp, open(out_path, 'wb') as f:
            shutil.copyfileobj(resp, f)
        return True
    except Exception as e:
        print(f"Download failed: {e}")
        return False


def find_download_candidates(driver):
    """Return list of (label, url) candidates detected on the page."""
    candidates = []

    # 1) Direct anchors labeled Download
    try:
        anchors = driver.find_elements(By.XPATH, "//a[contains(translate(normalize-space(.),'DOWNLOAD','download'),'download') and @href]")
        for a in anchors:
            href = a.get_attribute('href')
            if href:
                candidates.append(("anchor", href))
    except Exception:
        pass

    # 2) Any anchors that look like mp4/video
    try:
        anchors = driver.find_elements(By.XPATH, "//a[contains(@href,'.mp4') or contains(@href,'video')]")
        for a in anchors:
            href = a.get_attribute('href')
            if href:
                candidates.append(("media", href))
    except Exception:
        pass

    # 3) <video> or <source> elements
    try:
        srcs = driver.find_elements(By.XPATH, "//video/@src | //video/source/@src")
    except Exception:
        srcs = []
    # Selenium doesn't support attribute axes directly; do two passes
    try:
        videos = driver.find_elements(By.TAG_NAME, 'video')
        for v in videos:
            try:
                src = v.get_attribute('src')
                if src:
                    candidates.append(("video", src))
            except Exception:
                pass
            try:
                sources = v.find_elements(By.TAG_NAME, 'source')
                for s in sources:
                    src = s.get_attribute('src')
                    if src:
                        candidates.append(("video-src", src))
            except Exception:
                pass
    except Exception:
        pass

    # Deduplicate while preserving order
    seen = set()
    uniq = []
    for label, href in candidates:
        if href not in seen:
            seen.add(href)
            uniq.append((label, href))
    return uniq


def go_to_library_or_profile(driver):
    """Navigate to a page that likely lists your videos.
    Best-effort using common labels: Library, My videos, Profile.
    """
    # Try Library / My videos links
    for xp in [
        "//a[normalize-space()='Library']",
        "//a[contains(translate(normalize-space(.),'MY VIDEOS','my videos'),'my videos')]",
        "//a[contains(translate(normalize-space(.),'PROFILE','profile'),'profile')]",
    ]:
        try:
            el = driver.find_element(By.XPATH, xp)
            el.click()
            return True
        except Exception:
            continue

    # Try opening settings/profile button first
    for xp in [
        "//button[@aria-label='Settings']",
        "//button[@aria-label='Profile']",
    ]:
        try:
            el = driver.find_element(By.XPATH, xp)
            el.click()
            time.sleep(0.5)
            # Look for menu entries
            for mx in [
                "//a[normalize-space()='Profile']",
                "//a[normalize-space()='Library']",
                "//a[contains(.,'My videos')]",
            ]:
                try:
                    m = driver.find_element(By.XPATH, mx)
                    m.click()
                    return True
                except Exception:
                    continue
        except Exception:
            continue
    return False


def main(argv=None):
    p = argparse.ArgumentParser(description="Sora downloader (attach to Chrome, discover and download videos)")
    p.add_argument('--debugger-port', type=int, default=9333)
    p.add_argument('--start-chrome', action='store_true')
    p.add_argument('--user-data-dir', default=os.path.expanduser('~/.config/sora_profile_9333'))
    p.add_argument('--no-headless', action='store_true', help='Run Chrome visible (attach mode).')
    p.add_argument('--display', default=None)
    p.add_argument('--url', default='https://sora.chatgpt.com/explore')
    p.add_argument('--out-dir', default=os.path.join(os.getcwd(), 'downloads', 'sora'))
    p.add_argument('--max', type=int, default=3, help='Max number of files to download')
    p.add_argument('--dry-run', action='store_true', help='Only list candidates; do not download')
    args = p.parse_args(argv)

    if args.start_chrome and not devtools_ready(args.debugger_port):
        _ = start_chrome_with_debug(
            port=args.debugger_port,
            url=args.url,
            user_data_dir=args.user_data_dir,
            chrome_binary=None,
            display=args.display,
        )
        if not wait_for_devtools(args.debugger_port, timeout=30):
            raise SystemExit('DevTools endpoint not ready; Chrome may have failed to start.')

    with build_chrome_attached(debugger_port=args.debugger_port, chrome_binary=None) as driver:
        # Ensure page open
        driver.get(args.url)
        wait_for_page_loaded(driver, timeout=30)
        try:
            wait_for_quiet_resources(driver, stable_secs=1.5, timeout=30)
        except Exception:
            pass

        # Navigate to library/profile best-effort
        if not go_to_library_or_profile(driver):
            print('Could not locate Library/Profile directly; staying on current page.')

        # Collect candidates
        cands = find_download_candidates(driver)
        if not cands:
            print('No download candidates found on this page.')
            return 0

        print(f'Found {len(cands)} candidates:')
        for i, (lbl, href) in enumerate(cands[: args.max], 1):
            print(f'  [{i}] {lbl}: {href}')

        if args.dry_run:
            return 0

        ensure_dir(args.out_dir)
        downloaded = 0
        for lbl, href in cands:
            filename = sanitize_filename(os.path.basename(urlparse(href).path) or f'sora_video_{int(time.time())}.mp4')
            out_path = os.path.join(args.out_dir, filename)
            print(f'Downloading -> {out_path}')
            ok = http_download(href, out_path, driver=driver, timeout=180)
            if ok:
                downloaded += 1
                if downloaded >= args.max:
                    break
        print(f'Downloaded {downloaded} file(s).')
        return 0


if __name__ == '__main__':
    raise SystemExit(main())

