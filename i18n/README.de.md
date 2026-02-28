[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)



# SoraRemote

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20WSL-6c757d)
![Server](https://img.shields.io/badge/Server-Tornado%20API-0EA5E9)
![Frontend](https://img.shields.io/badge/Frontend-PWA-10B981)
![Status](https://img.shields.io/badge/Status-Experimental-F59E0B)

SoraRemote ist ein leichtgewichtiges Python- + Selenium-Toolkit zur Automatisierung der Sora-Weboberfläche.

Es unterstützt drei komplementäre Workflows:
1. CLI-Automatisierungsagent (`agents/sora_agent.py`) für Prompt-Eingabe und UI-Steueraktionen.
2. CLI-Downloader (`agents/sora_download.py`) zum Finden und Herunterladen von Media-Kandidaten.
3. Lokaler Tornado-Control-Server + PWA (`server/app.py` + `pwa/`) für API-gesteuerte und browserbasierte Steuerung.

Der aktuelle README-Inhalt bleibt als kanonische Betriebsanleitung erhalten und wurde für mehr Klarheit neu strukturiert.

## ✨ Überblick

Kerndesign:
- Anbindung an eine persistente Chrome-Sitzung über DevTools-Remote-Debugging (Standardport `9333`).
- Wiederverwendung des Browserprofil-Status für Login-/Sitzungskontinuität.
- Automatisierung zentraler Composer-Aktionen (tippen, plus/media anhängen, storyboard, settings, create).
- Bereitstellung derselben Aktionen über REST + WebSocket-Logs für einen lokalen PWA-Controller.

### Workflow-Schnappschuss

| Workflow | Einstiegspunkt | Hauptanwendung |
| --- | --- | --- |
| CLI-Agent | `agents/sora_agent.py` | Prompts eingeben, Controls klicken, Compose-Flow automatisieren |
| CLI-Downloader | `agents/sora_download.py` | Herunterladbare Medien finden und Dateien lokal speichern |
| API + PWA | `server/app.py` + `pwa/` | Remote-Steuerung und visuelle Orchestrierung im Browser |

## ✅ Funktionen

- Chrome-Attach/Start-Flow mit wiederverwendbarem Profil (`--debugger-port`, `--start-chrome`, `--user-data-dir`).
- Sichere oder erzwungene Klicks für zentrale Controls (`plus`, `storyboard`, `settings`, `create`, `profile`).
- Prompt-Eingabe mit Selector-Fallback-Verhalten.
- Media-Attach per Dateipfad mit DataTransfer-Injektion.
- Storyboard-Szenen befüllen + Script-Updates + storyboard-spezifisches Media-Attach.
- Einstellungsautomatisierung für model/orientation/duration/resolution.
- Separater Discover- + Download-Flow mit Browser-Cookies.
- Tornado-REST-API und Live-WebSocket-Debug-Stream.
- Installierbare lokale PWA mit Upload, Vorschau und granularen Controls.

## 🗂️ Projektstruktur

```text
SoraRemote/
├─ README.md
├─ requirements.txt
├─ .github/
│  └─ FUNDING.yml
├─ agents/
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
│  └─ (derzeit leer)
├─ uploads/
│  └─ .gitkeep
└─ selenium_template -> ../auto-publish/ (Symlink)
```

## 🧩 Voraussetzungen

- Python 3.10+ (empfohlen).
- Chrome/Chromium ist installiert und ausführbar.
- Eine Anzeige für nicht-headless Nutzung (`--no-headless`), wenn Login oder interaktive UI erforderlich ist.
- Zugriff auf ein Sora-Konto im angebundenen Chrome-Profil.

## 📦 Installation

Vorhandener Setup-Flow aus der kanonischen README:

```bash
conda activate agent
pip install -r requirements.txt
```

Abhängigkeiten in `requirements.txt`:

| Paket | Versionsvorgabe |
| --- | --- |
| `selenium` | `>=4.17.2` |
| `tornado` | `>=6.4` |
| `Pillow` | `>=9.4.0` |
| `pillow-heif` | `>=0.16.0` |

## 🚀 Nutzung

### Schnellstart (CLI-Agent)

Schnellstart (öffnet Sora in einem verwalteten Browser):

```bash
python agents/sora_agent.py
```

An Chrome mit persistenter Sitzung anbinden (für Sora empfohlen):

```bash
python -m agents.sora_agent --debugger-port 9333 --start-chrome --no-headless --login-timeout 600 --text "A sunset over Tokyo, cinematic."
```

Hinweise:
- Ein Chrome-Fenster öffnet sich auf der Sora-Seite. Falls zur Anmeldung weitergeleitet wird, melde dich an; das Skript wartet und tippt dann deinen Prompt.
- Um denselben Login wiederzuverwenden, übergib einen festen Profilpfad:

```bash
python -m agents.sora_agent --debugger-port 9333 --start-chrome --no-headless --user-data-dir "$HOME/chrome_sora_profile_9333"
```

### Zentrale CLI-Optionen (`agents/sora_agent.py`)

- `--url` Zielseite (Standard: `https://sora.chatgpt.com/explore`).
- `--debugger-port` an ein bestehendes Chrome anbinden, das mit `--remote-debugging-port=PORT` gestartet wurde.
- `--start-chrome` startet zusammen mit `--debugger-port` Chrome für dich (mit `--user-data-dir`).
- `--no-headless` startet einen sichtbaren Browser; nötig für Login und Cloudflare.
- `--selector` CSS zum Finden des Inputs (Standard passt zur Sora-Composer-Textarea).
- `--text` Text, der in das Inputfeld geschrieben wird.
- `--chrome-binary` setzt einen Chrome-/Chromium-Pfad explizit.
- `--action` UI-Aktionen: `list`, `plus`, `storyboard`, `settings`, `create`, `profile`.
- `--force-click` klickt auch dann, wenn ein Element deaktiviert erscheint.
- `--login-timeout` Wartefenster für den Abschluss manueller Authentifizierung.

Driver-Handling:
- Der Agent entfernt vor dem Start jeden veralteten `chromedriver` aus `PATH`.
- Selenium Manager löst anschließend automatisch einen passenden Driver für das installierte Chrome auf.

### CLI-Beispiele (UI-Controls)

Häufige Controls auflisten und klicken:

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action list --action storyboard --action settings --action plus
```

Create video-Button erzwungen klicken (auch wenn deaktiviert):

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action create --force-click
```

Profil/Settings öffnen und bei Bedarf manuell navigieren:

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action list --action profile
```

Wenn `profile` nicht erkannt wird, öffnet der `settings`-Button typischerweise dasselbe Menü.

### Downloader-Flow

Videos mit dem Wrapper-Skript finden und herunterladen:

- Dry-Run (nur Kandidaten auflisten): `./bin/sora_download.sh --dry-run`
- Bis zu 2 Dateien nach `./downloads/sora` herunterladen: `./bin/sora_download.sh --max 2`
- Ausgabeordner ändern: `OUT_DIR=$HOME/Videos/sora ./bin/sora_download.sh --max 1`

Direkte Modulenutzung ist ebenfalls über `python -m agents.sora_download ...` verfügbar.

## 🌐 Control Server + PWA

Tornado-Server starten:

```bash
python server/app.py
# listens on http://0.0.0.0:8791 and serves the PWA at /
```

Standardmäßig verwendet der Server:
- Wiederverwendung von Chrome auf Remote-Debugging-Port `9333`.
- Upload-Speicher in `./uploads`, sofern `SORA_UPLOADS_DIR` nicht gesetzt ist.

### Wichtige Endpunkte

Alle Endpunkte arbeiten gegen das aktuell angebundene Chrome (Standard Debugger-Port `9333`).

| Method | Path | Payload | Beschreibung |
| --- | --- | --- | --- |
| `GET` | `/api/status` | none | Gibt den DevTools-Bereitschaftsstatus und den aktiven Port zurück. |
| `POST` | `/api/open` | `{ url? }` | Navigiert den angebundenen Chrome-Tab zur angegebenen URL (Standard: Sora Explore). |
| `GET` | `/api/actions` | none | Prüft Button-/Control-Status (Metadaten found/displayed/disabled). |
| `POST` | `/api/click` | `{ key, force? }` | Drückt ein Control, wobei `key ∈ {plus, storyboard, settings, create, profile}`. |
| `POST` | `/api/type` | `{ text, selector?, url? }` | Schreibt Prompt-Text in den Composer-Selector. |
| `POST` | `/api/compose` | `{ text, click_create? }` | Öffnet die Compose-Seite, schreibt Text, klickt optional create. |
| `POST` | `/api/attach` | `{ path, click_plus? }` | Lädt Medien per DataTransfer-Injektion hoch; entfernt vorhandene Medien automatisch (`click_plus` standardmäßig `false`). |
| `POST` | `/api/describe` | `{ text }` | Befüllt die Textarea „Optionally describe your video…“. |
| `POST` | `/api/script-updates` | `{ text }` | Befüllt das Feld „Describe updates to your script…“. |
| `POST` | `/api/storyboard` | `{ scenes: ["scene 1", ...], script_updates?: "...", media_path?: "..." }` | Öffnet Storyboard, befüllt Szenen-Textareas und wendet optional Script-Updates sowie Storyboard-Medien an. |
| `POST` | `/api/storyboard-media` | `{ path }` | Hängt Medien an den storyboard-spezifischen Uploader an, wenn Storyboard bereits sichtbar ist. |
| `POST` | `/api/storyboard-attach-only` | `{ path }` | Stellt sicher, dass Storyboard geöffnet ist, und hängt dann Medien an. |
| `POST` | `/api/settings` | `{ model?, orientation?, duration?, resolution? }` | Öffnet Settings und setzt gewählte Werte; die Antwort spiegelt angewendete Labels wider. |
| `POST` | `/api/upload` | multipart form data | Speichert lokale Datei(en) im Upload-Verzeichnis des Servers und gibt serverseitige Pfade zurück. |
| `POST` | `/api/preview` | multipart form data | Konvertiert ein Bild zu einer PNG-Vorschau (nützlich für HEIC/HEIF/AVIF-Fallback in der UI). |
| `GET` | `/ws` | WebSocket | Streamt Action-/Debug-Events. |

### PWA-Controls

Öffne `http://0.0.0.0:8791` (oder den gewählten Host), nachdem `server/app.py` gestartet wurde.

Highlights aus der bestehenden Implementierung:
- Medien per Dateiauswahl oder durch Einfügen eines Pfads hochladen, dann **Plus** klicken, um ohne erneutes Öffnen von Systemdateidialogen anzuhängen.
- Medienbeschreibung im dedizierten Feld „Media description“ anwenden.
- Unabhängige Controls für **Set Model**, **Set Orientation**, **Set Duration**, **Set Resolution** und Script-Updates.
- Storyboard-Controls für Szenen, Script-Updates, Öffnen des Storyboard-Panels und Anhängen des aktuellen Storyboard-Pfads.
- Live-Debug-Log mit API-Aufrufen und von Sora zurückgegebenen Werten (z. B. gewähltes model/duration).

## ⚙️ Konfiguration

### Umgebungsvariablen

`server/app.py` liest:
- `SORA_DEBUGGER_PORT` (Standard `9333`)
- `SORA_USER_DATA_DIR` (Standard `~/chrome_sora_profile_<port>`)
- `SORA_DISPLAY` (optionales X-Display)
- `SORA_API_PORT` (Standard `8791`)
- `SORA_URL` (Standard `https://sora.chatgpt.com/explore`)
- `SORA_UPLOADS_DIR` (optionale Überschreibung des Upload-Verzeichnisses)

`agents/sora_agent.py` unterstützt außerdem:
- `CHROME_BINARY` (falls `--chrome-binary` nicht angegeben ist)

Wrapper-Skripte unterstützen:
- `PORT`, `SORA_PROFILE_DIR`, `TIMEOUT`, `LOGIN_TIMEOUT` (`bin/sora_type.sh`)
- `PORT`, `SORA_PROFILE_DIR`, `OUT_DIR` (`bin/sora_download.sh`)

## 🧪 Beispiele

### End-to-End-API-Beispiel (curl)

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

### Media-Upload + Attach per API

```bash
# Upload file and get server path
curl -s -X POST http://127.0.0.1:8791/api/upload -F 'file=@/absolute/path/to/input.jpg'

# Then attach using returned path
curl -s -X POST http://127.0.0.1:8791/api/attach \
  -H 'Content-Type: application/json' \
  -d '{"path":"/absolute/or/server-returned/path.jpg","click_plus":false}'
```

## 🛠️ Entwicklungshinweise

- Derzeit gibt es kein paketiertes Modul (`pyproject.toml`/`setup.py` sind nicht vorhanden).
- In diesem Repository-Snapshot gibt es derzeit keine CI-/Test-/Lint-Pipeline.
- `selenium_template` ist ein Symlink auf `../auto-publish/`; dessen Zielinhalt liegt außerhalb dieses Repos.
- Das PWA-Manifest verweist auf `/icons/icon-192.png` und `/icons/icon-512.png`; Icon-Assets werden in diesem Repository derzeit nicht versioniert.

## 🧯 Fehlerbehebung

- Chrome-Anbindung schlägt fehl:
  - Stelle sicher, dass Chrome mit `--remote-debugging-port=9333` (oder passendem `--debugger-port`) gestartet wurde.
  - Prüfe `GET /api/status` auf `devtools_ready: true`.
- Wiederholte Login-Abfragen:
  - Verwende ein persistentes `--user-data-dir` und vermeide zufällige Profilpfade.
- Cloudflare-/Login-Flow kommt nicht voran:
  - Nutze non-headless (`--no-headless`) und erhöhe `--login-timeout`.
- Media-Attach macht nichts:
  - Prüfe, ob der Dateipfad auf der Server-Maschine existiert, und nutze bei Unsicherheit `/api/upload` + den zurückgegebenen Pfad.
- Storyboard-Media-Attach schlägt fehl:
  - Versuche `POST /api/storyboard-attach-only` oder öffne zuerst Storyboard, dann `/api/storyboard-media`.
- Resolution-Control in der PWA nicht verfügbar:
  - `High` resolution ist nur verfügbar, wenn das model `Sora 2 Pro` ist.
- Falsche chromedriver-Probleme:
  - Entferne manuell gepinnten chromedriver aus deinem Shell-Profil; dieses Projekt lässt Selenium Manager absichtlich passende Versionen wählen.

## 🧭 Roadmap

Geplante/wahrscheinliche nächste Verbesserungen:
- Automatisierte Tests für Selector-Stabilität und API-Handler hinzufügen.
- Lint-/Format-Tooling und CI-Workflows hinzufügen.
- Versionierte PWA-Icon-Assets und robustere Offline-Caching-Strategie hinzufügen.
- Formale mehrsprachige README-Dateien unter `i18n/` hinzufügen.
- Packaging-Metadaten für einfachere Installation hinzufügen.

## 🤝 Mitwirken

Beiträge sind willkommen.

Empfohlener Ablauf:
1. Fork erstellen und einen Feature-Branch anlegen.
2. Änderungen klein halten und Reproduktions-/Nutzungshinweise für UI-Automatisierungsänderungen hinzufügen.
3. Flows manuell mit einer echten angebundenen Chrome-Sitzung validieren.
4. PR mit Details zum Verhalten vorher/nachher öffnen.

Wenn du Selectoren oder Interaktionslogik änderst, füge konkreten Sora-UI-Kontext hinzu, damit Regressionen leichter triagiert werden können.

## ❤️ Support / Sponsoring

Funding-Links aus `.github/FUNDING.yml`:
- GitHub Sponsors: https://github.com/sponsors/lachlanchen
- Projektlinks: https://lazying.art, https://chat.lazying.art, https://onlyideas.art

## 🙏 Danksagungen

- Selenium und Selenium Manager für Browser-Automatisierung und Driver-Auflösung.
- Tornado für den leichtgewichtigen asynchronen HTTP/WebSocket-Control-Service.
- Pillow und `pillow-heif` für lokale Bildkonvertierung/Vorschau-Unterstützung.

## 🧱 Known Good Build

Wenn du eine stabile Basis benötigst, die garantiert, dass Storyboard-Media-Attach end-to-end funktioniert (einschließlich der Buttons Open Storyboard / Attach Current Path und des kombinierten Apply-Flows), sieh dir folgenden Commit an:

`c6683ed6d9ee0ac110536352867a26a966e3e275`

## 📄 Lizenz

In diesem Repository-Snapshot ist derzeit keine Lizenzdatei vorhanden (in diesem Entwurf geprüft am **February 28, 2026**).

Annahme: Alle Rechte verbleiben beim Repository-Eigentümer, bis eine Lizenz hinzugefügt wird. Wenn das nicht beabsichtigt ist, füge eine `LICENSE`-Datei hinzu und aktualisiere diesen Abschnitt.
