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
  const resolutionEl = qs('#resolution');
  const resolutionWrapper = qs('#resolution-wrapper');
  const resolutionNote = qs('#resolution-note');
  const resolutionBtn = document.querySelector('button[data-action="apply-resolution"]');
  const fileEl = qs('#fileinput');
  const mediaDescEl = qs('#media-desc');
  const scriptUpdatesEl = qs('#script-updates');
  const prevImg = qs('#preview-img');
  const prevVideo = qs('#preview-video');
  let currentObjectUrl = null;
  let lastUploadedPath = null;

  const defaultServer = localStorage.getItem('sora_server') || `${location.origin}`;
  serverInput.value = defaultServer;

  function refreshResolutionControls() {
    const modelVal = (modelEl && modelEl.value || '').toLowerCase();
    const isPro = modelVal.includes('pro');
    if (resolutionEl) {
      resolutionEl.disabled = !isPro;
      if (!isPro) {
        resolutionEl.value = 'standard';
      }
    }
    if (resolutionWrapper) {
      resolutionWrapper.classList.toggle('disabled', !isPro);
    }
    if (resolutionNote) {
      resolutionNote.style.visibility = isPro ? 'hidden' : 'visible';
    }
    if (resolutionBtn) {
      resolutionBtn.disabled = !isPro;
    }
  }

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

  async function attachServerPath(path, label) {
    const data = await api('/api/attach', { method: 'POST', body: JSON.stringify({ path, click_plus: false }) });
    log(`${label || 'attach'}: ${JSON.stringify(data)}`);
    if (data && data.ok) lastUploadedPath = path;
    return data;
  }

  async function doAttachPath() {
    const path = filepathEl.value.trim();
    if (!path) return log('No filepath provided');
    await attachServerPath(path, 'attach');
  }

  async function doStoryboard() {
    const lines = (scenesEl.value || '').split(/\r?\n/).map(s => s.trim()).filter(Boolean);
    if (!lines.length) return log('No scenes provided');
    const data = await api('/api/storyboard', { method: 'POST', body: JSON.stringify({ scenes: lines }) });
    log(`storyboard: ${JSON.stringify(data)}`);
  }

  async function sendSettings(payload, label) {
    const data = await api('/api/settings', { method: 'POST', body: JSON.stringify(payload) });
    log(`${label}: ${JSON.stringify(data)}`);
    return data;
  }

  async function doModel() {
    const model = modelEl.value || null;
    const data = await sendSettings({ model }, 'model');
    if (data && data.applied && data.applied.model) {
      const val = data.applied.model.toLowerCase();
      modelEl.value = val.includes('pro') ? 'sora 2 pro' : 'sora 2';
    }
    refreshResolutionControls();
  }

  async function doOrientation() {
    const orientation = orientationEl.value || null;
    const data = await sendSettings({ orientation }, 'orientation');
    if (data && data.applied && data.applied.orientation && orientationEl) {
      const val = data.applied.orientation.toLowerCase();
      orientationEl.value = val.startsWith('landscape') ? 'landscape' : 'portrait';
    }
  }

  async function doDuration() {
    const duration = durationEl.value ? parseInt(durationEl.value, 10) : null;
    const data = await sendSettings({ duration }, 'duration');
    if (data && data.applied && typeof data.applied.duration !== 'undefined' && durationEl) {
      durationEl.value = String(data.applied.duration);
    }
  }

  async function doResolution() {
    const resolution = resolutionEl ? resolutionEl.value || null : null;
    const data = await sendSettings({ resolution }, 'resolution');
    if (data && data.applied && data.applied.resolution && resolutionEl) {
      const val = data.applied.resolution.toLowerCase();
      resolutionEl.value = val.includes('high') ? 'high' : 'standard';
    }
  }

  async function doDescribe() {
    if (!mediaDescEl) return log('Description textarea missing');
    const text = mediaDescEl.value || '';
    const data = await api('/api/describe', { method: 'POST', body: JSON.stringify({ text }) });
    log(`describe: ${JSON.stringify(data)}`);
  }

  async function doScriptUpdates() {
    if (!scriptUpdatesEl) return log('Script updates textarea missing');
    const text = scriptUpdatesEl.value || '';
    const data = await api('/api/script-updates', { method: 'POST', body: JSON.stringify({ text }) });
    log(`script-updates: ${JSON.stringify(data)}`);
  }

  async function doUploadAndAttach() {
    if (!fileEl.files || !fileEl.files.length) {
      if (lastUploadedPath) return attachServerPath(lastUploadedPath, 'attach(reuse)');
      return log('No file selected');
    }
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
    lastUploadedPath = path;
    await attachServerPath(path, 'attach(uploaded)');
  }

  async function doSmartPlus() {
    try {
      // Prefer directly sending a selected file, then a typed path.
      const hasFile = fileEl && fileEl.files && fileEl.files.length > 0;
      const pathVal = filepathEl && filepathEl.value && filepathEl.value.trim();
      if (hasFile) return await doUploadAndAttach();
      if (pathVal) return await doAttachPath();
      log('Select a file or supply a path before using Plus.');
      return;
    } catch (err) {
      log(`ERR(smart-plus): ${err.message}`);
    }
  }

  function clearPreview() {
    if (currentObjectUrl) {
      URL.revokeObjectURL(currentObjectUrl);
      currentObjectUrl = null;
    }
    // Reset elements and handlers so no broken frames flash
    prevImg.hidden = true;
    prevVideo.hidden = true;
    prevImg.onload = null;
    prevImg.onerror = null;
    prevVideo.onloadeddata = null;
    prevVideo.onerror = null;
    prevImg.removeAttribute('src');
    prevVideo.removeAttribute('src');
  }

  async function serverPreview(file) {
    try {
      const fd = new FormData();
      fd.append('file', file);
      const base = (localStorage.getItem('sora_server') || serverInput.value || '').replace(/\/$/, '');
      const url = `${base}/api/preview`;
      const res = await fetch(url, { method: 'POST', body: fd });
      if (!res.ok) return null;
      const data = await res.json();
      if (!data || !data.ok || !data.data_url) return null;
      return data.data_url;
    } catch (e) {
      return null;
    }
  }

  async function showPreview(file) {
    clearPreview();
    if (!file) return;

    const name = (file.name || '').toLowerCase();
    const ext = name.split('.').pop() || '';
    const type = (file.type || '').toLowerCase();
    const isImage = type.startsWith('image/') || ['heic','heif','avif','jpg','jpeg','png','webp'].includes(ext);
    const isVideo = type.startsWith('video/') || ['mp4','webm','mov','quicktime'].includes(ext);

    if (isImage) {
      if (['heic','heif','avif'].includes(ext) || !type) {
        const dataUrl = await serverPreview(file);
        if (dataUrl) {
          prevImg.onload = () => {
            prevVideo.hidden = true;
            prevImg.hidden = false;
          };
          prevImg.onerror = () => {
            prevImg.hidden = true;
            log('Preview failed for selected image.');
          };
          prevImg.src = dataUrl;
          return;
        }
      }
      const url = URL.createObjectURL(file);
      currentObjectUrl = url;
      prevImg.onload = () => {
        prevVideo.hidden = true;
        prevImg.hidden = false;
      };
      prevImg.onerror = async () => {
        const dataUrl = await serverPreview(file);
        if (dataUrl) {
          prevImg.onload = () => {
            prevVideo.hidden = true;
            prevImg.hidden = false;
          };
          prevImg.onerror = () => {
            prevImg.hidden = true;
            log('Preview failed for selected image.');
          };
          prevImg.src = dataUrl;
        } else {
          prevImg.hidden = true;
          log('Preview not available for selected image.');
        }
      };
      prevImg.src = url;
      return;
    }

    if (isVideo) {
      const url = URL.createObjectURL(file);
      currentObjectUrl = url;
      prevVideo.onloadeddata = () => {
        prevImg.hidden = true;
        prevVideo.hidden = false;
      };
      prevVideo.onerror = () => {
        prevVideo.hidden = true;
        log('Preview not available for selected video.');
      };
      prevVideo.src = url;
      prevVideo.load();
      return;
    }

    log('Preview not available for this file type.');
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
        if (action === 'apply-model') return await doModel();
        if (action === 'apply-orientation') return await doOrientation();
        if (action === 'apply-duration') return await doDuration();
        if (action === 'apply-resolution') return await doResolution();
        if (action === 'apply-script-updates') return await doScriptUpdates();
        if (action === 'describe') return await doDescribe();
        if (action === 'plus') return await doSmartPlus();
        if (['storyboard', 'settings', 'create'].includes(action)) return await doClick(action);
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

  modelEl && modelEl.addEventListener('change', refreshResolutionControls);
  refreshResolutionControls();

  fileEl && fileEl.addEventListener('change', (e) => {
    const f = fileEl.files && fileEl.files[0];
    showPreview(f || null);
  });
})();
