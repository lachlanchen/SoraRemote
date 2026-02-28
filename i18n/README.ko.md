[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


Language: **Korean** | i18n directory: [`i18n/`](../i18n/) (사용 가능, 번역 파일을 순차적으로 추가 중)

# SoraRemote

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20WSL-6c757d)
![Server](https://img.shields.io/badge/Server-Tornado%20API-0EA5E9)
![Frontend](https://img.shields.io/badge/Frontend-PWA-10B981)
![Status](https://img.shields.io/badge/Status-Experimental-F59E0B)

SoraRemote는 Sora 웹 UI 자동화를 위한 가벼운 Python + Selenium 툴킷입니다.

다음의 3가지 워크플로를 상호 보완적으로 지원합니다.
1. 프롬프트 입력 및 UI 제어를 위한 CLI 자동화 에이전트 (`agents/sora_agent.py`)
2. 미디어 후보 탐색 및 다운로드를 위한 CLI 다운로더 (`agents/sora_download.py`)
3. API 기반/브라우저 기반 제어를 위한 로컬 Tornado 제어 서버 + PWA (`server/app.py` + `pwa/`)

현재 README 내용은 공식 운영 가이드로 유지하면서, 가독성을 위해 재구성했습니다.

## ✨ 개요

핵심 설계:
- DevTools 원격 디버깅(기본 포트 `9333`)을 통해 지속형 Chrome 세션에 연결
- 브라우저 프로필 상태를 재사용해 로그인/세션 연속성 유지
- 컴포저의 핵심 동작(입력, plus/미디어 첨부, storyboard, settings, create) 자동화
- 동일한 동작을 REST + WebSocket 로그로 노출해 로컬 PWA에서 제어 가능

### 워크플로 한눈에 보기

| Workflow | Entry point | Primary use |
| --- | --- | --- |
| CLI Agent | `agents/sora_agent.py` | 프롬프트 입력, 컨트롤 클릭, 컴포즈 흐름 자동화 |
| CLI Downloader | `agents/sora_download.py` | 다운로드 가능한 미디어 탐색 및 로컬 저장 |
| API + PWA | `server/app.py` + `pwa/` | 브라우저 기반 원격 제어 및 시각적 오케스트레이션 |

## ✅ 기능

- 재사용 가능한 프로필 기반 Chrome 연결/실행 흐름 (`--debugger-port`, `--start-chrome`, `--user-data-dir`)
- 주요 컨트롤 안전 클릭/강제 클릭 (`plus`, `storyboard`, `settings`, `create`, `profile`)
- 셀렉터 폴백 동작을 포함한 프롬프트 입력
- DataTransfer 주입 기반 파일 경로 미디어 첨부
- 스토리보드 씬 입력 + 스크립트 업데이트 + 스토리보드 전용 미디어 첨부
- 모델/방향/길이/해상도 설정 자동화
- 브라우저 쿠키를 이용한 다운로드 후보 탐색 + 파일 가져오기 분리 흐름
- Tornado REST API 및 실시간 WebSocket 디버그 스트림
- 업로드/미리보기/세부 제어를 갖춘 설치형 로컬 PWA

## 🗂️ 프로젝트 구조

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
│  └─ (현재 번역 파일 포함)
├─ uploads/
│  └─ .gitkeep
└─ selenium_template -> ../auto-publish/ (symlink)
```

## 🧩 사전 요구사항

- Python 3.10+ (권장)
- 설치 및 실행 가능한 Chrome/Chromium
- 로그인 또는 상호작용 UI가 필요한 경우 비헤드리스 사용을 위한 디스플레이(`--no-headless`)
- 연결된 Chrome 프로필에서 Sora 계정 접근 가능

## 📦 설치

기존 정식 README의 설정 흐름:

```bash
conda activate agent
pip install -r requirements.txt
```

`requirements.txt` 의존성:

| Package | Version spec |
| --- | --- |
| `selenium` | `>=4.17.2` |
| `tornado` | `>=6.4` |
| `Pillow` | `>=9.4.0` |
| `pillow-heif` | `>=0.16.0` |

## 🚀 사용법

### 빠른 시작 (CLI 에이전트)

빠른 시작(관리되는 브라우저에서 Sora 열기):

```bash
python agents/sora_agent.py
```

지속 세션으로 Chrome에 연결(Sora 사용 시 권장):

```bash
python -m agents.sora_agent --debugger-port 9333 --start-chrome --no-headless --login-timeout 600 --text "A sunset over Tokyo, cinematic."
```

참고:
- Chrome 창이 Sora 페이지로 열립니다. 로그인으로 리다이렉트되면 로그인하고, 스크립트가 대기 후 프롬프트를 입력합니다.
- 동일 로그인 상태를 재사용하려면 고정 프로필 경로를 전달하세요:

```bash
python -m agents.sora_agent --debugger-port 9333 --start-chrome --no-headless --user-data-dir "$HOME/chrome_sora_profile_9333"
```

### 핵심 CLI 옵션 (`agents/sora_agent.py`)

- `--url` 대상 페이지 (기본값: `https://sora.chatgpt.com/explore`)
- `--debugger-port` `--remote-debugging-port=PORT`로 시작한 기존 Chrome에 연결
- `--start-chrome` `--debugger-port`와 함께 지정 시 Chrome을 자동 실행(`--user-data-dir` 사용)
- `--no-headless` 가시 브라우저 실행; 로그인/Cloudflare 처리에 필요
- `--selector` 입력창 탐색용 CSS (기본값은 Sora 컴포저 textarea에 매칭)
- `--text` 입력창에 타이핑할 텍스트
- `--chrome-binary` Chrome/Chromium 경로를 명시적으로 지정
- `--action` UI 동작: `list`, `plus`, `storyboard`, `settings`, `create`, `profile`
- `--force-click` 요소가 비활성처럼 보여도 클릭 강행
- `--login-timeout` 수동 인증 완료 대기 시간

드라이버 처리:
- 에이전트는 실행 전에 `PATH`에 있는 오래된 `chromedriver`를 제거합니다.
- 이후 Selenium Manager가 설치된 Chrome에 맞는 드라이버를 자동으로 해석합니다.

### CLI 예시 (UI 제어)

자주 쓰는 컨트롤 목록 확인 및 클릭:

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action list --action storyboard --action settings --action plus
```

Create video 버튼 강제 클릭(비활성 상태처럼 보여도 클릭):

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action create --force-click
```

필요 시 프로필/설정을 열고 수동 탐색:

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action list --action profile
```

`profile`이 감지되지 않으면, 일반적으로 `settings` 버튼이 동일 메뉴를 엽니다.

### 다운로더 흐름

핸들러 스크립트로 동영상 탐색 및 다운로드:

- 드라이런(후보만 출력): `./bin/sora_download.sh --dry-run`
- 최대 2개 파일을 `./downloads/sora`에 다운로드: `./bin/sora_download.sh --max 2`
- 출력 폴더 변경: `OUT_DIR=$HOME/Videos/sora ./bin/sora_download.sh --max 1`

`python -m agents.sora_download ...` 형태의 직접 모듈 실행도 가능합니다.

## 🌐 제어 서버 + PWA

Tornado 서버 실행:

```bash
python server/app.py
# listens on http://0.0.0.0:8791 and serves the PWA at /
```

기본적으로 서버는 다음을 사용합니다:
- 원격 디버깅 포트 `9333`의 Chrome 재사용
- `SORA_UPLOADS_DIR`가 없으면 업로드를 `./uploads`에 저장

### 주요 엔드포인트

모든 엔드포인트는 현재 연결된 Chrome(기본 디버거 포트 `9333`)을 대상으로 동작합니다.

| Method | Path | Payload | Description |
| --- | --- | --- | --- |
| `GET` | `/api/status` | none | DevTools 준비 상태와 활성 포트를 반환합니다. |
| `POST` | `/api/open` | `{ url? }` | 연결된 Chrome 탭을 지정 URL로 이동합니다(기본: Sora Explore). |
| `GET` | `/api/actions` | none | 버튼/컨트롤 상태를 검사합니다(found/displayed/disabled 메타데이터). |
| `POST` | `/api/click` | `{ key, force? }` | `key ∈ {plus, storyboard, settings, create, profile}` 중 하나의 컨트롤을 누릅니다. |
| `POST` | `/api/type` | `{ text, selector?, url? }` | 컴포저 셀렉터에 프롬프트 텍스트를 입력합니다. |
| `POST` | `/api/compose` | `{ text, click_create? }` | 컴포즈 페이지를 열고 텍스트를 입력한 뒤, 선택적으로 create를 클릭합니다. |
| `POST` | `/api/attach` | `{ path, click_plus? }` | DataTransfer 주입으로 미디어를 업로드합니다. 기존 미디어는 자동으로 정리됩니다(`click_plus` 기본값 `false`). |
| `POST` | `/api/describe` | `{ text }` | “Optionally describe your video…” textarea를 채웁니다. |
| `POST` | `/api/script-updates` | `{ text }` | “Describe updates to your script…” 필드를 채웁니다. |
| `POST` | `/api/storyboard` | `{ scenes: ["scene 1", ...], script_updates?: "...", media_path?: "..." }` | 스토리보드를 열고 씬 textarea를 채운 뒤, 필요 시 스크립트 업데이트와 스토리보드 미디어를 적용합니다. |
| `POST` | `/api/storyboard-media` | `{ path }` | 스토리보드가 이미 표시된 상태에서 스토리보드 전용 업로더에 미디어를 첨부합니다. |
| `POST` | `/api/storyboard-attach-only` | `{ path }` | 스토리보드가 열려 있음을 보장한 다음 미디어를 첨부합니다. |
| `POST` | `/api/settings` | `{ model?, orientation?, duration?, resolution? }` | 설정을 열고 선택 값을 적용합니다. 응답에는 적용된 레이블이 반영됩니다. |
| `POST` | `/api/upload` | multipart form data | 로컬 파일을 서버 업로드 디렉터리에 저장하고 서버 경로를 반환합니다. |
| `POST` | `/api/preview` | multipart form data | 이미지를 PNG 미리보기로 변환합니다(UI에서 HEIC/HEIF/AVIF 폴백에 유용). |
| `GET` | `/ws` | WebSocket | 동작/디버그 이벤트를 스트리밍합니다. |

### PWA 제어

`server/app.py` 실행 후 `http://0.0.0.0:8791`(또는 선택한 호스트)로 접속하세요.

기존 구현의 핵심:
- 파일 선택기 또는 경로 붙여넣기로 미디어 업로드 후 **Plus** 클릭 시 시스템 파일 대화상자를 다시 열지 않고 첨부
- 전용 “Media description” 박스에 미디어 설명 적용
- **Set Model**, **Set Orientation**, **Set Duration**, **Set Resolution**, 스크립트 업데이트를 각각 독립 제어
- 스토리보드 씬/스크립트 업데이트/스토리보드 패널 열기/현재 스토리보드 경로 첨부 제어
- API 호출 및 Sora 반환값(예: 선택된 모델/길이)을 보여주는 실시간 디버그 로그

## ⚙️ 설정

### 환경 변수

`server/app.py`에서 읽는 변수:
- `SORA_DEBUGGER_PORT` (기본값 `9333`)
- `SORA_USER_DATA_DIR` (기본값 `~/chrome_sora_profile_<port>`)
- `SORA_DISPLAY` (선택적 X display)
- `SORA_API_PORT` (기본값 `8791`)
- `SORA_URL` (기본값 `https://sora.chatgpt.com/explore`)
- `SORA_UPLOADS_DIR` (선택적 업로드 디렉터리 오버라이드)

`agents/sora_agent.py`에서 추가 지원:
- `CHROME_BINARY` (`--chrome-binary` 미지정 시 사용)

래퍼 스크립트 지원:
- `PORT`, `SORA_PROFILE_DIR`, `TIMEOUT`, `LOGIN_TIMEOUT` (`bin/sora_type.sh`)
- `PORT`, `SORA_PROFILE_DIR`, `OUT_DIR` (`bin/sora_download.sh`)

## 🧪 예제

### End-to-end API 예제 (curl)

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

### API로 미디어 업로드 + 첨부

```bash
# Upload file and get server path
curl -s -X POST http://127.0.0.1:8791/api/upload -F 'file=@/absolute/path/to/input.jpg'

# Then attach using returned path
curl -s -X POST http://127.0.0.1:8791/api/attach \
  -H 'Content-Type: application/json' \
  -d '{"path":"/absolute/or/server-returned/path.jpg","click_plus":false}'
```

## 🛠️ 개발 노트

- 현재 패키징된 모듈은 없습니다(`pyproject.toml`/`setup.py` 없음).
- 현재 저장소 스냅샷에는 CI/test/lint 파이프라인이 없습니다.
- `selenium_template`는 `../auto-publish/`를 가리키는 symlink이며, 대상 내용은 이 저장소 외부에 있습니다.
- PWA manifest는 `/icons/icon-192.png`와 `/icons/icon-512.png`를 참조하지만, 아이콘 에셋은 현재 이 저장소에서 추적되지 않습니다.

## 🧯 문제 해결

- Chrome 연결 실패:
  - Chrome이 `--remote-debugging-port=9333`(또는 동일한 `--debugger-port`)로 시작되었는지 확인하세요.
  - `GET /api/status`에서 `devtools_ready: true`를 확인하세요.
- 로그인 프롬프트가 반복됨:
  - 고정 `--user-data-dir`를 사용하고 임의 프로필 경로는 피하세요.
- Cloudflare/로그인 흐름이 진행되지 않음:
  - 비헤드리스(`--no-headless`)로 실행하고 `--login-timeout`을 늘리세요.
- 미디어 첨부가 동작하지 않음:
  - 파일 경로가 서버 머신에 존재하는지 확인하고, 확실하지 않다면 `/api/upload` 후 반환 경로를 사용하세요.
- 스토리보드 미디어 첨부 실패:
  - `POST /api/storyboard-attach-only`를 사용하거나, 스토리보드를 먼저 연 뒤 `/api/storyboard-media`를 호출하세요.
- PWA에서 해상도 제어가 보이지 않음:
  - `High` 해상도는 모델이 `Sora 2 Pro`일 때만 활성화됩니다.
- 잘못된 chromedriver 문제:
  - 쉘 프로필에 수동 고정한 chromedriver를 제거하세요. 이 프로젝트는 Selenium Manager가 호환 버전을 선택하도록 설계되어 있습니다.

## 🧭 로드맵

계획/예상되는 다음 개선 사항:
- 셀렉터 안정성과 API 핸들러용 자동 테스트 추가
- lint/format 도구 및 CI 워크플로 추가
- PWA 아이콘 에셋 추적 및 오프라인 캐싱 전략 강화
- `i18n/` 하위에 공식 다국어 README 파일 추가
- 설치 편의성을 위한 패키징 메타데이터 추가

## 🤝 기여

기여를 환영합니다.

권장 절차:
1. 포크 후 기능 브랜치를 생성합니다.
2. 변경 범위를 작게 유지하고 UI 자동화 변경에는 재현/사용 노트를 포함합니다.
3. 실제로 연결된 Chrome 세션으로 흐름을 수동 검증합니다.
4. 변경 전/후 동작 상세와 함께 PR을 생성합니다.

셀렉터 또는 상호작용 로직을 변경했다면, 회귀 이슈를 쉽게 분류할 수 있도록 구체적인 Sora UI 맥락을 함께 적어 주세요.

## ❤️ 지원 / 스폰서십

`.github/FUNDING.yml`의 후원 링크:
- GitHub Sponsors: https://github.com/sponsors/lachlanchen
- Project links: https://lazying.art, https://chat.lazying.art, https://onlyideas.art

## 🙏 감사의 말

- 브라우저 자동화와 드라이버 해석을 제공하는 Selenium 및 Selenium Manager
- 경량 비동기 HTTP/WebSocket 제어 서비스를 제공하는 Tornado
- 로컬 이미지 변환/미리보기 지원을 위한 Pillow 및 `pillow-heif`

## 🧱 검증된 빌드

스토리보드 미디어 첨부가 end-to-end로 안정적으로 동작하는 기준점(Open Storyboard / Attach Current Path 버튼 및 결합 Apply 흐름 포함)이 필요하면 아래 커밋을 확인하세요:

`c6683ed6d9ee0ac110536352867a26a966e3e275`

## 📄 라이선스

현재 저장소 스냅샷에는 라이선스 파일이 없습니다(이 초안 기준 확인일: **February 28, 2026**).

가정: 라이선스가 추가되기 전까지 모든 권리는 저장소 소유자에게 있습니다. 의도와 다르다면 `LICENSE` 파일을 추가하고 이 섹션을 업데이트하세요.
