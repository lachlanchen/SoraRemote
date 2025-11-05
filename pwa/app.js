(() => {
  const qs = (sel) => document.querySelector(sel);
  const serverInput = qs('#server');
  const statusEl = qs('#status');
  const logEl = qs('#log');
  const promptEl = qs('#prompt');
  const filepathEl = qs('#filepath');
  const scenesEl = qs('#scenes');
  const orientationEl = qs('#orientation');
  const durationEl = qs('#duration');

  const defaultServer = localStorage.getItem('sora_server') || `${location.origin}`;
  serverInput.value = defaultServer;

  function setStatus(text) {
    statusEl.textContent = text;
  }

  function log(msg) {
    const time = new Date().toLocaleTimeString();
    logEl.textContent += `[${time}] ${msg}\n`;
    logEl.scrollTop = logEl.scrollHeight;
  }

  qs('#btn-save-server').addEventListener('click', () => {
    localStorage.setItem('sora_server', serverInput.value.trim());
    setStatus('Saved server URL.');
  });

  async function api(path, opts) {
    const base = (localStorage.getItem('sora_server') || serverInput.value || '').replace(/\/$/, '');
    const url = `${base}${path}`;
    const res = await fetch(url, Object.assign({
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    }, opts || {}));
    if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
    return res.json();
  }

  async function doOpen() {
    const data = await api('/api/open', { method: 'POST', body: JSON.stringify({}) });
    log(`open: ${JSON.stringify(data)}`);
  }

  async function doList() {
    const data = await api('/api/actions');
    log(`actions: ${JSON.stringify(data.actions, null, 2)}`);
  }

  async function doClick(key) {
    const data = await api('/api/click', { method: 'POST', body: JSON.stringify({ key }) });
    log(`click(${key}): ${JSON.stringify(data)}`);
  }

  async function doAttachPath() {
    const path = filepathEl.value.trim();
    if (!path) return log('No filepath provided');
    const data = await api('/api/attach', { method: 'POST', body: JSON.stringify({ path, click_plus: true }) });
    log(`attach: ${JSON.stringify(data)}`);
  }

  async function doStoryboard() {
    const lines = (scenesEl.value || '').split(/\r?\n/).map(s => s.trim()).filter(Boolean);
    if (!lines.length) return log('No scenes provided');
    const data = await api('/api/storyboard', { method: 'POST', body: JSON.stringify({ scenes: lines }) });
    log(`storyboard: ${JSON.stringify(data)}`);
  }

  async function doSettings() {
    const orientation = orientationEl.value || null;
    const duration = durationEl.value ? parseInt(durationEl.value, 10) : null;
    const data = await api('/api/settings', { method: 'POST', body: JSON.stringify({ orientation, duration }) });
    log(`settings: ${JSON.stringify(data)}`);
  }

  async function doType(composeCreate) {
    const text = promptEl.value;
    if (composeCreate) {
      const data = await api('/api/compose', { method: 'POST', body: JSON.stringify({ text, click_create: true }) });
      log(`compose: ${JSON.stringify(data)}`);
    } else {
      const data = await api('/api/type', { method: 'POST', body: JSON.stringify({ text }) });
      log(`type: ${JSON.stringify(data)}`);
    }
  }

  document.body.addEventListener('click', (e) => {
    const btn = e.target.closest('button[data-action]');
    if (!btn) return;
    const action = btn.getAttribute('data-action');
    (async () => {
      try {
        if (action === 'open') return await doOpen();
        if (action === 'list') return await doList();
        if (action === 'type') return await doType(false);
        if (action === 'compose') return await doType(true);
        if (action === 'attach-path') return await doAttachPath();
        if (action === 'apply-storyboard') return await doStoryboard();
        if (action === 'apply-settings') return await doSettings();
        if (['plus', 'storyboard', 'settings', 'create'].includes(action)) return await doClick(action);
      } catch (err) {
        log(`ERR: ${err.message}`);
      }
    })();
  });

  function connectWS() {
    try {
      const base = (localStorage.getItem('sora_server') || serverInput.value || '').replace(/^http/, 'ws').replace(/\/$/, '');
      const ws = new WebSocket(`${base}/ws`);
      ws.onopen = () => setStatus('Connected');
      ws.onclose = () => setStatus('Disconnected');
      ws.onmessage = (ev) => {
        try {
          const msg = JSON.parse(ev.data);
          log(`ws:${msg.event}: ${JSON.stringify(msg.data)}`);
        } catch {
          log(`ws: ${ev.data}`);
        }
      };
      return ws;
    } catch (e) {
      log(`ws error: ${e.message}`);
      setStatus('WS error');
    }
  }

  connectWS();

  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js').catch((e) => log(`SW fail: ${e.message}`));
  }
})();
