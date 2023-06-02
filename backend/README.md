# backendの動かし方

## ローカルで動かしたい場合

- `pip install -r requirements.txt`と入力してライブラリをインストールする
- .envファイルを/backendに置く（これは全員共有のenvファイルなので後で共有します）
- `python manage.py createsuperuser`と打って管理者用のユーザを登録する。
コマンドを打ったら、ユーザ名とパスワードを聞かれるので入力する（メールアドレスは登録しなくていいからEnterで良き）
- `python manage.py migrate`と入力して、データベースを作成、もしくは更新する（db.sqlite3っていうファイルがデータベースです）
- `python manage.py runserver`と入力
- `http://127.0.0.1:8000/admin`にアクセスする
- さっき登録したユーザ名とパスワードを入力する
- もし下のようなエラーがでたら言ってください。ダミーデータを入れる必要があります
```
You are trying to add a non-nullable field 'group' to user without a default; we can't do that (the database needs something to populate existing rows).
Please select a fix:
 1) Provide a one-off default now (will be set on all existing rows with a null value for this column)
 2) Quit, and let me add a default in models.py
Select an option:
```