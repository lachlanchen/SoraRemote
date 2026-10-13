[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://lazying.art)

# SoraRemote

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20WSL-6c757d)
![Server](https://img.shields.io/badge/Server-Tornado%20API-0EA5E9)
![Frontend](https://img.shields.io/badge/Frontend-PWA-10B981)
![Status](https://img.shields.io/badge/Status-Experimental-F59E0B)
![Control%20Modes](https://img.shields.io/badge/Control%20Modes-CLI%20%7C%20REST%20%7C%20PWA-0EA5E9)
![Runtime](https://img.shields.io/badge/Runtime-Linux%20%7C%20macOS%20%7C%20WSL-6B7280)

SoraRemote는 Sora 웹 UI를 자동화하기 위한 가벼운 Python + Selenium 툴킷입니다.

하나의 자동화 워크플로를 위해 세 가지 보완적인 실행 모드를 지원합니다.
1. 프롬프트 입력과 UI 조작을 위한 **CLI 자동화 에이전트** (`agents/sora_agent.py`).
2. 미디어 후보를 찾고 다운로드하는 **CLI 다운로더** (`agents/sora_download.py`).
3. API 기반 브라우저 오케스트레이션을 위한 **Tornado + PWA 제어면** (`server/app.py` + `pwa/`).

현재 README의 내용은 본질적인 운영 지침을 유지하면서 가독성을 위해 재구성되었습니다.

## 🚀 Quick Access

| 목표 | 진입점 | 주 사용처 |
| --- | --- | --- |
| 스크립트 프롬프트 실행 | `agents/sora_agent.py` | CLI 또는 래퍼 스크립트로 작곡 동작 제어 |
| 생성된 미디어 수집 | `agents/sora_download.py` | 후보를 탐색해 로컬로 저장 |
| 원격 제어 | `server/app.py` + `pwa/` | REST/WebSocket + 브라우저 대시보드로 제어 |

## ✨ Overview

핵심 설계:
- DevTools 원격 디버깅(기본 `9333` 포트)을 통해 지속 Chrome 세션에 연결
- 브라우저 프로필 상태를 재사용해 로그인/세션 연속성 유지
- 핵심 컴포저 동작 자동화(입력, plus/미디어 첨부, storyboard, settings, create)
- 동일한 동작을 REST + WebSocket 로그로 노출하여 로컬 PWA 컨트롤러에서 조작 가능

### Workflow snapshot

| 워크플로 | 진입점 | 주 사용처 |
| --- | --- | --- |
| CLI Agent | `agents/sora_agent.py` | 프롬프트 입력, 버튼 클릭, compose 흐름 자동화 |
| CLI Downloader | `agents/sora_download.py` | 다운로드 가능한 미디어 탐색 및 로컬 저장 |
| API + PWA | `server/app.py` + `pwa/` | 브라우저 기반 원격 제어 및 시각적 오케스트레이션 |

## ✅ Features

- 재사용 가능한 프로필로 Chrome attach/시작 흐름 지원 (`--debugger-port`, `--start-chrome`, `--user-data-dir`).
- 주요 컨트롤의 안전 클릭/강제 클릭 지원 (`plus`, `storyboard`, `settings`, `create`, `profile`).
- 셀렉터 폴백 동작이 포함된 프롬프트 입력.
- 파일 경로 기반 미디어 첨부와 DataTransfer 주입.
- 스토리보드 장면 채우기 + 스크립트 업데이트 + 스토리보드 전용 미디어 첨부.
- 모델/방향/길이/해상도 설정 자동화.
- 브라우저 쿠키를 사용하는 별도 다운로드 후보 탐색 + fetch 흐름.
- Tornado REST API와 실시간 WebSocket 디버그 스트림.
- 업로드, 미리보기, 세부 제어를 갖춘 설치형(local installable) PWA.

## 🗂️ Project Structure

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

## 🧩 Prerequisites

- Python 3.10+ (권장).
- Chrome/Chromium 설치 및 실행 가능.
- 로그인 또는 대화형 UI가 필요할 때 비-headless 사용을 위한 디스플레이 (`--no-headless`).
- 연결된 Chrome 프로필에서 Sora 계정 접근 권한.

## 📦 Installation

영문 원본 기준의 기존 설치 흐름:

```bash
conda activate agent
pip install -r requirements.txt
```

`requirements.txt`의 종속성:

| 패키지 | 버전 사양 |
| --- | --- |
| `selenium` | `>=4.17.2` |
| `tornado` | `>=6.4` |
| `Pillow` | `>=9.4.0` |
| `pillow-heif` | `>=0.16.0` |

## 🚀 사용법

### Quick start (CLI agent)

빠른 시작 (관리되는 브라우저에서 Sora 실행):

```bash
python agents/sora_agent.py
```

지속 세션으로 Chrome에 연결 (Sora 권장):

```bash
python -m agents.sora_agent --debugger-port 9333 --start-chrome --no-headless --login-timeout 600 --text "A sunset over Tokyo, cinematic."
```

참고:
- Chrome 창이 Sora 페이지에서 열립니다. 로그인으로 리다이렉트되면 로그인하세요. 스크립트는 로그인 완료를 기다린 뒤 프롬프트를 입력합니다.
- 동일한 로그인 세션을 재사용하려면 고정 프로필 경로를 전달하세요:

```bash
python -m agents.sora_agent --debugger-port 9333 --start-chrome --no-headless --user-data-dir "$HOME/chrome_sora_profile_9333"
```

### 핵심 CLI 옵션 (`agents/sora_agent.py`)

- `--url` 대상 페이지 (기본값: `https://sora.chatgpt.com/explore`).
- `--debugger-port`: `--remote-debugging-port=PORT`로 시작된 기존 Chrome에 attach.
- `--start-chrome`: `--debugger-port`와 함께 사용하면 Chrome을 자동 실행( `--user-data-dir` 지정).
- `--no-headless`: 화면 표시 브라우저 실행, 로그인과 Cloudflare 처리에 필요.
- `--selector`: 입력창을 찾는 CSS 셀렉터(기본값은 Sora composer textarea에 맞춤).
- `--text`: 입력창에 넣을 텍스트.
- `--chrome-binary`: Chrome/Chromium 경로를 명시.
- `--action`: UI 액션 `list`, `plus`, `storyboard`, `settings`, `create`, `profile`.
- `--force-click`: 요소가 비활성처럼 보이더라도 클릭 강제 실행.
- `--login-timeout`: 수동 인증 완료 대기 시간.

드라이버 처리:
- 에이전트는 실행 전에 `PATH`의 오래된 `chromedriver`를 제거합니다.
- Selenium Manager가 설치된 Chrome에 맞는 드라이버를 자동으로 해결합니다.

### CLI examples (UI controls)

일반 컨트롤 목록 확인 및 클릭:

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action list --action storyboard --action settings --action plus
```

Create video 버튼을 강제로 클릭 (비활성 상태여도):

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action create --force-click
```

필요하면 profile/settings를 열고 수동으로 이동:

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action list --action profile
```

`profile`이 탐지되지 않으면, 보통 `settings` 버튼이 같은 메뉴를 엽니다.

### Downloader flow

핸들러 스크립트로 비디오 탐색 및 다운로드:

- 드라이 런(후보 목록만 조회): `./bin/sora_download.sh --dry-run`
- 최대 2개 파일을 `./downloads/sora`에 저장: `./bin/sora_download.sh --max 2`
- 출력 폴더 변경: `OUT_DIR=$HOME/Videos/sora ./bin/sora_download.sh --max 1`

직접 모듈 실행도 가능합니다: `python -m agents.sora_download ...`.

## 🌐 Control Server + PWA

Tornado 서버 실행:

```bash
python server/app.py
# listens on http://0.0.0.0:8791 and serves the PWA at /
```

기본 동작:
- 기본 포트 `9333`의 원격 디버깅 Chrome을 재사용합니다.
- `SORA_UPLOADS_DIR`이 설정되지 않은 경우 업로드를 `./uploads`에 저장합니다.

### Key endpoints

모든 엔드포인트는 현재 연결된 Chrome(기본 디버거 포트 `9333`)을 대상으로 동작합니다.

| Method | Path | Payload | Description |
| --- | --- | --- | --- |
| `GET` | `/api/status` | none | DevTools 준비 상태와 활성 포트를 반환합니다. |
| `POST` | `/api/open` | `{ url? }` | 연결된 Chrome 탭을 지정 URL로 이동합니다(기본값: Sora Explore). |
| `GET` | `/api/actions` | none | 버튼/컨트롤 상태(`found`/`displayed`/`disabled`) 메타데이터를 검사합니다. |
| `POST` | `/api/click` | `{ key, force? }` | `key ∈ {plus, storyboard, settings, create, profile}` 중 하나의 컨트롤을 클릭합니다. |
| `POST` | `/api/type` | `{ text, selector?, url? }` | composer selector에 프롬프트 텍스트를 입력합니다. |
| `POST` | `/api/compose` | `{ text, click_create? }` | compose 페이지를 열고 텍스트를 입력한 뒤(선택적으로) create를 클릭합니다. |
| `POST` | `/api/attach` | `{ path, click_plus? }` | DataTransfer 주입으로 미디어 업로드; 기존 미디어는 자동 정리(`click_plus` 기본값 `false`). |
| `POST` | `/api/describe` | `{ text }` | “Optionally describe your video…” 텍스트영역을 채웁니다. |
| `POST` | `/api/script-updates` | `{ text }` | “Describe updates to your script…” 필드를 채웁니다. |
| `POST` | `/api/storyboard` | `{ scenes: ["scene 1", ...], script_updates?: "...", media_path?: "..." }` | storyboard를 열고 씬 텍스트영역을 채우며, 필요 시 스크립트 업데이트와 storyboard 미디어를 적용합니다. |
| `POST` | `/api/storyboard-media` | `{ path }` | storyboard가 이미 보이는 상태에서 storyboard 전용 업로더로 미디어를 첨부합니다. |
| `POST` | `/api/storyboard-attach-only` | `{ path }` | storyboard가 열려 있는지 먼저 보장한 뒤 미디어를 첨부합니다. |
| `POST` | `/api/settings` | `{ model?, orientation?, duration?, resolution? }` | settings을 열고 선택값을 적용하며 응답에 적용된 라벨을 반환합니다. |
| `POST` | `/api/upload` | multipart form data | 로컬 파일(들)을 서버 업로드 디렉터리에 저장하고 서버 측 경로를 반환합니다. |
| `POST` | `/api/preview` | multipart form data | 이미지를 PNG 미리보기로 변환(HEIC/HEIF/AVIF 폴백에 유용). |
| `GET` | `/ws` | WebSocket | 액션/디버그 이벤트를 실시간 스트리밍. |

### PWA controls

`server/app.py` 실행 후 `http://0.0.0.0:8791`(또는 선택한 호스트)로 접속하세요.

기존 구현의 하이라이트:
- 파일 선택기에서 업로드하거나 경로를 붙여 넣은 뒤 **Plus** 버튼을 눌러 시스템 파일 대화상자를 다시 열지 않고 첨부
- 전용 "Media description" 상자에서 미디어 설명 입력
- **Set Model**, **Set Orientation**, **Set Duration**, **Set Resolution**, 스크립트 업데이트에 대한 독립 제어
- storyboard 씬/스크립트 업데이트/storyboard 패널 열기/현재 storyboard 경로 첨부 제어
- API 호출과 Sora가 반환한 값(예: 선택한 모델/길이)을 보여주는 실시간 디버그 로그

## ⚙️ Configuration

### Environment variables

`server/app.py`에서 읽는 변수:
- `SORA_DEBUGGER_PORT` (기본값 `9333`)
- `SORA_USER_DATA_DIR` (기본값 `~/chrome_sora_profile_<port>` )
- `SORA_DISPLAY` (선택 X 디스플레이)
- `SORA_API_PORT` (기본값 `8791`)
- `SORA_URL` (기본값 `https://sora.chatgpt.com/explore`)
- `SORA_UPLOADS_DIR` (선택 업로드 디렉터리 오버라이드)

`agents/sora_agent.py` 또한 지원:
- `CHROME_BINARY` (`--chrome-binary` 미지정 시)

래퍼 스크립트 지원 변수:
- `PORT`, `SORA_PROFILE_DIR`, `TIMEOUT`, `LOGIN_TIMEOUT` (`bin/sora_type.sh`)
- `PORT`, `SORA_PROFILE_DIR`, `OUT_DIR` (`bin/sora_download.sh`)

## 🧪 Examples

### End-to-end API example (curl)

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

### Media upload + attach via API

```bash
# Upload file and get server path
curl -s -X POST http://127.0.0.1:8791/api/upload -F 'file=@/absolute/path/to/input.jpg'

# Then attach using returned path
curl -s -X POST http://127.0.0.1:8791/api/attach \
  -H 'Content-Type: application/json' \
  -d '{"path":"/absolute/or/server-returned/path.jpg","click_plus":false}'
```

## 🛠️ Development Notes

- 현재 패키지화된 모듈은 없습니다(`pyproject.toml`/`setup.py` 미존재).
- 현재 저장소 스냅샷에는 CI/test/lint 파이프라인이 없습니다.
- `selenium_template`은 `../auto-publish/`를 가리키는 symlink입니다. 대상 내용은 이 저장소 외부에 있습니다.
- PWA manifest는 `/icons/icon-192.png`와 `/icons/icon-512.png`를 참조하지만, 아이콘 에셋은 현재 이 저장소에 추적되어 있지 않습니다.

## 🧯 Troubleshooting

- Chrome attach 실패:
  - Chrome이 `--remote-debugging-port=9333`(또는 일치하는 `--debugger-port`)로 시작되었는지 확인하세요.
  - `GET /api/status`에서 `devtools_ready: true`를 확인하세요.
- 로그인 프롬프트가 반복됨:
  - 고정된 `--user-data-dir`를 사용하고 무작위 프로필 경로는 피하세요.
- Cloudflare/로그인 흐름이 진행되지 않음:
  - 비 headless(`--no-headless`)로 실행하고 `--login-timeout`을 늘려 보세요.
- 미디어 첨부가 동작하지 않음:
  - 파일 경로가 서버 장비에 존재하는지 확인하고 확신이 없으면 `/api/upload` 후 반환 경로를 사용하세요.
- 스토리보드 미디어 첨부 실패:
  - `POST /api/storyboard-attach-only`를 시도하거나 먼저 storyboard를 열고 `/api/storyboard-media`를 호출하세요.
- PWA에서 해상도 제어를 사용할 수 없음:
  - `High` 해상도는 모델이 `Sora 2 Pro`일 때만 활성화됩니다.
- 잘못된 chromedriver 문제:
  - 셸 프로필에 수동 지정한 chromedriver를 제거하세요. 이 프로젝트는 Selenium Manager가 일치 버전을 선택하도록 의도되어 있습니다.

## 🧭 Roadmap

예정/예상되는 다음 개선 사항:
- selector 안정성 및 API 핸들러용 자동 테스트 추가
- lint/format 도구 및 CI 워크플로우 추가
- PWA 아이콘 에셋 추적 및 더 강한 오프라인 캐싱 전략 추가
- `i18n/` 아래 정식 다국어 README 파일 추가
- 설치를 쉽게 하는 패키징 메타데이터 추가

## 🤝 Contributing

기여를 환영합니다.

권장 프로세스:
1. 포크(Fork)하고 기능 브랜치를 생성하세요.
2. 변경 범위를 한정하고 UI 자동화 변경 시 재현/사용 노트(reroduction/usage notes)를 포함하세요.
3. 실제 연결된 Chrome 세션에서 수동으로 흐름을 검증하세요.
4. 변경 전후 동작 상세를 포함해 PR을 생성하세요.

셀렉터나 상호작용 로직을 변경했다면, 회귀 분석이 쉬워지도록 구체적인 Sora UI 맥락을 반드시 포함하세요.

## 🙏 Acknowledgements

- 브라우저 자동화와 드라이버 해석을 제공하는 Selenium 및 Selenium Manager
- 가벼운 비동기 HTTP/WebSocket 제어 서비스인 Tornado
- 로컬 이미지 변환/미리보기 지원을 위한 Pillow 및 `pillow-heif`

## 🧱 Known Good Build

스토리보드 미디어 첨부가 Open Storyboard / Attach Current Path 버튼과 결합 Apply 흐름까지 포함되어 엔드투엔드로 안정 동작하는 기준점이 필요하다면 다음 커밋을 확인하세요:

`c6683ed6d9ee0ac110536352867a26a966e3e275`

## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |

## 📄 License

현재 저장소 스냅샷에는 라이선스 파일이 없습니다(이 초안의 확인 시점: **February 28, 2026**).

모든 권리는 별도의 라이선스가 추가되기 전까지 저장소 소유자에게 있습니다. 의도에 맞지 않는다면 `LICENSE` 파일을 추가하고 이 섹션을 업데이트하세요.
