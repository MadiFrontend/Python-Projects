# database.py
import sqlite3
from datetime import datetime
from flask import current_app


def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(current_app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    return conn


class URLShortener:
    def __init__(self):
        self.conn = get_db_connection()

    def create_short_url(self, original_url, custom_code=None):
        """Create a new short URL entry"""
        cursor = self.conn.cursor()

        # Generate short code if not provided
        if not custom_code:
            short_code = self._generate_short_code()
        else:
            short_code = custom_code

        try:
            cursor.execute(
                """
                INSERT INTO urls (original_url, short_code, created_at)
                VALUES (?, ?, ?)
            """,
                (original_url, short_code, datetime.now()),
            )
            self.conn.commit()
            return short_code
        except sqlite3.IntegrityError:
            if custom_code:
                raise ValueError("Custom code already exists")
            # Retry with different code
            return self.create_short_url(original_url)

    def _generate_short_code(self, length=6):
        """Generate a random short code"""
        import random
        import string

        characters = string.ascii_letters + string.digits
        return "".join(random.choice(characters) for _ in range(length))

    def get_original_url(self, short_code):
        """Get original URL by short code"""
        cursor = self.conn.cursor()

        # Get URL and update click count
        cursor.execute(
            """
            UPDATE urls 
            SET clicks = clicks + 1, last_accessed = ?
            WHERE short_code = ?
        """,
            (datetime.now(), short_code),
        )

        cursor.execute(
            """
            SELECT original_url FROM urls WHERE short_code = ?
        """,
            (short_code,),
        )

        result = cursor.fetchone()
        self.conn.commit()

        return result[0] if result else None

    def get_url_stats(self, short_code):
        """Get statistics for a short URL"""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT original_url, short_code, created_at, clicks, last_accessed
            FROM urls WHERE short_code = ?
        """,
            (short_code,),
        )

        result = cursor.fetchone()
        if result:
            return dict(result)
        return None

    def close(self):
        """Close database connection"""
        self.conn.close()
