# biyoritter

## はじめに

ヽ(廿Δ廿 )にゃんぱすー。  
pythonの勉強も兼ねてTwitterのクライアント？的な何かを作ってるのんな～  

## つかいかた

1. アプリケーション登録をしてキーとトークンを取得するのん。

2. レポジトリをクローンorダウンロードするのん。

3. ライブラリを入れるのん。下のコマンドをそのまま打つのん。
    > pip install requests requests-oauthlib janome

4. main.pyを作成して取得したキーとトークンを書きこむのん。

```:main.py
> CONSUMER_KEY = "XXXXXXXXXX"  
> CONSUMER_SECRET = "XXXXXXXXXX"  
> ACCESS_TOKEN = "XXXXXXXXXX"  
> ACCESS_TOKEN_SECRET = "XXXXXXXXXX"
```

5. サブ垢を使いたいときはmain.pyと同様にsub.pyを作るのんな～。

6. 準備完了なのん！biyoritter.pyを実行するのん。

7. サブ垢を使いたいときはコマンドライン引数に何か入力してあげればいいのん！

## ライセンス

MIT
