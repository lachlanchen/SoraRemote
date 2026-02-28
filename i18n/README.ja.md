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

SoraRemote は、Sora Web UI を自動化するための軽量な Python + Selenium ツールキットです。

1 つの自動化ワークフローを補完する 3 つの実行モードを提供します。
1. **CLI 自動化エージェント** (`agents/sora_agent.py`): プロンプト入力と UI 操作。
2. **CLI ダウンローダー** (`agents/sora_download.py`): メディア候補の検出とダウンロード。
3. **Tornado + PWA 制御プレーン** (`server/app.py` + `pwa/`): API 駆動のブラウザ制御。

現在の README の内容を運用ガイドとして維持しつつ、読みやすさのために再構成しています。

## 🚀 Quick Access

| 目的 | 入口 | 主な用途 |
| --- | --- | --- |
| スクリプト化されたプロンプトを実行 | `agents/sora_agent.py` | CLI またはラッパーから作成・操作を実行 |
| 生成メディアを取得 | `agents/sora_download.py` | 候補を検出してローカル保存 |
| リモート制御 | `server/app.py` + `pwa/` | REST/WebSocket + ブラウザダッシュボードで制御 |

## ✨ Overview

コア設計:
- DevTools リモートデバッグ（デフォルトポート `9333`）で永続 Chrome セッションに接続。
- ブラウザのプロフィール状態を再利用し、ログイン/セッション継続性を維持。
- 主要なコンポーザー操作（入力、plus/メディア添付、storyboard、設定、作成）を自動化。
- 同じ操作を REST + WebSocket ログで公開し、ローカル PWA コントローラーから制御。

### ワークフローの全体像

| ワークフロー | エントリーポイント | 主な用途 |
| --- | --- | --- |
| CLI エージェント | `agents/sora_agent.py` | プロンプト入力、コントロールクリック、作成フロー自動化 |
| CLI ダウンローダー | `agents/sora_download.py` | ダウンロード可能メディアの検出とローカル保存 |
| API + PWA | `server/app.py` + `pwa/` | ブラウザからのリモート制御と可視化されたオーケストレーション |

## ✅ Features

- 再利用可能なプロフィール付きの Chrome 接続/起動フロー（`--debugger-port`、`--start-chrome`、`--user-data-dir`）。
- 主要コントロールの安全クリックまたは強制クリック（`plus`、`storyboard`、`settings`、`create`、`profile`）。
- セレクターのフォールバックを使ったプロンプト入力。
- DataTransfer 注入によるファイルパス指定メディア添付。
- Storyboard シーン入力 + スクリプト更新 + storyboard 固有のメディア添付。
- モデル/向き/長さ/解像度の設定自動化。
- ブラウザ Cookie を使う、別々の候補検出 + 取得フロー。
- Tornado REST API とリアルタイム WebSocket デバッグストリーム。
- アップロード、プレビュー、細かい操作に対応したインストール可能なローカル PWA。

## 🗂️ プロジェクト構成

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

## 🧩 前提条件

- Python 3.10+（推奨）。
- Chrome/Chromium がインストールされ、実行可能。
- ログインや対話 UI が必要な場合は `--no-headless` で非ヘッドレス表示。
- 接続先 Chrome プロファイルで Sora のアカウントにアクセス可能。

## 📦 インストール

正規 README の既存セットアップ手順:

```bash
conda activate agent
pip install -r requirements.txt
```

`requirements.txt` の依存関係:

| パッケージ | バージョン |
| --- | --- |
| `selenium` | `>=4.17.2` |
| `tornado` | `>=6.4` |
| `Pillow` | `>=9.4.0` |
| `pillow-heif` | `>=0.16.0` |

## 🚀 使い方

### クイックスタート（CLI エージェント）

クイックスタート（管理ブラウザーで Sora を開く）:

```bash
python agents/sora_agent.py
```

永続セッション付きで Chrome に接続（Sora では推奨）:

```bash
python -m agents.sora_agent --debugger-port 9333 --start-chrome --no-headless --login-timeout 600 --text "A sunset over Tokyo, cinematic."
```

メモ:
- Sora ページで Chrome ウィンドウが開きます。ログイン画面へ飛ばされた場合はサインインし、スクリプトが待機してからプロンプトを入力します。
- 同じログイン状態を再利用するには、固定のプロファイルパスを指定します:

```bash
python -m agents.sora_agent --debugger-port 9333 --start-chrome --no-headless --user-data-dir "$HOME/chrome_sora_profile_9333"
```

### 主要 CLI オプション (`agents/sora_agent.py`)

- `--url` 対象ページ（既定値: `https://sora.chatgpt.com/explore`）。
- `--debugger-port`: `--remote-debugging-port=PORT` で起動した既存 Chrome に接続します。
- `--start-chrome`: `--debugger-port` と併用すると `--user-data-dir` と共に Chrome を起動します。
- `--no-headless`: ブラウザーを表示して実行。ログインと Cloudflare 処理に必要。
- `--selector` 入力欄を特定する CSS（既定値は Sora composer textarea に一致）。
- `--text` 入力するテキスト。
- `--chrome-binary` Chrome/Chromium の実行ファイルを明示指定。
- `--action` UI アクション: `list`、`plus`、`storyboard`、`settings`、`create`、`profile`。
- `--force-click` 無効化表示でもクリックを試みます。
- `--login-timeout` 手動認証完了までの待機時間。

ドライバー処理:
- エージェントは起動前に `PATH` 内の古い `chromedriver` を削除します。
- Selenium Manager がインストール済み Chrome に対応するドライバーを自動解決します。

### CLI 例（UI 操作）

一般的なコントロールを列挙してクリック:

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action list --action storyboard --action settings --action plus
```

Create video ボタンを強制クリック（無効表示でも）:

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action create --force-click
```

profile/settings を開き、必要に応じて手動で操作:

```bash
python -m agents.sora_agent --debugger-port 9333 --no-headless --action list --action profile
```

`profile` が検出されない場合、通常は `settings` ボタンで同じメニューを開けます。

### ダウンローダーフロー

ハンドラースクリプトで動画候補を見つけ、ダウンロード:

- ドライラン（候補の一覧のみ）: `./bin/sora_download.sh --dry-run`
- 最大 2 ファイルを `./downloads/sora` にダウンロード: `./bin/sora_download.sh --max 2`
- 出力フォルダー変更: `OUT_DIR=$HOME/Videos/sora ./bin/sora_download.sh --max 1`

モジュールを直接使うこともできます: `python -m agents.sora_download ...`。

## 🌐 Control Server + PWA

Tornado サーバーを起動:

```bash
python server/app.py
# listens on http://0.0.0.0:8791 and serves the PWA at /
```

デフォルトではサーバーは次のように動作します:
- リモートデバッグポート `9333` の Chrome を再利用。
- `SORA_UPLOADS_DIR` が未設定の場合は `./uploads` にアップロードを保存。

### 主なエンドポイント

全エンドポイントは現在接続中の Chrome に対して動作します（既定デバッグポート: `9333`）。

| メソッド | パス | ペイロード | 説明 |
| --- | --- | --- | --- |
| `GET` | `/api/status` | none | DevTools の準備状態とアクティブポートを返します。 |
| `POST` | `/api/open` | `{ url? }` | 接続中 Chrome タブを指定 URL へ遷移（既定は Sora Explore）。 |
| `GET` | `/api/actions` | none | ボタン/コントロール状態（found/displayed/disabled のメタデータ）を取得。 |
| `POST` | `/api/click` | `{ key, force? }` | `key ∈ {plus, storyboard, settings, create, profile}` を 1 つ押下。 |
| `POST` | `/api/type` | `{ text, selector?, url? }` | composer セレクターへプロンプトテキストを入力。 |
| `POST` | `/api/compose` | `{ text, click_create? }` | compose ページを開いてテキストを入力し、必要なら create を押下。 |
| `POST` | `/api/attach` | `{ path, click_plus? }` | DataTransfer 注入でメディアをアップロード。既存メディアは自動的にクリア（`click_plus` は既定 `false`）。 |
| `POST` | `/api/describe` | `{ text }` | “Optionally describe your video…” テキストエリアを入力。 |
| `POST` | `/api/script-updates` | `{ text }` | “Describe updates to your script…” フィールドを入力。 |
| `POST` | `/api/storyboard` | `{ scenes: ["scene 1", ...], script_updates?: "...", media_path?: "..." }` | storyboard を開き、シーン入力欄を埋め、必要に応じて script updates と storyboard メディアを適用。 |
| `POST` | `/api/storyboard-media` | `{ path }` | storyboard がすでに表示中の場合、storyboard 専用アップローダーへメディア添付。 |
| `POST` | `/api/storyboard-attach-only` | `{ path }` | storyboard を確実に開いてからメディアを添付。 |
| `POST` | `/api/settings` | `{ model?, orientation?, duration?, resolution? }` | settings を開き選択値を適用。レスポンスに適用ラベルを返却。 |
| `POST` | `/api/upload` | multipart form data | ローカルファイルをサーバーのアップロードディレクトリに保存し、サーバー側パスを返却。 |
| `POST` | `/api/preview` | multipart form data | 画像を PNG プレビューへ変換（UI で HEIC/HEIF/AVIF の代替として有用）。 |
| `GET` | `/ws` | WebSocket | アクション/デバッグイベントをストリーム配信。 |

### PWA コントロール

`server/app.py` 起動後に `http://0.0.0.0:8791`（または設定したホスト）を開きます。

既存実装のハイライト:
- ファイルピッカーで指定するかパスを貼り付けてメディアをアップロードし、**Plus** を押して OS のファイルダイアログを再度開かずに添付。
- 専用の “Media description” ボックスでメディア説明を設定。
- **Set Model**、**Set Orientation**、**Set Duration**、**Set Resolution**、スクリプト更新を個別に制御。
- シーン、スクリプト更新、storyboard パネルの開閉、現在の storyboard パス添付のコントロール。
- API 呼び出しと Sora の戻り値（選択されたモデル/長さなど）を表示するライブデバッグログ。

## ⚙️ 設定

### 環境変数

`server/app.py` が読み取る値:
- `SORA_DEBUGGER_PORT`（既定: `9333`）
- `SORA_USER_DATA_DIR`（既定: `~/chrome_sora_profile_<port>`）
- `SORA_DISPLAY`（任意の X display）
- `SORA_API_PORT`（既定: `8791`）
- `SORA_URL`（既定: `https://sora.chatgpt.com/explore`）
- `SORA_UPLOADS_DIR`（アップロード先の上書き）

`agents/sora_agent.py` も対応:
- `CHROME_BINARY`（`--chrome-binary` が未指定の場合）

ラッパースクリプトのサポート変数:
- `PORT`、`SORA_PROFILE_DIR`、`TIMEOUT`、`LOGIN_TIMEOUT`（`bin/sora_type.sh`）
- `PORT`、`SORA_PROFILE_DIR`、`OUT_DIR`（`bin/sora_download.sh`）

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

## 🛠️ 開発ノート

- 現在の時点でパッケージ化モジュールはありません（`pyproject.toml` / `setup.py` は未作成）。
- このリポジトリには CI/test/lint パイプラインがまだありません。
- `selenium_template` は `../auto-publish/` へのシンボリックリンクです。リンク先内容はこのリポジトリ外です。
- PWA の manifest は `/icons/icon-192.png` と `/icons/icon-512.png` を参照しますが、アイコン資産は現時点でトラックされていません。

## 🧯 トラブルシューティング

- Chrome へアタッチできない:
  - Chrome が `--remote-debugging-port=9333`（または `--debugger-port` と一致）で起動していることを確認。
  - `GET /api/status` を確認し、`devtools_ready: true` を確認。
- ログインプロンプトが繰り返される:
  - `--user-data-dir` を固定し、ランダムなプロフィールを避ける。
- Cloudflare / ログインフローが進まない:
  - 非ヘッドレス（`--no-headless`）で実行し、`--login-timeout` を延長。
- メディア添付が反応しない:
  - サーバーマシン上にファイルパスが存在するか確認し、疑わしい場合は `/api/upload` と返却パスを使用。
- Storyboard へのメディア添付が失敗する:
  - `POST /api/storyboard-attach-only` を試すか、先に storyboard を開いてから `/api/storyboard-media` を呼び出す。
- PWA で解像度コントロールが無効:
  - `High` 解像度はモデルが `Sora 2 Pro` の場合のみ有効です。
- chromedriver が不一致:
  - シェルプロファイルに手動固定している chromedriver を削除してください。 このプロジェクトは Selenium Manager にバージョンマッチングを任せる想定です。

## 🧭 ロードマップ

予定/想定される次の改善点:
- セレクター安定性と API ハンドラー用の自動テストを追加。
- lint/format ツールと CI ワークフローを追加。
- PWA のアイコン資産を追跡対象に追加し、より強固なオフラインキャッシュ戦略を整備。
- `i18n/` 配下の正式な多言語 README を追加。
- インストール容易化のためのパッケージングメタデータを追加。

## 🤝 貢献

コントリビューションを歓迎します。

推奨プロセス:
1. フォークして feature branch を作成。
2. 変更範囲を限定し、UI 自動化の変更には再現手順/利用手順を含める。
3. 実際のアタッチ済み Chrome セッションで手動検証。
4. 変更前後の挙動を記載して PR を作成。

セレクターや操作ロジックを変更する場合は、回帰解析がしやすいよう Sora UI の具体的な状況を含めてください。

## 🙏 謝辞

- ブラウザ自動化とドライバー解決を提供する Selenium と Selenium Manager。
- 軽量な非同期 HTTP/WebSocket 制御サービスである Tornado。
- ローカル画像変換/プレビュー対応の Pillow と `pillow-heif`。

## 🧱 動作確認済みビルド

ストーリーボードメディア添付がエンドツーエンドで確実に動作する安定版ベースライン（Open Storyboard / Attach Current Path ボタンおよび統合 Apply フローを含む）を確認したい場合:

`c6683ed6d9ee0ac110536352867a26a966e3e275`

## 📄 ライセンス

このリポジトリのスナップショットには、現時点でライセンスファイルがありません（このドラフトで **February 28, 2026** 時点を確認）。

この状態が意図したものでない場合は、`LICENSE` を追加してこのセクションを更新してください。


## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |
