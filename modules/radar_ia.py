# ============================================================
# RADAR IA — ELLIT COGNITIVE CORE (CCISO EXECUTIVE RADAR)
# ============================================================

import streamlit as st
import plotly.graph_objects as go

# ============================================================
# SESSION STATE SAFE INIT (OBLIGATORIO)
# ============================================================

def init_state():
    defaults = {
        "radar_profile": {},
        "cciso_scores": None,
        "sgsi_result": None
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ============================================================
# BRAND STYLE (ELLIT)
# ============================================================

st.markdown("""
<style>
.card {
    background:#FFFFFF;
    padding:28px;
    border-radius:18px;
    border:1px solid #E5E7EB;
    margin-bottom:28px;
    box-shadow:0 12px 32px rgba(0,0,0,.06);
}
.kpi {
    background:#F9FAFB;
    border:1px solid #E5E7EB;
    border-radius:14px;
    padding:18px;
    text-align:center;
}
.kpi h3 {
    font-size:26px;
    color:#7C1F5E;
    margin:0;
}
.kpi span {
    font-size:13px;
    color:#6B7280;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# CONTEXTO ORGANIZATIVO (CISO REAL)
# ============================================================

def render_profile():

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("## Contexto organizativo")

    with st.form("context_form"):
        board = st.selectbox("Patrocinio del Board", ["Sí", "Parcial", "No"])
        ciso = st.selectbox("Rol CISO formal", ["Sí", "Parcial", "No"])
        infra = st.multiselect(
            "Infraestructura",
            ["On-prem", "Cloud público", "Cloud híbrido", "OT / ICS"]
        )
        third_party = st.selectbox(
            "Gestión de terceros",
            ["Formal", "Parcial", "No existente"]
        )

        submit = st.form_submit_button("Guardar contexto")

        if submit:
            st.session_state["radar_profile"] = {
                "board": board,
                "ciso": ciso,
                "infra": infra,
                "third_party": third_party
            }
            st.success("Contexto guardado.")

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# RADAR COGNITIVO (DASHBOARD ÚNICO)
# ============================================================

def render_radar():

    render_profile()

    profile = st.session_state.get("radar_profile") or {}

    if not profile:
        st.info("Completa el contexto para generar el Radar Cognitivo.")
        return

    if st.button(" Ejecutar Radar Cognitivo", type="primary"):

        # ▶ SCORES CCISO (baseline coherente)
        st.session_state["cciso_scores"] = {
            "Governance & Risk": 62,
            "Security Controls": 55,
            "Program Management": 50,
            "Incident Readiness": 47,
            "Business Resilience": 42
        }

    scores = st.session_state.get("cciso_scores")
    if not scores:
        return

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("## Indicadores Ejecutivos (CCISO)")

    cols = st.columns(len(scores))
    for i, (k, v) in enumerate(scores.items()):
        with cols[i]:
            st.markdown(
                f"<div class='kpi'><h3>{v}%</h3><span>{k}</span></div>",
                unsafe_allow_html=True
            )

    st.markdown("</div>", unsafe_allow_html=True)

    # Radar
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=list(scores.values()) + [list(scores.values())[0]],
        theta=list(scores.keys()) + [list(scores.keys())[0]],
        fill="toself",
        line_color="#7C1F5E"
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(range=[0, 100])),
        showlegend=False,
        height=420
    )

    st.plotly_chart(fig, use_container_width=True)
    st.download_button(
        "📥 Descargar radar (PNG)",
        fig.to_image(format="png"),
        "radar_cciso.png"
    )

# ============================================================
# MADUREZ SGSI (GAP ANALYSIS)
# ============================================================

def render_sgsi():

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("## Madurez del SGSI")

    questions = {
        "Políticas": st.slider("Políticas documentadas",0,5,2),
        "Gestión de riesgos": st.slider("Análisis de riesgos",0,5,2),
        "Controles": st.slider("Controles técnicos",0,5,2),
        "Concienciación": st.slider("Formación",0,5,2),
        "Mejora continua": st.slider("Mejora continua",0,5,1)
    }

    if st.button("Evaluar SGSI"):
        score = int(sum(questions.values()) / (len(questions)*5) * 100)
        st.session_state["sgsi_result"] = score

    result = st.session_state.get("sgsi_result")
    if result is not None:
        st.metric("Nivel de madurez SGSI", f"{result}%")

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# ROUTER SAFE – COMPATIBILIDAD TOTAL
# ============================================================

def render_radar_profile(): render_radar()
def render_radar_kpis(): render_radar()
def render_radar_cognitivo(): render_radar()
def render_radar_madurez(): render_sgsi()

def render_radar_pdf():
    st.info("Informe ejecutivo PDF — próximamente")
