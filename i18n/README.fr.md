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

SoraRemote est une boîte à outils Python + Selenium légère pour automatiser l’interface web de Sora.

Il prend en charge trois modes d’exécution complémentaires pour un même flux d’automatisation :
1. **Agent d’automatisation CLI** (`agents/sora_agent.py`) pour la saisie de prompts et les actions d’UI.
2. **Téléchargeur CLI** (`agents/sora_download.py`) pour découvrir et télécharger les médias candidats.
3. **Plan de contrôle Tornado + PWA** (`server/app.py` + `pwa/`) pour l’orchestration du navigateur pilotée par API.

Le contenu actuel du README est conservé comme guide opérationnel canonique et réorganisé pour plus de clarté.

## 🚀 Accès rapide

| Objectif | Point d’entrée | Utilisation principale |
| --- | --- | --- |
| Exécuter des prompts scriptés | `agents/sora_agent.py` | Piloter les actions du composeur depuis CLI ou script wrapper |
| Récupérer les médias générés | `agents/sora_download.py` | Découvrir et enregistrer les candidats localement |
| Contrôle à distance | `server/app.py` + `pwa/` | Contrôle via navigateur et REST/WebSocket |

## ✨ Aperçu

Conception de base :
- Connexion à une session Chrome persistante via le débogage distant DevTools (port `9333` par défaut).
- Réutilisation de l’état du profil navigateur pour conserver la continuité de connexion/session.
- Automatisation des actions clés du composeur (saisie, ajout de fichier/média, storyboard, paramètres, création).
- Exposition des mêmes actions via REST + flux WebSocket pour un contrôleur PWA local.

### Vue d’ensemble du flux de travail

| Flux | Point d’entrée | Usage principal |
| --- | --- | --- |
| Agent CLI | `agents/sora_agent.py` | Saisir des prompts, cliquer sur les contrôles, automatiser le flux de composition |
| Téléchargeur CLI | `agents/sora_download.py` | Découvrir les médias téléchargeables et enregistrer les fichiers localement |
| API + PWA | `server/app.py` + `pwa/` | Contrôle à distance et orchestration visuelle depuis navigateur |

## ✅ Fonctionnalités

- Flux d’attachement/démarrage Chrome avec profil réutilisable (`--debugger-port`, `--start-chrome`, `--user-data-dir`).
- Clics sûrs ou forcés pour les contrôles clés (`plus`, `storyboard`, `settings`, `create`, `profile`).
- Saisie de prompt avec comportement de repli des sélecteurs.
- Jointure de médias via chemin de fichier avec injection DataTransfer.
- Remplissage de scènes storyboard + mises à jour de script + ajout média spécifique au storyboard.
- Automatisation des paramètres pour modèle/orientation/durée/résolution.
- Flux séparé de découverte + téléchargement utilisant les cookies du navigateur.
- API REST Tornado et flux de débogage WebSocket en direct.
- PWA locale installable avec upload, aperçu et contrôles granulaires.

## 🗂️ Structure du projet

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

## 🧩 Prérequis

- Python 3.10+ (recommandé).
- Chrome/Chromium installé et exécutable.
- Un affichage pour une utilisation non-headless (`--no-headless`) quand la connexion ou une UI interactive est nécessaire.
- Accès à un compte Sora dans le profil Chrome attaché.

## 📦 Installation

Flux d’installation existant du README canonique :

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
- Une fenêtre Chrome s’ouvre sur la page Sora. Si redirigé vers la connexion, connectez-vous ; le script attend ensuite et saisit votre prompt.
- Pour réutiliser la même connexion, passez un chemin de profil fixe :

```bash
python -m agents.sora_agent --debugger-port 9333 --start-chrome --no-headless --user-data-dir "$HOME/chrome_sora_profile_9333"
```

### Options CLI principales (`agents/sora_agent.py`)

- `--url` page cible (par défaut : `https://sora.chatgpt.com/explore`).
- `--debugger-port` pour se connecter à un Chrome déjà lancé avec `--remote-debugging-port=PORT`.
- `--start-chrome` si défini avec `--debugger-port`, lance Chrome pour vous (avec un `--user-data-dir`).
- `--no-headless` pour exécuter un navigateur visible ; nécessaire pour la connexion et Cloudflare.
- `--selector` CSS pour localiser le champ de saisie (par défaut, il correspond au textarea du composeur Sora).
- `--text` contenu à saisir dans le champ.
- `--chrome-binary` définit explicitement un chemin Chrome/Chromium.
- `--action` actions UI : `list`, `plus`, `storyboard`, `settings`, `create`, `profile`.
- `--force-click` clique même si un élément semble désactivé.
- `--login-timeout` fenêtre d’attente pour la fin de l’authentification manuelle.

Gestion du driver :
- L’agent supprime tout `chromedriver` obsolète de `PATH` avant le lancement.
- Selenium Manager résout ensuite automatiquement un driver compatible avec la version installée de Chrome.

### Exemples CLI (contrôles UI)

Lister et cliquer les contrôles courants :

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action list --action storyboard --action settings --action plus
```

Forcer le clic du bouton Create video (même s’il est désactivé) :

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action create --force-click
```

Ouvrir profil/paramètres et naviguer manuellement si besoin :

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action list --action profile
```

Si `profile` n’est pas détecté, le bouton `settings` ouvre en général le même menu.

### Flux de téléchargement

Découvrir et télécharger des vidéos avec le script gestionnaire :

- Exécution à blanc (liste des candidats uniquement) : `./bin/sora_download.sh --dry-run`
- Télécharger jusqu’à 2 fichiers dans `./downloads/sora` : `./bin/sora_download.sh --max 2`
- Changer le dossier de sortie : `OUT_DIR=$HOME/Videos/sora ./bin/sora_download.sh --max 1`

L’utilisation directe du module est aussi possible avec `python -m agents.sora_download ...`.

## 🌐 Serveur de contrôle + PWA

Lancer le serveur Tornado :

```bash
python server/app.py
# listens on http://0.0.0.0:8791 and serves the PWA at /
```

Par défaut, le serveur :
- Réutilise Chrome sur le port de débogage distant `9333`.
- Stocke les uploads dans `./uploads` sauf si `SORA_UPLOADS_DIR` est défini.

### Endpoints principaux

Tous les endpoints s’appuient sur le Chrome actuellement attaché (port de débogage par défaut `9333`).

| Méthode | Chemin | Charge utile | Description |
| --- | --- | --- | --- |
| `GET` | `/api/status` | none | Renvoie l’état de disponibilité de DevTools et le port actif. |
| `POST` | `/api/open` | `{ url? }` | Navigue l’onglet Chrome attaché vers l’URL donnée (Sora Explore par défaut). |
| `GET` | `/api/actions` | none | Inspecte l’état des boutons/contrôles (`found`/`displayed`/`disabled`). |
| `POST` | `/api/click` | `{ key, force? }` | Clique sur un contrôle où `key ∈ {plus, storyboard, settings, create, profile}`. |
| `POST` | `/api/type` | `{ text, selector?, url? }` | Saisit le texte du prompt dans le sélecteur du composeur. |
| `POST` | `/api/compose` | `{ text, click_create? }` | Ouvre la page de composition, saisit le texte, clique éventuellement sur create. |
| `POST` | `/api/attach` | `{ path, click_plus? }` | Charge un média via injection DataTransfer ; efface automatiquement le média existant (`click_plus` vaut `false` par défaut). |
| `POST` | `/api/describe` | `{ text }` | Remplit le textarea “Optionally describe your video…”. |
| `POST` | `/api/script-updates` | `{ text }` | Remplit le champ “Describe updates to your script…”. |
| `POST` | `/api/storyboard` | `{ scenes: ["scene 1", ...], script_updates?: "...", media_path?: "..." }` | Ouvre le storyboard, remplit les textareas de scène, applique éventuellement les mises à jour de script et le média du storyboard. |
| `POST` | `/api/storyboard-media` | `{ path }` | Joint un média à l’uploader spécifique storyboard quand le storyboard est déjà visible. |
| `POST` | `/api/storyboard-attach-only` | `{ path }` | S’assure que le storyboard est ouvert, puis joint un média. |
| `POST` | `/api/settings` | `{ model?, orientation?, duration?, resolution? }` | Ouvre les paramètres et applique les valeurs sélectionnées ; la réponse renvoie les labels appliqués. |
| `POST` | `/api/upload` | multipart form data | Enregistre les fichiers locaux dans le répertoire d’upload serveur et renvoie les chemins côté serveur. |
| `POST` | `/api/preview` | multipart form data | Convertit une image en aperçu PNG (utile pour la compatibilité HEIC/HEIF/AVIF dans l’UI). |
| `GET` | `/ws` | WebSocket | Diffuse les événements d’action/de débogage. |

### Contrôles PWA

Ouvrez `http://0.0.0.0:8791` (ou votre hôte choisi) après avoir démarré `server/app.py`.

Points forts de l’implémentation existante :
- Upload de médias via sélecteur de fichier ou en collant un chemin, puis clic sur **Plus** pour joindre sans rouvrir les boîtes de dialogue système de fichiers.
- Application de la description des médias dans la zone dédiée “Media description”.
- Contrôles indépendants pour **Set Model**, **Set Orientation**, **Set Duration**, **Set Resolution**, et les mises à jour de script.
- Contrôles indépendants pour **Set Model**, **Set Orientation**, **Set Duration**, **Set Resolution**, et les mises à jour de script.
- Contrôles storyboard pour les scènes, les mises à jour de script, l’ouverture du panneau storyboard, et joindre le chemin actuel du storyboard.
- Journal de débogage en direct affichant les appels API et les valeurs renvoyées par Sora (par exemple modèle/durée sélectionnés).

## ⚙️ Configuration

### Variables d’environnement

`server/app.py` lit :
- `SORA_DEBUGGER_PORT` (par défaut `9333`)
- `SORA_USER_DATA_DIR` (par défaut `~/chrome_sora_profile_<port>`)
- `SORA_DISPLAY` (affichage X optionnel)
- `SORA_API_PORT` (par défaut `8791`)
- `SORA_URL` (par défaut `https://sora.chatgpt.com/explore`)
- `SORA_UPLOADS_DIR` (remplacement de dossier d’upload optionnel)

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

### Upload média + jointure via API

```bash
# Upload file and get server path
curl -s -X POST http://127.0.0.1:8791/api/upload -F 'file=@/absolute/path/to/input.jpg'

# Then attach using returned path
curl -s -X POST http://127.0.0.1:8791/api/attach \
  -H 'Content-Type: application/json' \
  -d '{"path":"/absolute/or/server-returned/path.jpg","click_plus":false}'
```

## 🛠️ Notes de développement

- Il n’y a actuellement aucun module packagé (`pyproject.toml`/`setup.py` absent).
- Il n’y a actuellement aucun pipeline CI/test/lint dans cet instantané du dépôt.
- `selenium_template` est un symlink vers `../auto-publish/` ; son contenu cible est en dehors de ce dépôt.
- Le manifeste PWA référence `/icons/icon-192.png` et `/icons/icon-512.png` ; les assets d’icônes ne sont pas actuellement suivis dans ce dépôt.

## 🧯 Dépannage

- Chrome ne parvient pas à s’attacher :
  - Vérifiez que Chrome a été démarré avec `--remote-debugging-port=9333` (ou un `--debugger-port` correspondant).
  - Vérifiez `GET /api/status` pour `devtools_ready: true`.
- Prompts de connexion répétés :
  - Utilisez un `--user-data-dir` persistant et évitez les chemins de profil aléatoires.
- Flux Cloudflare/connexion qui ne progresse pas :
  - Lancez en mode non-headless (`--no-headless`) et augmentez `--login-timeout`.
- L’ajout de médias ne fait rien :
  - Vérifiez que le chemin du fichier existe sur la machine serveur et utilisez `/api/upload` + le chemin renvoyé si doute.
- L’ajout de média storyboard échoue :
  - Essayez `POST /api/storyboard-attach-only` ou ouvrez d’abord le storyboard, puis `/api/storyboard-media`.
- Contrôle de résolution indisponible dans la PWA :
  - `High` est uniquement activé lorsque le modèle est `Sora 2 Pro`.
- Problème de mauvais chromedriver :
  - Supprimez un chromedriver manuellement épinglé depuis votre profil shell ; ce projet laisse volontairement Selenium Manager choisir les versions compatibles.

## 🧭 Feuille de route

Améliorations prévues/anticipées :
- Ajouter des tests automatisés pour la stabilité des sélecteurs et des handlers API.
- Ajouter des outils lint/format et des workflows CI.
- Ajouter des assets d’icônes PWA suivis et une stratégie de cache hors ligne plus robuste.
- Ajouter des README multilingues formels sous `i18n/`.
- Ajouter des métadonnées de packaging pour faciliter l’installation.

## 🤝 Contribuer

Les contributions sont les bienvenues.

Processus suggéré :
1. Forker et créer une branche de fonctionnalité.
2. Garder les changements ciblés et inclure des notes de reproduction/d’utilisation pour les changements d’automatisation UI.
3. Valider les flux manuellement avec une vraie session Chrome attachée.
4. Ouvrir une PR avec les détails de comportement avant/après.

Si vous modifiez les sélecteurs ou la logique d’interaction, incluez un contexte concret de l’UI Sora afin de faciliter le tri des régressions.

## 🙏 Remerciements

- Selenium et Selenium Manager pour l’automatisation navigateur et la résolution de driver.
- Tornado pour le service léger HTTP/WebSocket asynchrone de contrôle.
- Pillow et `pillow-heif` pour la conversion/aperçu d’images en local.

## 🧱 Build stable connue

Si vous avez besoin d’une base stable garantissant que l’attachement média storyboard fonctionne de bout en bout (y compris les boutons Open Storyboard / Attach Current Path et le flux Apply combiné), consultez le commit :

`c6683ed6d9ee0ac110536352867a26a966e3e275`

## 📄 Licence

Aucun fichier de licence n’est actuellement présent dans cet instantané du dépôt (vérifié dans cette version le **28 février 2026**).

Hypothèse : tous les droits restent avec le propriétaire du dépôt jusqu’à ce qu’une licence soit ajoutée. Si ce n’est pas voulu, ajoutez un fichier `LICENSE` et mettez à jour cette section.


## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |
