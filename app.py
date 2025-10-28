from flask import Flask, jsonify, render_template
import psycopg2

app = Flask(__name__)

DB_CONFIG = {
    "dbname": "sampledb3",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432"
}

def get_conn():
    return psycopg2.connect(**DB_CONFIG)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/menus")
def get_menus():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name, path FROM menus ORDER BY id")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    result = [{"id": r[0], "name": r[1], "path": r[2]} for r in rows]
    return jsonify(result)

@app.route("/api/employees")
def get_employees():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name, department FROM employees ORDER BY id")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    result = [{"id": r[0], "name": r[1], "department": r[2]} for r in rows]
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
