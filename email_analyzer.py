import re
from typing import Dict

URGENT_KEYWORDS = {'urgent','immediately','asap','action required','verify','password','expire','suspend','security alert'}


def extract_sender(headers: Dict[str,str]) -> str:
    return headers.get('From', '')


def count_links(text: str) -> int:
    return len(re.findall(r'https?://', text))


def has_display_name_mismatch(headers: Dict[str,str]) -> bool:
    # crude check: display name contains brand but from-domain differs
    from_hdr = headers.get('From','')
    m = re.search(r'"?([^\"]+)"?\s*<([^>]+)>', from_hdr)
    if not m:
        return False
    display, addr = m.groups()
    display = display.lower()
    addr = addr.lower()
    # if display contains a brand keyword but address domain doesn't match
    brands = ['microsoft','paypal','google','bank','apple']
    for b in brands:
        if b in display and b not in addr:
            return True
    return False


def nlp_urgency_score(text: str) -> float:
    t = text.lower()
    score = 0.0
    for k in URGENT_KEYWORDS:
        if k in t:
            score += 0.2
    # Cap
    return min(1.0, score)


def analyze_email(headers: Dict[str,str], body: str) -> dict:
    links = count_links(body)
    urgency = nlp_urgency_score(body)
    mismatch = has_display_name_mismatch(headers)
    exclamations = body.count('!')
    html_like = bool(re.search(r'<[^>]+>', body))

    score = 0.0
    score += 0.3 if mismatch else 0.0
    score += 0.25 if links > 2 else 0.0
    score += 0.3 * urgency
    score += 0.05 if exclamations > 3 else 0.0
    score += 0.1 if html_like else 0.0

    return {
        'from': extract_sender(headers),
        'links': links,
        'urgency_score': urgency,
        'display_name_mismatch': mismatch,
        'exclamation_count': exclamations,
        'html_like': html_like,
        'suspicion_score': min(1.0, score),
    }
