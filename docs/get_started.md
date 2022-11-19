# Githubのルール

## 1. ブランチの使い方
だいたいでいいのでgit-flowに従いましょう！（[参照](https://qiita.com/KosukeSone/items/514dd24828b485c69a05)）
* main = 世界中の人に見せる用のブランチ
* develop = 開発者が見るようのブランチ
* feature-○○ = なにか特定の機能を作るためのブランチ

基本は`feature-●●`ブランチで機能を追加した後で`develop`ブランチにマージしましょう。

`develop`ブランチである程度のものが完成したら`main`ブランチにマージして公開するという流れにしたいです！



## 2. コミットメッセージの書き方

どんな変更をしたか分かりやすくするために、コミットメッセージの前に下の4つのどれかを書くようにしましょう。([参照](https://qiita.com/itosho/items/9565c6ad2ffc24c09364))

* fix = バグの修正
* add = 新機能の追加
* update = 機能の修正
* remove =  削除

例）
```
git commit -m "[add] ボタンを追加した"