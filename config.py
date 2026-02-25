"""config.py — App configuration and global CSS."""

from dataclasses import dataclass


@dataclass
class _AppConfig:
    APP_NAME: str = "AI Fitness Planner"
    VERSION: str = "1.0.0"
    MODEL_DIR: str = "."


@dataclass
class _StyleConfig:
    CSS: str = """
<style>
/* ── Google Fonts ─────────────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,400;1,700&family=Epilogue:wght@300;400;500;600&family=Roboto+Mono:wght@400;500&display=swap');

/* ── Design Tokens ────────────────────────────────────────────────────────── */
:root {
    --cream:       #F5F0E8;
    --cream-dark:  #EDE6D6;
    --paper:       #FAF7F2;
    --ink:         #1A1A18;
    --ink-light:   #3D3D38;
    --ink-muted:   #8C8878;
    --rust:        #C4511A;
    --rust-light:  #E8673A;
    --sage:        #4A6741;
    --gold:        #B8963E;
    --border:      #D4CEC2;
    --border-dark: #B8B2A4;

    --font-display: 'Playfair Display', Georgia, serif;
    --font-body:    'Epilogue', sans-serif;
    --font-mono:    'Roboto Mono', monospace;

    --radius-sm:  6px;
    --radius-md:  12px;
    --radius-lg:  20px;
    --shadow-sm:  0 1px 4px rgba(26,26,24,0.08);
    --shadow-md:  0 4px 20px rgba(26,26,24,0.10);
    --shadow-lg:  0 8px 40px rgba(26,26,24,0.14);
}

/* ── Global Reset ─────────────────────────────────────────────────────────── */
html, body, [class*="css"] {
    background-color: var(--paper) !important;
    color: var(--ink) !important;
    font-family: var(--font-body) !important;
}

/* ── Animated background texture ─────────────────────────────────────────── */
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse at 10% 20%, rgba(196,81,26,0.04) 0%, transparent 50%),
        radial-gradient(ellipse at 90% 80%, rgba(74,103,65,0.04) 0%, transparent 50%),
        var(--paper) !important;
}

/* ── Sidebar ──────────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: var(--cream) !important;
    border-right: 2px solid var(--border) !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding-top: 2rem !important;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stNumberInput label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stTextArea label {
    color: var(--ink-muted) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.70rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
    font-weight: 500 !important;
}
[data-testid="stSidebar"] .stSelectbox > div,
[data-testid="stSidebar"] .stNumberInput > div input {
    background: var(--paper) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--ink) !important;
}

/* ── App Header ───────────────────────────────────────────────────────────── */
.app-header {
    padding: 3rem 0 2.5rem;
    text-align: center;
    position: relative;
    margin-bottom: 0.5rem;
}
.app-header-rule {
    width: 100%;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border-dark), transparent);
    margin: 1.5rem 0;
}
.app-kicker {
    font-family: var(--font-mono) !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.25em !important;
    color: var(--rust) !important;
    text-transform: uppercase !important;
    margin-bottom: 0.8rem !important;
    display: block;
}
.app-title {
    font-family: var(--font-display) !important;
    font-size: 4rem !important;
    font-weight: 900 !important;
    color: var(--ink) !important;
    line-height: 1.0 !important;
    letter-spacing: -0.02em !important;
    margin: 0 !important;
}
.app-title em {
    font-style: italic !important;
    color: var(--rust) !important;
}
.app-tagline {
    font-family: var(--font-body) !important;
    font-size: 1rem !important;
    color: var(--ink-muted) !important;
    font-weight: 300 !important;
    margin-top: 0.8rem !important;
    letter-spacing: 0.02em !important;
}

/* ── Landing Hero ─────────────────────────────────────────────────────────── */
.landing-hero {
    padding: 5rem 2rem 3rem;
    text-align: center;
}
.hero-title {
    font-family: var(--font-display) !important;
    font-size: 2.8rem !important;
    font-weight: 700 !important;
    color: var(--ink) !important;
    line-height: 1.15 !important;
}
.hero-title em { color: var(--rust) !important; font-style: italic !important; }
.hero-sub {
    color: var(--ink-muted) !important;
    font-size: 1.05rem !important;
    max-width: 520px !important;
    margin: 1.2rem auto 0 !important;
    line-height: 1.7 !important;
    font-weight: 300 !important;
}

/* ── Feature Cards ────────────────────────────────────────────────────────── */
.feature-card {
    background: var(--cream);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 2rem 1.6rem;
    text-align: left;
    position: relative;
    overflow: hidden;
    box-shadow: var(--shadow-sm);
    transition: box-shadow 0.3s, transform 0.3s;
}
.feature-card:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-2px);
}
.feature-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--rust), var(--gold));
}
.feature-icon {
    font-size: 1.8rem;
    margin-bottom: 1rem;
    display: block;
}
.feature-card h3 {
    font-family: var(--font-display) !important;
    font-size: 1.2rem !important;
    font-weight: 700 !important;
    color: var(--ink) !important;
    margin: 0 0 0.5rem !important;
}
.feature-card p {
    color: var(--ink-muted) !important;
    font-size: 0.88rem !important;
    line-height: 1.65 !important;
    font-weight: 300 !important;
}

/* ── Metric Cards ─────────────────────────────────────────────────────────── */
.metric-card {
    background: var(--cream);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 1.6rem 1.5rem;
    box-shadow: var(--shadow-sm);
    position: relative;
}
.metric-card.rust  { border-top: 3px solid var(--rust); }
.metric-card.sage  { border-top: 3px solid var(--sage); }
.metric-card.gold  { border-top: 3px solid var(--gold); }
.metric-card.plain { border-top: 3px solid var(--ink-light); }

.metric-label {
    font-family: var(--font-mono) !important;
    font-size: 0.68rem !important;
    color: var(--ink-muted) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.15em !important;
    display: block;
    margin-bottom: 0.4rem;
}
.metric-value {
    font-family: var(--font-display) !important;
    font-size: 3rem !important;
    font-weight: 900 !important;
    line-height: 1 !important;
    color: var(--ink) !important;
    display: block;
}
.metric-value.rust { color: var(--rust) !important; }
.metric-value.sage { color: var(--sage) !important; }
.metric-value.gold { color: var(--gold) !important; }
.metric-unit {
    font-family: var(--font-body) !important;
    font-size: 0.80rem !important;
    color: var(--ink-muted) !important;
    margin-top: 0.3rem !important;
    display: block;
    font-weight: 300;
}

/* ── Fitness Badge ────────────────────────────────────────────────────────── */
.fitness-badge {
    display: inline-block;
    background: var(--ink);
    color: var(--cream) !important;
    font-family: var(--font-display) !important;
    font-size: 0.9rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.05em !important;
    padding: 0.35rem 1rem;
    border-radius: 3px;
}

/* ── Section Headers ──────────────────────────────────────────────────────── */
.section-header {
    font-family: var(--font-display) !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
    color: var(--ink) !important;
    padding-bottom: 0.8rem;
    margin-bottom: 1.5rem !important;
    border-bottom: 2px solid var(--ink);
    display: flex;
    align-items: baseline;
    gap: 0.6rem;
}
.section-header-sub {
    font-family: var(--font-body) !important;
    font-size: 0.85rem !important;
    color: var(--ink-muted) !important;
    font-weight: 300 !important;
    font-style: italic !important;
    margin-left: auto;
}

/* ── Info Box ─────────────────────────────────────────────────────────────── */
.info-box {
    background: var(--cream-dark);
    border: 1px solid var(--border);
    border-left: 4px solid var(--rust);
    border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
    padding: 0.9rem 1.2rem;
    margin: 1rem 0;
    font-size: 0.9rem;
    color: var(--ink-light) !important;
    line-height: 1.6;
}

/* ── NLP Note ─────────────────────────────────────────────────────────────── */
.nlp-note {
    background: rgba(184,150,62,0.08);
    border: 1px solid rgba(184,150,62,0.30);
    border-radius: var(--radius-sm);
    padding: 0.75rem 1rem;
    margin: 0.4rem 0;
    font-size: 0.88rem;
    color: var(--ink-light) !important;
    line-height: 1.6;
}

/* ── Workout Day Card ─────────────────────────────────────────────────────── */
.day-card {
    background: var(--paper);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    box-shadow: var(--shadow-sm);
    transition: box-shadow 0.25s, border-color 0.25s;
}
.day-card:hover {
    box-shadow: var(--shadow-md);
    border-color: var(--border-dark);
}
.day-card.rest-day {
    background: var(--cream);
    opacity: 0.7;
}
.day-title {
    font-family: var(--font-display) !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    color: var(--ink) !important;
    margin-bottom: 1rem !important;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.day-focus-tag {
    font-family: var(--font-mono) !important;
    font-size: 0.68rem !important;
    background: var(--rust) !important;
    color: white !important;
    padding: 0.2rem 0.6rem;
    border-radius: 3px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-left: auto;
}
.day-focus-tag.rest { background: var(--ink-muted) !important; }

.exercise-row {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    padding: 0.45rem 0;
    border-bottom: 1px dashed var(--border);
    font-size: 0.88rem;
}
.exercise-row:last-child { border-bottom: none; }
.ex-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--rust);
    flex-shrink: 0;
}
.ex-name {
    flex: 2;
    color: var(--ink) !important;
    font-weight: 500;
}
.ex-sets {
    flex: 1;
    color: var(--rust) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.80rem !important;
    font-weight: 500;
}
.ex-muscle {
    flex: 2;
    color: var(--ink-muted) !important;
    font-size: 0.80rem !important;
    font-style: italic;
}
.day-note {
    margin-top: 0.8rem;
    font-size: 0.80rem;
    color: var(--ink-muted);
    line-height: 1.5;
    padding-top: 0.6rem;
    border-top: 1px solid var(--border);
    font-style: italic;
}

/* ── Meal Card ────────────────────────────────────────────────────────────── */
.meal-card {
    background: var(--paper);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 1.3rem 1.5rem;
    margin-bottom: 0.8rem;
    box-shadow: var(--shadow-sm);
    transition: box-shadow 0.2s;
}
.meal-card:hover { box-shadow: var(--shadow-md); }
.meal-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 0.6rem;
}
.meal-title {
    font-family: var(--font-mono) !important;
    font-size: 0.70rem !important;
    color: var(--rust) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
    font-weight: 500 !important;
}
.meal-calories {
    font-family: var(--font-display) !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    color: var(--ink) !important;
}
.meal-calories span {
    font-family: var(--font-body) !important;
    font-size: 0.72rem !important;
    font-weight: 300 !important;
    color: var(--ink-muted) !important;
}
.meal-item {
    font-size: 0.92rem;
    color: var(--ink-light);
    line-height: 1.5;
    margin-bottom: 0.8rem;
}
.meal-macros {
    display: flex;
    gap: 1rem;
    padding-top: 0.6rem;
    border-top: 1px dashed var(--border);
}
.macro-pill {
    font-family: var(--font-mono) !important;
    font-size: 0.72rem !important;
    color: var(--ink-muted) !important;
}
.macro-pill b {
    color: var(--ink-light) !important;
    font-weight: 500 !important;
}

/* ── Tabs ─────────────────────────────────────────────────────────────────── */
[data-testid="stTabs"] [role="tablist"] {
    border-bottom: 2px solid var(--border-dark) !important;
    gap: 0 !important;
    background: transparent !important;
}
[data-testid="stTabs"] [role="tab"] {
    font-family: var(--font-mono) !important;
    font-size: 0.72rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
    color: var(--ink-muted) !important;
    background: transparent !important;
    border: none !important;
    border-bottom: 3px solid transparent !important;
    border-radius: 0 !important;
    padding: 0.7rem 1.2rem !important;
    transition: color 0.2s, border-color 0.2s !important;
    margin-bottom: -2px !important;
}
[data-testid="stTabs"] [role="tab"]:hover {
    color: var(--rust) !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: var(--ink) !important;
    border-bottom-color: var(--rust) !important;
    font-weight: 600 !important;
}

/* ── Primary Button ───────────────────────────────────────────────────────── */
.stButton > button[kind="primary"] {
    background: var(--ink) !important;
    color: var(--cream) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    border: 2px solid var(--ink) !important;
    border-radius: var(--radius-sm) !important;
    padding: 0.7rem 1.8rem !important;
    transition: background 0.2s, color 0.2s !important;
    box-shadow: none !important;
}
.stButton > button[kind="primary"]:hover {
    background: var(--rust) !important;
    border-color: var(--rust) !important;
    color: white !important;
}

/* ── Divider ──────────────────────────────────────────────────────────────── */
hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 1.5rem 0 !important;
}

/* ── Streamlit metric overrides ──────────────────────────────────────────── */
[data-testid="stMetric"] {
    background: var(--cream);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 1rem 1.2rem !important;
}
[data-testid="stMetricLabel"] {
    font-family: var(--font-mono) !important;
    font-size: 0.68rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
    color: var(--ink-muted) !important;
}
[data-testid="stMetricValue"] {
    font-family: var(--font-display) !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    color: var(--ink) !important;
}
[data-testid="stMetricDelta"] {
    font-family: var(--font-mono) !important;
    font-size: 0.75rem !important;
}

/* ── Dataframe ────────────────────────────────────────────────────────────── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    overflow: hidden !important;
}

/* ── Expander ─────────────────────────────────────────────────────────────── */
[data-testid="stExpander"] {
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    background: var(--cream) !important;
}
[data-testid="stExpander"] summary {
    font-family: var(--font-body) !important;
    font-weight: 500 !important;
    color: var(--ink) !important;
}

/* ── Scrollbar ────────────────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--cream); }
::-webkit-scrollbar-thumb { background: var(--border-dark); border-radius: 3px; }

/* ── Plotly override ──────────────────────────────────────────────────────── */
.js-plotly-plot .plotly, .plot-container { background: transparent !important; }
</style>
"""


APP_CONFIG = _AppConfig()
STYLE_CONFIG = _StyleConfig()
