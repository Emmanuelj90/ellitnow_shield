# ==========================================================
# ELLIT SGSI MONITOR — MÓDULO COMPLETO (2025)
# ==========================================================
# Incluye:
# - Dashboard SGSI con KPIs y Radar
# - Registro histórico
# - Evidencias y mantenimiento
# - Comparativa normativa con soporte N/A
# - Motor de IA (Ellit Cognitive Core)
# ==========================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import uuid
import json
from datetime import datetime
from math import pi

from core.database import get_conn
from core.cognitive_core import EllitCognitiveCore


# ==========================================================
# ESTILOS CORPORATIVOS
# ==========================================================
CARD_STYLE = """
<style>
.metric-card {
    background-color: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 16px !important;
    padding: 20px;
    text-align: center;
    box-shadow: 0 3px 10px rgba(0,0,0,0.05);
    transition: all 0.2s ease;
}
.metric-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 16px rgba(0,0,0,0.1);
}
.metric-label {
    font-size: 13px;
    font-weight: 600;
    color: #64748B;
}
.metric-value {
    font-size: 32px;
    font-weight: 700;
    color: #0F172A;
}
</style>
"""


# ==========================================================
# UTILS
# ==========================================================
def get_active_tenant():
    return st.session_state.get("tenant_id")


def metric_card(label, value):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# BASE DE DATOS – KPIs
# ==========================================================
def db_get_kpi_log(tenant_id):
    conn = get_conn()
    df = pd.read_sql_query("""
        SELECT id, kpi_date, kpi_name, kpi_value
        FROM sgsi_kpis
        WHERE tenant_id = ?
        ORDER BY kpi_date ASC
    """, conn, params=(tenant_id,))
    conn.close()
    return df


def db_insert_kpi(tenant_id, name, value):
    conn = get_conn()
    conn.execute("""
        INSERT INTO sgsi_kpis (id, tenant_id, kpi_date, kpi_name, kpi_value)
        VALUES (?, ?, ?, ?, ?)
    """, (
        str(uuid.uuid4()),
        tenant_id,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        name,
        value
    ))
    conn.commit()
    conn.close()


# ==========================================================
# RADAR CHART – soporte N/A
# ==========================================================
def radar_fig(kpis):
    labels = list(kpis.keys())
    raw_values = list(kpis.values())

    values = [(0 if v == "N/A" else v) for v in raw_values]
    na_flags = [(v == "N/A") for v in raw_values]

    values += values[:1]
    num = len(labels)
    angles = [(n / num) * 2 * pi for n in range(num)]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={"polar": True})

    ax.fill(angles, values, alpha=0.20, color="#00B4FF")
    ax.plot(angles, values, linewidth=2, color="#00B4FF")

    adjusted_labels = [
        f"{label}\nN/A" if na else label
        for label, na in zip(labels, na_flags)
    ]

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(adjusted_labels, fontsize=9)
    ax.set_ylim(0, 100)

    return fig


# ==========================================================
# BLOQUE 1 — DASHBOARD SGSI
# ==========================================================
def render_sgsi_monitor_dashboard():
    st.markdown(CARD_STYLE, unsafe_allow_html=True)

    tenant_id = get_active_tenant()
    tenant_color = st.session_state.get("primary_color", "#0048FF")

    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg,{tenant_color} 0%, #00B4FF 100%);
            padding:18px;border-radius:16px;color:white;text-align:center;margin-bottom:20px;">
            <h2 style="margin:0;">Monitorización SGSI — Panel General</h2>
            <p style="opacity:0.85;margin:0;">KPIs, gráficas, radar y análisis inteligente</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    df = db_get_kpi_log(tenant_id)
    if df.empty:
        st.warning("No existen KPIs aún.")
        return

    df["kpi_date"] = pd.to_datetime(df["kpi_date"])

    kpi_selected = st.selectbox("Selecciona KPI", sorted(df["kpi_name"].unique()))
    df_kpi = df[df["kpi_name"] == kpi_selected]

    c1, c2, c3 = st.columns(3)
    with c1:
        metric_card("Valor actual", df_kpi["kpi_value"].iloc[-1])
    with c2:
        metric_card("Promedio histórico", round(df_kpi["kpi_value"].mean(), 1))
    with c3:
        metric_card("Total registros", len(df_kpi))

    fig, ax = plt.subplots(figsize=(8, 3))
    ax.plot(df_kpi["kpi_date"], df_kpi["kpi_value"], marker="o", color=tenant_color)
    ax.set_ylim(0, 100)
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)

    st.markdown("---")

    st.subheader("Radar SGSI")
    pivot = df.pivot_table(index="kpi_name", values="kpi_value", aggfunc="last")
    radar_data = {k: v for k, v in zip(pivot.index, pivot["kpi_value"])}
    st.pyplot(radar_fig(radar_data))

    st.markdown("---")

    st.subheader("Comparativa normativa (ENS / ISO / NIST / NIS2)")

    comp = {
        "ISO 27001": radar_data.get("ISO Gap (%)", "N/A"),
        "ENS": radar_data.get("ENS Gap (%)", "N/A"),
        "NIST CSF": radar_data.get("NIST Gap (%)", "N/A"),
        "NIS2": radar_data.get("NIS2 Gap (%)", "N/A")
    }

    fig2, ax2 = plt.subplots(figsize=(6.5, 3))

    for i, (label, value) in enumerate(comp.items()):
        if value == "N/A":
            ax2.bar(label, 0, color="#CBD5E1")
            ax2.text(i, 5, "N/A", ha="center", color="#475569")
        else:
            ax2.bar(label, value, color=tenant_color)
            ax2.text(i, value + 2, f"{value}%", ha="center")

    ax2.set_ylim(0, 100)
    ax2.grid(axis="y", alpha=0.2)
    st.pyplot(fig2)

    st.markdown("---")

    st.subheader("Análisis Inteligente (Ellit Cognitive Core)")

    clean = {k: ("No aplica" if v == "N/A" else f"{v}%") for k, v in radar_data.items()}

    prompt = f"""
Eres Ellit Cognitive Core, módulo ejecutivo SGSI.

Analiza estos KPIs:

{json.dumps(clean, indent=2)}

Genera:
- Estado general
- Riesgos principales
- Áreas más débiles
- Acciones recomendadas (30 / 90 / 180 días)
- Conclusión ejecutiva
Extensión máxima: 12 líneas.
"""

    try:
        client = st.session_state["client"]
        resp = client.analyze_text(prompt)
        st.info(resp)
    except:
        st.info("No fue posible obtener el análisis en este momento.")


# ==========================================================
# BLOQUE 2 — REGISTRO HISTÓRICO
# ==========================================================
def render_sgsi_monitor_history():
    st.markdown("<h2>Registro histórico del SGSI</h2>", unsafe_allow_html=True)

    tenant_id = get_active_tenant()
    df = db_get_kpi_log(tenant_id)

    if df.empty:
        st.info("No hay registros aún.")
        return

    df["kpi_date"] = pd.to_datetime(df["kpi_date"])
    df.rename(columns={"kpi_date": "Fecha", "kpi_name": "KPI", "kpi_value": "Valor"}, inplace=True)

    col1, col2 = st.columns(2)
    with col1:
        filtro_kpi = st.selectbox("Filtrar por KPI", ["Todos"] + sorted(df["KPI"].unique()))
    with col2:
        filtro_fecha = st.date_input("Fecha mínima", None)

    filtered = df.copy()
    if filtro_kpi != "Todos":
        filtered = filtered[filtered["KPI"] == filtro_kpi]
    if filtro_fecha:
        filtered = filtered[filtered["Fecha"] >= pd.to_datetime(filtro_fecha)]

    st.dataframe(filtered, use_container_width=True)

    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button("Exportar CSV", csv, "sgsi_history.csv")


# ==========================================================
# BLOQUE 3 — EVIDENCIAS + KPIs
# ==========================================================
def render_sgsi_monitor_evidences():
    st.markdown("<h2>Evidencias y mantenimiento del SGSI</h2>", unsafe_allow_html=True)

    tenant_id = get_active_tenant()

    st.markdown("### Registrar nueva evidencia")
    col1, col2 = st.columns(2)

    with col1:
        evidencia = st.text_area("Descripción de la evidencia")
        normativa = st.selectbox("Marco aplicable", ["ISO 27001", "ENS", "NIST CSF", "NIS2", "GDPR", "SOC 2", "PCI DSS"])
    with col2:
        hallazgos = st.text_area("Hallazgos detectados")
        acciones = st.text_area("Acciones correctivas propuestas")

    st.markdown("### Actualización de KPIs")

    k1 = st.slider("Disponibilidad operativa (%)", 0, 100, 95)
    k2 = st.number_input("Incidentes críticos (30 días)", 0, 999, 1)
    k3 = st.number_input("Tiempo medio de respuesta (min)", 0, 9999, 45)
    k4 = st.slider("Controles implementados (%)", 0, 100, 80)

    st.markdown("### Cumplimiento normativo")

    iso_na = st.checkbox("ISO 27001 — No aplica (N/A)")
    gap_iso = "N/A" if iso_na else st.slider("ISO 27001 Gap (%)", 0, 100, 20)

    ens_na = st.checkbox("ENS — No aplica (N/A)")
    gap_ens = "N/A" if ens_na else st.slider("ENS Gap (%)", 0, 100, 25)

    nist_na = st.checkbox("NIST CSF — No aplica (N/A)")
    gap_nist = "N/A" if nist_na else st.slider("NIST Gap (%)", 0, 100, 30)

    nis2_na = st.checkbox("NIS2 — No aplica (N/A)")
    gap_nis2 = "N/A" if nis2_na else st.slider("NIS2 Gap (%)", 0, 100, 40)

    if st.button("Guardar evidencia y KPIs"):
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        kpis = {
            "Disponibilidad operativa (%)": k1,
            "Incidentes críticos (últimos 30 días)": k2,
            "Tiempo medio de respuesta (min)": k3,
            "Controles implementados (%)": k4,
            "ISO Gap (%)": gap_iso,
            "ENS Gap (%)": gap_ens,
            "NIST Gap (%)": gap_nist,
            "NIS2 Gap (%)": gap_nis2
        }

        for k, v in kpis.items():
            db_insert_kpi(tenant_id, k, v)

        conn = get_conn()
        conn.execute("""
            INSERT INTO sgsi_evidences (tenant_id, ev_date, evidence, findings, actions, framework)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (tenant_id, fecha, evidencia, hallazgos, acciones, normativa))
        conn.commit()
        conn.close()

        st.success("Datos guardados correctamente.")
        st.rerun()
