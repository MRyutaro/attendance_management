1. Anacondaをダウンロードする
2. `Anaconda Powershell Prompt`を開く

![Anaconda Powershell Prompt](image/スクリーンショット%202022-12-12%20130225.png)

3. 仮想環境を作る
```
conda create -n attendance_management
```
4. 作った仮想環境の中に入る
```
conda activate attendance_management
```
5. cdコマンドを使って、自分が保存したフォルダまで移動する
6. リモートレポジトリの情報をローカルに反映させる
```
git pull origin feature-test-backend
```
7. backendフォルダに移動
```
cd backend
```
8. 必要なライブラリをインストールする
```
conda install conda_requirements.txt
```
9. プログラムを動かす
```
python app.py
```