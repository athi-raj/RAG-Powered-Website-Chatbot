import requests
import time
import logging
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

MAX_DEPTH  = 3
MAX_PAGES  = 50
DELAY      = 0.5
HEADERS    = {"User-Agent": "Mozilla/5.0 (compatible; RAGBot/1.0)"}
SKIP_EXTS  = {".pdf", ".jpg", ".jpeg", ".png", ".gif", ".zip", ".mp4"}


def _same_domain(url: str, base: str) -> bool:
    return urlparse(url).netloc == urlparse(base).netloc


def _skip(url: str) -> bool:
    path = urlparse(url).path.lower()
    return any(path.endswith(ext) for ext in SKIP_EXTS)


def fetch_page(url: str) -> dict | None:
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        soup  = BeautifulSoup(r.text, "html.parser")

        for tag in soup(["script","style","nav","footer",
                         "header","aside","form","noscript"]):
            tag.decompose()

        title = soup.title.string.strip() if soup.title else url
        text  = soup.get_text(separator=" ", strip=True)

        links = set()
        for a in soup.find_all("a", href=True):
            full = urljoin(url, a["href"])
            clean = urlparse(full)._replace(fragment="").geturl()
            links.add(clean)

        return {"url": url, "title": title, "text": text, "links": links}

    except Exception as e:
        logger.warning(f"Skipping {url}: {e}")
        return None


def crawl(seed: str, max_depth=MAX_DEPTH, max_pages=MAX_PAGES) -> list[dict]:
    visited = set()
    queue   = [(seed, 0)]
    pages   = []

    while queue and len(pages) < max_pages:
        url, depth = queue.pop(0)

        if url in visited or depth > max_depth or _skip(url):
            continue
        visited.add(url)

        logger.info(f"[depth={depth}] {url}")
        page = fetch_page(url)

        if page:
            pages.append(page)
            if depth < max_depth:
                for link in page["links"]:
                    if _same_domain(link, seed) and link not in visited:
                        queue.append((link, depth + 1))

        time.sleep(DELAY)

    logger.info(f"Done: {len(pages)} pages crawled.")
    return pages
