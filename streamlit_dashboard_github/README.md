# Hard drive early warning: the app

A [Streamlit](https://streamlit.io) app that shows, day by day, which hard drives of the Backblaze fleet a
technician should check first, according to the model of the project
[Predicting hard-drive failures with Backblaze Drive Stats](../README.md). It is in English and Spanish.

You can open it online from the link at the top of the [main README](../README.md), or run it on your computer.

## What you see

- **A day, as if it were today.** Pick any day between 1 July 2025 and 15 June 2026 with the date box or the
  arrows next to it; the model was not trained on these months. The app opens on 1 January 2026.
- **The hard drives that enter the alert list that day**, ordered by their risk score. A drive enters the list
  on the first day its risk score crosses the alert line; after that it counts as reviewed and does not appear
  again.
- **One drive in detail.** Click a row of the list to see the drive's model, capacity and age, why it entered
  the list and its risk score day by day.
- **Why it entered the list:** the ten facts that weigh most in its risk score, computed with SHAP. In pink, what
  raises it; in blue, what lowers it.
- **Show what happened next:** a switch that reveals whether the drive really failed afterwards, and when. It is
  what the technician could not know that day.
- **The ⓘ icons** explain each part of the screen.

## How to read the risk score

The risk score goes from 0 to 1: the higher it is, the higher the risk that the drive fails in the next 15 days.
It ranks the drives, but it is not a probability. The alert line, 0.834, was fixed on the validation period
(July – December 2025): with it, the model detects as many failures as the rule a technician would use today,
based on five S.M.A.R.T. attributes, with 55 % fewer false alarms.

## Run it on your computer

You need Python 3.12 or newer. From the root of the repository:

```bash
pip install -r streamlit_dashboard_github/requirements.txt
streamlit run streamlit_dashboard_github/streamlit_app.py --server.address localhost
```

Then open http://localhost:8501.

## What is in this folder

| File | What it is |
|---|---|
| `streamlit_app.py` | The app |
| `app_text.py` | Its texts in both languages, the readable names of the model's variables and how each language writes numbers and dates |
| `app_data/alerts.parquet` | One row per drive life that crosses the alert line, on its first day: the risk score, the value and SHAP value of each variable, and what happened next |
| `app_data/history.parquet` | The daily risk score of those drive lives, July 2025 – June 2026, with the 3 decimals the app shows |
| `app_data/meta.json` | The alert line and the days the app covers |
| `static/` | The header photo and its credit |
| `.streamlit/config.toml` | The app's colours and settings |
| `requirements.txt` | The four libraries the app needs, with fixed versions |

## Where the data come from

The tables in `app_data/` are a small extract of the project's results: the first alert of each drive life
between July 2025 and June 2026, with its SHAP values, and the daily risk score of those drives. The app needs
nothing else: neither the model nor the Backblaze data. They were computed from the public Backblaze Drive Stats
data with the project's pipeline, as the notebooks explain.

## Credits

Data: [Backblaze Drive Stats](https://www.backblaze.com/cloud-storage/resources/hard-drive-test-data). Header
photo: a Backblaze Storage Pod by ChrisDag, licensed under CC BY 2.0; see [`static/CREDITS.md`](static/CREDITS.md).
