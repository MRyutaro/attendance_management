# このフォルダの説明

`docker-compose up`とかいちいち打つのめんどうなので、コマンドで管理できるようにします。

`.sh`というシェルスクリプトファイルを使います。

## 自動化したいコマンドメモ

### docker-compose build --no-cacheとdocker-compose up
### pythonとpostgresはdocker上で動かし、nodeはローカルで動かすように。docker-compose.yamlを2種類作る
- docker-compose.yaml
- docker-compose.test.yaml
### テストデータをデータベース上で作成して、消す
### いずれかのコンテナとイメージだけ削除してコンテナを作成しなおす
### npm installしなおす