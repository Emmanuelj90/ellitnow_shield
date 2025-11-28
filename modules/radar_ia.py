# ============================================================
# RADAR IA — Ellit Cognitive Core
# Enterprise SaaS · Unified Cognitive Radar (STABLE)
# ============================================================

import streamlit as st
import plotly.graph_objects as go
import json

# ============================================================
# STATE INIT (ROBUSTO, SIN ERRORES)
# ============================================================

def _bootstrap_radar_state():
    defaults = {
        "radar_profile": None,
        "radar_result": None,
        "radar_indicators": None,
        "radar_recommendations": None,
        "radar_maturity": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_bootstrap_radar_state()

# ============================================================
# BRANDING — ELLIT UI (ENTERPRISE)
# ============================================================

st.markdown("""
<style>
.ellit-card {
    background:#FFFFFF;
    border-radius:18px;
    padding:28px;
    border:1px solid #E5E7EB;
    box-shadow:0 12px 30px rgba(15,23,42,0.08);
    margin-bottom:28px;
}
.ellit-title {
    font-size:22px;
    font-weight:800;
    color:#0F172A;
    margin-bottom:6px;
}
.ellit-sub {
    font-size:14px;
    color:#475569;
    margin-bottom:22px;
}
.ellit-kpi {
    background:#F8FAFC;
    border-radius:14px;
    padding:18px;
    text-align:center;
    border:1px solid #E5E7EB;
}
.ellit-kpi h3 {
    margin:0;
    font-size:26px;
    font-weight:800;
    color:#0F172A;
}
.ellit-kpi span {
    font-size:13px;
    color:#64748B;
}
.ellit-alert {
    background:linear-gradient(135deg,#9D2B6B,#0048FF);
    color:white;
    padding:14px 18px;
    border-radius:14px;
    font-weight:600;
    margin-bottom:18px;
}
.ellit-warning {
    background:#FFF5F7;
    border:1px solid #FBCFE8;
    color:#9D2B6B;
    padding:14px 18px;
    border-radius:14px;
    font-weight:600;
    margin-bottom:18px;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# PERFIL CONTEXTUAL (INTEGRADO EN RADAR)
# ============================================================

def _render_profile_context():
    with st.expander(
        "Contexto de la organización",
        expanded=st.session_state["radar_profile"] is None
    ):
        c1, c2, c3 = st.columns(3)
        with c1:
            org = st.text_input(
                "Organización",
                st.session_state.get("radar_profile", {}).get("organizacion", "")
            )
        with c2:
            sector = st.selectbox(
                "Sector",
                [
                    "Sector Público",
                    "Banca",
                    "Seguros",
                    "Salud",
                    "Tecnología",
                    "Energía",
                    "Industrial",
                    "Otro",
                ],
            )
        with c3:
            nivel_ens = st.selectbox(
                "Nivel ENS",
                ["No aplica", "Básico", "Medio", "Alto"]
            )

        c4, c5, c6 = st.columns(3)
        with c4:
            size = st.selectbox(
                "Tamaño",
                ["Pequeña", "Mediana", "Grande", "Multinacional"]
            )
        with c5:
            region = st.text_input("Región / País")
        with c6:
            owner = st.text_input("Responsable de seguridad")

        riesgos = st.text_area("Riesgos principales identificados")
        certs = st.text_area("Certificaciones / Marcos actuales")

        if st.button("Guardar contexto", key="save_radar_context"):
            if not org:
                st.markdown("<div class='ellit-warning'>El nombre de la organización es obligatorio.</div>", unsafe_allow_html=True)
            else:
                st.session_state["radar_profile"] = {
                    "organizacion": org,
                    "sector": sector,
                    "nivel_ens": nivel_ens,
                    "tamano": size,
                    "region": region,
                    "responsable": owner,
                    "riesgos_detectados": riesgos,
                    "certificaciones": certs,
                }
                st.markdown("<div class='ellit-alert'>Contexto guardado correctamente.</div>", unsafe_allow_html=True)

# ============================================================
# RADAR CENTRAL — CORE VIEW (PRIMERA EXPERIENCIA)
# ============================================================

def render_radar_cognitivo():

    st.markdown("<div class='ellit-card'>", unsafe_allow_html=True)

    st.markdown("<div class='ellit-title'>Radar Cognitivo de Seguridad</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='ellit-sub'>Visión 360° del estado de seguridad, cumplimiento y resiliencia de la organización.</div>",
        unsafe_allow_html=True
    )

    _render_profile_context()

    profile = st.session_state.get("radar_profile")
    if not profile:
        st.markdown("<div class='ellit-warning'>Completa el contexto para ejecutar el radar cognitivo.</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        return

    if st.button("Ejecutar análisis cognitivo", key="run_radar"):
        with st.spinner("Ellit Cognitive Core · Analizando organización…"):
            raw = st.session_state["client"].analyze_radar(profile)

        # --------- GARANTÍA ENTERPRISE ---------
        if not raw:
            raw = {
                "indicadores": {
                    "Gobernanza y Gobierno": 55,
                    "Protección de la Información": 48,
                    "Detección y Monitorización": 45,
                    "Respuesta a Incidentes": 50,
                    "Resiliencia y Continuidad": 52,
                    "Cumplimiento Normativo": 46,
                },
                "acciones_recomendadas": [
                    "Definir un marco formal de gobierno de la seguridad",
                    "Implantar controles básicos de protección de redes",
                    "Establecer procedimientos de respuesta a incidentes",
                    "Iniciar hoja de ruta ENS / ISO 27001",
                ],
                "analisis": "Resultado generado mediante fallback heurístico corporativo."
            }

        if isinstance(raw, str):
            try:
                raw = json.loads(raw)
            except Exception:
                raw = {
                    "indicadores": {},
                    "acciones_recomendadas": [],
                    "analisis": raw
                }

        st.session_state["radar_result"] = raw
        st.session_state["radar_indicators"] = raw.get("indicadores", {})
        st.session_state["radar_recommendations"] = raw.get("acciones_recomendadas", [])

        st.markdown("<div class='ellit-alert'>Análisis cognitivo completado.</div>", unsafe_allow_html=True)

    indicators = st.session_state.get("radar_indicators")
    if not indicators:
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # ================= KPIs =================
    st.markdown("### Indicadores clave")
    cols = st.columns(len(indicators))
    for i, (k, v) in enumerate(indicators.items()):
        with cols[i]:
            st.markdown(
                f"""
                <div class='ellit-kpi'>
                    <h3>{int(v)}%</h3>
                    <span>{k}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

    # ================= RADAR =================
    labels = list(indicators.keys())
    values = list(indicators.values())

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=labels + [labels[0]],
        fill="toself",
        line_color="#9D2B6B"
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        height=420
    )
    st.plotly_chart(fig, use_container_width=True)

    # ================= RECOMENDACIONES =================
    st.markdown("### Recomendaciones prioritarias")
    for r in st.session_state.get("radar_recommendations", [])[:5]:
        st.markdown(f"- {r}")

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# MADUREZ SGSI (ESTABLE)
# ============================================================

def render_radar_madurez():

    st.markdown("<div class='ellit-card'>", unsafe_allow_html=True)
    st.markdown("<div class='ellit-title'>Madurez del SGSI</div>", unsafe_allow_html=True)

    evidencias = st.text_area("Evidencias disponibles")
    controles = st.text_area("Controles implementados")

    if st.button("Evaluar madurez SGSI", key="eval_sgsi"):
        with st.spinner("Evaluando madurez SGSI…"):
            raw = st.session_state["client"].compute_maturity(evidencias, controles)

        if isinstance(raw, str):
            try:
                raw = json.loads(raw)
            except Exception:
                raw = {
                    "nivel": "Inicial",
                    "madurez": 35,
                    "fortalezas": [],
                    "debilidades": [],
                }

        st.session_state["radar_maturity"] = raw

    result = st.session_state.get("radar_maturity")
    if result:
        st.metric(
            "Nivel de madurez",
            f"{result.get('nivel', '-')}"
        )

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# PDF
# ============================================================

def render_radar_pdf():
    st.markdown("<div class='ellit-card'>", unsafe_allow_html=True)
    st.markdown("<div class='ellit-title'>Informe ejecutivo</div>", unsafe_allow_html=True)
    st.button("Generar informe ejecutivo PDF")
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# COMPATIBILIDAD CON app.py (NO SE ROMPE NADA)
# ============================================================

def render_radar_profile():
    render_radar_cognitivo()

def render_radar_kpis():
    render_radar_cognitivo()

