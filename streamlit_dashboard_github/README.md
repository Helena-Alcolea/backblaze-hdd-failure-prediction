# Dashboard

The technician's daily early-warning list as a [Streamlit](https://streamlit.io) app, in English and Spanish: for
a day between July 2025 and June 2026, the hard drives that cross the alert line for the first time, each with
its details, the facts that weigh most in its risk score (SHAP) and its risk score day by day.

The app reads only the compact tables in [`app_data/`](app_data): it needs neither the model, nor DuckDB, nor the
Backblaze data, so it installs and starts in seconds.

## Run it locally

From the root of the repository:

```bash
pip install -r streamlit_dashboard_github/requirements.txt
streamlit run streamlit_dashboard_github/streamlit_app.py --server.address localhost
```

Inside the project, with its own environment: `uv run streamlit run streamlit_dashboard_github/streamlit_app.py`.
Then open http://localhost:8501.

## Publish it on Streamlit Community Cloud

1. Upload this folder, as it is, to the root of the GitHub repository.
2. Sign in to https://share.streamlit.io with the GitHub account and create an app: the repository, the branch
   `main` and, as *Main file path*, `streamlit_dashboard_github/streamlit_app.py`.
3. Streamlit installs [`requirements.txt`](requirements.txt), from this folder, and reads its settings from
   [`.streamlit/config.toml`](.streamlit/config.toml), also in this folder. It has been tested with Python 3.12
   and 3.14.

## What is in this folder

| File | What it is |
|---|---|
| `streamlit_app.py` | The app |
| `app_text.py` | Its texts in both languages, the readable names of the model's variables and how numbers and dates are written in each language |
| `app_data/alerts.parquet` | One row per drive life that crosses the alert line, on its first day: the risk score, the value and SHAP value of each variable, and what happened next |
| `app_data/history.parquet` | The daily risk score of those lives, July 2025 – June 2026, with the 3 decimals the app shows |
| `app_data/meta.json` | The alert line and the days of the timeline |
| `static/` | The header photo and its credit |
| `.streamlit/config.toml` | Theme and settings |
| `requirements.txt` | The four libraries it needs, with fixed versions |

## Regenerate `app_data/`

`app_data/` is written by the project's `dashboard` step, from the model's predictions and SHAP values (which are
not in the repository: they are built from the Backblaze data by the steps before it):

```bash
uv run python -m backblaze_hdd_failure_prediction.dashboard
```

## Credits

Data: [Backblaze Drive Stats](https://www.backblaze.com/cloud-storage/resources/hard-drive-test-data). Header
photo: see [`static/CREDITS.md`](static/CREDITS.md).
