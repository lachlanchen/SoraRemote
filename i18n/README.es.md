[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)



# SoraRemote

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20WSL-6c757d)
![Server](https://img.shields.io/badge/Server-Tornado%20API-0EA5E9)
![Frontend](https://img.shields.io/badge/Frontend-PWA-10B981)
![Status](https://img.shields.io/badge/Status-Experimental-F59E0B)

SoraRemote es un toolkit ligero de Python + Selenium para automatizar la interfaz web de Sora.

Admite tres flujos de trabajo complementarios:
1. Agente de automatización por CLI (`agents/sora_agent.py`) para escribir prompts y ejecutar acciones de control en la UI.
2. Descargador por CLI (`agents/sora_download.py`) para descubrir y descargar candidatos de medios.
3. Servidor local de control Tornado + PWA (`server/app.py` + `pwa/`) para control impulsado por API y desde navegador.

El contenido actual de README se conserva como guía operativa canónica y se reorganiza para mayor claridad.

## ✨ Descripción general

Diseño principal:
- Conexión a una sesión persistente de Chrome mediante depuración remota de DevTools (puerto predeterminado `9333`).
- Reutilización del estado del perfil del navegador para mantener continuidad de login/sesión.
- Automatización de acciones clave del compositor (escribir, adjuntar con plus/media, storyboard, ajustes, crear).
- Exposición de las mismas acciones vía REST + registros WebSocket para un controlador PWA local.

### Resumen de flujos

| Flujo | Punto de entrada | Uso principal |
| --- | --- | --- |
| Agente CLI | `agents/sora_agent.py` | Escribir prompts, pulsar controles y automatizar el flujo de composición |
| Descargador CLI | `agents/sora_download.py` | Descubrir medios descargables y guardar archivos localmente |
| API + PWA | `server/app.py` + `pwa/` | Control remoto y orquestación visual desde navegador |

## ✅ Funcionalidades

- Flujo de conexión/inicio de Chrome con perfil reutilizable (`--debugger-port`, `--start-chrome`, `--user-data-dir`).
- Clics seguros o forzados para controles clave (`plus`, `storyboard`, `settings`, `create`, `profile`).
- Escritura de prompts con comportamiento de respaldo por selectores.
- Adjuntar medios mediante ruta de archivo con inyección de DataTransfer.
- Relleno de escenas en storyboard + actualizaciones de script + adjuntar medios específicos de storyboard.
- Automatización de ajustes para modelo/orientación/duración/resolución.
- Flujo separado de descubrimiento + descarga usando cookies del navegador.
- API REST de Tornado y flujo en vivo de depuración por WebSocket.
- PWA local instalable con carga de archivos, vista previa y controles granulares.

## 🗂️ Estructura del proyecto

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
│  └─ (actualmente vacío)
├─ uploads/
│  └─ .gitkeep
└─ selenium_template -> ../auto-publish/ (enlace simbólico)
```

## 🧩 Requisitos previos

- Python 3.10+ (recomendado).
- Chrome/Chromium instalado y ejecutable.
- Un entorno con display para uso no headless (`--no-headless`) cuando se requiera login o UI interactiva.
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

Conectarse a Chrome con sesión persistente (recomendado para Sora):

```bash
python -m agents.sora_agent --debugger-port 9333 --start-chrome --no-headless --login-timeout 600 --text "A sunset over Tokyo, cinematic."
```

Notas:
- Se abre una ventana de Chrome en la página de Sora. Si redirige al login, inicia sesión; el script espera y luego escribe tu prompt.
- Para reutilizar el mismo login, pasa una ruta fija de perfil:

```bash
python -m agents.sora_agent --debugger-port 9333 --start-chrome --no-headless --user-data-dir "$HOME/chrome_sora_profile_9333"
```

### Opciones clave de CLI (`agents/sora_agent.py`)

- `--url` página objetivo (predeterminado: `https://sora.chatgpt.com/explore`).
- `--debugger-port` conectarse a un Chrome existente iniciado con `--remote-debugging-port=PORT`.
- `--start-chrome` si se define junto con `--debugger-port`, inicia Chrome por ti (con `--user-data-dir`).
- `--no-headless` para ejecutar un navegador visible; necesario para login y Cloudflare.
- `--selector` CSS para localizar el input (predeterminado coincide con el textarea del compositor de Sora).
- `--text` texto que se va a escribir en el input.
- `--chrome-binary` define explícitamente una ruta de Chrome/Chromium.
- `--action` acciones de UI: `list`, `plus`, `storyboard`, `settings`, `create`, `profile`.
- `--force-click` hace clic incluso si un elemento parece deshabilitado.
- `--login-timeout` ventana de espera para completar autenticación manual.

Gestión del driver:
- El agente elimina cualquier `chromedriver` obsoleto de `PATH` antes de iniciar.
- Selenium Manager resuelve automáticamente un driver compatible con el Chrome instalado.

### Ejemplos de CLI (controles de UI)

Listar y pulsar controles comunes:

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action list --action storyboard --action settings --action plus
```

Forzar clic en el botón Create video (incluso si está deshabilitado):

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action create --force-click
```

Abrir perfil/ajustes y navegar manualmente si hace falta:

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action list --action profile
```

Si no se detecta `profile`, el botón `settings` normalmente abre el mismo menú.

### Flujo del descargador

Descubrir y descargar videos con el script wrapper:

- Simulación (solo listar candidatos): `./bin/sora_download.sh --dry-run`
- Descargar hasta 2 archivos en `./downloads/sora`: `./bin/sora_download.sh --max 2`
- Cambiar carpeta de salida: `OUT_DIR=$HOME/Videos/sora ./bin/sora_download.sh --max 1`

También se puede usar el módulo directamente con `python -m agents.sora_download ...`.

## 🌐 Servidor de control + PWA

Ejecuta el servidor Tornado:

```bash
python server/app.py
# listens on http://0.0.0.0:8791 and serves the PWA at /
```

Por defecto, el servidor:
- Reutiliza Chrome en el puerto de depuración remota `9333`.
- Guarda cargas en `./uploads` salvo que se defina `SORA_UPLOADS_DIR`.

### Endpoints clave

Todos los endpoints operan sobre el Chrome actualmente adjunto (por defecto puerto de depuración `9333`).

| Método | Ruta | Payload | Descripción |
| --- | --- | --- | --- |
| `GET` | `/api/status` | none | Devuelve el estado de disponibilidad de DevTools y el puerto activo. |
| `POST` | `/api/open` | `{ url? }` | Navega la pestaña de Chrome adjunta a la URL indicada (predeterminado: Sora Explore). |
| `GET` | `/api/actions` | none | Inspecciona estado de botones/controles (metadatos found/displayed/disabled). |
| `POST` | `/api/click` | `{ key, force? }` | Pulsa un control donde `key ∈ {plus, storyboard, settings, create, profile}`. |
| `POST` | `/api/type` | `{ text, selector?, url? }` | Escribe texto del prompt en el selector del compositor. |
| `POST` | `/api/compose` | `{ text, click_create? }` | Abre la página de composición, escribe texto y opcionalmente pulsa create. |
| `POST` | `/api/attach` | `{ path, click_plus? }` | Sube medios con inyección DataTransfer; limpia medios existentes automáticamente (`click_plus` por defecto `false`). |
| `POST` | `/api/describe` | `{ text }` | Rellena el textarea “Optionally describe your video…”. |
| `POST` | `/api/script-updates` | `{ text }` | Rellena el campo “Describe updates to your script…”. |
| `POST` | `/api/storyboard` | `{ scenes: ["scene 1", ...], script_updates?: "...", media_path?: "..." }` | Abre storyboard, rellena textareas de escenas y opcionalmente aplica actualizaciones de script y medios de storyboard. |
| `POST` | `/api/storyboard-media` | `{ path }` | Adjunta medios al uploader específico de storyboard cuando storyboard ya está visible. |
| `POST` | `/api/storyboard-attach-only` | `{ path }` | Asegura que storyboard esté abierto y luego adjunta medios. |
| `POST` | `/api/settings` | `{ model?, orientation?, duration?, resolution? }` | Abre ajustes y aplica valores seleccionados; la respuesta refleja las etiquetas aplicadas. |
| `POST` | `/api/upload` | multipart form data | Guarda archivo(s) local(es) en el directorio de cargas del servidor y devuelve rutas del lado del servidor. |
| `POST` | `/api/preview` | multipart form data | Convierte imagen a vista previa PNG (útil para fallback HEIC/HEIF/AVIF en la UI). |
| `GET` | `/ws` | WebSocket | Emite eventos de acción/depuración. |

### Controles de la PWA

Abre `http://0.0.0.0:8791` (o el host que elijas) después de iniciar `server/app.py`.

Puntos destacados de la implementación existente:
- Sube medios con selector de archivos o pegando una ruta, luego haz clic en **Plus** para adjuntar sin reabrir diálogos del sistema.
- Aplica descripción de medios en el cuadro dedicado “Media description”.
- Controles independientes para **Set Model**, **Set Orientation**, **Set Duration**, **Set Resolution** y actualizaciones de script.
- Controles de storyboard para escenas, actualizaciones de script, apertura del panel storyboard y adjuntar la ruta actual de storyboard.
- Registro de depuración en vivo que muestra llamadas de API y valores devueltos por Sora (por ejemplo modelo/duración seleccionados).

## ⚙️ Configuración

### Variables de entorno

`server/app.py` lee:
- `SORA_DEBUGGER_PORT` (predeterminado `9333`)
- `SORA_USER_DATA_DIR` (predeterminado `~/chrome_sora_profile_<port>`)
- `SORA_DISPLAY` (display X opcional)
- `SORA_API_PORT` (predeterminado `8791`)
- `SORA_URL` (predeterminado `https://sora.chatgpt.com/explore`)
- `SORA_UPLOADS_DIR` (opcional, para sobrescribir directorio de cargas)

`agents/sora_agent.py` también admite:
- `CHROME_BINARY` (si no se proporciona `--chrome-binary`)

Los scripts wrapper admiten:
- `PORT`, `SORA_PROFILE_DIR`, `TIMEOUT`, `LOGIN_TIMEOUT` (`bin/sora_type.sh`)
- `PORT`, `SORA_PROFILE_DIR`, `OUT_DIR` (`bin/sora_download.sh`)

## 🧪 Ejemplos

### Ejemplo API de extremo a extremo (curl)

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

### Carga de medios + adjuntar vía API

```bash
# Upload file and get server path
curl -s -X POST http://127.0.0.1:8791/api/upload -F 'file=@/absolute/path/to/input.jpg'

# Then attach using returned path
curl -s -X POST http://127.0.0.1:8791/api/attach \
  -H 'Content-Type: application/json' \
  -d '{"path":"/absolute/or/server-returned/path.jpg","click_plus":false}'
```

## 🛠️ Notas de desarrollo

- Actualmente no hay un módulo empaquetado (`pyproject.toml`/`setup.py` no están presentes).
- Actualmente no hay pipeline de CI/tests/lint en esta instantánea del repositorio.
- `selenium_template` es un enlace simbólico a `../auto-publish/`; el contenido de su destino está fuera de este repositorio.
- El manifiesto PWA referencia `/icons/icon-192.png` y `/icons/icon-512.png`; los recursos de iconos no están versionados actualmente en este repositorio.

## 🧯 Solución de problemas

- Chrome no logra conectarse:
  - Asegúrate de iniciar Chrome con `--remote-debugging-port=9333` (o el `--debugger-port` correspondiente).
  - Revisa `GET /api/status` para confirmar `devtools_ready: true`.
- Solicitudes de login repetidas:
  - Usa un `--user-data-dir` persistente y evita rutas de perfil aleatorias.
- Flujo de Cloudflare/login no avanza:
  - Ejecuta sin headless (`--no-headless`) y aumenta `--login-timeout`.
- Adjuntar medios no hace nada:
  - Confirma que la ruta del archivo exista en la máquina del servidor y usa `/api/upload` + la ruta devuelta si tienes dudas.
- Falla al adjuntar medios en storyboard:
  - Prueba `POST /api/storyboard-attach-only` o abre storyboard primero y luego `/api/storyboard-media`.
- Control de resolución no disponible en la PWA:
  - La resolución `High` solo se habilita cuando el modelo es `Sora 2 Pro`.
- Problemas con chromedriver incorrecto:
  - Elimina el chromedriver fijado manualmente de tu perfil de shell; este proyecto deja intencionalmente que Selenium Manager elija versiones compatibles.

## 🧭 Hoja de ruta

Próximas mejoras previstas/probables:
- Añadir tests automatizados para estabilidad de selectores y handlers de API.
- Añadir herramientas de lint/formato y workflows de CI.
- Añadir recursos de iconos PWA versionados y una estrategia de caché offline más sólida.
- Añadir archivos README multilingües formales bajo `i18n/`.
- Añadir metadatos de empaquetado para facilitar la instalación.

## 🤝 Contribuir

Las contribuciones son bienvenidas.

Proceso sugerido:
1. Haz un fork y crea una rama de funcionalidad.
2. Mantén los cambios acotados e incluye notas de reproducción/uso para cambios de automatización UI.
3. Valida los flujos manualmente con una sesión real de Chrome adjunto.
4. Abre un PR con detalles de comportamiento antes/después.

Si cambias selectores o lógica de interacción, incluye contexto concreto de la UI de Sora para facilitar el triaje de regresiones.

## ❤️ Soporte / Patrocinio

Enlaces de financiación desde `.github/FUNDING.yml`:
- GitHub Sponsors: https://github.com/sponsors/lachlanchen
- Enlaces del proyecto: https://lazying.art, https://chat.lazying.art, https://onlyideas.art

## 🙏 Agradecimientos

- Selenium y Selenium Manager por la automatización del navegador y la resolución del driver.
- Tornado por el servicio ligero asíncrono de control HTTP/WebSocket.
- Pillow y `pillow-heif` por el soporte local de conversión/vista previa de imágenes.

## 🧱 Build estable conocida

Si necesitas una base estable que garantice que la adjunción de medios en storyboard funcione de extremo a extremo (incluyendo los botones Open Storyboard / Attach Current Path y el flujo combinado Apply), revisa el commit:

`c6683ed6d9ee0ac110536352867a26a966e3e275`

## 📄 Licencia

Actualmente no hay archivo de licencia en esta instantánea del repositorio (verificado en este borrador el **28 de febrero de 2026**).

Suposición: todos los derechos siguen perteneciendo al propietario del repositorio hasta que se agregue una licencia. Si esto no es la intención, agrega un archivo `LICENSE` y actualiza esta sección.
