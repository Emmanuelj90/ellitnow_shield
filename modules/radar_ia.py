# ============================================================
# RADAR IA — ELLIT COGNITIVE CORE (EXECUTIVE CCISO RADAR)
# Governance · Risk · Controls · Resilience · Culture
# ============================================================

import streamlit as st
import plotly.graph_objects as go
from datetime import datetime

# ============================================================
# SESSION STATE SAFE INIT
# ============================================================

def init_state():
    defaults = {
        "radar_context": {},
        "cciso_raw_inputs": None,
        "cciso_scores": None,
        "risk_landscape": None,
        "sgsi_score": None,
        "branding": {}
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
.small {
    font-size:12px;
    color:#6B7280;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# COGNITIVE ENGINE — PESOS ELLIT
# ============================================================

SECTOR_WEIGHT = {
    "Banca": 1.25,
    "Seguros": 1.20,
    "Salud": 1.30,
    "Tecnología": 1.10,
    "Industria": 1.15,
    "Energía": 1.25,
    "Retail": 1.05,
    "Sector Público": 1.30,
    "Otro": 1.10
}

SIZE_WEIGHT = {
    "PYME": 1.10,
    "Mid Market": 1.15,
    "Enterprise": 1.20,
    "Multinacional": 1.30
}

REGULATION_WEIGHT = {
    "ENS": 1.10,
    "ISO 27001": 1.05,
    "NIS2": 1.15,
    "DORA": 1.20,
    "PCI DSS": 1.10,
    "HIPAA": 1.15,
    "TISAX": 1.10
}

def cognitive_adjust(raw_score: int, context: dict) -> int:
    score = raw_score

    score *= SECTOR_WEIGHT.get(context.get("sector"), 1.0)
    score *= SIZE_WEIGHT.get(context.get("size"), 1.0)

    for r in context.get("regulations", []):
        score *= REGULATION_WEIGHT.get(r, 1.0)

    if context.get("risks"):
        score *= 0.90  # penalización por riesgo explícito

    return max(0, min(int(score), 100))

# ============================================================
# CONTEXTO ORGANIZACIONAL (FORM ÚNICO)
# ============================================================

def render_context():

    with st.expander(" Contexto organizacional", expanded=False):

        st.markdown("<div class='card'>", unsafe_allow_html=True)

        with st.form("context_form"):

            org = st.text_input("Nombre de la organización")
            sector = st.selectbox(
                "Sector principal",
                list(SECTOR_WEIGHT.keys())
            )
            size = st.selectbox(
                "Tamaño de la organización",
                list(SIZE_WEIGHT.keys())
            )
            regulations = st.multiselect(
                "Marco regulatorio aplicable",
                list(REGULATION_WEIGHT.keys())
            )
            risks = st.text_area(
                "Riesgos críticos del negocio",
                placeholder="Ej: ransomware, terceros, parada operativa…"
            )

            submit = st.form_submit_button("Guardar contexto")

            if submit:
                st.session_state["radar_context"] = {
                    "org": org,
                    "sector": sector,
                    "size": size,
                    "regulations": regulations,
                    "risks": risks
                }
                st.success("Contexto organizacional guardado.")

        st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# CCISO INPUT (EJECUTIVO)
# ============================================================

def render_cciso_inputs():

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("##  Input ejecutivo CCISO")

    domains = {
        "Governance & Leadership": "Gobierno, ownership y board",
        "Risk Management": "Gestión del riesgo de negocio",
        "Controls & Architecture": "Controles y arquitectura",
        "Incident Readiness": "Preparación ante incidentes",
        "Resilience & Continuity": "Continuidad y resiliencia"
    }

    inputs = {}
    for d, desc in domains.items():
        st.subheader(d)
        inputs[d] = st.slider(desc, 0, 100, 50)

    if st.button("Evaluar postura real"):
        st.session_state["cciso_raw_inputs"] = inputs

        context = st.session_state.get("radar_context", {})
        adjusted = {
            d: cognitive_adjust(v, context)
            for d, v in inputs.items()
        }

        st.session_state["cciso_scores"] = adjusted

        st.session_state["risk_landscape"] = [
            {"risk": "Ransomware", "impact": 85, "prob": 70},
            {"risk": "Third-party failure", "impact": 75, "prob": 65},
            {"risk": "Regulatory sanctions", "impact": 80, "prob": 55},
        ]

        st.success("Evaluación cognitiva Ellit generada.")

    st.caption(
        "Las puntuaciones se ajustan automáticamente según "
        "sector, tamaño, regulación y riesgos declarados."
    )

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# DASHBOARD CCISO
# ============================================================

def render_radar_dashboard():

    scores = st.session_state.get("cciso_scores")
    if not scores:
        return

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("##  Postura global de Seguridad (Ellit Cognitive Score)")

    cols = st.columns(len(scores))
    for i, (k, v) in enumerate(scores.items()):
        with cols[i]:
            st.markdown(
                f"<div class='kpi'><h3>{v}%</h3><span>{k}</span></div>",
                unsafe_allow_html=True
            )

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

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# RISK LANDSCAPE
# ============================================================

def render_risk_landscape():

    risks = st.session_state.get("risk_landscape")
    if not risks:
        return

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("##  Landscape de Riesgo")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=[r["prob"] for r in risks],
        y=[r["impact"] for r in risks],
        text=[r["risk"] for r in risks],
        mode="markers+text",
        marker=dict(size=17, color="#7C1F5E"),
        textposition="top center"
    ))

    fig.update_layout(
        xaxis_title="Probabilidad",
        yaxis_title="Impacto",
        height=420
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# SGSI — MADUREZ
# ============================================================

def render_sgsi():

    with st.expander("🛡️ Madurez SGSI", expanded=False):

        st.markdown("<div class='card'>", unsafe_allow_html=True)

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
# PDF CORPORATE (WHITE-LABEL READY)
# ============================================================

def render_pdf_section():

    with st.expander("📄 Informe ejecutivo corporativo", expanded=False):

        st.markdown("<div class='card'>", unsafe_allow_html=True)

        st.markdown(
            "El informe se genera con identidad corporativa del cliente "
            "y *powered by Ellit Cognitive Core*."
        )

        st.info("Generación PDF corporate disponible en versión Enterprise Plus.")

        st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# MAIN ENTRY — LO QUE LLAMA app.py
# ============================================================

def render_radar_kpis():
    render_context()
    render_cciso_inputs()
    render_radar_dashboard()
    render_risk_landscape()
    render_sgsi()
    render_pdf_section()

def render_radar_profile():
    pass

def render_radar_cognitivo():
    pass

def render_radar_madurez():
    pass

def render_radar_pdf():
    pass
