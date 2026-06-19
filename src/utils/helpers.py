import hashlib, re

def url_to_filename(url: str, ext=".json") -> str:
    """Convert a URL to a safe filename."""
    slug = re.sub(r"[^\w]", "_", url)[:60]
    h    = hashlib.md5(url.encode()).hexdigest()[:6]
    return f"{slug}_{h}{ext}"

def count_tokens(text: str) -> int:
    """Rough token estimate (1 token ≈ 4 chars)."""
    return len(text) // 4

def deduplicate(items: list[dict], key="text") -> list[dict]:
    seen, out = set(), []
    for item in items:
        val = item.get(key, "")
        if val not in seen:
            seen.add(val)
            out.append(item)
    return out
