[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


# SoraRemote

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20WSL-6c757d)
![Server](https://img.shields.io/badge/Server-Tornado%20API-0EA5E9)
![Frontend](https://img.shields.io/badge/Frontend-PWA-10B981)
![Status](https://img.shields.io/badge/Status-Experimental-F59E0B)

SoraRemote là bộ công cụ nhẹ dùng Python + Selenium để tự động hóa giao diện web Sora.

Dự án hỗ trợ ba quy trình làm việc bổ trợ lẫn nhau:
1. Tác nhân tự động hóa CLI (`agents/sora_agent.py`) để nhập prompt và điều khiển thao tác UI.
2. Trình tải xuống CLI (`agents/sora_download.py`) để tìm và tải nội dung media phù hợp.
3. Máy chủ điều khiển Tornado cục bộ + PWA (`server/app.py` + `pwa/`) để điều khiển qua API và trình duyệt.

Nội dung README hiện tại được giữ làm hướng dẫn vận hành chuẩn và được sắp xếp lại cho rõ ràng hơn.

## ✨ Tổng quan

Thiết kế cốt lõi:
- Kết nối vào phiên Chrome duy trì sẵn qua DevTools remote debugging (cổng mặc định `9333`).
- Tái sử dụng trạng thái profile trình duyệt để giữ phiên đăng nhập liên tục.
- Tự động hóa các thao tác chính trong khung soạn thảo (nhập, đính kèm plus/media, storyboard, settings, create).
- Cung cấp chính các thao tác đó qua REST + nhật ký WebSocket cho bộ điều khiển PWA cục bộ.

### Ảnh chụp nhanh quy trình

| Quy trình | Điểm vào | Mục đích chính |
| --- | --- | --- |
| CLI Agent | `agents/sora_agent.py` | Nhập prompt, bấm điều khiển, tự động hóa luồng soạn thảo |
| CLI Downloader | `agents/sora_download.py` | Tìm media có thể tải và lưu file về máy |
| API + PWA | `server/app.py` + `pwa/` | Điều khiển từ xa và điều phối trực quan qua trình duyệt |

## ✅ Tính năng

- Luồng kết nối/khởi chạy Chrome với profile tái sử dụng (`--debugger-port`, `--start-chrome`, `--user-data-dir`).
- Bấm an toàn hoặc ép bấm cho các điều khiển chính (`plus`, `storyboard`, `settings`, `create`, `profile`).
- Nhập prompt với cơ chế fallback selector.
- Đính kèm media bằng đường dẫn file qua DataTransfer injection.
- Điền cảnh storyboard + cập nhật script + đính kèm media riêng cho storyboard.
- Tự động hóa settings cho model/orientation/duration/resolution.
- Luồng tìm + tải xuống riêng bằng cookie trình duyệt.
- Tornado REST API và luồng debug WebSocket thời gian thực.
- PWA cục bộ có thể cài đặt với upload, preview và điều khiển chi tiết.

## 🗂️ Cấu trúc dự án

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
│  └─ (currently empty)
├─ uploads/
│  └─ .gitkeep
└─ selenium_template -> ../auto-publish/ (symlink)
```

## 🧩 Điều kiện tiên quyết

- Python 3.10+ (khuyến nghị).
- Đã cài Chrome/Chromium và có thể chạy.
- Có màn hình hiển thị cho chế độ không headless (`--no-headless`) khi cần đăng nhập hoặc thao tác UI tương tác.
- Có quyền truy cập tài khoản Sora trong profile Chrome được kết nối.

## 📦 Cài đặt

Luồng thiết lập hiện có từ README chuẩn:

```bash
conda activate agent
pip install -r requirements.txt
```

Các dependency trong `requirements.txt`:

| Gói | Phiên bản |
| --- | --- |
| `selenium` | `>=4.17.2` |
| `tornado` | `>=6.4` |
| `Pillow` | `>=9.4.0` |
| `pillow-heif` | `>=0.16.0` |

## 🚀 Sử dụng

### Khởi động nhanh (CLI agent)

Khởi động nhanh (mở Sora trong trình duyệt được quản lý):

```bash
python agents/sora_agent.py
```

Kết nối Chrome với phiên bền vững (khuyến nghị cho Sora):

```bash
python -m agents.sora_agent --debugger-port 9333 --start-chrome --no-headless --login-timeout 600 --text "A sunset over Tokyo, cinematic."
```

Ghi chú:
- Một cửa sổ Chrome sẽ mở vào trang Sora. Nếu bị chuyển đến trang đăng nhập, hãy đăng nhập; script sẽ chờ rồi nhập prompt của bạn.
- Để tái sử dụng cùng một lần đăng nhập, truyền đường dẫn profile cố định:

```bash
python -m agents.sora_agent --debugger-port 9333 --start-chrome --no-headless --user-data-dir "$HOME/chrome_sora_profile_9333"
```

### Tùy chọn CLI chính (`agents/sora_agent.py`)

- `--url` trang đích (mặc định: `https://sora.chatgpt.com/explore`).
- `--debugger-port` kết nối vào Chrome đã chạy với `--remote-debugging-port=PORT`.
- `--start-chrome` nếu đặt cùng `--debugger-port`, sẽ tự khởi chạy Chrome (kèm `--user-data-dir`).
- `--no-headless` để chạy trình duyệt hiển thị; cần cho đăng nhập và Cloudflare.
- `--selector` CSS để định vị ô nhập (mặc định khớp textarea composer của Sora).
- `--text` nội dung cần nhập vào ô nhập.
- `--chrome-binary` đặt rõ đường dẫn Chrome/Chromium.
- `--action` các thao tác UI: `list`, `plus`, `storyboard`, `settings`, `create`, `profile`.
- `--force-click` bấm ngay cả khi phần tử có vẻ bị vô hiệu hóa.
- `--login-timeout` thời gian chờ hoàn tất xác thực thủ công.

Xử lý driver:
- Agent xóa mọi `chromedriver` cũ khỏi `PATH` trước khi khởi chạy.
- Sau đó Selenium Manager tự tìm driver phù hợp với Chrome đã cài.

### Ví dụ CLI (điều khiển UI)

Liệt kê và bấm các điều khiển phổ biến:

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action list --action storyboard --action settings --action plus
```

Ép bấm nút Create video (kể cả khi bị disable):

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action create --force-click
```

Mở hồ sơ/cài đặt và điều hướng thủ công nếu cần:

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action list --action profile
```

Nếu không phát hiện `profile`, nút `settings` thường sẽ mở cùng menu đó.

### Luồng downloader

Tìm và tải video bằng script wrapper:

- Chạy thử (chỉ liệt kê ứng viên): `./bin/sora_download.sh --dry-run`
- Tải tối đa 2 file vào `./downloads/sora`: `./bin/sora_download.sh --max 2`
- Đổi thư mục đầu ra: `OUT_DIR=$HOME/Videos/sora ./bin/sora_download.sh --max 1`

Bạn cũng có thể gọi trực tiếp module qua `python -m agents.sora_download ...`.

## 🌐 Máy chủ điều khiển + PWA

Chạy máy chủ Tornado:

```bash
python server/app.py
# listens on http://0.0.0.0:8791 and serves the PWA at /
```

Theo mặc định, server:
- Tái sử dụng Chrome tại cổng remote debugging `9333`.
- Lưu file upload trong `./uploads` trừ khi đặt `SORA_UPLOADS_DIR`.

### Endpoint chính

Mọi endpoint đều thao tác trên Chrome đang được kết nối (mặc định cổng debugger `9333`).

| Method | Path | Payload | Description |
| --- | --- | --- | --- |
| `GET` | `/api/status` | none | Returns DevTools readiness state and active port. |
| `POST` | `/api/open` | `{ url? }` | Navigates the attached Chrome tab to the given URL (defaults to Sora Explore). |
| `GET` | `/api/actions` | none | Inspects button/control state (found/displayed/disabled metadata). |
| `POST` | `/api/click` | `{ key, force? }` | Presses one control where `key ∈ {plus, storyboard, settings, create, profile}`. |
| `POST` | `/api/type` | `{ text, selector?, url? }` | Types prompt text into composer selector. |
| `POST` | `/api/compose` | `{ text, click_create? }` | Opens compose page, types text, optionally clicks create. |
| `POST` | `/api/attach` | `{ path, click_plus? }` | Uploads media via DataTransfer injection; clears existing media automatically (`click_plus` defaults to `false`). |
| `POST` | `/api/describe` | `{ text }` | Fills the “Optionally describe your video…” textarea. |
| `POST` | `/api/script-updates` | `{ text }` | Fills the “Describe updates to your script…” field. |
| `POST` | `/api/storyboard` | `{ scenes: ["scene 1", ...], script_updates?: "...", media_path?: "..." }` | Opens storyboard, fills scene textareas, optionally applies script updates and storyboard media. |
| `POST` | `/api/storyboard-media` | `{ path }` | Attaches media to storyboard-specific uploader when storyboard is already visible. |
| `POST` | `/api/storyboard-attach-only` | `{ path }` | Ensures storyboard is open, then attaches media. |
| `POST` | `/api/settings` | `{ model?, orientation?, duration?, resolution? }` | Opens settings and applies selected values; response echoes applied labels. |
| `POST` | `/api/upload` | multipart form data | Saves local file(s) to server upload directory and returns server-side paths. |
| `POST` | `/api/preview` | multipart form data | Converts image to PNG preview (useful for HEIC/HEIF/AVIF fallback in UI). |
| `GET` | `/ws` | WebSocket | Streams action/debug events. |

### Điều khiển PWA

Mở `http://0.0.0.0:8791` (hoặc host bạn chọn) sau khi khởi chạy `server/app.py`.

Điểm nổi bật từ phần triển khai hiện tại:
- Tải media lên qua bộ chọn file hoặc dán đường dẫn, sau đó bấm **Plus** để đính kèm mà không cần mở lại hộp thoại file của hệ thống.
- Áp dụng mô tả media trong ô “Media description” chuyên dụng.
- Điều khiển độc lập cho **Set Model**, **Set Orientation**, **Set Duration**, **Set Resolution**, và cập nhật script.
- Điều khiển storyboard cho scene, cập nhật script, mở bảng storyboard, và đính kèm đường dẫn storyboard hiện tại.
- Nhật ký debug trực tiếp hiển thị API call và giá trị Sora trả về (ví dụ model/duration đã chọn).

## ⚙️ Cấu hình

### Biến môi trường

`server/app.py` đọc:
- `SORA_DEBUGGER_PORT` (mặc định `9333`)
- `SORA_USER_DATA_DIR` (mặc định `~/chrome_sora_profile_<port>`)
- `SORA_DISPLAY` (X display tùy chọn)
- `SORA_API_PORT` (mặc định `8791`)
- `SORA_URL` (mặc định `https://sora.chatgpt.com/explore`)
- `SORA_UPLOADS_DIR` (ghi đè thư mục upload, tùy chọn)

`agents/sora_agent.py` cũng hỗ trợ:
- `CHROME_BINARY` (nếu không truyền `--chrome-binary`)

Script wrapper hỗ trợ:
- `PORT`, `SORA_PROFILE_DIR`, `TIMEOUT`, `LOGIN_TIMEOUT` (`bin/sora_type.sh`)
- `PORT`, `SORA_PROFILE_DIR`, `OUT_DIR` (`bin/sora_download.sh`)

## 🧪 Ví dụ

### Ví dụ API end-to-end (curl)

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

### Upload + đính kèm media qua API

```bash
# Upload file and get server path
curl -s -X POST http://127.0.0.1:8791/api/upload -F 'file=@/absolute/path/to/input.jpg'

# Then attach using returned path
curl -s -X POST http://127.0.0.1:8791/api/attach \
  -H 'Content-Type: application/json' \
  -d '{"path":"/absolute/or/server-returned/path.jpg","click_plus":false}'
```

## 🛠️ Ghi chú phát triển

- Hiện chưa có module đóng gói (`pyproject.toml`/`setup.py` chưa tồn tại).
- Trong ảnh chụp repo này hiện chưa có pipeline CI/test/lint.
- `selenium_template` là symlink tới `../auto-publish/`; nội dung đích nằm ngoài repo này.
- Manifest PWA tham chiếu `/icons/icon-192.png` và `/icons/icon-512.png`; các icon này hiện chưa được theo dõi trong repo.

## 🧯 Khắc phục sự cố

- Chrome không kết nối được:
  - Đảm bảo Chrome được khởi chạy với `--remote-debugging-port=9333` (hoặc cổng khớp với `--debugger-port`).
  - Kiểm tra `GET /api/status` có `devtools_ready: true`.
- Liên tục bị yêu cầu đăng nhập:
  - Dùng `--user-data-dir` cố định và tránh đường dẫn profile ngẫu nhiên.
- Luồng Cloudflare/đăng nhập không tiến triển:
  - Chạy không headless (`--no-headless`) và tăng `--login-timeout`.
- Đính kèm media không có tác dụng:
  - Xác nhận đường dẫn file tồn tại trên máy chủ và dùng `/api/upload` + đường dẫn trả về nếu chưa chắc chắn.
- Đính kèm media storyboard thất bại:
  - Thử `POST /api/storyboard-attach-only` hoặc mở storyboard trước rồi gọi `/api/storyboard-media`.
- Điều khiển resolution không khả dụng trong PWA:
  - Resolution `High` chỉ bật khi model là `Sora 2 Pro`.
- Lỗi chromedriver sai phiên bản:
  - Gỡ chromedriver ghim thủ công khỏi shell profile; dự án này chủ động để Selenium Manager chọn phiên bản phù hợp.

## 🧭 Lộ trình

Các cải tiến dự kiến/khả năng cao tiếp theo:
- Thêm kiểm thử tự động cho độ ổn định selector và API handler.
- Thêm công cụ lint/format và workflow CI.
- Thêm icon PWA được theo dõi và chiến lược cache offline tốt hơn.
- Thêm các README đa ngôn ngữ chính thức trong `i18n/`.
- Thêm metadata đóng gói để cài đặt thuận tiện hơn.

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón.

Quy trình gợi ý:
1. Fork và tạo nhánh tính năng.
2. Giữ phạm vi thay đổi gọn và kèm ghi chú tái hiện/sử dụng cho các thay đổi tự động hóa UI.
3. Xác thực thủ công các luồng với phiên Chrome thực đang được kết nối.
4. Mở PR kèm chi tiết hành vi trước/sau.

Nếu bạn thay selector hoặc logic tương tác, hãy thêm ngữ cảnh UI Sora cụ thể để dễ phân tích hồi quy hơn.

## ❤️ Hỗ trợ / Tài trợ

Liên kết tài trợ từ `.github/FUNDING.yml`:
- GitHub Sponsors: https://github.com/sponsors/lachlanchen
- Liên kết dự án: https://lazying.art, https://chat.lazying.art, https://onlyideas.art

## 🙏 Lời cảm ơn

- Selenium và Selenium Manager cho tự động hóa trình duyệt và phân giải driver.
- Tornado cho dịch vụ điều khiển HTTP/WebSocket async gọn nhẹ.
- Pillow và `pillow-heif` cho hỗ trợ chuyển đổi/preview ảnh cục bộ.

## 🧱 Bản dựng ổn định đã kiểm chứng

Nếu bạn cần một mốc ổn định bảo đảm tính năng đính kèm media storyboard hoạt động end-to-end (bao gồm các nút Open Storyboard / Attach Current Path và luồng Apply kết hợp), hãy checkout commit:

`c6683ed6d9ee0ac110536352867a26a966e3e275`

## 📄 Giấy phép

Hiện chưa có file license trong ảnh chụp repo này (đã kiểm tra trong bản nháp vào **February 28, 2026**).

Giả định: mọi quyền vẫn thuộc về chủ sở hữu repository cho đến khi có license được thêm vào. Nếu không phải ý định này, hãy thêm file `LICENSE` và cập nhật phần này.
