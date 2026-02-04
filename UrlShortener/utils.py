# utils.py
import re
import validators
from urllib.parse import urlparse


def validate_url(url):
    """
    Validate if the provided string is a valid URL
    """
    # Check if URL starts with http:// or https://
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    # Use validators library if available, otherwise use regex
    try:
        if validators.url(url):
            return url, True
    except:
        pass

    # Basic URL validation with regex
    url_pattern = re.compile(
        r"^(https?://)?"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"  # domain...
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )

    if url_pattern.match(url):
        return url, True

    return url, False


def is_valid_custom_code(code):
    """
    Validate custom short code
    """
    # Check length (3-20 characters)
    if len(code) < 3 or len(code) > 20:
        return False

    # Check if contains only alphanumeric characters and hyphens/underscores
    if not re.match(r"^[a-zA-Z0-9_-]+$", code):
        return False

    # Check if not a reserved word
    reserved_words = ["api", "admin", "stats", "about", "help", "shorten"]
    if code.lower() in reserved_words:
        return False

    return True


def format_stats(stats):
    """
    Format statistics for display
    """
    if not stats:
        return None

    from datetime import datetime

    formatted = stats.copy()

    # Format dates
    if formatted.get("created_at"):
        if isinstance(formatted["created_at"], str):
            formatted["created_at"] = datetime.fromisoformat(
                formatted["created_at"].replace("Z", "+00:00")
            )

    if formatted.get("last_accessed"):
        if isinstance(formatted["last_accessed"], str):
            formatted["last_accessed"] = datetime.fromisoformat(
                formatted["last_accessed"].replace("Z", "+00:00")
            )

    return formatted
