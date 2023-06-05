# 勤怠管理アプリ


# 開発ルール
[開発のルール](docs/get_started.md)

# バックエンドドキュメント
[バックエンドドキュメント](backend/README.md)

# dockerコマンド
- 詳細なログを出力しながら、キャッシュを利用せずにDockerイメージを作成
  - Dockerfileやソースコードを書き換えた後にDockerを使って実行したいときにまずはこれをしてbuildする
```
docker compose build --progress=plain --no-cache
```
- コンテナを作って起動する
```
docker-compose up
```

- バックグラウンドでコンテナを作って起動する
```
docker-compose up -d
```
