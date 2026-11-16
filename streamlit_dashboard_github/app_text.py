"""Texts of the Streamlit app in Spanish and English, and how each language writes numbers and dates.

The app is in both languages, with a switch at the top, Spanish by default. Spanish writes 1.254 and 0,83;
English writes 1,254 and 0.83.

It is part of the published app (streamlit_dashboard_github/), so it imports nothing from the project's package;
the project's notebooks and tests read the variable names from here, so that they say the same as the app.
"""

import math
from datetime import date

# Fixed in v1 and copied here so that the app needs only its own folder: the horizon of the label (gold.H) and the
# last day of the data (the end of the test period). tests/test_dashboard.py checks that they match the project.
H = 15
DATA_END = date(2026, 6, 30)

LANGUAGES = {"es": "🇪🇸 Español", "en": "🇬🇧 English"}

# Names of the S.M.A.R.T. attributes the model uses (the 39 that have data in training).
# 27, 71 and 90 have no standard meaning: each manufacturer uses them for its own purposes.
ATTRIBUTES = {
    1: ("Tasa de errores de lectura", "Read error rate"),
    2: ("Rendimiento de transferencia", "Throughput performance"),
    3: ("Tiempo de arranque", "Spin-up time"),
    4: ("Arranques y paradas", "Start/stop count"),
    5: ("Sectores reasignados", "Reallocated sectors"),
    7: ("Tasa de errores de búsqueda", "Seek error rate"),
    8: ("Rendimiento de búsqueda", "Seek time performance"),
    9: ("Horas encendido", "Power-on hours"),
    10: ("Reintentos de arranque", "Spin retry count"),
    11: ("Reintentos de calibración", "Calibration retry count"),
    12: ("Ciclos de encendido", "Power cycle count"),
    22: ("Nivel de helio", "Helium level"),
    27: ("Propio del fabricante", "Vendor specific"),
    71: ("Propio del fabricante", "Vendor specific"),
    90: ("Propio del fabricante", "Vendor specific"),
    183: ("Bajadas de velocidad SATA", "SATA downshift errors"),
    184: ("Errores de extremo a extremo", "End-to-end errors"),
    187: ("Errores no corregibles", "Reported uncorrectable errors"),
    188: ("Órdenes caducadas", "Command timeouts"),
    189: ("Escrituras con el cabezal alto", "High fly writes"),
    190: ("Temperatura del aire", "Airflow temperature"),
    191: ("Golpes y vibraciones", "G-sense error rate"),
    192: ("Retracciones por apagado", "Power-off retract count"),
    193: ("Ciclos de carga del cabezal", "Load/unload cycles"),
    194: ("Temperatura", "Temperature"),
    195: ("Errores corregidos por ECC", "Hardware ECC recovered"),
    196: ("Eventos de reasignación", "Reallocation events"),
    197: ("Sectores pendientes", "Current pending sectors"),
    198: ("Sectores ilegibles", "Offline uncorrectable sectors"),
    199: ("Errores CRC de la conexión", "UDMA CRC errors"),
    200: ("Errores de escritura multizona", "Multi-zone error rate"),
    220: ("Desplazamiento del disco", "Disk shift"),
    222: ("Horas con el cabezal cargado", "Loaded hours"),
    223: ("Reintentos de carga del cabezal", "Load/unload retries"),
    225: ("Ciclos de carga y descarga", "Load/unload cycle count"),
    226: ("Tiempo de carga del cabezal", "Load-in time"),
    240: ("Horas de vuelo del cabezal", "Head flying hours"),
    241: ("Datos escritos", "Total LBAs written"),
    242: ("Datos leídos", "Total LBAs read"),
}
# The three variables of each attribute: today's value, its change in 7 days and in 30 days.
KINDS = {
    "raw": ("valor del día", "value that day"),
    "raw_d7": ("cambio en 7 días", "7-day change"),
    "raw_d30": ("cambio en 30 días", "30-day change"),
    "normalized": ("normalizado, valor del día", "normalized, value that day"),
    "normalized_d7": ("normalizado, cambio en 7 días", "normalized, 7-day change"),
    "normalized_d30": ("normalizado, cambio en 30 días", "normalized, 30-day change"),
}
OTHER_VARIABLES = {
    "life": ("Vida del disco", "Drive life"),
    "drive_model": ("Modelo de disco", "Drive model"),
    "manufacturer": ("Marca", "Manufacturer"),
    "is_boot_drive": ("Disco de arranque", "Boot drive"),
    "capacity_tb": ("Capacidad", "Capacity"),
    "smart_reset": ("Contadores reiniciados", "Counters reset"),
    "physical_age_hours": ("Edad física", "Physical age"),
    "days_since_reinstall": ("Días desde la reinstalación", "Days since reinstall"),
}

MONTHS = {
    "es": ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"],
    "en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
}

TEXT = {
    "es": {
        "page_title": "Alerta temprana · Discos duros",
        "title": "Alerta temprana de discos duros",
        "intro": "Predicción de fallos en la flota de Backblaze: los discos con riesgo de fallar en los "
                 "próximos 15 días, según un modelo LightGBM.",
        "day": "Día",
        "day_help": "La app hace como si hoy fuera el día elegido. Jul – dic 2025 es el periodo de validación "
                    "(con él se eligió la raya de aviso); ene – jun 2026, el de prueba (no se usó para decidir "
                    "nada). El modelo no se entrenó con ninguno de los dos. Termina el 15 de junio: de los últimos "
                    "15 días de datos no se sabe qué pasó después.",
        "previous": "← Día anterior",
        "next": "Día siguiente →",
        "first_day": "**{day} · Arranque del sistema.** Entran de golpe los {n} discos que ya estaban por "
                     "encima de la raya; desde mañana, solo los avisos nuevos de cada día.",
        "metric_new": "Avisos nuevos hoy",
        "metric_reviewed": "Avisos anteriores, ya revisados",
        "metric_reviewed_help": "Cada disco entra en la lista una sola vez, el día que cruza la raya. Los de "
                                "días anteriores se dan por revisados y no vuelven, aunque su nota siga alta.",
        "outcome_toggle": "Mostrar qué pasó después",
        "outcome_help": "Lo que el técnico no sabría ese día: si el disco falló de verdad, y cuándo.",
        "col_rank": "#",
        "col_drive": "Disco",
        "col_model": "Modelo",
        "col_capacity": "Capacidad",
        "col_age": "Edad",
        "col_score": "Nota de riesgo",
        "col_score_help": "Nota de riesgo de fallar en los próximos 15 días, de 0 a 1, según el modelo. Sirve "
                          "para ordenar los discos: no es una probabilidad. La raya de aviso está en {line}.",
        "col_rise": "Subida desde ayer",
        "col_rise_help": "Cuánto ha subido la nota de riesgo respecto a ayer. «—» si el disco no informó ayer.",
        "col_outcome": "Qué pasó después",
        "col_outcome_help": "✓: falló dentro de los 15 días siguientes al aviso, el horizonte del modelo.",
        "no_alerts": "Hoy ningún disco cruza la raya por primera vez.",
        "drive": "Disco seleccionado: {serial}",
        "list_title": "Discos duros que entran en alerta el {day}",
        "pick_hint": "Selecciona un disco duro en la tabla para ver su ficha, por qué ha entrado y su nota de riesgo "
                     "día a día.",
        "range": "Periodo de la gráfica",
        "fact_model": "🏷️ Modelo",
        "fact_manufacturer": "🏭 Marca",
        "fact_capacity": "💾 Capacidad",
        "fact_age": "🕒 Años en funcionamiento",
        "fact_age_help": "Horas que lleva encendido, en años, contando las de vidas anteriores si sus contadores "
                         "se reiniciaron.",
        "fact_life": "♻️ Vida nº",
        "fact_life_help": "Un disco que vuelve a la flota tras un fallo empieza una vida nueva: 1 es la primera.",
        "fact_score": "📈 Nota de riesgo",
        "fact_score_help": "Nota de riesgo de fallar en los próximos 15 días, de 0 a 1, según el modelo, el día "
                           "del aviso.",
        "why_number": "Nº",
        "why_number_tip": "Número del atributo S.M.A.R.T. Cada disco informa a diario de decenas de contadores "
                          "sobre su estado (sectores dañados, errores, temperatura…), y cada uno tiene un número. "
                          "Son columnas de los datos diarios que publica Backblaze. Las filas sin número son otros "
                          "datos del disco, como su modelo o su edad.",
        "why_attribute": "Atributo",
        "why_attribute_tip": "Qué mide ese contador, según el estándar S.M.A.R.T. (algunos números no tienen un "
                             "significado estándar y cada fabricante los usa a su manera). Debajo, qué se mira de "
                             "él: el valor del día, lo que marca el contador el día del aviso, o su cambio en 7 o "
                             "en 30 días, cuánto ha cambiado respecto a 7 o 30 días antes.",
        "why_weight": "Peso en la nota",
        "why_weight_tip": "Cuánto pesa cada dato en la nota de este disco, en % del total de todos los datos: en "
                          "rosa, lo que la sube; en azul, lo que la baja. Sale de SHAP, que reparte la nota del "
                          "modelo entre los datos.",
        "why_value": "Valor",
        "history_subtitle": "La línea rosa discontinua es la raya de aviso ({line}): el disco entra en la lista "
                            "el primer día que su nota de riesgo la cruza. La nota empieza en julio de 2025: los "
                            "datos anteriores sirvieron para entrenar el modelo.",
        "why": "Por qué ha entrado en la lista",
        "history": "Su nota de riesgo día a día",
        "history_tip": "La nota de riesgo va de 0 a 1: cuanto más alta, más riesgo de que el disco falle en los "
                       "próximos 15 días. La raya de aviso, {line}, se fijó en validación: es la nota con la que el "
                       "modelo detecta los mismos fallos que la regla que usaría hoy un técnico, con un 55 % menos "
                       "de falsas alarmas.",
        "score": "Nota de riesgo (de 0 a 1)",
        "date": "Fecha",
        "alert_mark": "aviso",
        "failure_mark": "fallo",
        "line_label": "Raya de aviso · {line}",
        "footer": "Proyecto personal con fines de formación y aprendizaje. Datos: Backblaze Drive Stats.",
        "photo_credit": "Foto de la cabecera: [StoragePod](https://commons.wikimedia.org/wiki/File:StoragePod.jpg), "
                        "de ChrisDag (Wikimedia Commons), con licencia "
                        "[CC BY 2.0](https://creativecommons.org/licenses/by/2.0/); recortada y oscurecida.",
        "years": "{n} años",
        "empty": "vacío",
        "yes": "sí",
        "no": "no",
        "out_failed": "Falló a los {n} días",
        "out_failed_same_day": "Falló ese mismo día",
        "out_running": "Sin fallo, sigue en jun 2026",
        "out_retired": "Retirado sin fallo",
        "out_episode": "Retirado (episodio del MG08)",
        "out_unknown": "Sin datos suficientes",
        "detail_failed_in": "Falló el {day}, {n} días después del aviso: dentro de los 15 días, un acierto.",
        "detail_failed_same_day": "Falló el mismo día del aviso, {day}: un acierto, aunque sin margen para actuar.",
        "detail_failed_late": "Falló el {day}, {n} días después del aviso: más tarde de los 15 días del horizonte.",
        "detail_running": "No falló: seguía en la flota al final de los datos ({day}).",
        "detail_retired": "No falló: se retiró el {day}, sin fallo.",
        "detail_episode": "Se retiró el {day} en el episodio del MG08ACA16TEY, que cuenta como retirado sin fallo.",
        "detail_unknown": "No se sabe: los datos terminan el {day}, menos de 15 días después del aviso.",
    },
    "en": {
        "page_title": "Early warning · Hard drives",
        "title": "Hard drive early warning",
        "intro": "Failure prediction for the Backblaze fleet: the drives at risk of failing in the next "
                 "15 days, according to a LightGBM model.",
        "day": "Day",
        "day_help": "The app acts as if today were the chosen day. Jul – Dec 2025 is the validation period "
                    "(it was used to choose the alert line); Jan – Jun 2026, the test period (not used to "
                    "decide anything). The model was trained on neither. It ends on 15 June: for the last 15 days "
                    "of the data, what happened next is unknown.",
        "previous": "← Previous day",
        "next": "Next day →",
        "first_day": "**{day} · System start-up.** The {n} drives already above the line come in at once; "
                     "from tomorrow on, only each day's new alerts.",
        "metric_new": "New alerts today",
        "metric_reviewed": "Earlier alerts, already reviewed",
        "metric_reviewed_help": "Each drive enters the list once, on the day it crosses the line. Those from "
                                "earlier days are taken as reviewed and do not come back, even if their score "
                                "stays high.",
        "outcome_toggle": "Show what happened next",
        "outcome_help": "What the technician would not know that day: whether the drive really failed, and when.",
        "col_rank": "#",
        "col_drive": "Drive",
        "col_model": "Model",
        "col_capacity": "Capacity",
        "col_age": "Age",
        "col_score": "Risk score",
        "col_score_help": "Risk score of failing in the next 15 days, from 0 to 1, according to the model. It "
                          "ranks the drives: it is not a probability. The alert line is at {line}.",
        "col_rise": "Rise since yesterday",
        "col_rise_help": "How much the risk score rose since yesterday. \"—\" if the drive did not report "
                         "yesterday.",
        "col_outcome": "What happened next",
        "col_outcome_help": "✓: it failed within the 15 days after the alert, the model's horizon.",
        "no_alerts": "No drive crosses the line for the first time today.",
        "drive": "Selected drive: {serial}",
        "list_title": "Hard drives flagged on {day}",
        "pick_hint": "Select a hard drive in the table to see its details, why it is on the list and its daily "
                     "risk score.",
        "range": "Chart period",
        "fact_model": "🏷️ Model",
        "fact_manufacturer": "🏭 Manufacturer",
        "fact_capacity": "💾 Capacity",
        "fact_age": "🕒 Years in service",
        "fact_age_help": "Hours it has been powered on, in years, counting those of earlier lives if its counters "
                         "were reset.",
        "fact_life": "♻️ Life no.",
        "fact_life_help": "A drive that comes back to the fleet after a failure starts a new life: 1 is the first.",
        "fact_score": "📈 Risk score",
        "fact_score_help": "Risk score of failing in the next 15 days, from 0 to 1, according to the model, on the "
                           "alert.",
        "why_number": "No.",
        "why_number_tip": "Number of the S.M.A.R.T. attribute. Every drive reports dozens of counters about its "
                          "health every day (bad sectors, errors, temperature…), each with a number. They are "
                          "columns of the daily data Backblaze publishes. Rows without a number are other facts "
                          "about the drive, such as its model or age.",
        "why_attribute": "Attribute",
        "why_attribute_tip": "What that counter measures, according to the S.M.A.R.T. standard (some numbers have "
                             "no standard meaning and each manufacturer uses them its own way). Below, what is "
                             "looked at: the value that day, what the counter shows on the day of the alert, or its "
                             "7- or 30-day change, how much it changed since 7 or 30 days before.",
        "why_weight": "Weight in the score",
        "why_weight_tip": "How much each fact weighs in this drive's score, as a % of the total over all facts: in "
                          "pink, what raises it; in blue, what lowers it. It comes from SHAP, which splits the "
                          "model's score among the facts.",
        "why_value": "Value",
        "history_subtitle": "The pink dashed line is the alert line ({line}): a drive enters the list on the first "
                            "day its risk score crosses it. The score starts in July 2025: earlier data trained "
                            "the model.",
        "why": "Why it is on the list",
        "history": "Its risk score day by day",
        "history_tip": "The risk score goes from 0 to 1: the higher it is, the higher the risk that the drive "
                       "fails in the next 15 days. The alert line, {line}, was fixed on validation: it is the score "
                       "at which the model detects as many failures as the rule a technician would use today, with "
                       "55 % fewer false alarms.",
        "score": "Risk score (0 to 1)",
        "date": "Date",
        "alert_mark": "alert",
        "failure_mark": "failure",
        "line_label": "Alert line · {line}",
        "footer": "Personal project for training and learning purposes. Data: Backblaze Drive Stats.",
        "photo_credit": "Header photo: [StoragePod](https://commons.wikimedia.org/wiki/File:StoragePod.jpg) by "
                        "ChrisDag (Wikimedia Commons), licensed under "
                        "[CC BY 2.0](https://creativecommons.org/licenses/by/2.0/); cropped and darkened.",
        "years": "{n} years",
        "empty": "empty",
        "yes": "yes",
        "no": "no",
        "out_failed": "Failed after {n} days",
        "out_failed_same_day": "Failed the same day",
        "out_running": "No failure, still running in Jun 2026",
        "out_retired": "Retired without failure",
        "out_episode": "Retired (MG08 episode)",
        "out_unknown": "Not enough data",
        "detail_failed_in": "It failed on {day}, {n} days after the alert: within the 15 days, a hit.",
        "detail_failed_same_day": "It failed on the day of the alert, {day}: a hit, but with no time to act.",
        "detail_failed_late": "It failed on {day}, {n} days after the alert: later than the model's 15-day horizon.",
        "detail_running": "No failure: it was still in the fleet at the end of the data ({day}).",
        "detail_retired": "No failure: it was retired on {day}, without failing.",
        "detail_episode": "It was retired on {day} in the MG08ACA16TEY episode, which counts as retired without "
                          "failure.",
        "detail_unknown": "Unknown: the data end on {day}, less than 15 days after the alert.",
    },
}
assert TEXT["es"].keys() == TEXT["en"].keys(), "every text needs both languages"

# The last day of the data (30 Jun 2026): a life whose last day is this one was still running.


def text(lang: str, key: str, **values) -> str:
    """A text of the app in one language, with its placeholders filled in."""
    return TEXT[lang][key].format(**values)


def number(x: float, lang: str, decimals: int = 0, sign: bool = False) -> str:
    """A number written the way each language writes it: 1.254,5 in Spanish, 1,254.5 in English."""
    s = f"{x:+,.{decimals}f}" if sign else f"{x:,.{decimals}f}"
    if lang == "es":
        s = s.replace(",", "\0").replace(".", ",").replace("\0", ".")
    return s


def score(p: float, lang: str) -> str:
    """A risk score from 0 to 1 with three decimals: 0,934 in Spanish, 0.934 in English. It is shown from 0 to 1,
    not as a percentage, because it is not a calibrated probability; three decimals because
    the scores of the list go from 0.834 to 0.996, and with two, 85 % of the alerts would tie with another
    one of the same day."""
    return number(p, lang, 3)


def day_label(d: date, lang: str) -> str:
    """A date with the month in letters, unambiguous in both languages: 12 ago 2025, 12 Aug 2025."""
    return f"{d.day} {MONTHS[lang][d.month - 1]} {d.year}"


def years(hours: float, lang: str) -> str:
    """An age in hours, written in years with one decimal."""
    return text(lang, "years", n=number(hours / 24 / 365.25, lang, 1))


def variable_label(name: str, lang: str) -> str:
    """Readable name of a model variable: "197 Sectores pendientes · cambio en 30 días"."""
    i = 0 if lang == "es" else 1
    if name in OTHER_VARIABLES:
        return OTHER_VARIABLES[name][i]
    if name.startswith("smart_"):
        attribute, kind = name.removeprefix("smart_").split("_", 1)
        if attribute.isdigit() and int(attribute) in ATTRIBUTES and kind in KINDS:
            return f"{attribute} {ATTRIBUTES[int(attribute)][i]} · {KINDS[kind][i]}"
    return name


def variable_parts(name: str, lang: str) -> tuple[str, str, str]:
    """A model variable split for the table of why a drive is on the list: the attribute number (empty
    for variables that are not S.M.A.R.T. attributes), its name and what is measured of it."""
    i = 0 if lang == "es" else 1
    if name.startswith("smart_"):
        attribute, kind = name.removeprefix("smart_").split("_", 1)
        if attribute.isdigit() and int(attribute) in ATTRIBUTES and kind in KINDS:
            return attribute, ATTRIBUTES[int(attribute)][i], KINDS[kind][i].capitalize()
    return "", OTHER_VARIABLES.get(name, (name, name))[i], ""


def variable_value(name: str, value, lang: str) -> str:
    """The value of a model variable, written for the app: empty values (attributes a manufacturer does
    not report) say so, ages go in years and capacities in TB."""
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return text(lang, "empty")
    if isinstance(value, bool):
        return text(lang, "yes" if value else "no")
    if isinstance(value, str):
        return value
    if name == "physical_age_hours":
        return years(value, lang)
    if name == "capacity_tb":  # 8.0016 TB of the drive model is an 8 TB drive
        return number(value, lang, 0 if abs(value - round(value)) < 0.05 else 1) + " TB"
    change = name.endswith(("_d7", "_d30")) and value != 0  # changes carry their sign: +24, -3; no change is 0
    if float(value).is_integer():
        return number(value, lang, 0, sign=change)
    return number(value, lang, 2, sign=change)


def outcome(alert_day: date, failure_day: date | None, last_day: date, is_episode: bool,
            lang: str) -> tuple[str, str]:
    """What happened to an alerted life after its alert: a short text for the list and a sentence for
    the detail. A failure within the horizon (the 15 days after the alert) is a hit, marked with ✓."""
    if failure_day is not None:
        n = (failure_day - alert_day).days
        day = day_label(failure_day, lang)
        if n == 0:
            return text(lang, "out_failed_same_day") + " ✓", text(lang, "detail_failed_same_day", day=day)
        if n <= H:
            return text(lang, "out_failed", n=n) + " ✓", text(lang, "detail_failed_in", day=day, n=n)
        return text(lang, "out_failed", n=number(n, lang)), text(lang, "detail_failed_late", day=day,
                                                                  n=number(n, lang))
    day = day_label(last_day, lang)
    if is_episode:
        return text(lang, "out_episode"), text(lang, "detail_episode", day=day)
    if last_day >= DATA_END and (DATA_END - alert_day).days < H:  # the data end before the horizon does
        return text(lang, "out_unknown"), text(lang, "detail_unknown", day=day)
    if last_day >= DATA_END:
        return text(lang, "out_running"), text(lang, "detail_running", day=day)
    return text(lang, "out_retired"), text(lang, "detail_retired", day=day)
