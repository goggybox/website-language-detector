import requests
from bs4 import BeautifulSoup
import langid
from urllib.parse import urlparse

def normalise_url(url: str) -> str:
    """
    ensure given URL hsa a scheme (defualt to http://)
    """
    parsed = urlparse(url)
    if not parsed.scheme:
        return "http://"+url
    return url

def fetch_text_from_url(url: str, user_language: str = "en") -> str:
    """
    fetch HTML file from a given url and extract text
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept-Language": user_language
    }
    response = requests.get(url, timeout=30, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator=" ")
    return " ".join(text.split())

def detect_language(text: str) -> tuple[str, float]:
    """
    detect language using adbar/py3langid
    """
    if len(text) < 0:
        return ("unknown")
    lang, _ = langid.classify(text)
    if lang == "la":
        # this is default behaviour when it cannot classify. default to english.
        lang = "en"
    return lang