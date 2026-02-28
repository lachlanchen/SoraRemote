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

SoraRemote là một bộ công cụ Python + Selenium nhẹ, dùng để tự động hóa giao diện web Sora.

Nó hỗ trợ ba chế độ thực thi bổ sung cho cùng một quy trình tự động hóa:
1. **Tác nhân tự động hóa CLI** (`agents/sora_agent.py`) để nhập prompt và thao tác UI.
2. **CLI downloader** (`agents/sora_download.py`) để phát hiện và tải về các phương án media.
3. **Mặt phẳng điều khiển Tornado + PWA** (`server/app.py` + `pwa/`) cho điều phối trình duyệt theo API.

Nội dung README hiện tại được giữ nguyên làm hướng dẫn vận hành chuẩn và được tổ chức lại cho rõ ràng hơn.

## 🚀 Truy cập nhanh

| Mục tiêu | Điểm vào | Sử dụng chính |
| --- | --- | --- |
| Chạy prompt theo kịch bản | `agents/sora_agent.py` | Điều khiển hành động composer từ CLI hoặc script wrapper |
| Tải media đã sinh | `agents/sora_download.py` | Phát hiện và lưu các media candidate về máy |
| Điều khiển từ xa | `server/app.py` + `pwa/` | Điều khiển qua REST/WebSocket + dashboard trình duyệt |

## ✨ Tổng quan

Thiết kế cốt lõi:
- Gắn vào một phiên Chrome bền vững qua DevTools remote debugging (mặc định cổng `9333`).
- Tái sử dụng trạng thái profile trình duyệt để duy trì đăng nhập và liên kết phiên.
- Tự động hóa các thao tác tạo chính (gõ chữ, gắn media, storyboard, settings, create).
- Expose cùng một tập thao tác qua REST + log WebSocket cho bộ điều khiển PWA cục bộ.

### Ảnh nhanh quy trình

| Quy trình | Điểm vào | Sử dụng chính |
| --- | --- | --- |
| CLI Agent | `agents/sora_agent.py` | Nhập prompt, bấm điều khiển, tự động hóa luồng soạn thảo |
| CLI Downloader | `agents/sora_download.py` | Phát hiện media có thể tải và lưu file cục bộ |
| API + PWA | `server/app.py` + `pwa/` | Điều khiển từ xa và phối hợp trực quan qua trình duyệt |

## ✅ Tính năng

- Luồng gắn/kết nối và khởi chạy Chrome với profile có thể tái sử dụng (`--debugger-port`, `--start-chrome`, `--user-data-dir`).
- Nhấn click an toàn hoặc ép click cho các điều khiển chính (`plus`, `storyboard`, `settings`, `create`, `profile`).
- Gõ prompt với hành vi fallback selector.
- Đính kèm media bằng đường dẫn file thông qua DataTransfer injection.
- Điền cảnh storyboard + cập nhật script + đính kèm media riêng cho storyboard.
- Tự động hóa settings cho model/orientation/duration/resolution.
- Luồng tách riêng cho phát hiện và tải media dùng cookie trình duyệt.
- REST API của Tornado và luồng debug WebSocket thời gian thực.
- PWA cục bộ cài đặt được với khả năng upload, preview và điều khiển chi tiết.

## 🗂️ Cấu trúc dự án

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

## 🧩 Điều kiện tiên quyết

- Python 3.10+ (khuyến nghị).
- Đã cài Chrome/Chromium và có thể chạy.
- Có màn hình cho chế độ không headless (`--no-headless`) khi cần đăng nhập hoặc thao tác UI tương tác.
- Có quyền truy cập tài khoản Sora trong profile Chrome đã gắn.

## 📦 Cài đặt

Luồng thiết lập có sẵn từ README chuẩn:

```bash
conda activate agent
pip install -r requirements.txt
```

Các phụ thuộc trong `requirements.txt`:

| Gói | Quy định phiên bản |
| --- | --- |
| `selenium` | `>=4.17.2` |
| `tornado` | `>=6.4` |
| `Pillow` | `>=9.4.0` |
| `pillow-heif` | `>=0.16.0` |

## 🚀 Sử dụng

### Bắt đầu nhanh (CLI agent)

Khởi động nhanh (mở Sora trong trình duyệt được quản lý):

```bash
python agents/sora_agent.py
```

Gắn vào Chrome với phiên bền vững (khuyến nghị cho Sora):

```bash
python -m agents.sora_agent --debugger-port 9333 --start-chrome --no-headless --login-timeout 600 --text "A sunset over Tokyo, cinematic."
```

Lưu ý:
- Một cửa sổ Chrome mở ở trang Sora. Nếu bị chuyển sang trang đăng nhập, hãy đăng nhập; script sẽ chờ rồi gõ prompt của bạn.
- Để tái sử dụng cùng một lần đăng nhập, truyền đường dẫn profile cố định:

```bash
python -m agents.sora_agent --debugger-port 9333 --start-chrome --no-headless --user-data-dir "$HOME/chrome_sora_profile_9333"
```

### Tùy chọn CLI chính (`agents/sora_agent.py`)

- `--url` trang đích (mặc định: `https://sora.chatgpt.com/explore`).
- `--debugger-port` gắn vào Chrome đang chạy với `--remote-debugging-port=PORT`.
- `--start-chrome`: nếu kết hợp với `--debugger-port`, khởi chạy Chrome cho bạn (với một `--user-data-dir`).
- `--no-headless` chạy trình duyệt nhìn thấy được; cần cho đăng nhập và Cloudflare.
- `--selector` CSS để xác định input (mặc định trùng textarea composer của Sora).
- `--text` nội dung để điền vào input.
- `--chrome-binary` chỉ định rõ path Chrome/Chromium.
- `--action` hành động UI: `list`, `plus`, `storyboard`, `settings`, `create`, `profile`.
- `--force-click` bắt buộc click kể cả khi phần tử hiển thị như bị vô hiệu hóa.
- `--login-timeout` thời gian chờ cho hoàn tất xác thực thủ công.

Xử lý driver:
- Agent xoá mọi `chromedriver` lỗi thời khỏi `PATH` trước khi khởi chạy.
- Selenium Manager sau đó tự động chọn driver phù hợp với Chrome đã cài.

### Ví dụ CLI (điều khiển UI)

Liệt kê và bấm các điều khiển phổ biến:

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action list --action storyboard --action settings --action plus
```

Bắt buộc bấm nút Create video (kể cả khi bị vô hiệu hóa):

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action create --force-click
```

Mở profile/settings và điều hướng thủ công nếu cần:

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action list --action profile
```

Nếu `profile` không được phát hiện, nút `settings` thường mở cùng menu đó.

### Luồng downloader

Phát hiện và tải video bằng script handler:

- Chạy thử (chỉ liệt kê ứng viên): `./bin/sora_download.sh --dry-run`
- Tải tối đa 2 file vào `./downloads/sora`: `./bin/sora_download.sh --max 2`
- Thay đổi thư mục đầu ra: `OUT_DIR=$HOME/Videos/sora ./bin/sora_download.sh --max 1`

Bạn cũng có thể dùng trực tiếp module qua `python -m agents.sora_download ...`.

## 🌐 Máy chủ điều khiển + PWA

Khởi chạy Tornado server:

```bash
python server/app.py
# listens on http://0.0.0.0:8791 and serves the PWA at /
```

Theo mặc định server:
- Tái sử dụng Chrome tại cổng remote debugging `9333`.
- Lưu uploads trong `./uploads` nếu chưa đặt `SORA_UPLOADS_DIR`.

### Các endpoint chính

Tất cả endpoint hoạt động trên Chrome đang gắn hiện tại (mặc định cổng debugger là `9333`).

| Phương thức | Đường dẫn | Payload | Mô tả |
| --- | --- | --- | --- |
| `GET` | `/api/status` | none | Trả về trạng thái sẵn sàng của DevTools và cổng đang hoạt động. |
| `POST` | `/api/open` | `{ url? }` | Điều hướng tab Chrome đã gắn đến URL cho trước (mặc định Sora Explore). |
| `GET` | `/api/actions` | none | Kiểm tra trạng thái nút/điều khiển (metadata found/displayed/disabled). |
| `POST` | `/api/click` | `{ key, force? }` | Nhấn một điều khiển với `key ∈ {plus, storyboard, settings, create, profile}`. |
| `POST` | `/api/type` | `{ text, selector?, url? }` | Điền prompt vào selector composer. |
| `POST` | `/api/compose` | `{ text, click_create? }` | Mở trang compose, gõ text, tuỳ chọn nhấn create. |
| `POST` | `/api/attach` | `{ path, click_plus? }` | Upload media qua DataTransfer injection; tự động xóa media hiện có (`click_plus` mặc định `false`). |
| `POST` | `/api/describe` | `{ text }` | Điền vào textarea “Optionally describe your video…”. |
| `POST` | `/api/script-updates` | `{ text }` | Điền vào trường “Describe updates to your script…”. |
| `POST` | `/api/storyboard` | `{ scenes: ["scene 1", ...], script_updates?: "...", media_path?: "..." }` | Mở storyboard, điền text scenes, tuỳ chọn áp dụng script updates và media storyboard. |
| `POST` | `/api/storyboard-media` | `{ path }` | Đính kèm media vào uploader riêng của storyboard khi storyboard đã hiển thị. |
| `POST` | `/api/storyboard-attach-only` | `{ path }` | Đảm bảo storyboard đang mở, rồi đính kèm media. |
| `POST` | `/api/settings` | `{ model?, orientation?, duration?, resolution? }` | Mở settings và áp dụng giá trị đã chọn; phản hồi trả lại nhãn đã áp dụng. |
| `POST` | `/api/upload` | multipart form data | Lưu file cục bộ vào thư mục upload của server và trả về đường dẫn bên phía server. |
| `POST` | `/api/preview` | multipart form data | Chuyển ảnh sang preview PNG (hữu ích cho HEIC/HEIF/AVIF dự phòng trong UI). |
| `GET` | `/ws` | WebSocket | Streaming action/debug events. |

### Điều khiển PWA

Mở `http://0.0.0.0:8791` (hoặc host bạn chọn) sau khi chạy `server/app.py`.

Điểm nổi bật từ triển khai hiện tại:
- Upload media qua file picker hoặc dán đường dẫn, rồi bấm **Plus** để đính kèm mà không cần mở lại dialog file hệ thống.
- Áp dụng mô tả media trong ô “Media description” chuyên biệt.
- Điều khiển độc lập cho **Set Model**, **Set Orientation**, **Set Duration**, **Set Resolution**, và cập nhật script.
- Điều khiển storyboard cho scenes, cập nhật script, mở panel storyboard và đính kèm đường dẫn storyboard hiện tại.
- Log debug thời gian thực hiển thị API calls và giá trị trả về từ Sora (ví dụ model/duration đã chọn).

## ⚙️ Cấu hình

### Biến môi trường

`server/app.py` đọc:
- `SORA_DEBUGGER_PORT` (mặc định `9333`)
- `SORA_USER_DATA_DIR` (mặc định `~/chrome_sora_profile_<port>`)
- `SORA_DISPLAY` (X display tuỳ chọn)
- `SORA_API_PORT` (mặc định `8791`)
- `SORA_URL` (mặc định `https://sora.chatgpt.com/explore`)
- `SORA_UPLOADS_DIR` (đè thư mục upload tùy chọn)

`agents/sora_agent.py` cũng hỗ trợ:
- `CHROME_BINARY` (nếu `--chrome-binary` không được truyền)

Wrapper scripts hỗ trợ:
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

- Hiện không có module đóng gói (`pyproject.toml`/`setup.py` chưa tồn tại).
- Hiện không có pipeline CI/test/lint trong snapshot repo này.
- `selenium_template` là symlink đến `../auto-publish/`; nội dung đích nằm ngoài repo này.
- PWA manifest tham chiếu `/icons/icon-192.png` và `/icons/icon-512.png`; icon assets hiện chưa được theo dõi trong repo.

## 🧯 Khắc phục sự cố

- Chrome không thể attach:
  - Đảm bảo Chrome đã khởi chạy với `--remote-debugging-port=9333` (hoặc cổng khớp với `--debugger-port`).
  - Kiểm tra `GET /api/status` để thấy `devtools_ready: true`.
- Bị yêu cầu đăng nhập lặp lại:
  - Dùng `--user-data-dir` cố định và tránh tạo profile path ngẫu nhiên.
- Luồng Cloudflare/đăng nhập không tiến triển:
  - Chạy không headless (`--no-headless`) và tăng `--login-timeout`.
- Đính kèm media không có hiệu lực:
  - Xác nhận đường dẫn file tồn tại trên máy chủ và dùng `/api/upload` + đường dẫn trả về khi chưa chắc.
- Đính kèm media storyboard bị lỗi:
  - Thử `POST /api/storyboard-attach-only` hoặc mở storyboard trước, rồi gọi `/api/storyboard-media`.
- Điều khiển độ phân giải không khả dụng trong PWA:
  - `High` resolution chỉ khả dụng khi model là `Sora 2 Pro`.
- Lỗi chromedriver sai phiên bản:
  - Gỡ các bản chromedriver pin thủ công khỏi shell profile; dự án này cố tình để Selenium Manager chọn đúng version.

## 🧭 Lộ trình

Các cải tiến dự kiến/có khả năng sẽ tới:
- Thêm automated tests cho ổn định selector và API handlers.
- Thêm công cụ lint/format và workflow CI.
- Thêm PWA icon assets và chiến lược cache offline mạnh hơn.
- Thêm README đa ngôn ngữ chính thức trong `i18n/`.
- Thêm metadata đóng gói để cài đặt dễ dàng hơn.

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón.

Quy trình gợi ý:
1. Fork và tạo nhánh tính năng.
2. Giữ phạm vi thay đổi hẹp, kèm ghi chú tái tạo/sử dụng cho các thay đổi tự động hóa UI.
3. Kiểm tra luồng thủ công với một phiên Chrome thật đang gắn.
4. Mở PR kèm chi tiết hành vi trước/sau.

Nếu bạn thay đổi selectors hoặc logic tương tác, hãy đính kèm ngữ cảnh UI của Sora để việc truy tìm regression dễ hơn.

## 🙏 Lời cảm ơn

- Selenium và Selenium Manager cho tự động hóa trình duyệt và việc giải quyết driver.
- Tornado cho service điều khiển HTTP/WebSocket async nhẹ.
- Pillow và `pillow-heif` cho hỗ trợ chuyển đổi/preview ảnh local.

## 🧱 Bản dựng ổn định đã kiểm chứng

Nếu bạn cần một baseline ổn định đảm bảo media attachment của storyboard hoạt động trọn chuỗi end-to-end (bao gồm các nút Open Storyboard / Attach Current Path và luồng Apply kết hợp), hãy xem commit:

`c6683ed6d9ee0ac110536352867a26a966e3e275`

## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |

## 📄 License

Hiện chưa có file license trong snapshot repository này (đã kiểm tra trong bản nháp này vào ngày **February 28, 2026**).

Giả định: mọi quyền vẫn thuộc về chủ sở hữu repository cho đến khi thêm file `LICENSE`. Nếu không đúng ý định này, hãy thêm file `LICENSE` và cập nhật phần này.
