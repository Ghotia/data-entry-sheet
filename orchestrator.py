import datetime
import uuid
from .logger import log_detection


def _now_iso():
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'


def make_alert(vector, target, threat_type, risk_score, analysis, actions):
    alert = {
        'timestamp': _now_iso(),
        'threat_id': f"phish_{uuid.uuid4().hex[:8]}",
        'vector': vector,
        'target': target,
        'threat_type': threat_type,
        'risk_score': float(risk_score),
        'severity': _severity_from_score(risk_score),
        'analysis': analysis,
        'action_taken': actions,
        'knowledge_base_updated': False,
    }
    # log for audit
    log_detection(alert)
    return alert


def _severity_from_score(s: float) -> str:
    if s >= 0.9:
        return 'Critical'
    if s >= 0.7:
        return 'High'
    if s >= 0.4:
        return 'Medium'
    return 'Low'


def quarantine_email(email_id: str, reason: str):
    # SAFE STUB: do not delete or forward; only log action
    action = f"Email {email_id} quarantined (simulated): {reason}"
    log_detection({'timestamp': _now_iso(), 'action': action})
    return action


def block_url(url: str, reason: str):
    # SAFE STUB: simulate network block by logging only
    action = f"URL blocked at gateway (simulated): {url} - {reason}"
    log_detection({'timestamp': _now_iso(), 'action': action})
    return action


def alert_user(user: str, message: str):
    # SAFE STUB: do not send real messages; log the intended user alert
    action = f"User alert for {user}: {message}"
    log_detection({'timestamp': _now_iso(), 'action': action})
    return action
