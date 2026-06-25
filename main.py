from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3, os
from datetime import datetime

app = Flask(__name__)
CORS(app)

DB_PATH = "bridge.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS inspections (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            saved_at     TEXT,
            bridge_id    TEXT,
            bridge_name  TEXT,
            location     TEXT,
            inspect_date TEXT,
            damage_rank  TEXT,
            comment      TEXT
        )
    """)
    conn.commit()
    conn.close()

@app.route("/save", methods=["POST"])
def save():
    body = request.json
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        INSERT INTO inspections
        (saved_at, bridge_id, bridge_name, location, inspect_date, damage_rank, comment)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        body.get("bridge_id"),
        body.get("bridge_name"),
        body.get("location"),
        body.get("inspect_date"),
        body.get("damage_rank"),
        body.get("comment"),
    ))
    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})

@app.route("/list", methods=["GET"])
def list_all():
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT * FROM inspections ORDER BY id DESC").fetchall()
    conn.close()
    return jsonify([{
        "id": r[0], "saved_at": r[1], "bridge_id": r[2],
        "bridge_name": r[3], "location": r[4], "inspect_date": r[5],
        "damage_rank": r[6], "comment": r[7]
    } for r in rows])

init_db()

if __name__ == "__main__":
    app.run()

