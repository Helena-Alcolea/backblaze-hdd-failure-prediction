"""Streamlit app: the technician's list of one day, and why each drive is on it.

What it shows was decided with Helena (29 Oct, 8 Nov and 12 Nov; see DIARIO.md):
- one day from 1 July 2025 to 15 June 2026 (validation and test, the periods the model did not train on;
  the last 15 days of the data have no labels for healthy drives),
  "as if" today were that day; the first day of test, 1 January 2026, by default (Helena, 12 Nov);
- the lives that reach the working threshold (0.83) for the first time that day. Each life enters the
  list once and is then taken as reviewed, so earlier alerts are counted but not listed again;
- ordered by that day's score, from highest to lowest, with how much it rose since yesterday as a column;
  a drive is picked by clicking any cell of its row;
- the first day of validation as it is (1,254 alerts), with a note: it is the day the system is
  switched on;
- for the chosen drive, its facts as small figures, why it entered the list (a small table with the
  weight of each fact in its score, from SHAP) and its risk score day by day, with the alert line;
- the risk score from 0 to 1 with three decimals, not as a percentage, which would read as a calibrated
  probability; an ⓘ next to the chart's title says what it is and how the alert line was fixed (Helena, 13 Nov);
- every help tip looks the same, Streamlit's own ones included: an ⓘ and a navy box (Helena, 13 Nov);
- what happened next (whether and when the drive failed) behind a switch that is off by default;
- in Spanish and English, with a switch with flags at the top, Spanish by default;
- a header with a photo of a Backblaze Storage Pod (CC BY 2.0, credited in the footer) behind the title;
- the colours of Helena's palette (coolors.co/2b2d42-8d99ae-edf2f4-ef233c-d90429), with a reddish page
  and borders because the Backblaze logo is red: the page in .streamlit/config.toml, the boxes (figures,
  list and charts) in BOXES, with a 2 px border, and the charts in COLORS; the header and the footer
  without a border (Helena, 13 Nov); few explanatory captions, in black;
- the day picked with buttons for the day before and after around a narrow date box, and the period of
  the score chart chosen with a slider.

It is the published app: this folder (streamlit_dashboard_github/) holds everything it needs and nothing else, so it
can go to GitHub and Streamlit Community Cloud as it is (Helena, 13 Nov, as in her other projects). It reads only
the compact tables in app_data/, written by the project's `dashboard` step: the first alerts, the daily scores and
meta.json (the alert line and the days of the timeline). It needs neither the model nor DuckDB.

Usage, from the root of the project:
    uv run streamlit run streamlit_dashboard_github/streamlit_app.py
See README.md in this folder for publishing it.
"""

import html
import json
import sys
from datetime import date, timedelta
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

# Streamlit puts this script's folder on the import path, so the texts are found next to it. Without writing a
# __pycache__ folder here: this folder is uploaded as it is.
sys.dont_write_bytecode = True
from app_text import LANGUAGES, day_label, number, outcome, score, text, variable_parts, variable_value  # noqa: E402

# The app's data, next to it: the tables and meta.json written by the project's `dashboard` step.
DATA_DIR = Path(__file__).resolve().parent / "app_data"
ALERTS, HISTORY = DATA_DIR / "alerts.parquet", DATA_DIR / "history.parquet"
META = json.loads((DATA_DIR / "meta.json").read_text(encoding="utf-8"))
# The timeline of the list, from the first day of validation to the last day with a label for every drive
FIRST_DAY, TEST_START, LAST_DAY = (date.fromisoformat(META[k]) for k in ("first_day", "test_start", "last_list_day"))

TOP_VARIABLES = 10
# Header photo: a Backblaze Storage Pod by ChrisDag, CC BY 2.0 (see static/CREDITS.md), served by
# Streamlit from the static/ folder next to this script (server.enableStaticServing in .streamlit/config.toml).
HEADER_PHOTO = "app/static/storage_pod_banner.jpg"
# The app has a single, light theme (.streamlit/config.toml). It used to have a dark one too, chosen from
# `st.context.theme`, but Streamlit infers that from the page's background colour and does not know it on
# the first run of a session, so the boxes changed colour after the first click (12 Nov). Helena had not
# asked for a dark mode: removed.
# Colours of the charts, from Helena's palette: red raises the score and a more saturated slate blue
# lowers it (checked with the data-viz palette validator against the boxes: lightness, chroma,
# colour-blind separation and contrast), the score line in the palette's navy over a rose area, the alert
# line in red, the alert day in the palette's grey, the texts in navy (black, not grey: Helena, 12 Nov)
# and a thin light grey grid.
COLORS = {"up": "#d90429", "down": "#3f67b0", "line": "#2b2d42", "area": "#d9a0a5", "alert_line": "#ef233c",
          "muted": "#8d99ae", "failure": "#d90429", "ink": "#2b2d42", "grid": "#ddd5d2"}
# Boxes of the figures, the list, the charts and the footer: a warm white background on the pastel red page,
# with a red border, a darker shade of the page (Helena, 12 Nov). The page is in .streamlit/config.toml, in this
# folder.
BOXES = {"background": "#fffaf7", "border": "#9b2c35", "track": "#f1e1df", "tip": "#2b2d42", "tip_ink": "#f5eeee",
         "on_page": "#2b2d42", "ink": "#2b2d42", "selected": "#f6d3d4"}


def style() -> str:
    """CSS of the page: the boxes, the centred figures, the larger language switch, the small table of why a
    drive is on the list, and the info tips: ours and Streamlit's (fields, figures and the list's columns) with
    the same ⓘ and the same navy box. Only the help icons change: the buttons of the table's toolbar keep theirs."""
    b = BOXES
    return f"""<style>
[data-testid="stMetric"], .st-key-list_box, .st-key-why_box, .st-key-history_box, .st-key-footer_box {{
  background: {b['background']}; border: 2px solid {b['border']} !important; border-radius: 0.8rem;
}}
.st-key-footer_box {{ border: none !important; }}
.st-key-kpis [data-testid="stMetric"] {{ text-align: center; }}
.st-key-kpis [data-testid="stMetric"] > div {{ align-items: center; }}
.st-key-kpis [data-testid="stMetricLabel"], .st-key-kpis [data-testid="stMetricValue"] {{
  display: flex; width: 100%; justify-content: center;
}}
.st-key-facts [data-testid="stMetricValue"] {{ font-size: 1.2rem; }}
.st-key-switch label > div:first-of-type {{
  background: {b['background']} !important; box-shadow: inset 0 0 0 1.5px {b['border']};
}}
.st-key-switch label > div:first-of-type > div {{ background: {b['border']} !important; }}
.st-key-switch label:has(input:checked) > div:first-of-type {{ background: {b['border']} !important; }}
.st-key-switch label:has(input:checked) > div:first-of-type > div {{ background: {b['background']} !important; }}
.hero {{
  display: flex; flex-direction: column; justify-content: center; min-height: 15rem; padding: 2.4rem 2.4rem;
  border-radius: 1rem; color: #ffffff;
  background: linear-gradient(90deg, rgba(18, 10, 14, 0.94) 0%, rgba(18, 10, 14, 0.84) 38%,
              rgba(18, 10, 14, 0.35) 72%, rgba(94, 11, 18, 0.15) 100%),
              url("{HEADER_PHOTO}") center 45% / cover no-repeat;
}}
.hero h1 {{ color: #ffffff; font-size: 3rem; font-weight: 800; line-height: 1.1; margin: 0 0 0.7rem;
  letter-spacing: -0.02em; text-shadow: 0 2px 14px rgba(0, 0, 0, 0.45); max-width: 42rem; padding: 0; }}
.hero p {{ color: #f5eeee; font-size: 1.1rem; margin: 0; max-width: 38rem; text-shadow: 0 1px 8px rgba(0, 0, 0, 0.5); }}
.hero .accent {{ width: 4rem; height: 0.3rem; background: #ef233c; border-radius: 0.2rem; margin-bottom: 1rem; }}
.st-key-drive_title h3, .st-key-daynav [data-testid="stWidgetLabel"] p,
.st-key-switch label p, .st-key-daynav [data-testid="stTooltipIcon"], .st-key-switch [data-testid="stTooltipIcon"] {{
  color: {b['on_page']} !important;
}}
.st-key-lang button {{ min-height: 2.75rem; padding: 0.4rem 1.1rem; }}
.st-key-lang button, .st-key-daynav [data-testid^="stBaseButton"] {{
  background: {b['background']} !important; color: {b['ink']} !important; border-color: {b['background']} !important;
}}
.st-key-lang button[aria-checked="true"] {{
  background: {b['tip']} !important; color: {b['tip_ink']} !important; border-color: {b['tip']} !important;
}}
.st-key-lang button p, .st-key-daynav [data-testid^="stBaseButton"] p {{ color: inherit !important; }}
.st-key-daynav [data-testid^="stBaseButton"]:disabled {{ opacity: 0.55; }}
.st-key-lang button p {{ font-size: 1.05rem; font-weight: 600; }}
.why {{ width: 100%; table-layout: fixed; border-collapse: collapse; font-size: 0.9rem; }}
.why th {{ text-align: left; font-weight: 600; padding: 0.3rem 0.4rem; border-bottom: 2px solid {b['border']}; white-space: nowrap; }}
.why td {{ padding: 0.35rem 0.4rem; border-bottom: 1px solid {b['track']}; vertical-align: middle; }}
.why .num {{ width: 2.8rem; font-variant-numeric: tabular-nums; font-weight: 600; }}
.why .attribute {{ width: 34%; line-height: 1.2; }}
.why .kind {{ display: block; font-size: 0.78rem; opacity: 0.7; }}
.why .bar {{ width: 22%; }}
.why .share {{ width: 3.4rem; text-align: right; font-variant-numeric: tabular-nums; font-weight: 600; }}
.why .value {{ text-align: right; font-variant-numeric: tabular-nums; font-size: 0.85rem; white-space: nowrap;
  overflow: hidden; text-overflow: ellipsis; }}
.track {{ position: relative; height: 0.9rem; background: {b['track']}; border-radius: 0.45rem; }}
.zero {{ position: absolute; left: 50%; top: -0.15rem; bottom: -0.15rem; width: 2px; background: {b['border']}; }}
.fill {{ position: absolute; top: 0; bottom: 0; border-radius: 0.45rem; }}
.tip {{ position: relative; display: inline-flex; align-items: center; justify-content: center; width: 1.05rem;
  height: 1.05rem; margin-left: 0.3rem; border: 1.5px solid currentColor; border-radius: 50%; font-size: 0.68rem;
  font-weight: 700; opacity: 0.7; cursor: help; vertical-align: middle; }}
.tip:hover, .tip:focus {{ opacity: 1; outline: none; }}
[data-testid="stTooltipIcon"] svg {{ display: none; }}
[data-testid="stTooltipIcon"] button::before {{ content: "i"; display: inline-flex; align-items: center;
  justify-content: center; width: 1.05rem; height: 1.05rem; border: 1.5px solid currentColor; border-radius: 50%;
  font-size: 0.68rem; font-weight: 700; line-height: 1; opacity: 0.7; }}
[data-testid="stTooltipIcon"] button:hover::before {{ opacity: 1; }}
[data-testid="stTooltipContent"], [data-testid="stDataFrameTooltipContent"] {{ background: {b['tip']} !important;
  color: {b['tip_ink']} !important; border-radius: 0.5rem; font-size: 0.8rem; line-height: 1.35; }}
[data-testid="stTooltipContent"] *, [data-testid="stDataFrameTooltipContent"] * {{ color: {b['tip_ink']} !important; }}
.tip:hover::after, .tip:focus::after {{ content: attr(data-tip); position: absolute; top: 140%; left: -0.5rem; z-index: 20;
  width: 17rem; padding: 0.55rem 0.7rem; border-radius: 0.5rem; background: {b['tip']}; color: {b['tip_ink']};
  font-size: 0.8rem; font-weight: 400; line-height: 1.35; white-space: normal; text-align: left; }}
</style>"""


def as_dates(column: pd.Series) -> pd.Series:
    """A column of dates as Python dates (None where empty), whatever type the Parquet reader gives."""
    return pd.to_datetime(column).dt.date.astype(object).where(column.notna(), None)


@st.cache_data
def load_alerts() -> pd.DataFrame:
    alerts = pd.read_parquet(ALERTS)
    for c in ("date", "failure_day", "last_day"):
        alerts[c] = as_dates(alerts[c])
    return alerts


@st.cache_data
def load_history() -> pd.DataFrame:
    history = pd.read_parquet(HISTORY)
    history["date"] = pd.to_datetime(history["date"])
    return history.set_index(["serial_number", "life"]).sort_index()


def threshold() -> float:
    """The alert line, fixed in validation (comparison B against the 30-day rule), from meta.json."""
    return float(META["threshold"])


def plain(value):
    """A value of a pandas row as a plain Python value, None if it is empty."""
    if value is None or pd.isna(value):
        return None
    return value.item() if hasattr(value, "item") else value


def language() -> str:
    """The language switch, at the top right of the page."""
    with st.container(horizontal=True, horizontal_alignment="right"):
        return st.segmented_control("Idioma / Language", list(LANGUAGES), format_func=LANGUAGES.get, default="es",
                                    required=True, key="lang", label_visibility="collapsed")


def pick_day(lang: str) -> date:
    """The day of the list, in the middle of the page: a narrow date box between the buttons for the day
    before and the day after."""
    st.session_state.setdefault("day", TEST_START)

    def move(days: int) -> None:
        st.session_state.day = min(max(st.session_state.day + timedelta(days=days), FIRST_DAY), LAST_DAY)

    with st.container(horizontal=True, horizontal_alignment="center", vertical_alignment="bottom", gap="medium",
                      key="daynav"):
        st.button(text(lang, "previous"), on_click=move, args=(-1,), disabled=st.session_state.day <= FIRST_DAY)
        st.date_input(text(lang, "day"), min_value=FIRST_DAY, max_value=LAST_DAY, key="day", width=190,
                      help=text(lang, "day_help"), format="DD/MM/YYYY" if lang == "es" else "YYYY-MM-DD")
        st.button(text(lang, "next"), on_click=move, args=(1,), disabled=st.session_state.day >= LAST_DAY)
    return st.session_state.day


def day_table(day_alerts: pd.DataFrame, lang: str, show_outcome: bool, line: float) -> tuple[pd.DataFrame, dict]:
    """The list of the day as the app writes it, and the configuration of each column."""
    columns = {key: text(lang, key) for key in
               ("col_rank", "col_drive", "col_model", "col_capacity", "col_age", "col_score", "col_rise", "col_outcome")}
    rows = []
    for rank, r in enumerate(day_alerts.itertuples(), 1):
        previous = plain(r.previous_probability)
        row = {
            columns["col_rank"]: rank,
            columns["col_drive"]: r.serial_number,
            columns["col_model"]: r.drive_model,
            columns["col_capacity"]: variable_value("capacity_tb", plain(r.capacity_tb), lang),
            columns["col_age"]: variable_value("physical_age_hours", plain(r.physical_age_hours), lang),
            columns["col_score"]: score(r.probability, lang),
            columns["col_rise"]: "—" if previous is None else number(r.probability - previous, lang, 3, sign=True),
        }
        if show_outcome:
            row[columns["col_outcome"]] = outcome(r.date, r.failure_day, r.last_day, bool(r.is_episode), lang)[0]
        rows.append(row)
    config = {
        columns["col_rank"]: st.column_config.NumberColumn(width=40, alignment="center"),
        columns["col_drive"]: st.column_config.Column(width="medium"),
        columns["col_model"]: st.column_config.Column(width="large"),
        columns["col_score"]: st.column_config.Column(help=text(lang, "col_score_help", line=score(line, lang))),
        columns["col_rise"]: st.column_config.Column(help=text(lang, "col_rise_help")),
        columns["col_outcome"]: st.column_config.Column(help=text(lang, "col_outcome_help")),
    }
    return pd.DataFrame(rows), config


def drive_facts(r: pd.Series, lang: str) -> None:
    """The facts of the chosen drive, as a row of small figures."""
    facts = [
        ("fact_model", r["drive_model"], None),
        ("fact_manufacturer", r["manufacturer"], None),
        ("fact_capacity", variable_value("capacity_tb", plain(r["capacity_tb"]), lang), None),
        ("fact_age", number(plain(r["physical_age_hours"]) / 24 / 365.25, lang, 1)
         if plain(r["physical_age_hours"]) is not None else "—", "fact_age_help"),
        ("fact_life", str(r["life"]), "fact_life_help"),
        ("fact_score", score(r["probability"], lang), "fact_score_help"),
    ]
    with st.container(horizontal=True, key="facts"):
        for label, value, help_key in facts:
            st.metric(text(lang, label), value, help=text(lang, help_key) if help_key else None, border=True,
                      width="stretch")


def tip(lang: str, key: str, **values) -> str:
    """A small ⓘ next to a header that shows an explanation when the pointer is over it, or after a click
    on it (tabindex lets it take the focus) until the next click elsewhere."""
    return f'<span class="tip" tabindex="0" data-tip="{html.escape(text(lang, key, **values))}">i</span>'


def why_table(r: pd.Series, variables: list[str], lang: str, colors: dict) -> str:
    """The facts that weigh most in an alert's score, as a small table with a bar per fact. The weight of
    a fact is its SHAP value as a share of the sum of all of them in absolute value: in % of the total,
    positive (red) if it raises the score and negative (blue) if it lowers it."""
    parts = pd.DataFrame({"name": variables, "shap": [float(r[f"shap_{v}"]) for v in variables]})
    parts["share"] = parts["shap"] / parts["shap"].abs().sum()
    top = parts.reindex(parts["share"].abs().sort_values(ascending=False).index).head(TOP_VARIABLES)
    widest = top["share"].abs().max()
    header = (f"<tr><th class='num'>{text(lang, 'why_number')}{tip(lang, 'why_number_tip')}</th>"
              f"<th class='attribute'>{text(lang, 'why_attribute')}{tip(lang, 'why_attribute_tip')}</th>"
              f"<th class='bar'>{text(lang, 'why_weight')}{tip(lang, 'why_weight_tip')}</th><th class='share'></th>"
              f"<th class='value'>{text(lang, 'why_value')}</th></tr>")
    rows = []
    for name, share in zip(top["name"], top["share"]):
        attribute, label, kind = variable_parts(name, lang)
        width = 50 * abs(share) / widest
        left = 50 if share > 0 else 50 - width
        color = colors["up"] if share > 0 else colors["down"]
        value = html.escape(variable_value(name, plain(r[name]), lang), quote=True)
        rows.append(
            f"<tr><td class='num'>{attribute or '—'}</td>"
            f"<td class='attribute'>{html.escape(label)}<span class='kind'>{kind}</span></td>"
            f"<td class='bar'><div class='track'><div class='zero'></div>"
            f"<div class='fill' style='left:{left:.1f}%;width:{width:.1f}%;background:{color}'></div></div></td>"
            f"<td class='share'>{number(100 * share, lang, 0, sign=True)}&nbsp;%</td>"
            f"<td class='value' title='{value}'>{value}</td></tr>")
    return f"<table class='why'><thead>{header}</thead><tbody>{''.join(rows)}</tbody></table>"


def history_chart(history: pd.DataFrame, alert_day: date, failure_day: date | None, line: float, lang: str,
                  colors: dict) -> alt.Chart:
    """The daily risk score of a life over the period, from 0 to 1, with the alert line (labelled with its value),
    the alert day and, if given, the failure day."""
    h = history.reset_index(drop=True)
    h["score_text"] = [score(p, lang) for p in h["probability"]]
    h["date_text"] = [day_label(d.date(), lang) for d in h["date"]]
    x = alt.X("date:T", title=text(lang, "date"), axis=alt.Axis(format="%d/%m" if lang == "es" else "%b %d"))
    # From 0 to 1 with one decimal; Vega writes a decimal point, so Spanish swaps it for a comma
    labels = "replace(format(datum.value, '.1f'), '.', ',')" if lang == "es" else "format(datum.value, '.1f')"
    y = alt.Y("probability:Q", title=text(lang, "score"), scale=alt.Scale(domain=[0, 1]),
              axis=alt.Axis(labelExpr=labels, tickCount=10))
    hover = alt.selection_point(fields=["date"], nearest=True, on="pointerover", empty=False, clear="pointerout")
    alert_line = pd.DataFrame({"y": [line], "date": [h["date"].min()],
                               "label": [text(lang, "line_label", line=score(line, lang))]})
    layers = [
        alt.Chart(h).mark_area(opacity=0.25, color=colors["area"]).encode(x=x, y=y),
        alt.Chart(h).mark_line(strokeWidth=3, color=colors["line"]).encode(x=x, y=y),
        alt.Chart(h).mark_point(size=80, filled=True, color=colors["line"]).encode(
            x=x, y=y, opacity=alt.condition(hover, alt.value(1), alt.value(0)),
            tooltip=[alt.Tooltip("date_text:N", title=text(lang, "date")),
                     alt.Tooltip("score_text:N", title=text(lang, "score"))],
        ).add_params(hover),
        alt.Chart(alert_line).mark_rule(strokeDash=[6, 4], strokeWidth=2, color=colors["alert_line"]).encode(y="y:Q"),
        alt.Chart(alert_line).mark_text(align="left", dx=4, dy=-8, fontWeight="bold", color=colors["ink"]).encode(
            x="date:T", y="y:Q", text="label:N"),
    ]
    first, last = h["date"].min(), h["date"].max()
    marks = [(day, label, color, ink) for day, label, color, ink in
             [(alert_day, text(lang, "alert_mark"), colors["muted"], colors["ink"]),
              (failure_day, text(lang, "failure_mark"), colors["failure"], colors["failure"])]
             if day is not None and first <= pd.Timestamp(day) <= last]  # only the days inside the chart
    middle = first + (last - first) / 2
    for row, (day, label, color, ink) in enumerate(marks):  # the failure label one line lower than the alert's
        mark = pd.DataFrame({"date": [pd.Timestamp(day)], "y": [1.0], "label": [label]})
        right_half = pd.Timestamp(day) > middle  # the label goes on the side with room for it
        layers.append(alt.Chart(mark).mark_rule(color=color, strokeWidth=2).encode(x="date:T"))
        layers.append(alt.Chart(mark).mark_text(color=ink, align="right" if right_half else "left",
                                                dx=-4 if right_half else 4, dy=8 + 14 * row,
                                                fontWeight="bold").encode(
            x="date:T", y="y:Q", text="label:N"))
    # Transparent, so that the chart takes the colour of its box; its texts in black, and the grid in a
    # thin light grey (the theme drew it in the dark border colour, which made the chart hard to read)
    return (alt.layer(*layers).properties(height=340).configure(background="transparent")
            .configure_axis(titleColor=colors["ink"], labelColor=colors["ink"], titleFontWeight=600,
                            gridColor=colors["grid"], gridWidth=0.6, domainColor=colors["grid"],
                            tickColor=colors["grid"]))


def main() -> None:
    st.set_page_config(page_title=text(st.session_state.get("lang", "es"), "page_title"), page_icon="💽",
                       layout="wide")
    colors = COLORS
    st.html(style())
    lang = language()
    alerts, history, line = load_alerts(), load_history(), threshold()
    variables = [c.removeprefix("shap_") for c in alerts.columns if c.startswith("shap_") and c != "shap_base"]

    st.html(f"<div class='hero'><div class='accent'></div><h1>{html.escape(text(lang, 'title'))}</h1>"
            f"<p>{html.escape(text(lang, 'intro'))}</p></div>")

    day = pick_day(lang)
    # Ordered by score; two drives with the same score, by serial number, so that the list is always the same
    day_alerts = (alerts[alerts["date"] == day].sort_values(["probability", "serial_number"], ascending=[False, True])
                  .reset_index(drop=True))
    earlier = int((alerts["date"] < day).sum())
    if day == FIRST_DAY:
        st.warning(text(lang, "first_day", day=day_label(day, lang), n=number(len(day_alerts), lang)), icon="⚡")

    with st.container(horizontal=True, horizontal_alignment="center", key="kpis", gap="large"):
        st.metric(text(lang, "metric_new"), number(len(day_alerts), lang), border=True, width=300)
        st.metric(text(lang, "metric_reviewed"), number(earlier, lang), help=text(lang, "metric_reviewed_help"),
                  border=True, width=300)
    with st.container(horizontal=True, horizontal_alignment="center", key="switch"):
        show_outcome = st.toggle(text(lang, "outcome_toggle"), value=False, help=text(lang, "outcome_help"))

    if day_alerts.empty:
        st.info(text(lang, "no_alerts"))
        return
    table, config = day_table(day_alerts, lang, show_outcome, line)
    # The chosen drive: a click on any cell of its row picks it (single-cell selection, without the column of
    # tick boxes) and the whole row is highlighted (Helena, 12 Nov). The row is also kept in the session,
    # in case the table's selection is reset when its colours change.
    key = f"list-{day}"
    cells = st.session_state[key].selection.cells if key in st.session_state else []
    if cells:
        st.session_state[f"row-{day}"] = cells[0][0]
    row = st.session_state.get(f"row-{day}", 0)
    with st.container(border=True, key="list_box"):
        title_day = day.strftime("%d/%m/%Y") if lang == "es" else day_label(day, lang)
        st.markdown(f"#### {text(lang, 'list_title', day=title_day)}")
        st.markdown(text(lang, "pick_hint"))  # in the text colour: grey captions read badly (Helena, 12 Nov)
        # The cells take the colour of the box, like the figures and the charts; the chosen row is shaded
        cells_style = {"background-color": BOXES["background"], "color": colors["ink"]}
        styled = table.style.set_properties(**cells_style).apply(
            lambda r: [f"background-color: {BOXES['selected']}; font-weight: 600" if r.name == row else ""] * len(r),
            axis=1)
        st.dataframe(styled, hide_index=True, on_select="rerun", selection_mode="single-cell", key=key,
                     column_config=config, height=min(420, 35 * (len(table) + 1) + 3), width="stretch")
    r = day_alerts.iloc[row]

    with st.container(key="drive_title"):
        st.subheader(text(lang, "drive", serial=r["serial_number"]))
    drive_facts(r, lang)
    if show_outcome:
        st.info(outcome(r["date"], r["failure_day"], r["last_day"], bool(r["is_episode"]), lang)[1])

    why, days = st.columns(2, gap="medium")
    with why, st.container(border=True, key="why_box", height="stretch"):
        st.markdown(f"#### {text(lang, 'why')}")
        st.html(why_table(r, variables, lang, colors))
    with days, st.container(border=True, key="history_box", height="stretch"):
        # The ⓘ says that the risk score goes from 0 to 1 and is not a probability (Helena, 13 Nov)
        st.markdown(f"#### {html.escape(text(lang, 'history'))}{tip(lang, 'history_tip', line=score(line, lang))}",
                    unsafe_allow_html=True)
        st.markdown(text(lang, "history_subtitle", line=score(line, lang)))
        life_history = history.loc[[(r["serial_number"], r["life"])]]
        dates = life_history["date"].dt.date
        if dates.min() < dates.max():  # the period of the chart, the whole one by default
            start, end = st.slider(text(lang, "range"), min_value=dates.min(), max_value=dates.max(),
                                   value=(dates.min(), dates.max()), key=f"range-{r['serial_number']}-{r['life']}",
                                   format="DD/MM/YYYY" if lang == "es" else "YYYY-MM-DD",
                                   label_visibility="collapsed")
            life_history = life_history[((dates >= start) & (dates <= end)).to_numpy()]
        failure_day = r["failure_day"] if show_outcome else None  # marked only if it falls inside the chart
        st.altair_chart(history_chart(life_history, r["date"], failure_day, line, lang, colors), width="stretch")

    with st.container(border=True, key="footer_box"):
        st.markdown(text(lang, "footer"))
        st.markdown(text(lang, "photo_credit"))


main()
