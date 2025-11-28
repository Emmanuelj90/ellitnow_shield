# =====================================================================
#   ELLIT – PREDICTIVE INTELLIGENCE ENGINE
#   STANDARD & PRIME · Enterprise SaaS Module
#   Usa EllitCognitiveCore como cerebro único
# =====================================================================

import streamlit as st
from datetime import datetime

# ✅ SOLO se importa el wrapper, NUNCA engines internos
from core.cognitive_core import EllitCognitiveCore


# ============================================================
# SAFE CLIENT ACCESS
# ============================================================

def _get_client() -> EllitCognitiveCore:
    if "client" not in st.session_state:
        st.error("Motor cognitivo no inicializado.")
        st.stop()
    return st.session_state["client"]


# ============================================================
# UI HELPERS
# ============================================================

def _section(title: str, subtitle: str = ""):
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg,#123A6A 0%,#0B1F3A 100%);
            padding:18px;border-radius:16px;
            color:white;text-align:center;margin-bottom:22px;">
            <h2 style="margin:0;">{title}</h2>
            <p style="opacity:.85;margin:0;">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _info_box(text: str):
    st.markdown(
        f"""
        <div style="
            background:#F1F5F9;
            border-left:4px solid #7C1F5E;
            padding:14px;border-radius:8px;
            color:#0F172A;">
            {text}
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# PREDICTIVE STANDARD
# ============================================================

def render_predictive_standard():
    """
    Inteligencia predictiva básica
    Pensada para managers, risk owners y CISO operativo
    """
    _section(
        "Predictive Intelligence — Standard",
        "Riesgos, impactos y recomendaciones a corto y medio plazo"
    )

    client = _get_client()

    query = st.text_area(
        "Situación a analizar",
        placeholder=(
            "Ejemplo:\n"
            "- Incremento de incidentes de phishing\n"
            "- Cambio tecnológico crítico\n"
            "- Nueva obligación normativa\n"
            "- Dependencia de proveedor cloud"
        ),
        height=160,
    )

    col1, col2 = st.columns([1, 3])
    with col1:
        run = st.button("Generar predicción", type="primary")

    if run:
        if not query.strip():
            st.warning("Describe una situación real para analizar.")
            return

        with st.spinner("Ejecutando análisis predictivo…"):
            result = client.predict_standard(query)

        st.success("Predicción generada.")

        _info_box(result)

        st.markdown("---")

        st.caption(
            f"⏱ Generado el {datetime.now().strftime('%Y-%m-%d %H:%M')} · "
            "Ellit Cognitive Core"
        )


# ============================================================
# PREDICTIVE PRIME
# ============================================================

def render_predictive_prime():
    """
    Inteligencia predictiva avanzada
    Board-level · Horizon scanning · GeoRisk
    """
    _section(
        "Predictive Intelligence — PRIME",
        "Análisis avanzado con benchmark, alertas y horizonte estratégico"
    )

    client = _get_client()

    query = st.text_area(
        "Escenario estratégico a analizar",
        placeholder=(
            "Ejemplo:\n"
            "- Expansión internacional en LATAM\n"
            "- Dependencia crítica de proveedor SaaS\n"
            "- Riesgo geopolítico y cadena de suministro\n"
            "- Preparación ante NIS2 / DORA"
        ),
        height=160,
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        benchmark = st.checkbox("Benchmark sectorial", value=True)
    with c2:
        alerts = st.checkbox("Alertas globales", value=True)
    with c3:
        horizon = st.selectbox(
            "Horizonte temporal",
            ["30 días", "90 días", "6 meses", "12 meses"],
            index=1,
        )

    run = st.button("Generar inteligencia PRIME", type="primary")

    if run:
        if not query.strip():
            st.warning("Introduce un escenario estratégico.")
            return

        with st.spinner("Ejecutando inteligencia PRIME…"):
            result = client.predict_prime(
                query,
                benchmark=benchmark,
                alerts=alerts,
                horizon=horizon,
            )

        st.success("Inteligencia PRIME generada.")

        _info_box(result)

        st.markdown("---")

        st.caption(
            f"🧠 Análisis PRIME · {horizon} · "
            f"{datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )


# ============================================================
# BACKWARD COMPATIBILITY (NO TOCAR)
# ============================================================

# Estas funciones existen para no romper app.py ni el router

def render_predictive():
    render_predictive_standard()

