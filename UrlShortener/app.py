# app.py
from flask import Flask, render_template, request, redirect, jsonify
import sqlite3
import hashlib
import string
import random
from datetime import datetime

app = Flask(__name__)

# Configuration
app.config["DATABASE"] = "urls.db"
app.config["BASE_URL"] = "http://localhost:5000"
app.config["SHORT_URL_LENGTH"] = 6


def init_db():
    """Initialize the SQLite database"""
    conn = sqlite3.connect(app.config["DATABASE"])
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT NOT NULL,
            short_code TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            clicks INTEGER DEFAULT 0,
            last_accessed TIMESTAMP
        )
    """
    )
    conn.commit()
    conn.close()


@app.route("/")
def index():
    """Render the homepage"""
    return render_template("index.html")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
