import re
import os
import joblib
import numpy as np
import pandas as pd
from scipy.sparse import hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score


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


def main():
    here = os.path.dirname(__file__)
    data_path = os.path.join(here, 'sample_urls.csv')
    df = pd.read_csv(data_path)

    X_urls = df['url'].astype(str).values
    y = df['label'].values

    # Vectorize URL strings using character n-grams
    vec = TfidfVectorizer(analyzer='char_wb', ngram_range=(3,5), max_features=2000)
    X_text = vec.fit_transform(X_urls)

    # Heuristic features
    X_heur = extract_heuristics(X_urls)

    # Combine
    from scipy import sparse
    X = hstack([X_text, sparse.csr_matrix(X_heur)])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    clf = LogisticRegression(max_iter=1000, class_weight='balanced')
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    print('Accuracy:', accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    # Save artifacts
    model_path = os.path.join(here, 'model.joblib')
    vec_path = os.path.join(here, 'vectorizer.joblib')
    joblib.dump(clf, model_path)
    joblib.dump(vec, vec_path)
    print('Saved model to', model_path)
    print('Saved vectorizer to', vec_path)


if __name__ == '__main__':
    main()
