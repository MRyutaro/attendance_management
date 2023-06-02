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