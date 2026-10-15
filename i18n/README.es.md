[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


[![LazyingArt banner — apps and four buddies](https://lazying.art/media/brand/lazyingart-intro.gif)](https://lazying.art)

# SoraRemote

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20WSL-6c757d)
![Server](https://img.shields.io/badge/Server-Tornado%20API-0EA5E9)
![Frontend](https://img.shields.io/badge/Frontend-PWA-10B981)
![Status](https://img.shields.io/badge/Status-Experimental-F59E0B)
![Control%20Modes](https://img.shields.io/badge/Control%20Modes-CLI%20%7C%20REST%20%7C%20PWA-0EA5E9)
![Runtime](https://img.shields.io/badge/Runtime-Linux%20%7C%20macOS%20%7C%20WSL-6B7280)

SoraRemote es un kit de herramientas de Python + Selenium ligero para automatizar la interfaz web de Sora.

Admite tres modos de ejecución complementarios para un mismo flujo de automatización:
1. **Agente de automatización CLI** (`agents/sora_agent.py`) para escribir prompts y controlar la UI.
2. **Descargador CLI** (`agents/sora_download.py`) para descubrir y descargar medios candidatos.
3. **Plano de control Tornado + PWA** (`server/app.py` + `pwa/`) para orquestación del navegador mediante API.

El contenido actual del README se conserva como referencia operativa canónica y se reorganiza para mayor claridad.

## 🚀 Acceso rápido

| Objetivo | Punto de entrada | Uso principal |
| --- | --- | --- |
| Ejecutar prompts por script | `agents/sora_agent.py` | Ejecutar acciones del compositor desde CLI o script wrapper |
| Obtener medios generados | `agents/sora_download.py` | Descubrir y guardar candidatos localmente |
| Control remoto | `server/app.py` + `pwa/` | Control por REST/WebSocket + panel de navegador |

## ✨ Descripción general

Diseño principal:
- Conexión a una sesión persistente de Chrome mediante depuración remota de DevTools (puerto predeterminado `9333`).
- Reutilización del estado del perfil del navegador para conservar continuidad de sesión/login.
- Automatización de acciones clave del compositor (escribir, adjuntar plus/media, storyboard, ajustes, crear).
- Exposición de las mismas acciones mediante REST + logs WebSocket para un controlador PWA local.

### Vista rápida del flujo

| Flujo | Punto de entrada | Uso principal |
| --- | --- | --- |
| Agente CLI | `agents/sora_agent.py` | Escribir prompts, pulsar controles, automatizar el flujo de composición |
| Descargador CLI | `agents/sora_download.py` | Descubrir medios descargables y guardar archivos localmente |
| API + PWA | `server/app.py` + `pwa/` | Control remoto y orquestación visual desde navegador |

## ✅ Características

- Flujo de anexado/inicio de Chrome con perfil reutilizable (`--debugger-port`, `--start-chrome`, `--user-data-dir`).
- Clic seguro o forzado para controles clave (`plus`, `storyboard`, `settings`, `create`, `profile`).
- Escritura de prompts con comportamiento de respaldo de selectores.
- Adjuntar medios mediante ruta de archivo con inyección de DataTransfer.
- Relleno de escenas de storyboard + actualizaciones de guion + adjunto de medios específicos para storyboard.
- Automatización de ajustes para modelo/orientación/duración/resolución.
- Flujo separado de descubrimiento + descarga usando cookies del navegador.
- API REST de Tornado y stream de depuración en tiempo real por WebSocket.
- PWA local instalable con carga, vista previa y controles granulares.

## 🗂️ Estructura del proyecto

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

## 🧩 Requisitos previos

- Python 3.10+ (recomendado).
- Chrome/Chromium instalado y ejecutable.
- Una pantalla para uso sin headless (`--no-headless`) cuando se requiera inicio de sesión o UI interactiva.
- Acceso a cuenta de Sora en el perfil de Chrome adjunto.

## 📦 Instalación

Flujo de configuración existente del README canónico:

```bash
conda activate agent
pip install -r requirements.txt
```

Dependencias en `requirements.txt`:

| Paquete | Especificación de versión |
| --- | --- |
| `selenium` | `>=4.17.2` |
| `tornado` | `>=6.4` |
| `Pillow` | `>=9.4.0` |
| `pillow-heif` | `>=0.16.0` |

## 🚀 Uso

### Inicio rápido (agente CLI)

Inicio rápido (abre Sora en un navegador gestionado):

```bash
python agents/sora_agent.py
```

Conectar a Chrome con sesión persistente (recomendado para Sora):

```bash
python -m agents.sora_agent --debugger-port 9333 --start-chrome --no-headless --login-timeout 600 --text "A sunset over Tokyo, cinematic."
```

Notas:
- Se abre una ventana de Chrome en la página de Sora. Si se redirige al login, inicia sesión; el script espera y luego escribe tu prompt.
- Para reutilizar el mismo login, pasa una ruta de perfil fija:

```bash
python -m agents.sora_agent --debugger-port 9333 --start-chrome --no-headless --user-data-dir "$HOME/chrome_sora_profile_9333"
```

### Opciones clave de CLI (`agents/sora_agent.py`)

- `--url` página destino (predeterminado: `https://sora.chatgpt.com/explore`).
- `--debugger-port` para conectarse a un Chrome existente iniciado con `--remote-debugging-port=PORT`.
- `--start-chrome`: si se usa junto con `--debugger-port`, inicia Chrome por ti (con `--user-data-dir`).
- `--no-headless` para ejecutar un navegador visible; necesario para login y Cloudflare.
- `--selector` CSS para localizar el input (por defecto coincide con el textarea del compositor de Sora).
- `--text` qué texto introducir en el input.
- `--chrome-binary` define explícitamente la ruta de Chrome/Chromium.
- `--action` acciones de UI: `list`, `plus`, `storyboard`, `settings`, `create`, `profile`.
- `--force-click` hace clic incluso si un elemento parece deshabilitado.
- `--login-timeout` tiempo de espera para completar autenticación manual.

Gestión del driver:
- El agente elimina de `PATH` cualquier `chromedriver` obsoleto antes del arranque.
- Selenium Manager resuelve automáticamente un driver compatible con el Chrome instalado.

### Ejemplos de CLI (controles de UI)

Listar y pulsar controles comunes:

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action list --action storyboard --action settings --action plus
```

Forzar clic en el botón Create (incluso si está deshabilitado):

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action create --force-click
```

Abrir perfil/ajustes y navegar manualmente si fuera necesario:

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action list --action profile
```

Si no se detecta `profile`, normalmente `settings` abre el mismo menú.

### Flujo del descargador

Descubrir y descargar vídeos con el script wrapper:

- Simulación (solo listar candidatos): `./bin/sora_download.sh --dry-run`
- Descargar hasta 2 archivos a `./downloads/sora`: `./bin/sora_download.sh --max 2`
- Cambiar carpeta de salida: `OUT_DIR=$HOME/Videos/sora ./bin/sora_download.sh --max 1`

También está disponible el uso directo del módulo mediante `python -m agents.sora_download ...`.

## 🌐 Servidor de control + PWA

Ejecutar el servidor Tornado:

```bash
python server/app.py
# listens on http://0.0.0.0:8791 and serves the PWA at /
```

Por defecto el servidor:
- Reutiliza Chrome en el puerto de depuración remota `9333`.
- Almacena cargas en `./uploads` salvo que se establezca `SORA_UPLOADS_DIR`.

### Endpoints clave

Todos los endpoints operan sobre el Chrome actualmente adjunto (por defecto al puerto de depuración `9333`).

| Método | Ruta | Carga útil | Descripción |
| --- | --- | --- | --- |
| `GET` | `/api/status` | none | Devuelve estado de disponibilidad de DevTools y puerto activo. |
| `POST` | `/api/open` | `{ url? }` | Navega la pestaña adjunta de Chrome a la URL indicada (por defecto, Sora Explore). |
| `GET` | `/api/actions` | none | Inspecciona estado de botones/controles (`found`/`displayed`/`disabled`). |
| `POST` | `/api/click` | `{ key, force? }` | Pulsa un control donde `key ∈ {plus, storyboard, settings, create, profile}`. |
| `POST` | `/api/type` | `{ text, selector?, url? }` | Escribe el texto del prompt en el selector del compositor. |
| `POST` | `/api/compose` | `{ text, click_create? }` | Abre la página de composición, escribe el texto y opcionalmente pulsa crear. |
| `POST` | `/api/attach` | `{ path, click_plus? }` | Sube medios mediante inyección DataTransfer; limpia los medios existentes automáticamente (`click_plus` es `false` por defecto). |
| `POST` | `/api/describe` | `{ text }` | Rellena el textarea “Optionally describe your video…”. |
| `POST` | `/api/script-updates` | `{ text }` | Rellena el campo “Describe updates to your script…”. |
| `POST` | `/api/storyboard` | `{ scenes: ["scene 1", ...], script_updates?: "...", media_path?: "..." }` | Abre storyboard, rellena los textareas de escenas y opcionalmente aplica actualizaciones de guion y medios de storyboard. |
| `POST` | `/api/storyboard-media` | `{ path }` | Adjunta medios al uploader específico de storyboard cuando storyboard ya está visible. |
| `POST` | `/api/storyboard-attach-only` | `{ path }` | Asegura que storyboard esté abierto y luego adjunta medios. |
| `POST` | `/api/settings` | `{ model?, orientation?, duration?, resolution? }` | Abre ajustes y aplica los valores seleccionados; la respuesta refleja las etiquetas aplicadas. |
| `POST` | `/api/upload` | multipart form data | Guarda archivo(s) local(es) en el directorio de cargas del servidor y devuelve rutas del lado del servidor. |
| `POST` | `/api/preview` | multipart form data | Convierte una imagen a vista previa PNG (útil para fallback HEIC/HEIF/AVIF en la UI). |
| `GET` | `/ws` | WebSocket | Emite eventos de acción/depuración en vivo. |

### Controles de la PWA

Abre `http://0.0.0.0:8791` (o tu host elegido) tras iniciar `server/app.py`.

Características de la implementación actual:
- Cargar medios mediante selector de archivos o pegando una ruta, luego pulsar **Plus** para adjuntar sin reabrir diálogos del sistema.
- Aplicar descripción de medios en el recuadro dedicado “Media description”.
- Controles independientes para **Set Model**, **Set Orientation**, **Set Duration**, **Set Resolution** y actualizaciones de guion.
- Controles de storyboard para escenas, actualizaciones de guion, abrir panel de storyboard y adjuntar la ruta actual de storyboard.
- Registro de depuración en vivo mostrando llamadas a la API y valores devueltos por Sora (por ejemplo, modelo/duración seleccionados).

## ⚙️ Configuración

### Variables de entorno

`server/app.py` lee:
- `SORA_DEBUGGER_PORT` (predeterminado `9333`)
- `SORA_USER_DATA_DIR` (predeterminado `~/chrome_sora_profile_<port>`)
- `SORA_DISPLAY` (pantalla X opcional)
- `SORA_API_PORT` (predeterminado `8791`)
- `SORA_URL` (predeterminado `https://sora.chatgpt.com/explore`)
- `SORA_UPLOADS_DIR` (sobrescritura opcional del directorio de cargas)

`agents/sora_agent.py` también admite:
- `CHROME_BINARY` (si no se proporciona `--chrome-binary`)

Los scripts wrapper admiten:
- `PORT`, `SORA_PROFILE_DIR`, `TIMEOUT`, `LOGIN_TIMEOUT` (`bin/sora_type.sh`)
- `PORT`, `SORA_PROFILE_DIR`, `OUT_DIR` (`bin/sora_download.sh`)

## 🧪 Ejemplos

### Ejemplo de API de extremo a extremo (curl)

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

### Carga y adjunto de medios vía API

```bash
# Upload file and get server path
curl -s -X POST http://127.0.0.1:8791/api/upload -F 'file=@/absolute/path/to/input.jpg'

# Then attach using returned path
curl -s -X POST http://127.0.0.1:8791/api/attach \
  -H 'Content-Type: application/json' \
  -d '{"path":"/absolute/or/server-returned/path.jpg","click_plus":false}'
```

## 🛠️ Notas de desarrollo

- Actualmente no hay un módulo empaquetado (`pyproject.toml`/`setup.py` no está presente).
- Actualmente no hay pipeline de CI/tests/lint en esta instantánea del repositorio.
- `selenium_template` es un enlace simbólico a `../auto-publish/`; su contenido objetivo está fuera de este repositorio.
- El manifiesto de PWA referencia `/icons/icon-192.png` y `/icons/icon-512.png`; los recursos de iconos no se rastrean actualmente en este repositorio.

## 🧯 Solución de problemas

- Chrome no se consigue anexar:
  - Asegúrate de que Chrome se inicie con `--remote-debugging-port=9333` (o el puerto indicado por `--debugger-port`).
  - Comprueba `GET /api/status` y `devtools_ready: true`.
- Prompts de inicio de sesión repetidos:
  - Usa un `--user-data-dir` persistente y evita rutas de perfil aleatorias.
- Flujo de Cloudflare/login que no avanza:
  - Ejecuta sin headless (`--no-headless`) y aumenta `--login-timeout`.
- Adjuntar medios no hace nada:
  - Confirma que la ruta del archivo exista en la máquina del servidor y usa `/api/upload` + ruta devuelta si no estás seguro.
- Adjuntar medios a storyboard falla:
  - Prueba `POST /api/storyboard-attach-only` o abre primero storyboard y luego `/api/storyboard-media`.
- El control de resolución no está disponible en PWA:
  - La resolución `High` solo se habilita cuando el modelo es `Sora 2 Pro`.
- Problemas con chromedriver incorrecto:
  - Elimina de tu perfil de shell cualquier `chromedriver` anclado manualmente; este proyecto deja que Selenium Manager elija versiones compatibles de forma intencional.

## 🧭 Hoja de ruta

Mejoras previstas/probables:
- Añadir pruebas automatizadas para estabilidad de selectores y manejadores de API.
- Añadir herramientas de lint/format y flujos de CI.
- Añadir assets de iconos PWA rastreables y estrategia de caché offline más robusta.
- Añadir archivos README multilingües formales bajo `i18n/`.
- Añadir metadatos de empaquetado para facilitar la instalación.

## 🤝 Contribuciones

Las contribuciones son bienvenidas.

Proceso sugerido:
1. Haz un fork y crea una rama de características.
2. Mantén los cambios acotados e incluye notas de reproducción/uso para cambios en automatización de UI.
3. Valida los flujos manualmente con una sesión real de Chrome adjunta.
4. Abre un PR con detalles de comportamiento antes/después.

Si cambias selectores o la lógica de interacción, incluye contexto UI de Sora concreto para que las regresiones sean más fáciles de depurar.

## 🙏 Agradecimientos

- Selenium y Selenium Manager por la automatización de navegador y resolución del driver.
- Tornado por el servicio HTTP/WebSocket async ligero.
- Pillow y `pillow-heif` por soporte local de conversión y vista previa de imagen.

## 🧱 Build estable conocida

Si necesitas una base estable que garantice que la adjunción de medios de storyboard funcione de extremo a extremo (incluyendo los botones Open Storyboard / Attach Current Path y el flujo combinado Apply), consulta el commit:

`c6683ed6d9ee0ac110536352867a26a966e3e275`

## 📄 Licencia

Actualmente no hay archivo de licencia en esta instantánea del repositorio (comprobado en este borrador el **28 de febrero de 2026**).

Se asume que todos los derechos permanecen con el propietario del repositorio hasta que se añada una licencia. Si esto no es lo deseado, añade un archivo `LICENSE` y actualiza esta sección.


## ❤️ Support

<!-- support:start -->
[![GitHub Sponsors](https://img.shields.io/badge/GitHub-Sponsors-EA4AAA?style=for-the-badge&logo=githubsponsors&logoColor=white)](https://github.com/sponsors/lachlanchen)
[![LazyingArt Support](https://img.shields.io/badge/LazyingArt-Support-0EA5E9?style=for-the-badge)](https://chat.lazying.art/donate)
[![PayPal Support](https://img.shields.io/badge/PayPal-Support-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/RongzhouChen)
[![Stripe Support](https://img.shields.io/badge/Stripe-Support-635BFF?style=for-the-badge&logo=stripe&logoColor=white)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400)
<!-- support:end -->
