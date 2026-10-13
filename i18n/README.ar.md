[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


[![LazyingArt banner — apps and four buddies](https://github.com/lachlanchen/LazyingArtWebsite/raw/main/media/brand/lazyingart-intro.gif)](https://lazying.art)

# SoraRemote

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20WSL-6c757d)
![Server](https://img.shields.io/badge/Server-Tornado%20API-0EA5E9)
![Frontend](https://img.shields.io/badge/Frontend-PWA-10B981)
![Status](https://img.shields.io/badge/Status-Experimental-F59E0B)
![Control%20Modes](https://img.shields.io/badge/Control%20Modes-CLI%20%7C%20REST%20%7C%20PWA-0EA5E9)
![Runtime](https://img.shields.io/badge/Runtime-Linux%20%7C%20macOS%20%7C%20WSL-6B7280)

SoraRemote هي أداة خفيفة تجمع بين Python وSelenium لأتمتة واجهة Sora الويب.

تدعم ثلاثة أوضاع تنفيذية متكاملة لنفس سير عمل الأتمتة:
1. **وكيل أتمتة CLI** (`agents/sora_agent.py`) لكتابة الموجّهات وتنفيذ إجراءات الواجهة.
2. **أداة تنزيل CLI** (`agents/sora_download.py`) لاكتشاف وتنزيل المرشحين للوسائط.
3. **طبقة تحكم Tornado + PWA** (`server/app.py` + `pwa/`) لتنسيق المتصفح عبر API.

تم الإبقاء على محتوى README الحالي كمرجع تشغيلي أساسي وتم إعادة تنظيمه لتحسين الوضوح.

## 🚀 الوصول السريع

| الهدف | نقطة الدخول | الاستخدام الأساسي |
| --- | --- | --- |
| تشغيل الموجّهات النصية | `agents/sora_agent.py` | إدارة إجراءات المؤلف من خلال CLI أو سكربت محيط |
| جلب الوسائط المولَّدة | `agents/sora_download.py` | اكتشاف وترحيل المرشحين محليًا |
| التحكم عن بُعد | `server/app.py` + `pwa/` | تحكم عبر REST/WebSocket + لوحة تحكم المتصفح |

## ✨ نظرة عامة

التصميم الأساسي:
- الاتصال بجلسة Chrome دائمة عبر DevTools Remote Debugging (المنفذ الافتراضي `9333`).
- إعادة استخدام حالة ملف تعريف المتصفح للحفاظ على استمرارية تسجيل الدخول والجلسة.
- أتمتة إجراءات المؤلف الأساسية (الكتابة، إضافة وسائط، storyboard، settings، create).
- إتاحة نفس الإجراءات عبر REST + سجل WebSocket للتحكم في PWA المحلي.

### لقطة سير العمل

| سير العمل | نقطة الدخول | الاستخدام الأساسي |
| --- | --- | --- |
| وكيل CLI | `agents/sora_agent.py` | كتابة الموجّهات، النقر على عناصر التحكم، أتمتة تدفق التكوين |
| أداة تنزيل CLI | `agents/sora_download.py` | اكتشاف الوسائط القابلة للتنزيل وحفظ الملفات محليًا |
| API + PWA | `server/app.py` + `pwa/` | تحكم عن بُعد وتنسيق مرئي من المتصفح |

## ✅ الميزات

- تدفق إرفاق/تشغيل Chrome مع ملف تعريف قابل لإعادة الاستخدام (`--debugger-port`, `--start-chrome`, `--user-data-dir`).
- نقرات آمنة أو مقيدة (`force`) على عناصر التحكم الأساسية (`plus`, `storyboard`, `settings`, `create`, `profile`).
- كتابة الموجّهات مع سلوك احتياطي للمحددات (selectors).
- إرفاق وسائط عبر مسار ملف باستخدام حقن DataTransfer.
- تعبئة مشاهد Storyboard + تحديث النصوص + إرفاق وسائط Storyboard.
- أتمتة الإعدادات المتعلقة بـ model/orientation/duration/resolution.
- تدفق منفصل لاكتشاف الملفات القابلة للتنزيل ثم جلبها باستخدام ملفات تعريف الارتباط الخاصة بالمتصفح.
- واجهة REST API قائمة على Tornado مع تدفق WebSocket مباشر لأحداث التصحيح.
- PWA محلي قابل للتثبيت مع رفع ومعاينة وعناصر تحكم تفصيلية.

## 🗂️ بنية المشروع

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

## 🧩 المتطلبات المسبقة

- Python 3.10+ (موصى به).
- Chrome/Chromium مثبت وقابل للتشغيل.
- شاشة عرض عند التشغيل غير headless (`--no-headless`) عندما يلزم تسجيل الدخول أو التفاعل اليدوي.
- وصول إلى حساب Sora في ملف تعريف Chrome المرفق.

## 📦 التثبيت

سير الإعداد كما في README الأساسي:

```bash
conda activate agent
pip install -r requirements.txt
```

التبعيات في `requirements.txt`:

| الحزمة | مواصفات الإصدار |
| --- | --- |
| `selenium` | `>=4.17.2` |
| `tornado` | `>=6.4` |
| `Pillow` | `>=9.4.0` |
| `pillow-heif` | `>=0.16.0` |

## 🚀 الاستخدام

### بدء سريع (وكيل CLI)

البدء السريع (يفتح Sora في متصفح مُدار):

```bash
python agents/sora_agent.py
```

الاتصال بـ Chrome مع جلسة مستمرة (موصى به لـ Sora):

```bash
python -m agents.sora_agent --debugger-port 9333 --start-chrome --no-headless --login-timeout 600 --text "A sunset over Tokyo, cinematic."
```

ملاحظات:
- تفتح نافذة Chrome على صفحة Sora. إذا تم إعادة التوجيه إلى تسجيل الدخول، سجّل الدخول؛ السكربت ينتظر حتى الإنهاء ثم يكتب الموجّه.
- لإعادة استخدام نفس جلسة تسجيل الدخول، مرّر مسار ملف تعريف ثابت:

```bash
python -m agents.sora_agent --debugger-port 9333 --start-chrome --no-headless --user-data-dir "$HOME/chrome_sora_profile_9333"
```

### خيارات CLI الأساسية (`agents/sora_agent.py`)

- `--url` الصفحة المستهدفة (الافتراضي: `https://sora.chatgpt.com/explore`).
- `--debugger-port` للاتصال بـ Chrome الذي شُغّل باستخدام `--remote-debugging-port=PORT`.
- `--start-chrome` إذا استُخدم مع `--debugger-port`، فهو يشغّل Chrome تلقائيًا (مع `--user-data-dir`).
- `--no-headless` لتشغيل متصفح مرئي؛ ضروري لعمليات تسجيل الدخول وCloudflare.
- `--selector` محدد CSS لتحديد حقل الإدخال (الافتراضي يتوافق مع textarea الخاص بمؤلف Sora).
- `--text` النص المراد كتابته في الحقل.
- `--chrome-binary` تحديد مسار Chrome/Chromium صريح.
- `--action` إجراءات الواجهة: `list`, `plus`, `storyboard`, `settings`, `create`, `profile`.
- `--force-click` تنفيذ النقر حتى لو بدا العنصر معطلاً.
- `--login-timeout` مدة الانتظار لإكمال التحقق اليدوي من الهوية.

معالجة المُشغّل:
- يزيل الوكيل أي `chromedriver` قديم من `PATH` قبل التشغيل.
- ثم يقوم Selenium Manager تلقائيًا بتحديد إصدار متوافق مع Chrome المثبت.

### أمثلة CLI (تحكم الواجهة)

قائمة العناصر الشائعة والنقر عليها:

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action list --action storyboard --action settings --action plus
```

نقر قسري على زر Create video (حتى لو كان معطّلاً):

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action create --force-click
```

فتح profile/settings والتنقل يدويًا إذا لزم الأمر:

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action list --action profile
```

إذا لم يتم اكتشاف `profile`، فزر `settings` يفتح عادةً نفس القائمة.

### مسار التنزيل

اكتشاف وتنزيل الفيديوهات عبر سكربت الوسيط:

- تشغيل تجريبي (عرض المرشحين فقط): `./bin/sora_download.sh --dry-run`
- تنزيل حتى ملفين إلى `./downloads/sora`: `./bin/sora_download.sh --max 2`
- تغيير مجلد الإخراج: `OUT_DIR=$HOME/Videos/sora ./bin/sora_download.sh --max 1`

يمكن أيضًا استخدام الاستدعاء المباشر للوحدة عبر `python -m agents.sora_download ...`.

## 🌐 خادم التحكم + PWA

تشغيل خادم Tornado:

```bash
python server/app.py
# listens on http://0.0.0.0:8791 and serves the PWA at /
```

افتراضيًا، الخادم:
- يعيد استخدام Chrome على منفذ remote debugging `9333`.
- يحفظ الملفات المرفوعة في `./uploads` ما لم يتم ضبط `SORA_UPLOADS_DIR`.

### نقاط النهاية الرئيسية

تعمل جميع نقاط النهاية على Chrome المتصل حاليًا (المنفذ الافتراضي لـ debugger هو `9333`).

| Method | Path | Payload | الوصف |
| --- | --- | --- | --- |
| `GET` | `/api/status` | none | تُعيد حالة جاهزية DevTools والمنفذ النشط. |
| `POST` | `/api/open` | `{ url? }` | يوجّه تبويب Chrome المتصل إلى عنوان URL المحدد (الافتراضي Sora Explore). |
| `GET` | `/api/actions` | none | يفحص حالة الأزرار/عناصر التحكم (حالة found/displayed/disabled). |
| `POST` | `/api/click` | `{ key, force? }` | ينفّذ ضغطًا على عنصر تحكم واحد حيث `key ∈ {plus, storyboard, settings, create, profile}`. |
| `POST` | `/api/type` | `{ text, selector?, url? }` | يكتب نص الموجّه داخل محدد composer. |
| `POST` | `/api/compose` | `{ text, click_create? }` | يفتح صفحة الإنشاء، يكتب النص، وينقر على create اختياريًا. |
| `POST` | `/api/attach` | `{ path, click_plus? }` | يرفع الوسائط عبر حقن DataTransfer؛ ويقوم تلقائيًا بتفريغ الوسائط الحالية (`click_plus` افتراضيه `false`). |
| `POST` | `/api/describe` | `{ text }` | يملأ حقل “Optionally describe your video…”. |
| `POST` | `/api/script-updates` | `{ text }` | يملأ حقل “Describe updates to your script…”. |
| `POST` | `/api/storyboard` | `{ scenes: ["scene 1", ...], script_updates?: "...", media_path?: "..." }` | يفتح storyboard، يملأ حقول المشاهد، ويطبّق تحديثات النص ووسائط storyboard اختيارياً. |
| `POST` | `/api/storyboard-media` | `{ path }` | يرفق وسائط على uploader مخصص لـ storyboard عندما يكون storyboard ظاهراً. |
| `POST` | `/api/storyboard-attach-only` | `{ path }` | يضمن فتح storyboard أولاً ثم يرفق الوسائط. |
| `POST` | `/api/settings` | `{ model?, orientation?, duration?, resolution? }` | يفتح إعدادات Sora ويطبّق القيم المحددة؛ وتعيد الاستجابة الملصقات المطبّقة. |
| `POST` | `/api/upload` | multipart form data | يحفظ الملفات المحلية في دليل رفع الخادم ويعيد المسارات الجانبية للخادم. |
| `POST` | `/api/preview` | multipart form data | يحول الصورة إلى معاينة PNG (مفيد كبديل fallback لـ HEIC/HEIF/AVIF في الواجهة). |
| `GET` | `/ws` | WebSocket | يرسل تدفقًا مباشراً لأحداث الإجراء والتصحيح. |

### عناصر تحكم PWA

افتح `http://0.0.0.0:8791` (أو المضيف الذي تختاره) بعد تشغيل `server/app.py`.

أبرز المزايا في التطبيق الحالي:
- رفع وسائط عبر ملف أو لصق مسار ثم النقر على **Plus** للإرفاق دون إعادة فتح حوارات اختيار الملفات.
- تعبئة وصف الوسائط في مربع “Media description” المخصّص.
- عناصر تحكم مستقلة لـ **Set Model** و**Set Orientation** و**Set Duration** و**Set Resolution** مع تحديثات النص.
- عناصر تحكم Storyboard للمشاهد وتحديثات النص وفتح لوحة storyboard ورفق مسار storyboard الحالي.
- سجل تصحيح مباشر يعرض استدعاءات API والقيم المرجعة من Sora (مثل model/duration المختارين).

## ⚙️ الإعداد

### متغيرات البيئة

`server/app.py` يقرأ:
- `SORA_DEBUGGER_PORT` (الافتراضي `9333`)
- `SORA_USER_DATA_DIR` (الافتراضي `~/chrome_sora_profile_<port>`)
- `SORA_DISPLAY` (عرض X اختياري)
- `SORA_API_PORT` (الافتراضي `8791`)
- `SORA_URL` (الافتراضي `https://sora.chatgpt.com/explore`)
- `SORA_UPLOADS_DIR` (تجاوز اختياري لدليل الرفع)

`agents/sora_agent.py` يدعم أيضًا:
- `CHROME_BINARY` (إذا لم يتم تمرير `--chrome-binary`)

تدعم سكربتات التغليف:
- `PORT`, `SORA_PROFILE_DIR`, `TIMEOUT`, `LOGIN_TIMEOUT` (`bin/sora_type.sh`)
- `PORT`, `SORA_PROFILE_DIR`, `OUT_DIR` (`bin/sora_download.sh`)

## 🧪 أمثلة

### مثال API شامل (curl)

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

### رفع وسائط + إرفاقها عبر API

```bash
# Upload file and get server path
curl -s -X POST http://127.0.0.1:8791/api/upload -F 'file=@/absolute/path/to/input.jpg'

# Then attach using returned path
curl -s -X POST http://127.0.0.1:8791/api/attach \
  -H 'Content-Type: application/json' \
  -d '{"path":"/absolute/or/server-returned/path.jpg","click_plus":false}'
```

## 🛠️ ملاحظات التطوير

- لا توجد حاليًا وحدة تعبئة كمكتبة (`pyproject.toml`/`setup.py` غير موجودين).
- لا يوجد حاليًا CI/test/lint في لقطة هذا المستودع.
- `selenium_template` هو symlink إلى `../auto-publish/`؛ محتوى الهدف يقع خارج هذا المستودع.
- ملف تعريف PWA يشير إلى `/icons/icon-192.png` و`/icons/icon-512.png`; أصول الأيقونات غير مضافة حاليًا في هذا المستودع.

## 🧯 استكشاف الأخطاء وإصلاحها

- فشل اتصال Chrome:
  - تأكد من تشغيل Chrome باستخدام `--remote-debugging-port=9333` (أو المنفذ المطابق لقيمة `--debugger-port`).
  - افحص `GET /api/status` للتأكد من `devtools_ready: true`.
- تكرار طلبات تسجيل الدخول:
  - استخدم `--user-data-dir` ثابتًا وتجنب مسارات ملفات تعريف عشوائية.
- تعثّر تدفق Cloudflare/تسجيل الدخول:
  - شغل بدون headless (`--no-headless`) وزد `--login-timeout`.
- إرفاق الوسائط لا يعمل:
  - تأكد أن المسار موجود فعليًا على خادم التشغيل، واستخدم `/api/upload` + المسار المُعاد إذا لزم الأمر.
- فشل إرفاق وسائط Storyboard:
  - جرّب `POST /api/storyboard-attach-only` أو افتح storyboard أولًا ثم `/api/storyboard-media`.
- تحكم الدقة غير متاح في PWA:
  - دقة `High` لا تتاح إلا عندما يكون model هو `Sora 2 Pro`.
- مشاكل chromedriver غير متوافق:
  - احذف أي نسخة chromedriver مثبّتة يدويًا من إعدادات shell الخاصة بك؛ هذا المشروع يعتمد عمداً على Selenium Manager لاختيار النسخ المتوافقة.

## 🧭 خارطة الطريق

التحسينات المخطط لها/المحتملة:
- إضافة اختبارات آلية لاستقرار المحددات ومعالجات API.
- إضافة أدوات lint/format وسير عمل CI.
- إضافة أصول أيقونات PWA المتتبعة وتطوير استراتيجية أقوى للتخزين المؤقت بدون اتصال.
- إضافة ملفات README متعددة اللغات رسمية تحت `i18n/`.
- إضافة بيانات تعريف الحزمة لتسهيل التثبيت.

## 🤝 المساهمة

نرحب بالمساهمات.

الخطوات المقترحة:
1. أنشئ fork وأنشئ فرع ميزة.
2. اجعل التغييرات ضمن نطاق واضح وضمّن ملاحظات إعادة الإنتاج/الاستخدام لتغييرات تفاعل الواجهة.
3. تحقّق يدويًا من التدفقات باستخدام جلسة Chrome حقيقية.
4. افتح PR مع تفاصيل سلوك قبل/بعد.

إذا غيّرت المحددات أو منطق التفاعل، أضف سياقًا فعليًا لواجهة Sora لتسهيل تتبع الانحدارات.

## 🙏 الشكر والتقدير

- Selenium وSelenium Manager لأتمتة المتصفح وحل أدوار driver.
- Tornado لخدمة التحكم الخفيفة عبر HTTP/WebSocket.
- Pillow و`pillow-heif` لدعم التحويل/المعاينة المحلية للصور.

## 🧱 نسخة مرجعية مستقرة

إذا احتجت إلى قاعدة مستقرة تضمن عمل إرفاق وسائط Storyboard بشكل شامل نهاية إلى نهاية (بما في ذلك أزرار Open Storyboard / Attach Current Path وتدفق Apply المدمج)، استخدم هذا الـ commit:

`c6683ed6d9ee0ac110536352867a26a966e3e275`

## 📄 الترخيص

لا يوجد ملف ترخيص حاليًا في هذه النسخة من المستودع (تم التحقق في هذه المسودة بتاريخ **February 28, 2026**).

الافتراض: جميع الحقوق مملوكة لمالك المستودع حتى يتم إضافة ملف ترخيص. إذا لم يكن هذا مقصودًا، أضف ملف `LICENSE` وحدث هذا القسم.


## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |
