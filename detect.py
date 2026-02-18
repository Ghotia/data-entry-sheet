import os
import re
import joblib
import numpy as np
from scipy.sparse import hstack


def has_ip(url):
    return 1 if re.search(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", url) else 0


def count_digits(url):
    return sum(c.isdigit() for c in url)


def extract_heuristics(urls):
    heur = []
    for u in urls:
        heur.append([
            len(u),
            u.count('@'),
            u.count('-'),
            u.count('?'),
            u.count('%'),
            1 if u.startswith('https') else 0,
            has_ip(u),
            count_digits(u),
        ])
    return np.array(heur)


_here = os.path.dirname(__file__)
_model_path = os.path.join(_here, 'model.joblib')
_vec_path = os.path.join(_here, 'vectorizer.joblib')


def load_artifacts():
    if not os.path.exists(_model_path) or not os.path.exists(_vec_path):
        raise FileNotFoundError('Model artifacts not found. Run train.py first to create them.')
    clf = joblib.load(_model_path)
    vec = joblib.load(_vec_path)
    return clf, vec


def predict_url(url, clf=None, vec=None):
    if clf is None or vec is None:
        clf, vec = load_artifacts()
    X_text = vec.transform([url])
    heur = extract_heuristics([url])
    from scipy import sparse
    X = hstack([X_text, sparse.csr_matrix(heur)])
    prob = clf.predict_proba(X)[0,1]
    label = int(prob >= 0.5)
    return {'url': url, 'phishing_prob': float(prob), 'label': label}


def explain_url(url, clf=None, vec=None, top_n=10):
    """Provide a simple explainability report for linear models.

    Returns top positive and negative feature contributions. If `shap` is
    available it will be used; otherwise this falls back to coefficient * feature.
    """
    if clf is None or vec is None:
        clf, vec = load_artifacts()

    X_text = vec.transform([url])
    heur = extract_heuristics([url])
    from scipy import sparse
    X = hstack([X_text, sparse.csr_matrix(heur)])

    # Build feature names: vectorizer features + heuristic names
    try:
        text_features = list(vec.get_feature_names_out())
    except Exception:
        # fallback
        text_features = [f'text_ngram_{i}' for i in range(X_text.shape[1])]
    heur_names = ['length','count_at','count_hyphen','count_question','count_percent','starts_https','has_ip','digit_count']
    feature_names = text_features + heur_names

    # Try SHAP if installed and supported
    try:
        import shap
        explainer = shap.Explainer(clf, feature_perturbation='interventional')
        shap_values = explainer(X)
        # shap_values values for positive class index 1 if available
        vals = shap_values.values[0]
    except Exception:
        # Fallback for linear models: coef * x
        import numpy as np
        x_arr = X.toarray()[0]
        coef = clf.coef_[0]
        vals = coef * x_arr

    # Pair names with contributions
    contribs = []
    for name, v in zip(feature_names, vals[:len(feature_names)]):
        contribs.append({'feature': name, 'contribution': float(v)})

    # sort
    contribs_sorted = sorted(contribs, key=lambda x: x['contribution'], reverse=True)
    pos = contribs_sorted[:top_n]
    neg = sorted(contribs, key=lambda x: x['contribution'])[:top_n]

    return {'url': url, 'top_positive': pos, 'top_negative': neg}


if __name__ == '__main__':
    import argparse
    import csv

    parser = argparse.ArgumentParser(description='Phishing URL detector')
    parser.add_argument('--url', help='Single URL to classify')
    parser.add_argument('--csv', help='CSV file with column "url" to classify and output results to stdout')
    args = parser.parse_args()

    clf, vec = None, None
    if args.url:
        clf, vec = load_artifacts()
        print(predict_url(args.url, clf=clf, vec=vec))
    elif args.csv:
        clf, vec = load_artifacts()
        with open(args.csv, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            writer = csv.DictWriter(None, fieldnames=['url','phishing_prob','label'])
            # Print CSV header
            print('url,phishing_prob,label')
            for row in reader:
                out = predict_url(row['url'], clf=clf, vec=vec)
                print(f"{out['url']},{out['phishing_prob']:.4f},{out['label']}")
    else:
        print('Provide --url, --csv, or --explain. Run train.py first if artifacts are missing.')
