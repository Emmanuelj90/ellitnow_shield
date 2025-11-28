# ============================================================
# RADAR IA — Ellit Cognitive Core (CCISO + SGSI)
# ============================================================

import streamlit as st
import plotly.graph_objects as go

# ------------------------------------------------------------
# STATE INIT (SAFE)
# ------------------------------------------------------------
def _init_state():
    defaults = {
        "radar_profile": None,
        "cciso_scores": None,
        "risk_matrix": [],
        "sgsi_answers": {},
        "sgsi_result": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init_state()

# ------------------------------------------------------------
# STYLES
# ------------------------------------------------------------
st.markdown("""
<style>
.card{background:#fff;border-radius:16px;padding:24px;margin-bottom:24px;
box-shadow:0 8px 24px rgba(0,0,0,.06)}
.kpi{text-align:center}
.kpi h2{margin:0;color:#7C1F5E}
.kpi span{font-size:13px;color:#64748B}
.tag{background:#FDF2F8;color:#7C1F5E;padding:6px 10px;
border-radius:6px;display:inline-block;margin:4px 0}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# RADAR COGNITIVO (EXECUTIVE)
# ------------------------------------------------------------
def render_radar_cognitivo():

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("## Radar Cognitivo Ejecutivo (CCISO)")

    with st.expander("Contexto organizativo", expanded=True):
        org = st.text_input("Organización")
        sector = st.selectbox("Sector", ["Finanzas","Salud","Tecnología","Público","Industrial"])
        if st.button("Guardar contexto"):
            st.session_state["radar_profile"] = {"org":org,"sector":sector}

    if not st.session_state["radar_profile"]:
        st.info("Completa el contexto para continuar.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    if st.button("Ejecutar Radar Cognitivo", type="primary"):
        # MOCK REALISTA (luego IA refina)
        scores = {
            "Governance & Risk": 60,
            "Security Controls": 55,
            "Program Management": 50,
            "Incident Readiness": 45,
            "Business Resilience": 40,
        }
        st.session_state["cciso_scores"] = scores
        st.session_state["risk_matrix"] = [
            {"risk":"Ransomware","impact":5,"prob":4},
            {"risk":"Data Leak","impact":4,"prob":3},
            {"risk":"Supply Chain","impact":3,"prob":4},
        ]

    scores = st.session_state["cciso_scores"]
    if not scores:
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # KPIs
    st.markdown("### Indicadores ejecutivos")
    cols = st.columns(len(scores))
    for i,(k,v) in enumerate(scores.items()):
        with cols[i]:
            st.markdown(f"<div class='kpi'><h2>{v}%</h2><span>{k}</span></div>", unsafe_allow_html=True)

    # Radar
    fig = go.Figure()
    labels = list(scores.keys())
    values = list(scores.values())
    fig.add_trace(go.Scatterpolar(
        r=values+[values[0]],
        theta=labels+[labels[0]],
        fill='toself',
        line_color='#7C1F5E'
    ))
    fig.update_layout(height=420,showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    # Risk Landscape
    st.markdown("### Risk landscape")
    fig2 = go.Figure()
    for r in st.session_state["risk_matrix"]:
        fig2.add_trace(go.Scatter(
            x=[r["prob"]], y=[r["impact"]],
            mode="markers+text", text=r["risk"]
        ))
    fig2.update_layout(
        xaxis_title="Probabilidad",
        yaxis_title="Impacto",
        height=360
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------
# MADUREZ SGSI (AUDITOR REAL)
# ------------------------------------------------------------
SGSI_QUESTIONS = {
    "Política & Gobierno": [
        "Existe política aprobada",
        "Roles definidos"
    ],
    "Riesgos": [
        "Análisis formal de riesgos",
        "Revisión periódica"
    ],
    "Continuidad": [
        "Plan BCP documentado",
        "Pruebas realizadas"
    ]
}

def render_radar_madurez():

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("## Madurez SGSI (Gap Analysis)")

    score = 0
    total = 0

    for domain, qs in SGSI_QUESTIONS.items():
        st.markdown(f"### {domain}")
        for q in qs:
            v = st.radio(q,[0,1,2,3],horizontal=True,key=f"{domain}-{q}")
            score += v
            total += 3

    if st.button("Calcular madurez SGSI"):
        maturity = int((score/total)*100)
        st.session_state["sgsi_result"] = maturity

    if st.session_state["sgsi_result"]:
        st.metric("Madurez SGSI", f"{st.session_state['sgsi_result']}%")
        st.markdown("<span class='tag'>Gap Analysis generado</span>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------
# ROUTER SAFE
# ------------------------------------------------------------
def render_radar_kpis(): render_radar_cognitivo()
def render_radar_profile(): render_radar_cognitivo()
