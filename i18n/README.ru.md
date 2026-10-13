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

SoraRemote — это лёгкий Python + Selenium тулкит для автоматизации веб-интерфейса Sora.

Он поддерживает три взаимодополняющих режима выполнения в рамках одного рабочего процесса:
1. **CLI агент автоматизации** (`agents/sora_agent.py`) для ввода промптов и действий в интерфейсе.
2. **CLI downloader** (`agents/sora_download.py`) для поиска и загрузки медиа-кандидатов.
3. **Tornado + PWA control plane** (`server/app.py` + `pwa/`) для оркестрации браузера через API.

Текущий README сохраняет канонические операционные рекомендации и переорганизован для лучшей читаемости.

## 🚀 Быстрый доступ

| Цель | Точка входа | Основное назначение |
| --- | --- | --- |
| Запуск скриптовых промптов | `agents/sora_agent.py` | Управление действиями composer из CLI или wrapper-скрипта |
| Получение сгенерированных медиа | `agents/sora_download.py` | Поиск и сохранение кандидатов локально |
| Удалённое управление | `server/app.py` + `pwa/` | Контроль через REST/WebSocket + панель браузера |

## ✨ Обзор

Ключевая логика:
- Подключение к постоянной сессии Chrome через удалённую отладку DevTools (порт по умолчанию `9333`).
- Повторное использование состояния профиля браузера для сохранения логина/сессии.
- Автоматизация основных действий composer (ввод текста, вложение файлов, storyboard, настройки, создание).
- Предоставление тех же действий через REST + WebSocket-логи для локального PWA-контроллера.

### Снимок рабочего процесса

| Поток | Точка входа | Основное назначение |
| --- | --- | --- |
| CLI Agent | `agents/sora_agent.py` | Ввод промптов, клики по контролам, автоматизация процесса compose |
| CLI Downloader | `agents/sora_download.py` | Поиск скачиваемых медиа и сохранение файлов локально |
| API + PWA | `server/app.py` + `pwa/` | Удалённое управление и визуальная оркестрация в браузере |

## ✅ Возможности

- Поток attach/start Chrome с переиспользуемым профилем (`--debugger-port`, `--start-chrome`, `--user-data-dir`).
- Безопасные или принудительные клики по ключевым контролам (`plus`, `storyboard`, `settings`, `create`, `profile`).
- Ввод промпта с резервным поведением выбора селектора.
- Вложение медиа по пути с инъекцией через DataTransfer.
- Заполнение сцен storyboard + обновление скрипта + вложение медиа для storyboard.
- Автоматизация настроек модели/orientation/duration/resolution.
- Разделённые потоки поиска и скачивания кандидатов с использованием cookie браузера.
- Tornado REST API и потоковая передача WebSocket для живого дебага.
- Устанавливаемый локальный PWA с загрузкой, предпросмотром и детальными контролами.

## 🗂️ Структура проекта

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

## 🧩 Предварительные требования

- Python 3.10+ (рекомендуется).
- Установленный и рабочий Chrome/Chromium.
- Доступный дисплей для не-headless режима (`--no-headless`), если нужен логин или интерактивный UI.
- Доступ к аккаунту Sora в подключённом профиле Chrome.

## 📦 Установка

Существующий процесс настройки из канонического README:

```bash
conda activate agent
pip install -r requirements.txt
```

Зависимости из `requirements.txt`:

| Пакет | Версия |
| --- | --- |
| `selenium` | `>=4.17.2` |
| `tornado` | `>=6.4` |
| `Pillow` | `>=9.4.0` |
| `pillow-heif` | `>=0.16.0` |

## 🚀 Использование

### Быстрый старт (CLI агент)

Быстрый запуск (открывает Sora в управляемом браузере):

```bash
python agents/sora_agent.py
```

Подключение к Chrome с сохранённой сессией (рекомендуется для Sora):

```bash
python -m agents.sora_agent --debugger-port 9333 --start-chrome --no-headless --login-timeout 600 --text "A sunset over Tokyo, cinematic."
```

Примечания:
- Открывается окно Chrome на странице Sora. Если произошло перенаправление на страницу входа, выполните вход — скрипт подождёт, а затем набьёт ваш промпт.
- Чтобы повторно использовать тот же логин, передайте фиксированный путь к профилю:

```bash
python -m agents.sora_agent --debugger-port 9333 --start-chrome --no-headless --user-data-dir "$HOME/chrome_sora_profile_9333"
```

### Ключевые параметры CLI (`agents/sora_agent.py`)

- `--url` целевая страница (по умолчанию: `https://sora.chatgpt.com/explore`).
- `--debugger-port` подключение к уже запущенному Chrome с флагом `--remote-debugging-port=PORT`.
- `--start-chrome` при одновременном указании `--debugger-port` запускает Chrome за вас (с `--user-data-dir`).
- `--no-headless` для запуска видимого браузера; требуется для входа и Cloudflare.
- `--selector` CSS-селектор для определения поля ввода (по умолчанию совпадает с textarea composer Sora).
- `--text` текст для ввода в поле.
- `--chrome-binary` задаёт явный путь к Chrome/Chromium.
- `--action` действия UI: `list`, `plus`, `storyboard`, `settings`, `create`, `profile`.
- `--force-click` выполняет клик даже если элемент кажется отключённым.
- `--login-timeout` окно ожидания ручного завершения авторизации.

Обработка драйвера:
- Перед запуском агент удаляет устаревший `chromedriver` из `PATH`.
- Затем Selenium Manager автоматически подбирает совместимый драйвер для установленного Chrome.

### Примеры CLI (UI-контролы)

Вывести и нажать частые контролы:

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action list --action storyboard --action settings --action plus
```

Принудительно нажать кнопку Create video (даже если отключена):

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action create --force-click
```

Открыть профиль/настройки и при необходимости перейти вручную:

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action list --action profile
```

Если `profile` не обнаружен, кнопка `settings` обычно открывает тот же меню.

### Процесс загрузки (downloader)

Обнаружение и загрузка видео обработчиком:

- Dry-run (только список кандидатов): `./bin/sora_download.sh --dry-run`
- Загрузить до 2 файлов в `./downloads/sora`: `./bin/sora_download.sh --max 2`
- Изменить папку вывода: `OUT_DIR=$HOME/Videos/sora ./bin/sora_download.sh --max 1`

Прямой вызов модуля также доступен через `python -m agents.sora_download ...`.

## 🌐 Сервер управления + PWA

Запуск Tornado-сервера:

```bash
python server/app.py
# listens on http://0.0.0.0:8791 and serves the PWA at /
```

По умолчанию сервер:
- Повторно использует Chrome на порту удалённой отладки `9333`.
- Сохраняет загрузки в `./uploads`, если не задано `SORA_UPLOADS_DIR`.

### Ключевые эндпоинты

Все эндпоинты работают с текущим подключённым Chrome (порт по умолчанию — `9333`).

| Метод | Путь | Тело запроса | Описание |
| --- | --- | --- | --- |
| `GET` | `/api/status` | none | Возвращает состояние готовности DevTools и активный порт. |
| `POST` | `/api/open` | `{ url? }` | Перенаправляет прикреплённую вкладку Chrome на указанный URL (по умолчанию Sora Explore). |
| `GET` | `/api/actions` | none | Проверяет состояние кнопок/контролов (метаданные found/displayed/disabled). |
| `POST` | `/api/click` | `{ key, force? }` | Нажимает один контрол, где `key ∈ {plus, storyboard, settings, create, profile}`. |
| `POST` | `/api/type` | `{ text, selector?, url? }` | Вводит текст промпта в селектор composer. |
| `POST` | `/api/compose` | `{ text, click_create? }` | Открывает страницу compose, вводит текст, при необходимости нажимает create. |
| `POST` | `/api/attach` | `{ path, click_plus? }` | Загружает медиа через DataTransfer injection; автоматически очищает существующие медиа (`click_plus` по умолчанию `false`). |
| `POST` | `/api/describe` | `{ text }` | Заполняет textarea “Optionally describe your video…”. |
| `POST` | `/api/script-updates` | `{ text }` | Заполняет поле “Describe updates to your script…”. |
| `POST` | `/api/storyboard` | `{ scenes: ["scene 1", ...], script_updates?: "...", media_path?: "..." }` | Открывает storyboard, заполняет текстовые поля сцен, при необходимости применяет обновления скрипта и media для storyboard. |
| `POST` | `/api/storyboard-media` | `{ path }` | Вкладывает медиа в загрузчик storyboard, когда storyboard уже открыт. |
| `POST` | `/api/storyboard-attach-only` | `{ path }` | Обеспечивает открытие storyboard, затем прикладывает медиа. |
| `POST` | `/api/settings` | `{ model?, orientation?, duration?, resolution? }` | Открывает настройки и применяет выбранные значения; ответ содержит применённые метки. |
| `POST` | `/api/upload` | multipart form data | Сохраняет локальные файл(ы) в папку загрузок сервера и возвращает пути на стороне сервера. |
| `POST` | `/api/preview` | multipart form data | Конвертирует изображение в PNG-превью (полезно для fallback HEIC/HEIF/AVIF в UI). |
| `GET` | `/ws` | WebSocket | Передаёт поток action/debug событий. |

### Управление в PWA

Откройте `http://0.0.0.0:8791` (или выбранный хост) после запуска `server/app.py`.

Ключевые моменты текущей реализации:
- Загрузка медиа через выбор файла или вставку пути, затем кнопка **Plus** для вложения без повторного открытия системного диалога.
- Применение описания медиа в специальном поле “Media description”.
- Отдельные контролы для **Set Model**, **Set Orientation**, **Set Duration**, **Set Resolution**, и обновлений скрипта.
- Управление storyboard: сцены, обновления скрипта, открытие панели storyboard и присоединение текущего пути storyboard.
- Живой debug-лог с API-вызовами и значениями, возвращаемыми Sora (например выбранная модель/длительность).

## ⚙️ Конфигурация

### Переменные окружения

`server/app.py` читает:
- `SORA_DEBUGGER_PORT` (по умолчанию `9333`)
- `SORA_USER_DATA_DIR` (по умолчанию `~/chrome_sora_profile_<port>`)
- `SORA_DISPLAY` (необязательный X-дисплей)
- `SORA_API_PORT` (по умолчанию `8791`)
- `SORA_URL` (по умолчанию `https://sora.chatgpt.com/explore`)
- `SORA_UPLOADS_DIR` (необязательное переопределение каталога загрузок)

`agents/sora_agent.py` также поддерживает:
- `CHROME_BINARY` (если флаг `--chrome-binary` не передан)

Wrapper-скрипты поддерживают:
- `PORT`, `SORA_PROFILE_DIR`, `TIMEOUT`, `LOGIN_TIMEOUT` (`bin/sora_type.sh`)
- `PORT`, `SORA_PROFILE_DIR`, `OUT_DIR` (`bin/sora_download.sh`)

## 🧪 Примеры

### End-to-end пример через curl

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

### Загрузка и прикрепление медиа через API

```bash
# Upload file and get server path
curl -s -X POST http://127.0.0.1:8791/api/upload -F 'file=@/absolute/path/to/input.jpg'

# Then attach using returned path
curl -s -X POST http://127.0.0.1:8791/api/attach \
  -H 'Content-Type: application/json' \
  -d '{"path":"/absolute/or/server-returned/path.jpg","click_plus":false}'
```

## 🛠️ Заметки по разработке

- На текущий момент нет упакованного модуля (`pyproject.toml`/`setup.py` отсутствует).
- На текущий момент в снимке репозитория нет CI/test/lint пайплайна.
- `selenium_template` — это symlink на `../auto-publish/`; его содержимое находится вне этого репозитория.
- В PWA manifest указаны `/icons/icon-192.png` и `/icons/icon-512.png`; иконки пока не отслеживаются в репозитории.

## 🧯 Устранение неполадок

- Chrome не подключается:
  - Убедитесь, что Chrome запущен с `--remote-debugging-port=9333` (или совпадает с `--debugger-port`).
  - Проверьте `GET /api/status` на наличие `devtools_ready: true`.
- Повторяющиеся окна входа:
  - Используйте постоянный `--user-data-dir` и избегайте случайных путей профилей.
- Cloudflare/процесс входа не продвигается:
  - Запустите non-headless (`--no-headless`) и увеличьте `--login-timeout`.
- Вложение медиа не работает:
  - Проверьте, что путь к файлу существует на машине сервера, и при необходимости используйте `/api/upload` + возвращённый путь.
- Не удаётся вложить storyboard медиа:
  - Попробуйте `POST /api/storyboard-attach-only` или сначала откройте storyboard, затем `/api/storyboard-media`.
- В PWA недоступна настройка resolution:
  - `High` доступен только при модели `Sora 2 Pro`.
- Проблемы с неверным chromedriver:
  - Удалите вручную закреплённый chromedriver из вашего shell profile; проект намеренно полагается на Selenium Manager для выбора совместимых версий.

## 🧭 Дорожная карта

Планируемые/вероятные следующие улучшения:
- Добавить автоматизированные тесты для стабильности селекторов и API-обработчиков.
- Добавить инструменты lint/format и CI workflows.
- Добавить отслеживаемые ресурсы иконок PWA и усиленную стратегию офлайн-кэширования.
- Добавить формальные многоязычные README в `i18n/`.
- Добавить метаданные для упрощения установки.

## 🤝 Вклад в проект

Вклады приветствуются.

Предлагаемый процесс:
1. Сделайте форк и создайте feature branch.
2. Держите изменения scoped и добавляйте заметки по воспроизведению/использованию для изменений в UI-автоматизации.
3. Проверяйте сценарии вручную с реальной сессией подключённого Chrome.
4. Открывайте PR с деталями поведения до/после.

Если вы меняете селекторы или логику взаимодействия, добавляйте конкретный контекст Sora UI, чтобы регрессии было легче triage.

## 🙏 Благодарности

- Selenium и Selenium Manager за автоматизацию браузера и подбор драйвера.
- Tornado за лёгкий асинхронный HTTP/WebSocket сервис управления.
- Pillow и `pillow-heif` за локальную конвертацию/превью изображений.

## 🧱 Надёжная базовая версия

Если вам нужна стабильная база, гарантирующая, что вложение медиа в storyboard работает end-to-end (включая кнопки Open Storyboard / Attach Current Path и комбинированный Apply flow), используйте этот коммит:

`c6683ed6d9ee0ac110536352867a26a966e3e275`

## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |

## 📄 License

В текущем снапшоте репозитория файл лицензии отсутствует (проверено в этом черновике на **28 февраля 2026 года**).

Предполагается, что все права остаются у владельца репозитория до добавления лицензии. Если это не соответствует вашим планам, добавьте `LICENSE` и обновите этот раздел.
