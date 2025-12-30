from flask import Flask, jsonify, request
import os
import psycopg2

app = Flask(__name__)

def get_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        database=os.getenv("DB_NAME", "studentsdb"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
    )

@app.get("/health")
def health():
    return jsonify(status="ok")

@app.get("/students")
def list_students():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS students (id SERIAL PRIMARY KEY, name TEXT NOT NULL);")
    cur.execute("SELECT id, name FROM students ORDER BY id;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{"id": r[0], "name": r[1]} for r in rows])

@app.post("/students")
def add_student():
    data = request.get_json(force=True)
    name = (data.get("name") or "").strip()
    if not name:
        return jsonify(error="name is required"), 400

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS students (id SERIAL PRIMARY KEY, name TEXT NOT NULL);")
    cur.execute("INSERT INTO students (name) VALUES (%s) RETURNING id;", (name,))
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(id=new_id, name=name), 201

if __name__ == "__main__":
    # Flask dev server is fine for semester demo.
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
