# ============================================================
# RADAR IA — ELLIT COGNITIVE CORE (CCISO EXECUTIVE RADAR)
# ============================================================

import streamlit as st
import plotly.graph_objects as go

# ============================================================
# SESSION STATE SAFE INIT
# ============================================================

def init_radar_state():
    defaults = {
        "radar_profile": {},
        "radar_result": None,
        "cciso_scores": None,
        "risk_matrix": None,
        "sgsi_result": None
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_radar_state()

# ============================================================
# BRAND STYLE
# ============================================================

st.markdown("""
<style>
.card{
    background:#ffffff;
    padding:28px;
    border-radius:16px;
    margin-bottom:28px;
    border:1px solid #E6E8EC;
    box-shadow:0 10px 30px rgba(0,0,0,.06);
}
.kpi{
    text-align:center;
    padding:18px;
    border-radius:14px;
    background:#F9FAFB;
    border:1px solid #E5E7EB;
}
.kpi h3{
    color:#7C1F5E;
    font-size:26px;
    margin:0;
}
.kpi span{
    font-size:13px;
    color:#6B7280;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# CONTEXTO ORGANIZACIÓN — CISO STYLE
# ============================================================

def render_profile():

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("## Contexto Organizativo")

    with st.form("org_context"):
        st.subheader("Gobierno y Estrategia")
        board = st.selectbox("¿Existe patrocinio del Board?", ["Sí", "Parcial", "No"])
        ciso = st.selectbox("¿Existe rol CISO formal?", ["Sí", "Parcial", "No"])

        st.subheader("Tecnología")
        infra = st.multiselect(
            "Infraestructura",
            ["On-prem", "Cloud público", "Cloud híbrido", "OT / ICS"]
        )

        st.subheader("Riesgos")
        incidents = st.selectbox("Incidentes graves últimos 24 meses", ["Sí", "No"])
        ransomware = st.selectbox("Riesgo de ransomware percibido", ["Alto", "Medio", "Bajo"])

        st.subheader("Cumplimiento")
        iso = st.checkbox("ISO 27001")
        ens = st.checkbox("ENS")
        tisax = st.checkbox("TISAX")
        gdpr = st.checkbox("RGPD")

        st.subheader("Terceras partes")
        third_party = st.selectbox("Gestión de proveedores críticos", ["Formal", "Parcial", "No existente"])

        submit = st.form_submit_button("Guardar contexto")

        if submit:
            st.session_state["radar_profile"] = {
                "board": board,
                "ciso": ciso,
                "infra": infra,
                "incidents": incidents,
                "ransomware": ransomware,
                "iso": iso,
                "ens": ens,
                "tisax": tisax,
                "gdpr": gdpr,
                "third_party": third_party
            }
            st.success("Contexto registrado")

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# RADAR COGNITIVO (ÚNICA VISTA)
# ============================================================

def render_radar():

    render_profile()

    if not st.session_state["radar_profile"]:
        st.info("Completa el contexto para generar el Radar Cognitivo.")
        return

    if st.button("🚀 Ejecutar Radar Cognitivo", type="primary"):

        # --- SIMULACIÓN COHERENTE (hasta afinar IA) ---
        cciso = {
            "Governance & Risk": 60,
            "Security Controls": 55,
            "Program Management": 50,
            "Incident Readiness": 45,
            "Business Resilience": 40
        }

        st.session_state["cciso_scores"] = cciso

    scores = st.session_state["cciso_scores"]
    if not scores:
        return

    # KPIs
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("## Indicadores Ejecutivos")

    cols = st.columns(len(scores))
    for i,(k,v) in enumerate(scores.items()):
        with cols[i]:
            st.markdown(f"<div class='kpi'><h3>{v}%</h3><span>{k}</span></div>", unsafe_allow_html=True)

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
        polar=dict(radialaxis=dict(range=[0,100])),
        showlegend=False,
        height=420
    )
    st.plotly_chart(fig, use_container_width=True)
    st.download_button("📥 Descargar radar (PNG)", fig.to_image(format="png"), "radar_cciso.png")

# ============================================================
# MADUREZ SGSI — AUDITOR REAL
# ============================================================

def render_sgsi():

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("## Madurez del SGSI")

    questions = {
        "Políticas formales": st.slider("Políticas documentadas",0,5,2),
        "Gestión de riesgo": st.slider("Análisis de riesgos",0,5,2),
        "Controles técnicos": st.slider("Controles técnicos",0,5,2),
        "Concienciación": st.slider("Formación",0,5,2),
        "Mejora continua": st.slider("Mejora continua",0,5,1)
    }

    if st.button("Evaluar SGSI"):
        total = sum(questions.values())
        max_score = len(questions)*5
        maturity = int((total/max_score)*100)

        st.session_state["sgsi_result"] = {
            "score": maturity,
            "domain": questions
        }

    result = st.session_state.get("sgsi_result")
    if result:
        st.metric("Nivel de madurez SGSI", f"{result['score']}%")
        fig = go.Figure(go.Bar(
            x=list(result["domain"].keys()),
            y=list(result["domain"].values()),
            marker_color="#7C1F5E"
        ))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# ROUTER SAFE FUNCTIONS
# ============================================================

def render_radar_profile(): render_radar()
def render_radar_kpis(): render_radar()
def render_radar_cognitivo(): render_radar()
def render_radar_madurez(): render_sgsi()
def render_radar_pdf():
    st.info("Generación de PDF ejecutiva próximamente")


