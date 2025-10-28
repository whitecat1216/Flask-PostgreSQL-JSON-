from flask import Flask, jsonify, render_template, request
import json
import os
import psycopg2

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(BASE_DIR, "config")

# ✅ PostgreSQL接続設定（自分の環境に合わせて変更）
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "sampledb3",
    "user": "postgres",
    "password": "postgres"
}

# --- JSON読み込み ---
def load_json(filename):
    path = os.path.join(CONFIG_DIR, filename)
    with open(path, encoding="utf-8") as f:
        return json.load(f)

# --- DB接続 ---
def get_connection():
    return psycopg2.connect(**DB_CONFIG)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/menus")
def get_menus():
    return jsonify(load_json("menu.json"))

@app.route("/api/employees")
def get_employees():
    source = request.args.get("source", "json")

    if source == "db":
        # --- PostgreSQLから取得 ---
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT id, name, department FROM employees ORDER BY id;")
            rows = cur.fetchall()
            data = [{"id": r[0], "name": r[1], "department": r[2]} for r in rows]
            cur.close()
            conn.close()
            return jsonify(data)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    else:
        # --- JSONから取得 ---
        return jsonify(load_json("employees.json"))

if __name__ == "__main__":
    app.run(debug=True)
