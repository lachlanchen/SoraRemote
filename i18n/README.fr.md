[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


# SoraRemote

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20WSL-6c757d)
![Server](https://img.shields.io/badge/Server-Tornado%20API-0EA5E9)
![Frontend](https://img.shields.io/badge/Frontend-PWA-10B981)
![Status](https://img.shields.io/badge/Status-Experimental-F59E0B)

SoraRemote est une boîte à outils légère en Python + Selenium pour automatiser l’interface web de Sora.

Elle prend en charge trois workflows complémentaires :
1. Agent d’automatisation CLI (`agents/sora_agent.py`) pour la saisie de prompts et les actions de contrôle de l’UI.
2. Téléchargeur CLI (`agents/sora_download.py`) pour découvrir et télécharger des médias candidats.
3. Serveur de contrôle Tornado local + PWA (`server/app.py` + `pwa/`) pour un contrôle piloté par API et via navigateur.

Le contenu actuel du README est conservé comme guide opérationnel canonique et réorganisé pour plus de clarté.

## ✨ Vue d’ensemble

Conception principale :
- Connexion à une session Chrome persistante via le débogage distant DevTools (port par défaut `9333`).
- Réutilisation de l’état du profil navigateur pour conserver la continuité de connexion/session.
- Automatisation des actions clés du composeur (saisie, ajout plus/média, storyboard, paramètres, création).
- Exposition des mêmes actions via REST + logs WebSocket pour un contrôleur PWA local.

### Aperçu des workflows

| Workflow | Point d’entrée | Usage principal |
| --- | --- | --- |
| Agent CLI | `agents/sora_agent.py` | Saisir des prompts, cliquer sur les contrôles, automatiser le flux de composition |
| Téléchargeur CLI | `agents/sora_download.py` | Trouver des médias téléchargeables et enregistrer les fichiers localement |
| API + PWA | `server/app.py` + `pwa/` | Contrôle à distance et orchestration visuelle depuis le navigateur |

## ✅ Fonctionnalités

- Flux d’attachement/démarrage Chrome avec profil réutilisable (`--debugger-port`, `--start-chrome`, `--user-data-dir`).
- Clics sûrs ou forcés pour les contrôles clés (`plus`, `storyboard`, `settings`, `create`, `profile`).
- Saisie de prompt avec comportement de repli sur les sélecteurs.
- Ajout de média via chemin de fichier avec injection DataTransfer.
- Remplissage des scènes storyboard + mises à jour de script + ajout média spécifique au storyboard.
- Automatisation des paramètres pour modèle/orientation/durée/résolution.
- Flux séparé de découverte puis de récupération des téléchargements via cookies navigateur.
- API REST Tornado et flux de debug WebSocket en direct.
- PWA locale installable avec upload, aperçu et contrôles granulaires.

## 🗂️ Structure du projet

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
│  └─ (actuellement vide)
├─ uploads/
│  └─ .gitkeep
└─ selenium_template -> ../auto-publish/ (symlink)
```

## 🧩 Prérequis

- Python 3.10+ (recommandé).
- Chrome/Chromium installé et exécutable.
- Un affichage pour l’usage non headless (`--no-headless`) lorsqu’une connexion ou une UI interactive est requise.
- Accès au compte Sora dans le profil Chrome attaché.

## 📦 Installation

Flux d’installation existant depuis le README canonique :

```bash
conda activate agent
pip install -r requirements.txt
```

Dépendances dans `requirements.txt` :

| Package | Spécification de version |
| --- | --- |
| `selenium` | `>=4.17.2` |
| `tornado` | `>=6.4` |
| `Pillow` | `>=9.4.0` |
| `pillow-heif` | `>=0.16.0` |

## 🚀 Utilisation

### Démarrage rapide (agent CLI)

Démarrage rapide (ouvre Sora dans un navigateur géré) :

```bash
python agents/sora_agent.py
```

Connexion à Chrome avec session persistante (recommandé pour Sora) :

```bash
python -m agents.sora_agent --debugger-port 9333 --start-chrome --no-headless --login-timeout 600 --text "A sunset over Tokyo, cinematic."
```

Remarques :
- Une fenêtre Chrome s’ouvre sur la page Sora. En cas de redirection vers la connexion, authentifiez-vous ; le script attend puis saisit votre prompt.
- Pour réutiliser la même connexion, passez un chemin de profil fixe :

```bash
python -m agents.sora_agent --debugger-port 9333 --start-chrome --no-headless --user-data-dir "$HOME/chrome_sora_profile_9333"
```

### Options CLI clés (`agents/sora_agent.py`)

- `--url` page cible (par défaut : `https://sora.chatgpt.com/explore`).
- `--debugger-port` se connecte à un Chrome existant lancé avec `--remote-debugging-port=PORT`.
- `--start-chrome` si défini avec `--debugger-port`, lance Chrome pour vous (avec un `--user-data-dir`).
- `--no-headless` pour exécuter un navigateur visible ; requis pour la connexion et Cloudflare.
- `--selector` CSS pour localiser l’entrée (par défaut correspond au textarea du composeur Sora).
- `--text` texte à saisir dans l’entrée.
- `--chrome-binary` définit explicitement un chemin Chrome/Chromium.
- `--action` actions UI : `list`, `plus`, `storyboard`, `settings`, `create`, `profile`.
- `--force-click` clique même si un élément semble désactivé.
- `--login-timeout` fenêtre d’attente pour la fin de l’authentification manuelle.

Gestion du driver :
- L’agent supprime tout `chromedriver` obsolète de `PATH` avant le lancement.
- Selenium Manager résout ensuite automatiquement un driver compatible avec le Chrome installé.

### Exemples CLI (contrôles UI)

Lister et cliquer les contrôles courants :

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action list --action storyboard --action settings --action plus
```

Forcer le clic du bouton Create video (même s’il est désactivé) :

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action create --force-click
```

Ouvrir le profil/paramètres et naviguer manuellement si nécessaire :

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action list --action profile
```

Si `profile` n’est pas détecté, le bouton `settings` ouvre généralement le même menu.

### Flux de téléchargement

Découvrir et télécharger des vidéos avec le script handler :

- Dry-run (liste uniquement les candidats) : `./bin/sora_download.sh --dry-run`
- Télécharger jusqu’à 2 fichiers vers `./downloads/sora` : `./bin/sora_download.sh --max 2`
- Changer le dossier de sortie : `OUT_DIR=$HOME/Videos/sora ./bin/sora_download.sh --max 1`

L’utilisation directe du module est aussi disponible via `python -m agents.sora_download ...`.

## 🌐 Serveur de contrôle + PWA

Lancer le serveur Tornado :

```bash
python server/app.py
# listens on http://0.0.0.0:8791 and serves the PWA at /
```

Par défaut, le serveur :
- Réutilise Chrome sur le port de débogage distant `9333`.
- Stocke les uploads dans `./uploads` sauf si `SORA_UPLOADS_DIR` est défini.

### Endpoints clés

Tous les endpoints opèrent sur le Chrome actuellement attaché (par défaut port de débogage `9333`).

| Method | Path | Payload | Description |
| --- | --- | --- | --- |
| `GET` | `/api/status` | none | Retourne l’état de disponibilité DevTools et le port actif. |
| `POST` | `/api/open` | `{ url? }` | Navigue l’onglet Chrome attaché vers l’URL donnée (par défaut Sora Explore). |
| `GET` | `/api/actions` | none | Inspecte l’état des boutons/contrôles (métadonnées found/displayed/disabled). |
| `POST` | `/api/click` | `{ key, force? }` | Appuie sur un contrôle où `key ∈ {plus, storyboard, settings, create, profile}`. |
| `POST` | `/api/type` | `{ text, selector?, url? }` | Saisit le texte du prompt dans le sélecteur du composeur. |
| `POST` | `/api/compose` | `{ text, click_create? }` | Ouvre la page de composition, saisit le texte, clique éventuellement sur create. |
| `POST` | `/api/attach` | `{ path, click_plus? }` | Upload un média via injection DataTransfer ; efface automatiquement le média existant (`click_plus` vaut `false` par défaut). |
| `POST` | `/api/describe` | `{ text }` | Remplit le textarea “Optionally describe your video…”. |
| `POST` | `/api/script-updates` | `{ text }` | Remplit le champ “Describe updates to your script…”. |
| `POST` | `/api/storyboard` | `{ scenes: ["scene 1", ...], script_updates?: "...", media_path?: "..." }` | Ouvre le storyboard, remplit les textareas de scène, applique éventuellement les mises à jour de script et le média storyboard. |
| `POST` | `/api/storyboard-media` | `{ path }` | Ajoute un média au chargeur spécifique storyboard quand le storyboard est déjà visible. |
| `POST` | `/api/storyboard-attach-only` | `{ path }` | S’assure que le storyboard est ouvert, puis ajoute le média. |
| `POST` | `/api/settings` | `{ model?, orientation?, duration?, resolution? }` | Ouvre les paramètres et applique les valeurs sélectionnées ; la réponse renvoie les labels appliqués. |
| `POST` | `/api/upload` | multipart form data | Enregistre des fichiers locaux dans le dossier d’upload serveur et renvoie les chemins côté serveur. |
| `POST` | `/api/preview` | multipart form data | Convertit une image en aperçu PNG (utile pour le fallback HEIC/HEIF/AVIF dans l’UI). |
| `GET` | `/ws` | WebSocket | Diffuse les événements d’action/debug. |

### Contrôles PWA

Ouvrez `http://0.0.0.0:8791` (ou votre hôte choisi) après avoir démarré `server/app.py`.

Points forts de l’implémentation existante :
- Upload de média via sélecteur de fichier ou en collant un chemin, puis clic sur **Plus** pour joindre sans rouvrir les boîtes de dialogue système.
- Application de la description média dans la zone dédiée “Media description”.
- Contrôles indépendants pour **Set Model**, **Set Orientation**, **Set Duration**, **Set Resolution**, et mises à jour de script.
- Contrôles storyboard pour scènes, mises à jour de script, ouverture du panneau storyboard, et ajout du chemin storyboard courant.
- Log de debug en direct affichant les appels API et les valeurs renvoyées par Sora (par exemple modèle/durée sélectionnés).

## ⚙️ Configuration

### Variables d’environnement

`server/app.py` lit :
- `SORA_DEBUGGER_PORT` (par défaut `9333`)
- `SORA_USER_DATA_DIR` (par défaut `~/chrome_sora_profile_<port>`)
- `SORA_DISPLAY` (affichage X optionnel)
- `SORA_API_PORT` (par défaut `8791`)
- `SORA_URL` (par défaut `https://sora.chatgpt.com/explore`)
- `SORA_UPLOADS_DIR` (surcharge optionnelle du dossier d’upload)

`agents/sora_agent.py` prend aussi en charge :
- `CHROME_BINARY` (si `--chrome-binary` n’est pas fourni)

Les scripts wrapper prennent en charge :
- `PORT`, `SORA_PROFILE_DIR`, `TIMEOUT`, `LOGIN_TIMEOUT` (`bin/sora_type.sh`)
- `PORT`, `SORA_PROFILE_DIR`, `OUT_DIR` (`bin/sora_download.sh`)

## 🧪 Exemples

### Exemple API de bout en bout (curl)

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

### Upload média + ajout via API

```bash
# Upload file and get server path
curl -s -X POST http://127.0.0.1:8791/api/upload -F 'file=@/absolute/path/to/input.jpg'

# Then attach using returned path
curl -s -X POST http://127.0.0.1:8791/api/attach \
  -H 'Content-Type: application/json' \
  -d '{"path":"/absolute/or/server-returned/path.jpg","click_plus":false}'
```

## 🛠️ Notes de développement

- Il n’y a actuellement pas de module empaqueté (`pyproject.toml`/`setup.py` absents).
- Il n’y a actuellement pas de pipeline CI/test/lint dans cet état du dépôt.
- `selenium_template` est un symlink vers `../auto-publish/` ; le contenu cible est hors de ce dépôt.
- Le manifeste PWA référence `/icons/icon-192.png` et `/icons/icon-512.png` ; les assets d’icônes ne sont pas suivis dans ce dépôt à ce stade.

## 🧯 Dépannage

- Chrome ne s’attache pas :
  - Vérifiez que Chrome a été lancé avec `--remote-debugging-port=9333` (ou un `--debugger-port` correspondant).
  - Vérifiez `GET /api/status` pour `devtools_ready: true`.
- Demandes de connexion répétées :
  - Utilisez un `--user-data-dir` persistant et évitez les chemins de profil aléatoires.
- Le flux Cloudflare/connexion ne progresse pas :
  - Exécutez en mode non-headless (`--no-headless`) et augmentez `--login-timeout`.
- L’ajout de média ne fait rien :
  - Vérifiez que le chemin de fichier existe sur la machine serveur et utilisez `/api/upload` + le chemin renvoyé en cas de doute.
- L’ajout de média storyboard échoue :
  - Essayez `POST /api/storyboard-attach-only` ou ouvrez d’abord le storyboard, puis `/api/storyboard-media`.
- Contrôle de résolution indisponible dans la PWA :
  - La résolution `High` n’est activée que lorsque le modèle est `Sora 2 Pro`.
- Problèmes de mauvais chromedriver :
  - Retirez le chromedriver épinglé manuellement de votre profil shell ; ce projet laisse volontairement Selenium Manager choisir les versions compatibles.

## 🧭 Feuille de route

Améliorations planifiées/probables :
- Ajouter des tests automatisés pour la stabilité des sélecteurs et les handlers API.
- Ajouter des outils lint/format et des workflows CI.
- Ajouter des assets d’icônes PWA suivis et une stratégie de cache hors ligne plus robuste.
- Ajouter des fichiers README multilingues formels sous `i18n/`.
- Ajouter des métadonnées de packaging pour faciliter l’installation.

## 🤝 Contribution

Les contributions sont les bienvenues.

Processus suggéré :
1. Forkez puis créez une branche de fonctionnalité.
2. Gardez des changements ciblés et incluez des notes de reproduction/usage pour les changements d’automatisation UI.
3. Validez les flux manuellement avec une vraie session Chrome attachée.
4. Ouvrez une PR avec les détails de comportement avant/après.

Si vous modifiez des sélecteurs ou la logique d’interaction, incluez un contexte UI Sora concret afin de faciliter le tri des régressions.

## ❤️ Support / Sponsoring

Liens de financement issus de `.github/FUNDING.yml` :
- GitHub Sponsors: https://github.com/sponsors/lachlanchen
- Project links: https://lazying.art, https://chat.lazying.art, https://onlyideas.art

## 🙏 Remerciements

- Selenium et Selenium Manager pour l’automatisation navigateur et la résolution de drivers.
- Tornado pour le service de contrôle HTTP/WebSocket asynchrone léger.
- Pillow et `pillow-heif` pour la conversion/aperçu d’images en local.

## 🧱 Build stable connu

Si vous avez besoin d’une base stable garantissant que l’ajout de média storyboard fonctionne de bout en bout (y compris les boutons Open Storyboard / Attach Current Path et le flux Apply combiné), consultez le commit :

`c6683ed6d9ee0ac110536352867a26a966e3e275`

## 📄 Licence

Aucun fichier de licence n’est actuellement présent dans cet état du dépôt (vérifié dans ce brouillon le **February 28, 2026**).

Hypothèse : tous les droits restent avec le propriétaire du dépôt jusqu’à l’ajout d’une licence. Si ce n’est pas l’intention, ajoutez un fichier `LICENSE` et mettez à jour cette section.
