from flask import Flask, jsonify, render_template, request
import psycopg2
import os, json

app = Flask(__name__)

# ---------------------------------------------
# 設定ディレクトリ
# ---------------------------------------------
CONFIG_DIR = os.path.join(os.path.dirname(__file__), "config")


# ---------------------------------------------
# JSON ファイル読み込みユーティリティ
# ---------------------------------------------
def load_json(path):
    """指定パスの JSON を読み込む"""
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------
# PostgreSQL 接続取得
# ---------------------------------------------
def get_connection():
    """PostgreSQL への接続を返す"""
    return psycopg2.connect(
        host="localhost",
        port="5432",
        database="sampledb3",
        user="postgres",
        password="postgres"
    )


# ---------------------------------------------
# ルート（index.html を返す）
# ---------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


# ---------------------------------------------
# メニュー取得 API
# ---------------------------------------------
@app.route("/api/menu")
def get_menu():
    """メニュー情報を返す"""
    menu = [
        {"label": "社員一覧", "path": "employees"},
        {"label": "部署一覧", "path": "departments"}
    ]
    return jsonify(menu)


# ---------------------------------------------
# UI 定義取得 API
# search.json と list.json を自動読み込み
# ---------------------------------------------
@app.route("/api/ui/<page>")
def get_ui(page):
    """
    指定ページの UI 定義を返す。
    - main JSON: ui/<page>/<page>.json
    - search.json / list.json を自動統合
    """
    base_path = os.path.join(CONFIG_DIR, "ui", page)
    main_json_path = os.path.join(base_path, f"{page}.json")

    if not os.path.exists(main_json_path):
        return jsonify({"error": f"メイン定義が見つかりません: {main_json_path}"}), 404

    ui_def = load_json(main_json_path)

    # parts を読み込む場合（従来のサブ JSON）
    if "parts" in ui_def:
        for part in ui_def["parts"]:
            sub_path = os.path.join(base_path, part["path"])
            if os.path.exists(sub_path):
                try:
                    ui_def[part["type"]] = load_json(sub_path)
                except Exception as e:
                    ui_def[part["type"]] = {"error": f"{part['path']} 読み込み失敗: {str(e)}"}
            else:
                ui_def[part["type"]] = {}

    # search.json / list.json を自動読み込み
    for filename in ["search.json", "list.json"]:
        file_path = os.path.join(base_path, filename)
        key = filename.split(".")[0]  # search.json -> "search"
        if os.path.exists(file_path):
            try:
                ui_def[key] = load_json(file_path)
            except Exception as e:
                ui_def[key] = {"error": f"{filename} 読み込み失敗: {str(e)}"}
        else:
            ui_def[key] = {}

    return jsonify(ui_def)


# ---------------------------------------------
# 社員一覧取得 API（検索付き）
# ---------------------------------------------
@app.route("/api/employees")
def get_employees():
    """社員一覧を返す。name / department で検索可能"""
    name = request.args.get("name", "")
    department = request.args.get("department", "")

    conn = get_connection()
    cur = conn.cursor()

    sql = "SELECT id, name, department, skills FROM employees WHERE 1=1"
    params = []

    if name:
        sql += " AND name ILIKE %s"
        params.append(f"%{name}%")
    if department:
        sql += " AND department ILIKE %s"
        params.append(f"%{department}%")

    sql += " ORDER BY id"
    cur.execute(sql, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    # skills 列を配列に変換
    result = [
        {
            "id": r[0],
            "name": r[1],
            "department": r[2],
            "skills": r[3].split(",") if r[3] else []
        }
        for r in rows
    ]
    return jsonify(result)


# ---------------------------------------------
# 部署一覧取得 API
# ---------------------------------------------
@app.route("/api/departments")
def get_departments():
    """部署一覧を返す"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM departments ORDER BY id")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{"id": r[0], "name": r[1]} for r in rows])


# ---------------------------------------------
# アプリ起動
# ---------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
