"""
ui_components.py — Gradio UI rendering helpers
Converted from Streamlit to Gradio
Maintains original theme & layout structure
"""

import gradio as gr


# ─────────────────────────────────────────────
# THEME CSS (Preserving Your Style)
# ─────────────────────────────────────────────

CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Epilogue:wght@300;400;500;600&display=swap');

body {
    background-color: #FAF7F2 !important;
    font-family: 'Epilogue', sans-serif !important;
    color: #1A1A18 !important;
}

.app-header {
    text-align: center;
    padding: 2rem 0;
}

.app-title {
    font-family: 'Playfair Display', serif;
    font-size: 3.2rem;
    font-weight: 900;
    color: #1A1A18;
}

.app-title em {
    color: #C4511A;
}

.app-subtitle {
    color: #8C8878;
    font-size: 1rem;
    font-weight: 300;
}

.section-header {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    margin-top: 2rem;
    border-bottom: 2px solid #1A1A18;
    padding-bottom: 0.5rem;
}

.metric-box {
    background: #F5F0E8;
    border: 1px solid #D4CEC2;
    padding: 1rem;
    border-radius: 12px;
    text-align: center;
}
"""


# ─────────────────────────────────────────────
# HEADER COMPONENT
# ─────────────────────────────────────────────

def render_header():
    gr.Markdown("""
    <div class="app-header">
        <div class="app-title">
            Personal <em>Fitness</em> Planner
        </div>
        <div class="app-subtitle">
            Machine learning meets nutrition science — built around you.
        </div>
    </div>
    """, elem_classes="app-header")


# ─────────────────────────────────────────────
# SECTION HEADER
# ─────────────────────────────────────────────

def render_section_header(title: str):
    gr.Markdown(
        f'<div class="section-header">{title}</div>',
        elem_classes="section-header"
    )


# ─────────────────────────────────────────────
# METRIC CARD COMPONENT
# ─────────────────────────────────────────────

def render_metric(label: str, value: str):
    return gr.Markdown(
        f"""
        <div class="metric-box">
            <strong>{label}</strong><br>
            <span style="font-size:1.5rem;">{value}</span>
        </div>
        """,
        elem_classes="metric-box"
    )
