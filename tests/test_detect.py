import os
import json
from phishing_detector.detect import predict_url, explain_url


def test_predict_and_explain_fallback():
    # This test assumes model artifacts exist; if not, skip
    here = os.path.dirname(__file__)
    root = os.path.dirname(here)
    model = os.path.join(root, 'model.joblib')
    vec = os.path.join(root, 'vectorizer.joblib')
    if not (os.path.exists(model) and os.path.exists(vec)):
        import pytest
        pytest.skip('Model artifacts not present; skip training-dependent test')

    url = 'http://example.com/login'
    res = predict_url(url)
    assert 'phishing_prob' in res
    assert 0.0 <= res['phishing_prob'] <= 1.0

    expl = explain_url(url)
    assert 'top_positive' in expl and 'top_negative' in expl
    assert isinstance(expl['top_positive'], list)
