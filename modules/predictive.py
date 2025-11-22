# =====================================================================
#   ELLIT – PREDICTIVE INTELLIGENCE ENGINE (MÓDULO PREMIUM COMPLETO)
#   Forecast 12 meses · Sector Intelligence · GeoRisk · Correlation Core
#   Compatible con Enterprise y PRIME
# =====================================================================

import streamlit as st
from datetime import datetime
from app import download_pdf_button
from cognitive_core import (
    predictive_full_forecast,
    predictive_sector_intel,
    predictive_geo_exposure,
    predictive_correlations,
    predictive_short_term_analysis
)


# ==========================================================
# UTILIDADES DE LICENCIA
# ==========================================================
def has_enterprise():
    return st.session_state.get("tenant_enterprise", False)


def has_prime():
    return st.session_state.get("tenant_prime", False)


# ==========================================================
# ESTILO CORPORATIVO ELLIT
# ==========================================================
HEADER = """
<div style="
    background: linear-gradient(135deg, #FF0080 0%, #0048FF 100%);
    padding: 20px; border-radius: 18px; color: white;
    text-align: center; margin-bottom: 25px;">
    <h2 style="margin:0;font-weight:800;">Ellit Predictive Intelligence</h2>
    <p style="opacity:0.85;margin:0;">Threat Forecast · Sector Intelligence · GeoRisk</p>
</div>
"""

SEPARATOR = "<hr style='margin:25px 0; opacity:0.2;'>"


# ==========================================================
# 1) PANEL PRINCIPAL – OVERVIEW EJECUTIVO
# ==========================================================
def render_predictive_standard():

    if not has_enterprise():
        st.error("Este módulo requiere licencia Enterprise.")
        return

    st.markdown(HEADER, unsafe_allow_html=True)

    sector = st.selectbox(
        "📌 Selecciona tu sector",
        [
            "Finanzas", "Seguros", "Gobierno", "Salud",
            "Retail", "Tecnología", "Logística", "Energía",
            "Educación", "Industrial", "Otro"
        ]
    )

    region = st.selectbox(
        "🌍 Región principal",
        ["Europa", "LatAm", "Estados Unidos", "APAC", "Global"]
    )

    st.markdown(SEPARATOR, unsafe_allow_html=True)

    # ------------------------------------------------------
    # 1. OVERVIEW — índice global de riesgo
    # ------------------------------------------------------
    st.subheader("📊 Global Risk Overview (AI Executive Layer)")

    with st.spinner("Calculando riesgo global…"):
        overview = predictive_full_forecast(
            st.session_state.client,
            sector=sector,
            region=region
        )

    col1, col2, col3 = st.columns(3)
    col1.metric("Índice Global de Riesgo (GRI)", f"{overview['global_risk_index']} / 100")
    col2.metric("Probabilidad Promedio", f"{overview['avg_probability']}%")
    col3.metric("Impacto Operativo Estimado", f"{overview['avg_impact']}%")

    st.info(overview["executive_summary"])

    st.markdown(SEPARATOR, unsafe_allow_html=True)

    # ------------------------------------------------------
    # 2. FORECAST — amenazas próximas 12 meses
    # ------------------------------------------------------
    st.subheader("📅 Threat Forecast — Próximos 12 meses")

    for item in overview["forecast_12m"]:
        st.markdown(f"""
        <div style="padding:12px;border-radius:10px;border:1px solid #E5E7EB;margin-bottom:12px;">
            <b>{item['mes']}</b> — {item['nivel']}
            <br>Probabilidad: {item['probabilidad']}%
            <br>Impacto: {item['impacto']}%
            <br><i>{item['descripcion']}</i>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(SEPARATOR, unsafe_allow_html=True)

    # ------------------------------------------------------
    # 3. SECTOR INTELLIGENCE
    # ------------------------------------------------------
    st.subheader("🏭 Sector Intelligence")

    with st.spinner("Analizando tu sector…"):
        sec = predictive_sector_intel(st.session_state.client, sector)

    st.success(sec["sector_summary"])

    st.markdown("### Riesgos principales del sector")
    for r in sec["top_risks"]:
        st.markdown(f"- {r}")

    st.markdown("### Brechas típicas del sector")
    for g in sec["sector_gaps"]:
        st.markdown(f"- {g}")

    st.markdown(SEPARATOR, unsafe_allow_html=True)

    # ------------------------------------------------------
    # 4. GEOGRAPHIC EXPOSURE
    # ------------------------------------------------------
    st.subheader("🌐 Geographic Exposure")

    with st.spinner("Analizando dependencia geográfica…"):
        geo = predictive_geo_exposure(st.session_state.client, region)

    st.metric("Estabilidad regional", f"{geo['stability_score']} / 100")
    st.metric("Riesgo regulatorio estimado", geo["regulatory_risk"])

    st.markdown("### Factores críticos:")
    for f in geo["factors"]:
        st.markdown(f"- {f}")

    st.markdown(SEPARATOR, unsafe_allow_html=True)

    # ------------------------------------------------------
    # 5. RECOMENDACIONES 30 / 60 / 180 días
    # ------------------------------------------------------
    st.subheader("🧭 Recomendaciones estratégicas")

    with st.spinner("Generando roadmap…"):
        rec = predictive_short_term_analysis(st.session_state.client, sector, region)

    for horizon, tasks in rec.items():
        with st.expander(horizon):
            for t in tasks:
                st.markdown(f"- {t}")

    st.markdown(SEPARATOR, unsafe_allow_html=True)

    # ------------------------------------------------------
    # 6. DESCARGA DE INFORME PDF
    # ------------------------------------------------------
    if st.button("📄 Descargar informe PDF"):
        pdf_text = build_predictive_pdf(overview, sec, geo, rec, sector, region)
        filename = f"Ellit_Predictive_Intel_{datetime.now().strftime('%Y%m%d')}.pdf"
        download_pdf_button("Predictive Intelligence Report", sector, pdf_text, filename)


# ==========================================================
# 2) MÓDULO PRIME — CORRELATION ENGINE
# ==========================================================
def render_predictive_prime():

    if not has_prime():
        st.error("Este módulo requiere licencia PRIME.")
        return

    st.markdown("""
        <div style="
            background:linear-gradient(135deg,#FF0080 0%,#D8278A 100%);
            padding:22px;border-radius:16px;color:white;text-align:center;
            margin-bottom:25px;">
            <h2 style="margin:0;font-weight:800;">Ellit PRIME — Correlation Engine</h2>
            <p style="opacity:0.85;margin:0;">Análisis avanzado de correlación entre amenazas</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### Selecciona tu sector y región")

    sector = st.selectbox("Sector", [
        "Finanzas", "Seguros", "Gobierno", "Salud",
        "Retail", "Tecnología", "Logística", "Energía",
        "Educación", "Industrial", "Otro"
    ])

    region = st.selectbox("Región", ["Europa", "LatAm", "Estados Unidos", "APAC", "Global"])

    if st.button("Calcular Correlation Matrix"):
        with st.spinner("Analizando correlaciones…"):
            data = predictive_correlations(st.session_state.client, sector, region)

        st.success("Análisis completado")

        st.markdown("### Matriz de correlación")
        for k, v in data.items():
            st.markdown(f"**{k}:** {v['nivel']}")
            st.markdown(f"<i>{v['explicacion']}</i>", unsafe_allow_html=True)

        st.markdown(SEPARATOR, unsafe_allow_html=True)

        if st.button("📄 Descargar PDF PRIME"):
            pdf = build_predictive_prime_pdf(data, sector, region)
            filename = f"Ellit_CORRELATION_PRIME_{datetime.now().strftime('%Y%m%d')}.pdf"
            download_pdf_button("Correlation Engine PRIME", sector, pdf, filename)


# ==========================================================
# PDF BUILDER
# ==========================================================
def build_predictive_pdf(overview, sec, geo, rec, sector, region):
    text = []

    text.append("ELLIT — Predictive Intelligence Report\n")
    text.append(f"Sector: {sector}")
    text.append(f"Región: {region}\n")

    text.append("\n--- GLOBAL RISK OVERVIEW ---")
    text.append(f"GRI: {overview['global_risk_index']}")
    text.append(f"Probabilidad Media: {overview['avg_probability']}%")
    text.append(f"Impacto Medio: {overview['avg_impact']}%")
    text.append(f"\n{overview['executive_summary']}")

    text.append("\n--- FORECAST 12 MESES ---")
    for item in overview["forecast_12m"]:
        text.append(f"{item['mes']} → {item['nivel']} • Prob:{item['probabilidad']}% • Impact:{item['impacto']}%")
        text.append(f"- {item['descripcion']}")

    text.append("\n--- SECTOR INTELLIGENCE ---")
    text.append(sec["sector_summary"])
    for r in sec["top_risks"]:
        text.append(f"- {r}")

    text.append("\n--- GEO EXPOSURE ---")
    text.append(f"Estabilidad: {geo['stability_score']}")
    text.append(f"Riesgo regulatorio: {geo['regulatory_risk']}")
    for f in geo["factors"]:
        text.append(f"- {f}")

    text.append("\n--- ROADMAP 30/60/180 ---")
    for h, tasks in rec.items():
        text.append(f"\n{h}:")
        for t in tasks:
            text.append(f"- {t}")

    return "\n".join(text)


def build_predictive_prime_pdf(data, sector, region):
    text = []
    text.append("ELLIT PRIME — Correlation Engine\n")
    text.append(f"Sector: {sector}\nRegión: {region}\n")

    for k, v in data.items():
        text.append(f"\n{k}: {v['nivel']}")
        text.append(v["explicacion"])

    return "\n".join(text)


# ==========================================================
# FIN DEL MÓDULO
# ==========================================================
