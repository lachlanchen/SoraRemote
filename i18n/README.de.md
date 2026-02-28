[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# SoraRemote

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20WSL-6c757d)
![Server](https://img.shields.io/badge/Server-Tornado%20API-0EA5E9)
![Frontend](https://img.shields.io/badge/Frontend-PWA-10B981)
![Status](https://img.shields.io/badge/Status-Experimental-F59E0B)
![Control%20Modes](https://img.shields.io/badge/Control%20Modes-CLI%20%7C%20REST%20%7C%20PWA-0EA5E9)
![Runtime](https://img.shields.io/badge/Runtime-Linux%20%7C%20macOS%20%7C%20WSL-6B7280)

SoraRemote ist ein leichtgewichtiges Python-+Selenium-Toolkit zur Automatisierung der Sora-Web-UI.

Es unterstützt drei komplementäre Ausführungsmodi für einen Automatisierungsablauf:
1. **CLI-Automatisierungs-Agent** (`agents/sora_agent.py`) für das Tippen von Prompts und UI-Aktionen.
2. **CLI-Downloader** (`agents/sora_download.py`) zum Erkennen und Herunterladen von Medienkandidaten.
3. **Tornado + PWA-Control-Plane** (`server/app.py` + `pwa/`) für browserseitige Orchestrierung über APIs.

Der aktuelle README-Inhalt wird als operative Leitlinie beibehalten und zur besseren Lesbarkeit neu strukturiert.

## 🚀 Schnellzugriff

| Ziel | Einstiegspunkt | Hauptverwendung |
| --- | --- | --- |
| Skriptgesteuerte Prompts ausführen | `agents/sora_agent.py` | Komponieraktionen per CLI oder Wrapper-Skript steuern |
| Generierte Medien abrufen | `agents/sora_download.py` | Kandidaten lokal entdecken und speichern |
| Fernsteuerung | `server/app.py` + `pwa/` | Steuerung über REST/WebSocket + Browser-Dashboard |

## ✨ Überblick

Kern-Design:
- Anbindung an eine persistente Chrome-Sitzung via DevTools-Remote-Debugging (Standardport `9333`).
- Wiederverwendung des Browser-Profils zur Erhaltung von Login-/Sitzungszuständen.
- Automatisierung zentraler Komponieraktionen (Tippen, Plus/Medien anhängen, Storyboard, Einstellungen, Erstellen).
- Exponierung derselben Aktionen über REST + WebSocket-Logs für einen lokalen PWA-Controller.

### Ablaufübersicht

| Ablauf | Einstiegspunkt | Hauptverwendung |
| --- | --- | --- |
| CLI-Agent | `agents/sora_agent.py` | Prompts eingeben, Steuerelemente klicken, Erstellungsfluss automatisieren |
| CLI-Downloader | `agents/sora_download.py` | Herunterladbare Medien erkennen und lokal speichern |
| API + PWA | `server/app.py` + `pwa/` | Remote-Steuerung und visuelle Orchestrierung aus dem Browser |

## ✅ Funktionen

- Chrome-Ankopplungs-/Startablauf mit wiederverwendbarem Profil (`--debugger-port`, `--start-chrome`, `--user-data-dir`).
- Sicheres oder erzwungenes Klicken bei wichtigen Steuerelementen (`plus`, `storyboard`, `settings`, `create`, `profile`).
- Texteingabe mit Fallback-Verhalten für Selektoren.
- Medienanhang per Dateipfad mit DataTransfer-Injektion.
- Storyboard-Szenarien ausfüllen + Skriptänderungen + storyboard-spezifischen Medienanhang.
- Einstellungs-Automatisierung für Modell/Ausrichtung/Dauer/Auflösung.
- Getrennter Flow für Entdecken und Abrufen von Downloads mit Browser-Cookies.
- Tornado REST API und Live WebSocket-Debug-Stream.
- Installierbare lokale PWA mit Upload-, Vorschau- und fein granularen Steuerelementen.

## 🗂️ Projektstruktur

```text
SoraRemote/
├─ README.md
├─ requirements.txt
├─ .github/
│  └─ FUNDING.yml
├─ agents/
│  ├─ __init__.py
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
│  ├─ README.ar.md
│  ├─ README.de.md
│  ├─ README.es.md
│  ├─ README.fr.md
│  ├─ README.ja.md
│  ├─ README.ko.md
│  ├─ README.ru.md
│  ├─ README.vi.md
│  ├─ README.zh-Hans.md
│  └─ README.zh-Hant.md
├─ uploads/
│  └─ .gitkeep
└─ selenium_template -> ../auto-publish/ (symlink)
```

## 🧩 Voraussetzungen

- Python 3.10+ (empfohlen).
- Installiertes und ausführbares Chrome/Chromium.
- Ein Display für nicht-headless Nutzung (`--no-headless`), wenn Login oder interaktive UI erforderlich ist.
- Zugriff auf ein Sora-Konto im angehängten Chrome-Profil.

## 📦 Installation

Bekannte Installationsanleitung aus dem Original-README:

```bash
conda activate agent
pip install -r requirements.txt
```

Abhängigkeiten in `requirements.txt`:

| Paket | Versionsangabe |
| --- | --- |
| `selenium` | `>=4.17.2` |
| `tornado` | `>=6.4` |
| `Pillow` | `>=9.4.0` |
| `pillow-heif` | `>=0.16.0` |

## 🚀 Verwendung

### Schnellstart (CLI-Agent)

Kurzer Start (öffnet Sora in einem verwalteten Browser):

```bash
python agents/sora_agent.py
```

Mit persistenter Sitzung an Chrome anfügen (für Sora empfohlen):

```bash
python -m agents.sora_agent --debugger-port 9333 --start-chrome --no-headless --login-timeout 600 --text "A sunset over Tokyo, cinematic."
```

Hinweise:
- Ein Chrome-Fenster öffnet sich auf der Sora-Seite. Falls eine Weiterleitung zum Login erfolgt, anmelden Sie sich; das Skript wartet anschließend und tippt dann Ihren Prompt.
- Um dasselbe Login wiederzuverwenden, verwenden Sie einen festen Profilpfad:

```bash
python -m agents.sora_agent --debugger-port 9333 --start-chrome --no-headless --user-data-dir "$HOME/chrome_sora_profile_9333"
```

### Wichtige CLI-Optionen (`agents/sora_agent.py`)

- `--url` Zielseite (Standard: `https://sora.chatgpt.com/explore`).
- `--debugger-port` für das Anfügen an ein bestehendes Chrome, gestartet mit `--remote-debugging-port=PORT`.
- `--start-chrome` startet zusammen mit `--debugger-port` Chrome automatisch für Sie (mit `--user-data-dir`).
- `--no-headless` für ein sichtbares Browserfenster; erforderlich für Login und Cloudflare.
- `--selector` CSS-Selektor zum Auffinden des Eingabefelds (Standard entspricht der Sora-Composer-Textarea).
- `--text` Text, der in das Eingabefeld geschrieben wird.
- `--chrome-binary` gibt explizit einen Chrome/Chromium-Pfad an.
- `--action` UI-Aktionen: `list`, `plus`, `storyboard`, `settings`, `create`, `profile`.
- `--force-click` klickt auch, wenn ein Element als deaktiviert erscheint.
- `--login-timeout` Wartezeitfenster für das manuelle Abschließen der Authentifizierung.

Driver-Verhalten:
- Der Agent entfernt veraltete `chromedriver`-Einträge aus `PATH` vor dem Start.
- Selenium Manager löst danach automatisch einen passenden Treiber zur installierten Chrome-Version auf.

### CLI-Beispiele (UI-Steuerung)

Gemeinsame Steuerelemente auflisten und anklicken:

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action list --action storyboard --action settings --action plus
```

Erzwingt das Klicken auf den Erstellen-Button (auch wenn deaktiviert):

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action create --force-click
```

Profil/Einstellungen öffnen und bei Bedarf manuell navigieren:

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action list --action profile
```

Wenn `profile` nicht erkannt wird, öffnet die Schaltfläche `settings` normalerweise dasselbe Menü.

### Downloader-Ablauf

Entdecken und herunterladen von Videos mit dem Wrapper-Skript:

- Trockentest (nur Kandidaten auflisten): `./bin/sora_download.sh --dry-run`
- Bis zu 2 Dateien nach `./downloads/sora` herunterladen: `./bin/sora_download.sh --max 2`
- Ausgabeverzeichnis ändern: `OUT_DIR=$HOME/Videos/sora ./bin/sora_download.sh --max 1`

Direkte Modulanwendung ist ebenfalls möglich mit `python -m agents.sora_download ...`.

## 🌐 Control Server + PWA

Tornado-Server starten:

```bash
python server/app.py
# listens on http://0.0.0.0:8791 and serves the PWA at /
```

Standardmäßig:
- Reicht Chrome auf Remote-Debugging-Port `9333` wiederverwendet.
- Speichert Uploads in `./uploads`, sofern `SORA_UPLOADS_DIR` nicht gesetzt ist.

### Wichtige Endpunkte

Alle Endpunkte arbeiten gegen das aktuell angehängte Chrome (Standard: Debugger-Port `9333`).

| Methode | Pfad | Nutzlast | Beschreibung |
| --- | --- | --- | --- |
| `GET` | `/api/status` | none | Gibt DevTools-Bereitschaftsstatus und den aktiven Port zurück. |
| `POST` | `/api/open` | `{ url? }` | Öffnet den angeschlossenen Chrome-Tab auf der angegebenen URL (Standard ist Sora Explore). |
| `GET` | `/api/actions` | none | Prüft den Zustand der Schaltflächen/Steuerelemente (found/displayed/disabled-Metadaten). |
| `POST` | `/api/click` | `{ key, force? }` | Betätigt eine Steuerung, wobei `key ∈ {plus, storyboard, settings, create, profile}`.
| `POST` | `/api/type` | `{ text, selector?, url? }` | Schreibt Prompteingabetext in den Composer-Selektor. |
| `POST` | `/api/compose` | `{ text, click_create? }` | Öffnet die Compose-Seite, schreibt Text und klickt optional auf Erstellen. |
| `POST` | `/api/attach` | `{ path, click_plus? }` | Lädt Medien via DataTransfer-Injektion hoch; vorhandene Medien werden automatisch entfernt (`click_plus` standardmäßig `false`). |
| `POST` | `/api/describe` | `{ text }` | Füllt die Textarea „Optionally describe your video…“ aus. |
| `POST` | `/api/script-updates` | `{ text }` | Füllt das Feld „Describe updates to your script…“ aus. |
| `POST` | `/api/storyboard` | `{ scenes: ["scene 1", ...], script_updates?: "...", media_path?: "..." }` | Öffnet Storyboard, füllt Szenen-Textareas und wendet optional Skriptänderungen sowie Storyboard-Medien an. |
| `POST` | `/api/storyboard-media` | `{ path }` | Hängt Medien an den bereits sichtbaren Storyboard-Uploader an. |
| `POST` | `/api/storyboard-attach-only` | `{ path }` | Stellt sicher, dass Storyboard geöffnet ist, und hängt dann Medien an. |
| `POST` | `/api/settings` | `{ model?, orientation?, duration?, resolution? }` | Öffnet die Einstellungen und wendet ausgewählte Werte an; die Antwort enthält die angewendeten Labels. |
| `POST` | `/api/upload` | multipart form data | Speichert lokale Datei(en) im Server-Upload-Verzeichnis und gibt serverseitige Pfade zurück. |
| `POST` | `/api/preview` | multipart form data | Wandelt Bild zu PNG-Vorschau (nützlich für HEIC/HEIF/AVIF-Fallback in der UI). |
| `GET` | `/ws` | WebSocket | Sendet Aktionen/Debug-Ereignisse als Stream. |

### PWA-Steuerung

Öffnen Sie `http://0.0.0.0:8791` (oder Ihren gewählten Host), nachdem Sie `server/app.py` gestartet haben.

Wichtige Punkte aus der aktuellen Implementierung:
- Medien über Dateiauswahl oder durch Einfügen eines Pfads hochladen, anschließend auf **Plus** klicken, um anzuhängen, ohne Dateidialoge des Systems erneut zu öffnen.
- Medienbeschreibung im dedizierten Feld „Media description“ eintragen.
- Unabhängige Steuerelemente für **Set Model**, **Set Orientation**, **Set Duration**, **Set Resolution** sowie Skriptänderungen.
- Storyboard-Steuerelemente für Szenen, Skriptaktualisierungen, Storyboard-Panel öffnen und aktuellen Storyboard-Pfad anhängen.
- Live-Debug-Log, das API-Aufrufe und von Sora zurückgelieferte Werte anzeigt (beispielsweise gewähltes Modell/Dauer).

## ⚙️ Konfiguration

### Umgebungsvariablen

`server/app.py` liest:
- `SORA_DEBUGGER_PORT` (Standard `9333`)
- `SORA_USER_DATA_DIR` (Standard `~/chrome_sora_profile_<port>`)
- `SORA_DISPLAY` (optional X-Display)
- `SORA_API_PORT` (Standard `8791`)
- `SORA_URL` (Standard `https://sora.chatgpt.com/explore`)
- `SORA_UPLOADS_DIR` (optionaler Override für Upload-Verzeichnis)

`agents/sora_agent.py` unterstützt zusätzlich:
- `CHROME_BINARY` (falls `--chrome-binary` nicht gesetzt ist)

Wrapper-Skripte unterstützen:
- `PORT`, `SORA_PROFILE_DIR`, `TIMEOUT`, `LOGIN_TIMEOUT` (`bin/sora_type.sh`)
- `PORT`, `SORA_PROFILE_DIR`, `OUT_DIR` (`bin/sora_download.sh`)

## 🧪 Beispiele

### Ende-zu-Ende-API-Beispiel (curl)

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

### Medien-Upload + Anfügen via API

```bash
# Upload file and get server path
curl -s -X POST http://127.0.0.1:8791/api/upload -F 'file=@/absolute/path/to/input.jpg'

# Then attach using returned path
curl -s -X POST http://127.0.0.1:8791/api/attach \
  -H 'Content-Type: application/json' \
  -d '{"path":"/absolute/or/server-returned/path.jpg","click_plus":false}'
```

## 🛠️ Entwicklungshinweise

- Aktuell gibt es kein Paket-Modul (`pyproject.toml`/`setup.py` sind nicht vorhanden).
- Aktuell ist keine CI/Test/Lint-Pipeline in diesem Repository-Snapshot enthalten.
- `selenium_template` ist ein Symlink auf `../auto-publish/`; der Zielinhalt liegt außerhalb dieses Repos.
- Das PWA-Manifest verweist auf `/icons/icon-192.png` und `/icons/icon-512.png`; Icon-Assets werden hier im Repository derzeit nicht mitverfolgt.

## 🧯 Fehlerbehebung

- Chrome kann nicht angehängt werden:
  - Stellen Sie sicher, dass Chrome mit `--remote-debugging-port=9333` gestartet wurde (oder mit passendem `--debugger-port`).
  - Prüfen Sie `GET /api/status` auf `devtools_ready: true`.
- Wiederholte Login-Eingabefenster:
  - Verwenden Sie einen persistenten `--user-data-dir` und vermeiden Sie wechselnde Profilpfade.
- Cloudflare/Login-Flow läuft nicht weiter:
  - Starten Sie non-headless (`--no-headless`) und erhöhen Sie `--login-timeout`.
- Medienanhang hat keine Wirkung:
  - Stellen Sie sicher, dass der Dateipfad auf dem Server vorhanden ist und nutzen Sie im Zweifel `/api/upload` + zurückgegebenen Pfad.
- Storyboard-Medienanhang schlägt fehl:
  - Versuchen Sie `POST /api/storyboard-attach-only` oder öffnen Sie zuerst Storyboard und danach `/api/storyboard-media`.
- Auflösungseinstellung in der PWA nicht verfügbar:
  - `High`-Auflösung ist nur aktiv, wenn das Modell `Sora 2 Pro` ausgewählt ist.
- Falscher Chromedriver:
  - Entfernen Sie manuell festgelegte `chromedriver` aus Ihrem Shell-Profil; dieses Projekt setzt bewusst auf Selenium Manager für passende Versionen.

## 🧭 Roadmap

Geplante/zu erwartende nächste Verbesserungen:
- Tests für Selektorstabilität und API-Handler automatisieren.
- Lint-/Format-Tools und CI-Workflows ergänzen.
- Gecachte PWA-Icons nachtragen und bessere Offline-Caching-Strategie implementieren.
- Formale mehrsprachige README-Dateien unter `i18n/` hinzufügen.
- Installations-Metadaten für einfachere Installation ergänzen.

## 🤝 Mitwirken

Beiträge sind willkommen.

Vorgeschlagener Ablauf:
1. Erstellen Sie einen Fork und einen Feature-Branch.
2. Halten Sie Änderungen fokussiert und fügen Sie bei UI-Automatisierungsänderungen Reproduktions-/Nutzungshinweise hinzu.
3. Validieren Sie die Abläufe manuell mit einer echten angebundenen Chrome-Sitzung.
4. Öffnen Sie eine PR mit Vorher-/Nachher-Verhaltensdetails.

Wenn Sie Selektoren oder Interaktionslogik ändern, fügen Sie konkrete Sora-UI-Kontexte hinzu, damit Regressionen leichter triagiert werden können.

## 🙏 Danksagungen

- Selenium und Selenium Manager für Browserautomatisierung und Treiberauflösung.
- Tornado für den leichten asynchronen HTTP/WebSocket-Kontrollservice.
- Pillow und `pillow-heif` für lokale Bildkonvertierung/Vorschau.

## 🧱 Bekannte stabile Version

Wenn Sie eine stabile Basis benötigen, die sicherstellt, dass Storyboard-Medienanhang end-to-end funktioniert (einschließlich der Schaltflächen Open Storyboard / Attach Current Path und des kombinierten Apply-Flows), nutzen Sie den Commit:

`c6683ed6d9ee0ac110536352867a26a966e3e275`

## 📄 Lizenz

In diesem Repository-Snapshot liegt derzeit keine Lizenzdatei vor (in diesem Entwurf geprüft am **28. Februar 2026**).

Voraussetzung: Alle Rechte verbleiben beim Repository-Eigentümer, bis eine Lizenz hinzugefügt wird. Wenn dies nicht beabsichtigt ist, fügen Sie eine `LICENSE`-Datei hinzu und aktualisieren Sie diesen Abschnitt.


## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |
