[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


Language: **Japanese** | i18n directory: [`i18n/`](../i18n/)（利用可能、翻訳ファイルを順次追加中）

# SoraRemote

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20WSL-6c757d)
![Server](https://img.shields.io/badge/Server-Tornado%20API-0EA5E9)
![Frontend](https://img.shields.io/badge/Frontend-PWA-10B981)
![Status](https://img.shields.io/badge/Status-Experimental-F59E0B)

SoraRemote は、Sora Web UI を自動化するための軽量な Python + Selenium ツールキットです。

以下の3つのワークフローを相互補完的にサポートします。
1. CLI 自動化エージェント（`agents/sora_agent.py`）: プロンプト入力とUI操作。
2. CLI ダウンローダー（`agents/sora_download.py`）: ダウンロード候補の検出とメディア保存。
3. ローカル Tornado 制御サーバー + PWA（`server/app.py` + `pwa/`）: API駆動およびブラウザベースの操作。

現在の README 内容は、正式な運用ガイドとして保持しつつ、読みやすさのために再構成しています。

## ✨ 概要

コア設計:
- DevTools のリモートデバッグ（既定ポート `9333`）経由で永続 Chrome セッションにアタッチ。
- ブラウザプロファイル状態を再利用し、ログイン/セッション継続性を維持。
- Composer の主要操作（入力、plus/メディア添付、storyboard、settings、create）を自動化。
- 同じ操作を REST + WebSocket ログとして公開し、ローカル PWA から制御可能。

### ワークフロー早見表

| Workflow | Entry point | Primary use |
| --- | --- | --- |
| CLI Agent | `agents/sora_agent.py` | プロンプト入力、コントロールクリック、Composeフロー自動化 |
| CLI Downloader | `agents/sora_download.py` | ダウンロード可能メディアの検出とローカル保存 |
| API + PWA | `server/app.py` + `pwa/` | ブラウザからのリモート制御と可視的オーケストレーション |

## ✅ 機能

- 再利用可能プロファイル付きの Chrome アタッチ/起動フロー（`--debugger-port`, `--start-chrome`, `--user-data-dir`）。
- 主要コントロールの安全クリック/強制クリック（`plus`, `storyboard`, `settings`, `create`, `profile`）。
- セレクタフォールバック付きプロンプト入力。
- DataTransfer 注入によるファイルパスメディア添付。
- Storyboard シーン入力 + script updates + storyboard専用メディア添付。
- model/orientation/duration/resolution の settings 自動化。
- ブラウザCookieを利用したダウンロード候補検出 + 取得フロー。
- Tornado REST API とライブ WebSocket デバッグストリーム。
- アップロード、プレビュー、詳細操作に対応したローカル PWA。

## 🗂️ プロジェクト構成

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

## 🧩 前提条件

- Python 3.10+（推奨）。
- Chrome/Chromium がインストール済みで実行可能。
- 非ヘッドレス利用（`--no-headless`）時、ログインや対話UIに必要な表示環境。
- アタッチ先 Chrome プロファイルで Sora アカウントにアクセス可能。

## 📦 インストール

正式 README の既存セットアップ手順:

```bash
conda activate agent
pip install -r requirements.txt
```

`requirements.txt` の依存関係:

| Package | Version spec |
| --- | --- |
| `selenium` | `>=4.17.2` |
| `tornado` | `>=6.4` |
| `Pillow` | `>=9.4.0` |
| `pillow-heif` | `>=0.16.0` |

## 🚀 使い方

### クイックスタート（CLI agent）

クイックスタート（管理ブラウザで Sora を開く）:

```bash
python agents/sora_agent.py
```

永続セッション付き Chrome にアタッチ（Sora では推奨）:

```bash
python -m agents.sora_agent --debugger-port 9333 --start-chrome --no-headless --login-timeout 600 --text "A sunset over Tokyo, cinematic."
```

メモ:
- Sora ページで Chrome ウィンドウが開きます。ログイン画面にリダイレクトされた場合はサインインしてください。スクリプトは待機後にプロンプトを入力します。
- 同じログインを再利用するには、固定プロファイルパスを指定します:

```bash
python -m agents.sora_agent --debugger-port 9333 --start-chrome --no-headless --user-data-dir "$HOME/chrome_sora_profile_9333"
```

### 主な CLI オプション（`agents/sora_agent.py`）

- `--url` 対象ページ（既定: `https://sora.chatgpt.com/explore`）。
- `--debugger-port` `--remote-debugging-port=PORT` で起動済みの Chrome にアタッチ。
- `--start-chrome` を `--debugger-port` と併用すると、`--user-data-dir` 付きで Chrome を自動起動。
- `--no-headless` 可視ブラウザで実行。ログインや Cloudflare に必要。
- `--selector` 入力欄特定用 CSS（既定は Sora composer textarea に一致）。
- `--text` 入力するテキスト。
- `--chrome-binary` Chrome/Chromium のパスを明示指定。
- `--action` UI 操作: `list`, `plus`, `storyboard`, `settings`, `create`, `profile`。
- `--force-click` 要素が無効表示でもクリック。
- `--login-timeout` 手動認証完了までの待機時間。

ドライバ処理:
- エージェントは起動前に `PATH` 内の古い `chromedriver` を除去します。
- その後 Selenium Manager が、インストール済み Chrome に一致するドライバを自動解決します。

### CLI 例（UI操作）

一般的なコントロールの一覧表示とクリック:

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action list --action storyboard --action settings --action plus
```

Create video ボタンを強制クリック（無効表示でもクリック）:

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action create --force-click
```

profile/settings を開き、必要に応じて手動で遷移:

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action list --action profile
```

`profile` が検出されない場合、多くは `settings` ボタンで同じメニューを開けます。

### ダウンローダーフロー

ハンドラースクリプトで動画を検出・ダウンロード:

- ドライラン（候補一覧のみ）: `./bin/sora_download.sh --dry-run`
- 最大2件を `./downloads/sora` へダウンロード: `./bin/sora_download.sh --max 2`
- 出力先を変更: `OUT_DIR=$HOME/Videos/sora ./bin/sora_download.sh --max 1`

`python -m agents.sora_download ...` による直接モジュール実行にも対応しています。

## 🌐 制御サーバー + PWA

Tornado サーバーを起動:

```bash
python server/app.py
# listens on http://0.0.0.0:8791 and serves the PWA at /
```

既定ではサーバーは以下のように動作します:
- リモートデバッグポート `9333` の Chrome を再利用。
- `SORA_UPLOADS_DIR` 未設定時は `./uploads` にアップロードを保存。

### 主なエンドポイント

すべてのエンドポイントは、現在アタッチ中の Chrome（既定デバッグポート `9333`）に対して動作します。

| Method | Path | Payload | Description |
| --- | --- | --- | --- |
| `GET` | `/api/status` | none | DevTools 準備状態と使用ポートを返します。 |
| `POST` | `/api/open` | `{ url? }` | アタッチ中の Chrome タブを指定URLへ遷移（既定は Sora Explore）。 |
| `GET` | `/api/actions` | none | ボタン/コントロール状態（found/displayed/disabled メタデータ）を検査。 |
| `POST` | `/api/click` | `{ key, force? }` | `key ∈ {plus, storyboard, settings, create, profile}` の1操作を実行。 |
| `POST` | `/api/type` | `{ text, selector?, url? }` | composer セレクタへプロンプトテキストを入力。 |
| `POST` | `/api/compose` | `{ text, click_create? }` | composeページを開いてテキスト入力し、任意で create をクリック。 |
| `POST` | `/api/attach` | `{ path, click_plus? }` | DataTransfer 注入でメディアをアップロード。既存メディアは自動クリア（`click_plus` 既定 `false`）。 |
| `POST` | `/api/describe` | `{ text }` | “Optionally describe your video…” テキストエリアに入力。 |
| `POST` | `/api/script-updates` | `{ text }` | “Describe updates to your script…” 欄に入力。 |
| `POST` | `/api/storyboard` | `{ scenes: ["scene 1", ...], script_updates?: "...", media_path?: "..." }` | storyboard を開き、シーン入力、必要に応じて script updates と storyboard メディアを適用。 |
| `POST` | `/api/storyboard-media` | `{ path }` | storyboard 表示済み時に storyboard 専用アップローダーへメディア添付。 |
| `POST` | `/api/storyboard-attach-only` | `{ path }` | storyboard を確実に開いてからメディア添付。 |
| `POST` | `/api/settings` | `{ model?, orientation?, duration?, resolution? }` | settings を開いて選択値を適用。応答には適用ラベルを返却。 |
| `POST` | `/api/upload` | multipart form data | ローカルファイルをサーバーのアップロードディレクトリに保存し、サーバー側パスを返却。 |
| `POST` | `/api/preview` | multipart form data | 画像を PNG プレビューに変換（HEIC/HEIF/AVIF のUIフォールバックに有用）。 |
| `GET` | `/ws` | WebSocket | 操作/デバッグイベントをストリーミング。 |

### PWA コントロール

`server/app.py` 起動後、`http://0.0.0.0:8791`（または設定ホスト）を開きます。

既存実装のハイライト:
- ファイル選択またはパス貼り付けでメディアを指定し、**Plus** をクリックしてシステムファイルダイアログを再表示せず添付。
- 専用の “Media description” ボックスでメディア説明を適用。
- **Set Model**、**Set Orientation**、**Set Duration**、**Set Resolution**、script updates を独立制御。
- シーン、script updates、storyboardパネル表示、現在の storyboard path 添付を個別に操作。
- API呼び出しと Sora 返却値（例: 選択モデル/duration）を表示するライブデバッグログ。

## ⚙️ 設定

### 環境変数

`server/app.py` で読み取る値:
- `SORA_DEBUGGER_PORT`（既定 `9333`）
- `SORA_USER_DATA_DIR`（既定 `~/chrome_sora_profile_<port>`）
- `SORA_DISPLAY`（任意の X display）
- `SORA_API_PORT`（既定 `8791`）
- `SORA_URL`（既定 `https://sora.chatgpt.com/explore`）
- `SORA_UPLOADS_DIR`（アップロード先ディレクトリの任意上書き）

`agents/sora_agent.py` でも対応:
- `CHROME_BINARY`（`--chrome-binary` 未指定時）

ラッパースクリプトで対応:
- `PORT`, `SORA_PROFILE_DIR`, `TIMEOUT`, `LOGIN_TIMEOUT`（`bin/sora_type.sh`）
- `PORT`, `SORA_PROFILE_DIR`, `OUT_DIR`（`bin/sora_download.sh`）

## 🧪 例

### エンドツーエンド API 例（curl）

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

### API でのメディアアップロード + 添付

```bash
# Upload file and get server path
curl -s -X POST http://127.0.0.1:8791/api/upload -F 'file=@/absolute/path/to/input.jpg'

# Then attach using returned path
curl -s -X POST http://127.0.0.1:8791/api/attach \
  -H 'Content-Type: application/json' \
  -d '{"path":"/absolute/or/server-returned/path.jpg","click_plus":false}'
```

## 🛠️ 開発メモ

- 現時点ではパッケージ化モジュールはありません（`pyproject.toml`/`setup.py` は未存在）。
- このリポジトリスナップショットには CI/test/lint パイプラインがまだありません。
- `selenium_template` は `../auto-publish/` へのシンボリックリンクで、リンク先内容はこのリポジトリ外です。
- PWA manifest は `/icons/icon-192.png` と `/icons/icon-512.png` を参照しますが、アイコン資産は現在このリポジトリで追跡されていません。

## 🧯 トラブルシューティング

- Chrome にアタッチできない:
  - Chrome を `--remote-debugging-port=9333`（または一致する `--debugger-port`）で起動したか確認。
  - `GET /api/status` で `devtools_ready: true` を確認。
- ログイン要求が繰り返される:
  - 永続 `--user-data-dir` を使用し、ランダムなプロファイルパスを避ける。
- Cloudflare/ログインフローが進まない:
  - 非ヘッドレス（`--no-headless`）で実行し、`--login-timeout` を増やす。
- メディア添付しても反応がない:
  - サーバーマシン上でファイルパスが存在するか確認。不明な場合は `/api/upload` + 返却パスを使用。
- Storyboard へのメディア添付に失敗する:
  - `POST /api/storyboard-attach-only` を試すか、先に storyboard を開いてから `/api/storyboard-media` を実行。
- PWA で解像度コントロールが使えない:
  - `High` 解像度はモデルが `Sora 2 Pro` のときのみ有効。
- 誤った chromedriver 問題:
  - シェルプロファイルで固定指定した chromedriver を削除。このプロジェクトは Selenium Manager に一致バージョン選択を任せる設計です。

## 🧭 ロードマップ

予定/想定される改善:
- セレクタ安定性と API ハンドラ向けの自動テスト追加。
- lint/format ツールと CI ワークフロー追加。
- 追跡対象の PWA アイコン資産追加と、より強いオフラインキャッシュ戦略。
- `i18n/` 配下の正式な多言語 README 追加。
- インストール容易化のためのパッケージメタデータ追加。

## 🤝 コントリビュート

コントリビュートを歓迎します。

推奨プロセス:
1. Fork して feature branch を作成。
2. 変更範囲を絞り、UI 自動化変更には再現/利用手順を含める。
3. 実際にアタッチした Chrome セッションで手動検証。
4. 変更前後の挙動詳細を添えて PR を作成。

セレクタや操作ロジックを変更する場合は、回帰切り分けを容易にするため具体的な Sora UI 文脈を記載してください。

## ❤️ サポート / スポンサー

`.github/FUNDING.yml` 由来の支援リンク:
- GitHub Sponsors: https://github.com/sponsors/lachlanchen
- Project links: https://lazying.art, https://chat.lazying.art, https://onlyideas.art

## 🙏 謝辞

- ブラウザ自動化とドライバ解決を担う Selenium と Selenium Manager。
- 軽量な非同期 HTTP/WebSocket 制御サービスを提供する Tornado。
- ローカル画像変換/プレビュー支援のための Pillow と `pillow-heif`。

## 🧱 動作確認済みビルド

Storyboard メディア添付がエンドツーエンドで確実に動作する安定ベースライン（Open Storyboard / Attach Current Path ボタンと、統合 Apply フローを含む）が必要な場合は、次のコミットを参照してください:

`c6683ed6d9ee0ac110536352867a26a966e3e275`

## 📄 ライセンス

このリポジトリスナップショットには、現時点でライセンスファイルがありません（このドラフトで **2026年2月28日** 時点確認）。

前提: ライセンスが追加されるまでは、すべての権利はリポジトリ所有者に留保されます。意図と異なる場合は `LICENSE` ファイルを追加し、このセクションを更新してください。
