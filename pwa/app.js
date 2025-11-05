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
  const modelEl = qs('#model');
  const fileEl = qs('#fileinput');
  const prevImg = qs('#preview-img');
  const prevVideo = qs('#preview-video');
  const prevFallback = qs('#preview-fallback');
  const prevName = qs('#preview-name');
  const prevType = qs('#preview-type');
  const prevSize = qs('#preview-size');
  let currentObjectUrl = null;

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
    const model = modelEl.value || null;
    const data = await api('/api/settings', { method: 'POST', body: JSON.stringify({ orientation, duration, model }) });
    log(`settings: ${JSON.stringify(data)}`);
  }

  async function doUploadAndAttach() {
    if (!fileEl.files || !fileEl.files.length) return log('No file selected');
    const fd = new FormData();
    fd.append('file', fileEl.files[0]);
    const base = (localStorage.getItem('sora_server') || serverInput.value || '').replace(/\/$/, '');
    const url = `${base}/api/upload`;
    const res = await fetch(url, { method: 'POST', body: fd });
    if (!res.ok) return log(`upload failed: ${res.status}`);
    const data = await res.json();
    log(`upload: ${JSON.stringify(data)}`);
    if (!data.paths || !data.paths.length) return;
    const path = data.paths[0];
    const attach = await api('/api/attach', { method: 'POST', body: JSON.stringify({ path, click_plus: true }) });
    log(`attach(uploaded): ${JSON.stringify(attach)}`);
  }

  function bytesToStr(n) {
    if (!n && n !== 0) return '';
    const i = n;
    if (i < 1024) return `${i} B`;
    const kb = i / 1024;
    if (kb < 1024) return `${kb.toFixed(1)} KB`;
    const mb = kb / 1024;
    return `${mb.toFixed(1)} MB`;
  }

  function clearPreview() {
    if (currentObjectUrl) {
      URL.revokeObjectURL(currentObjectUrl);
      currentObjectUrl = null;
    }
    prevImg.hidden = true;
    prevVideo.hidden = true;
    prevFallback.hidden = true;
    prevImg.removeAttribute('src');
    prevVideo.removeAttribute('src');
  }

  function showPreview(file) {
    clearPreview();
    if (!file) return;
    prevName.textContent = file.name || '(unnamed)';
    prevType.textContent = file.type || 'unknown';
    prevSize.textContent = bytesToStr(file.size || 0);

    const name = (file.name || '').toLowerCase();
    const ext = name.split('.').pop() || '';
    const url = URL.createObjectURL(file);
    currentObjectUrl = url;

    const isImage = (file.type && file.type.startsWith('image/')) || ['heic','heif','avif','jpg','jpeg','png','webp'].includes(ext);
    const isVideo = (file.type && file.type.startsWith('video/')) || ['mp4','webm','mov'].includes(ext);

    if (isImage) {
      prevImg.hidden = false;
      prevImg.src = url;
      prevImg.onload = () => { /* ok */ };
      prevImg.onerror = () => {
        prevImg.hidden = true;
        prevFallback.hidden = false;
      };
      prevFallback.hidden = true;
      prevVideo.hidden = true;
      return;
    }
    if (isVideo) {
      prevVideo.hidden = false;
      prevVideo.src = url;
      prevVideo.load();
      prevFallback.hidden = true;
      prevImg.hidden = true;
      return;
    }
    // Fallback
    prevFallback.hidden = false;
    prevImg.hidden = true;
    prevVideo.hidden = true;
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
        if (action === 'upload-and-attach') return await doUploadAndAttach();
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

  fileEl && fileEl.addEventListener('change', (e) => {
    const f = fileEl.files && fileEl.files[0];
    showPreview(f || null);
  });
})();
