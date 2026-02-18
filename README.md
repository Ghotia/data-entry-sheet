# Phishing Detector (simple)

This repository contains a small, beginner-friendly phishing URL detector you can upload to GitHub and run locally.

What it includes

- `train.py` — trains a simple logistic regression model on `sample_urls.csv` and saves `model.joblib` and `vectorizer.joblib`.
- `detect.py` — loads artifacts and predicts whether a URL is phishing.
- `sample_urls.csv` — small sample dataset (for demo/training).
- `requirements.txt` — Python dependencies.

Quick start

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
# source .venv/bin/activate
pip install -r phishing_detector/requirements.txt
```

2. Train the model:

```bash
python phishing_detector/train.py
```

3. Classify a single URL:

```bash
python phishing_detector/detect.py --url "http://example.com/login"
```

Notes

- This is a small demo using URL character n-grams + simple heuristics. For production use, gather a large labeled dataset, add more features (HTML, WHOIS, hosting), and evaluate thoroughly.

License: add your license before publishing.
 
Publishing & CI

- The repository includes a GitHub Actions CI workflow at `.github/workflows/ci.yml` that installs dependencies, trains the demo model, and runs tests.
- Before pushing to GitHub, ensure you have a Python 3.8+ environment available on the runner.

How to publish (local push)

1. Create a repo on GitHub (via web UI) or use the `gh` CLI.
2. From this folder run:

```powershell
cd /d D:\Projects\red-team-framework\phishing_detector
git init
git branch -M main
git add .
git commit -m "Initial: phishing detector MVP with explainability and CI"
git remote add origin https://github.com/<your-username>/<repo>.git
git push -u origin main
```

If you want me to push directly I can do so if you provide a GitHub repository URL and a personal access token with repo permissions — otherwise run the commands above locally.
