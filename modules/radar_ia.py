# ============================================================
# RADAR IA — Ellit Cognitive Core
# CCISO-Aligned · Executive Security Radar
# ============================================================

import streamlit as st
import plotly.graph_objects as go
import json

# ============================================================
# SESSION STATE SAFE INIT (OBLIGATORIO)
# ============================================================

if "radar_profile" not in st.session_state:
    st.session_state["radar_profile"] = None



# ============================================================
# STATE INIT (ENTERPRISE SAFE)
# ============================================================

def _init_state():
    defaults = {
        "radar_profile": None,
        "radar_result": None,
        "radar_domains": None,
        "radar_summary": None,
        "radar_roadmap": None,
        "sgsi_maturity": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init_state()

# ============================================================
# STYLES — ELLIT PREMIUM
# ============================================================

st.markdown("""
<style>
.ellit-card {
    background:#FFFFFF;
    border-radius:18px;
    padding:28px;
    border:1px solid #E5E7EB;
    box-shadow:0 12px 30px rgba(0,0,0,0.06);
    margin-bottom:28px;
}
.ellit-title {
    font-size:22px;
    font-weight:800;
    color:#0F172A;
}
.ellit-sub {
    font-size:14px;
    color:#475569;
    margin-bottom:18px;
}
.ellit-msg-ok {
    background:linear-gradient(135deg,#0F766E,#14B8A6);
    color:white;
    padding:14px;
    border-radius:10px;
}
.ellit-msg-warn {
    background:linear-gradient(135deg,#7C1F5E,#C0267E);
    color:white;
    padding:14px;
    border-radius:10px;
}
.ellit-kpi {
    background:#F8FAFC;
    border-radius:12px;
    padding:18px;
    text-align:center;
    border:1px solid #E5E7EB;
}
.ellit-kpi h3 {
    margin:0;
    font-size:26px;
    font-weight:800;
}
.ellit-kpi span {
    font-size:13px;
    color:#64748B;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# PROFILE CONTEXT (CISO FRIENDLY)
# ============================================================

def _render_profile():
    profile = st.session_state.get("radar_profile") or {}


    with st.expander("Contexto de la organización", expanded=not profile):
        c1, c2, c3 = st.columns(3)
        with c1:
            org = st.text_input("Organización", profile.get("organizacion",""))
        with c2:
            sector = st.selectbox(
                "Sector",
                ["Sector Público","Banca","Seguros","Salud","Tecnología","Energía","Industrial","Otro"]
            )
        with c3:
            ens = st.selectbox("Nivel ENS", ["No aplica","Básico","Medio","Alto"])

        c4, c5 = st.columns(2)
        with c4:
            size = st.selectbox("Tamaño", ["Pequeña","Mediana","Grande","Multinacional"])
        with c5:
            region = st.text_input("Región / País")

        riesgos = st.text_area("Riesgos críticos conocidos")
        certs = st.text_area("Certificaciones / Marcos")

        if st.button("Guardar contexto"):
            if not org:
                st.error("La organización es obligatoria.")
                return

            st.session_state["radar_profile"] = {
                "organizacion": org,
                "sector": sector,
                "nivel_ens": ens,
                "tamano": size,
                "region": region,
                "riesgos": riesgos,
                "certificaciones": certs
            }
            st.success("Contexto guardado.")

# ============================================================
# MAIN RADAR — CCISO CORE
# ============================================================

def render_radar_cognitivo():

    st.markdown("<div class='ellit-card'>", unsafe_allow_html=True)
    st.markdown("<div class='ellit-title'>Radar Cognitivo de Seguridad (CCISO)</div>", unsafe_allow_html=True)
    st.markdown("<div class='ellit-sub'>Visión ejecutiva 360° para CISO y Comité de Riesgos</div>", unsafe_allow_html=True)

    _render_profile()

    profile = st.session_state["radar_profile"]
    if not profile:
        st.info("Defina primero el contexto organizativo.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    if st.button("Ejecutar Radar Cognitivo", type="primary"):
        with st.spinner("Analizando postura de seguridad…"):
            raw = st.session_state["client"].analyze_radar(profile)

        if not raw:
            st.markdown("<div class='ellit-msg-warn'>El motor no devolvió resultados estructurados.</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            return

        if isinstance(raw, str):
            try:
                raw = json.loads(raw)
            except Exception:
                st.markdown("<div class='ellit-msg-warn'>Respuesta no estructurada del motor.</div>", unsafe_allow_html=True)
                return

        # ===== NORMALIZACIÓN CCISO =====
        st.session_state["radar_summary"] = raw.get("resumen_ejecutivo") or raw.get("analisis","")
        st.session_state["radar_domains"] = raw.get("dominios_cciso") or {
            "Governance & Risk": raw.get("gobierno", 60),
            "Security Controls": raw.get("controles", 55),
            "Program Management": raw.get("programa", 50),
            "Incident Readiness": raw.get("incidentes", 45),
            "Business Resilience": raw.get("resiliencia", 40),
        }
        st.session_state["radar_roadmap"] = raw.get("roadmap", {})

        st.markdown("<div class='ellit-msg-ok'>Análisis completado con éxito.</div>", unsafe_allow_html=True)

    domains = st.session_state.get("radar_domains")
    if not domains:
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # =====================================================
    # EXECUTIVE SUMMARY
    # =====================================================

    if st.session_state.get("radar_summary"):
        st.markdown("### Executive Insight")
        st.info(st.session_state["radar_summary"])

    # =====================================================
    # KPI PANEL (CISO)
    # =====================================================

    st.markdown("### Indicadores ejecutivos")
    cols = st.columns(len(domains))
    for i,(k,v) in enumerate(domains.items()):
        with cols[i]:
            st.markdown(
                f"<div class='ellit-kpi'><h3>{int(v)}%</h3><span>{k}</span></div>",
                unsafe_allow_html=True
            )

    # =====================================================
    # RADAR CCISO
    # =====================================================

    labels = list(domains.keys())
    values = list(domains.values())

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=labels + [labels[0]],
        fill='toself',
        line_color='#9D2B6B'
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(range=[0,100], visible=True)),
        showlegend=False,
        height=460
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# SGSI MATURITY — GAP ANALYSIS
# ============================================================

def render_radar_madurez():

    st.markdown("<div class='ellit-card'>", unsafe_allow_html=True)
    st.markdown("<div class='ellit-title'>Madurez SGSI y Gap Analysis</div>", unsafe_allow_html=True)

    evidencias = st.text_area("Evidencias")
    controles = st.text_area("Controles")

    if st.button("Evaluar madurez"):
        with st.spinner("Evaluando SGSI…"):
            raw = st.session_state["client"].compute_maturity(evidencias, controles)

        if isinstance(raw, str):
            try:
                raw = json.loads(raw)
            except Exception:
                st.error("Respuesta no estructurada del motor.")
                return

        st.session_state["sgsi_maturity"] = raw

    res = st.session_state.get("sgsi_maturity")
    if res:
        st.metric("Nivel de madurez", f"{res.get('nivel','-')} ({res.get('madurez',0)}%)")

        c1,c2 = st.columns(2)
        with c1:
            st.markdown("**Fortalezas**")
            for f in res.get("fortalezas",[]): st.markdown(f"- {f}")
        with c2:
            st.markdown("**Gaps / Debilidades**")
            for d in res.get("debilidades",[]): st.markdown(f"- {d}")

        st.markdown("**Plan de acción recomendado**")
        for a in res.get("acciones_requeridas",[]): st.markdown(f"- {a}")

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# PDF HOOK
# ============================================================

def render_radar_pdf():
    st.markdown("<div class='ellit-card'>", unsafe_allow_html=True)
    st.markdown("<div class='ellit-title'>Informe Ejecutivo</div>", unsafe_allow_html=True)
    st.button("Generar informe PDF", type="primary")
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# ROUTER COMPATIBILITY (NO TOCAR)
# ============================================================

def render_radar_profile(): render_radar_cognitivo()
def render_radar_kpis(): render_radar_cognitivo()

