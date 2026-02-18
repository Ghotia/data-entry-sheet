import re
import zlib
import math
from urllib.parse import urlparse

SUSPICIOUS_TLDS = {"info","xyz","top","ru","cn"}


def shannon_entropy(s: str) -> float:
    if not s:
        return 0.0
    probs = [float(s.count(c)) / len(s) for c in set(s)]
    return -sum(p * math.log2(p) for p in probs)


def kolmogorov_approx(s: str) -> float:
    # Approximate Kolmogorov complexity by compressed length
    if not s:
        return 0.0
    comp = zlib.compress(s.encode('utf-8'))
    return len(comp)


def has_ip(url: str) -> bool:
    return bool(re.search(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", url))


def extract_domain(url: str) -> str:
    try:
        p = urlparse(url)
        host = p.netloc or p.path
        return host.lower()
    except Exception:
        return url.lower()


def url_heuristics(url: str) -> dict:
    u = url.strip()
    host = extract_domain(u)
    features = {
        'length': len(u),
        'count_dots': host.count('.'),
        'count_hyphen': u.count('-'),
        'count_at': u.count('@'),
        'count_question': u.count('?'),
        'has_ip': int(has_ip(u)),
        'starts_https': int(u.startswith('https')),
        'shannon_entropy': shannon_entropy(u),
        'kolmogorov_approx': kolmogorov_approx(u),
        'suspicious_tld': int(any(host.endswith('.' + t) for t in SUSPICIOUS_TLDS)),
        'digit_count': sum(c.isdigit() for c in u),
    }
    return features


def analyze_url(url: str) -> dict:
    """Return a structured analysis dict for a single URL."""
    heur = url_heuristics(url)
    suspicion_score = 0.0
    # Simple scoring heuristic for MVP
    suspicion_score += 0.3 if heur['has_ip'] else 0.0
    suspicion_score += 0.2 if heur['count_dots'] > 3 else 0.0
    suspicion_score += 0.15 if heur['count_hyphen'] > 2 else 0.0
    suspicion_score += 0.15 if heur['shannon_entropy'] > 4.0 else 0.0
    suspicion_score += 0.1 if heur['suspicious_tld'] else 0.0
    suspicion_score += 0.1 if heur['digit_count'] > 5 else 0.0

    return {
        'url': url,
        'heuristics': heur,
        'suspicion_score': min(1.0, suspicion_score),
    }
