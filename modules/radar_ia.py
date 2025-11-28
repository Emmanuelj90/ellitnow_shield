# ============================================================
# RADAR IA — ELLIT COGNITIVE CORE (CCISO EXECUTIVE RADAR)
# Governance · Risk · Controls · Resilience · Culture
# ============================================================

import streamlit as st
import plotly.graph_objects as go

# ============================================================
# SESSION STATE SAFE INIT
# ============================================================

def init_state():
    defaults = {
        "radar_context": {},
        "cciso_scores": None,
        "risk_landscape": None,
        "sgsi_score": None,
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
    font-size:28px;
    color:#7C1F5E;
    margin:0;
}
.kpi span {
    font-size:13px;
    color:#6B7280;
}
.info {
    background:#FDF2F8;
    border-left:4px solid #7C1F5E;
    padding:16px;
    border-radius:8px;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# CONTEXTO ORGANIZACIONAL
# ============================================================

def render_context():

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("## Contexto organizacional")

    with st.form("context_form"):

        org = st.text_input("Nombre de la organización")
        sector = st.selectbox(
            "Sector principal",
            ["Banca","Seguros","Salud","Tecnología","Industria","Energía","Retail","Sector Público","Otro"]
        )
        size = st.selectbox(
            "Tamaño",
            ["PYME","Mid Market","Enterprise","Multinacional"]
        )
        regulations = st.multiselect(
            "Marco regulatorio aplicable",
            ["ENS","ISO 27001","NIS2","DORA","PCI DSS","HIPAA","TISAX"]
        )
        risks = st.text_area(
            "Riesgos percibidos por el negocio",
            placeholder="Ej: ransomware, dependencia de terceros, fuga de datos, impacto reputacional…"
        )

        submit = st.form_submit_button("Guardar contexto")

        if submit:
            if not org:
                st.error("El nombre de la organización es obligatorio.")
            else:
                st.session_state["radar_context"] = {
                    "org": org,
                    "sector": sector,
                    "size": size,
                    "regulations": regulations,
                    "risks": risks
                }
                st.success("Contexto guardado.")

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# CCISO ASSESSMENT (EXECUTIVE)
# ============================================================

def render_cciso_assessment():

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("## Evaluación CCISO")

    st.markdown("Responde desde una **perspectiva ejecutiva real**.")

    domains = {
        "Governance & Leadership": "Gobierno, ownership y board",
        "Risk Management": "Gestión de riesgo de negocio",
        "Controls & Architecture": "Controles y arquitectura",
        "Incident Readiness": "Preparación ante incidentes",
        "Resilience & Continuity": "Continuidad y resiliencia"
    }

    scores = {}

    for d, desc in domains.items():
        st.subheader(d)
        scores[d] = st.slider(desc, 0, 100, 50)

    if st.button("Calcular Radar CCISO"):
        st.session_state["cciso_scores"] = scores

        # === RISK LANDSCAPE DERIVADO ===
        st.session_state["risk_landscape"] = [
            {"risk":"Ransomware", "impact":85, "prob":70},
            {"risk":"Third-party breach", "impact":75, "prob":65},
            {"risk":"Regulatory sanctions", "impact":80, "prob":55},
        ]

        st.success("Radar CCISO generado.")

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# RADAR + GRÁFICOS
# ============================================================

def render_radar_dashboard():

    scores = st.session_state.get("cciso_scores")
    if not scores:
        return

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("## Postura global de Seguridad (CCISO)")

    # KPIs
    cols = st.columns(len(scores))
    for i, (k, v) in enumerate(scores.items()):
        with cols[i]:
            st.markdown(
                f"<div class='kpi'><h3>{v}%</h3><span>{k}</span></div>",
                unsafe_allow_html=True
            )

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
    st.download_button("Descargar Radar (PNG)", fig.to_image("png"), "radar_cciso.png")

    st.markdown("</div>", unsafe_allow_html=True)

    # Heatmap Riesgo
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("## Landscape de Riesgo (Impacto vs Probabilidad)")

    risks = st.session_state["risk_landscape"]
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=[r["prob"] for r in risks],
        y=[r["impact"] for r in risks],
        text=[r["risk"] for r in risks],
        mode="markers+text",
        marker=dict(size=18, color="#7C1F5E"),
        textposition="top center"
    ))
    fig2.update_layout(
        xaxis_title="Probabilidad",
        yaxis_title="Impacto",
        height=420
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# SGSI – GAP ANALYSIS
# ============================================================

def render_sgsi():

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("## Madurez del SGSI")

    questions = [
        "Políticas formales definidas",
        "Gestión de riesgos periódica",
        "Controles efectivos",
        "Formación y concienciación",
        "Mejora continua"
    ]

    values = [st.slider(q, 0, 5, 2) for q in questions]

    if st.button("Evaluar SGSI"):
        st.session_state["sgsi_score"] = int(sum(values)/(len(values)*5)*100)

    score = st.session_state.get("sgsi_score")
    if score is not None:
        st.metric("Madurez SGSI", f"{score}%")

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# ROUTER SAFE
# ============================================================

def render_radar_profile():
    render_context()

def render_radar_kpis():
    render_radar_cognitivo()

def render_radar_cognitivo():
    render_context()
    render_cciso_assessment()
    render_radar_dashboard()

def render_radar_madurez():
    render_sgsi()

def render_radar_pdf():
    st.info("Informe ejecutivo PDF próximamente")
