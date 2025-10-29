# Flask + PostgreSQL CRUD アプリセットアップ手順
🔧 仮想環境の作成とアクティベート
1. 	プロジェクトフォルダに移動：
cd C:\Users\Yuuki\Documents\3.個人用\flask-postgres-crud
2. 	仮想環境を作成：
python -m venv venv
3. 	仮想環境をアクティベート：
venv\Scripts\activate
4. 	✅ 成功するとプロンプトが以下のように変化します：

(venv) PS C:\Users\Yuuki\Documents\3.個人用\flask-postgres-crud>

📦 依存パッケージのインストール


📋 インストール確認

pip install flask psycopg2-binary
以下のように表示されていれば OK：
Flask               3.x.x
psycopg2-binary     2.x.x

🚀 アプリ起動

python app.py

🌐 ブラウザでアクセス
http://127.0.0.1:5000
