# note_auto_uploader
noteの記事を音声から自動でアップロードする


#### 概要
`note_auto_uploader` プロジェクトは、note.comでの様々なタスクを自動化するための複数のPythonスクリプトで構成されています。これらのスクリプトは、サイトへのログイン、自動化されたタスク（RPA）、テキストやマルチメディアコンテンツの処理などの機能を備えています。

#### スクリプトの説明

1. **v2txt.py**
   - mp3フォーマットの音声ファイルからWhisperでテキストに変換します。その後、gpt-3.5 APIで記事の要約を行います。JSON形式のファイルとして保存します。

2. **v2txt_all.py**
   - 指定したディレクトリからmp3のファイルリストを取得し、`v2txt.py`の関数を順次実行します。

2. **note_login.py**
   - note.comへのログインプロセスを自動化します。

3. **note_rpa.py**
   - 記事を投稿します。note.com上での自動化されたタスク（Robotic Process Automation）を実行します。

4. **note_rpa_pkl.py**
   - `note_rpa.py`の変形版で、pickleを使用してブラウザの状態を保存し、復元する追加機能を備えています。note_login.pyを実行したあとに実行します。

5. **noteall.py**
   - 特定のディレクトリで要約ファイルを探し、記事投稿をバッチ処理します。

1. **check_json.py**
   - JSONファイルを特定のフォーマットや内容要件に対して検証します。


#### インストールとセットアップ

1. システムにPythonがインストールされていることを確認します。
2. リポジトリをクローンするか、ZIPファイルをダウンロードして内容を展開します。

#### スクリプトの実行

- 各スクリプトは、手元のタスクに応じて個別に実行できます。
- 例えば、`note_login.py` を実行するには `python note_login.py` を使用します。
- 各スクリプトの実行に必要な認証情報や入力ファイルを用意してください。

- .envを適宜設定して実行してください。
