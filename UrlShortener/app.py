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

# app.py (updated)
from flask import Flask, render_template, request, redirect, jsonify, url_for
from database import URLShortener
from utils import validate_url, is_valid_custom_code, format_stats
import os

app = Flask(__name__)

# Configuration
app.config["DATABASE"] = "urls.db"
app.config["BASE_URL"] = os.environ.get("BASE_URL", "http://localhost:5000")
app.config["SHORT_URL_LENGTH"] = 6


def get_shortener():
    """Get URL shortener instance"""
    return URLShortener()


@app.route("/")
def index():
    """Render the homepage"""
    return render_template("index.html", base_url=app.config["BASE_URL"])


@app.route("/shorten", methods=["POST"])
def shorten_url():
    """Shorten a URL"""
    data = request.get_json() or request.form

    original_url = data.get("url", "").strip()
    custom_code = data.get("custom_code", "").strip() or None

    # Validate URL
    validated_url, is_valid = validate_url(original_url)
    if not is_valid:
        return jsonify({"error": "Invalid URL provided"}), 400

    # Validate custom code if provided
    if custom_code and not is_valid_custom_code(custom_code):
        return jsonify({"error": "Invalid custom code"}), 400

    # Create short URL
    shortener = get_shortener()
    try:
        short_code = shortener.create_short_url(validated_url, custom_code)
        short_url = f"{app.config['BASE_URL']}/{short_code}"

        response = {
            "original_url": validated_url,
            "short_url": short_url,
            "short_code": short_code,
        }

        return jsonify(response), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An error occurred"}), 500
    finally:
        shortener.close()


@app.route("/<short_code>")
def redirect_to_url(short_code):
    """Redirect to original URL"""
    shortener = get_shortener()
    try:
        original_url = shortener.get_original_url(short_code)
        if original_url:
            return redirect(original_url)
        else:
            return jsonify({"error": "Short URL not found"}), 404
    finally:
        shortener.close()


@app.route("/api/stats/<short_code>")
def get_stats(short_code):
    """Get statistics for a short URL"""
    shortener = get_shortener()
    try:
        stats = shortener.get_url_stats(short_code)
        if stats:
            formatted_stats = format_stats(stats)
            return jsonify(formatted_stats)
        else:
            return jsonify({"error": "Short URL not found"}), 404
    finally:
        shortener.close()


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
