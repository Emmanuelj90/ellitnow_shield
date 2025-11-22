# ==========================================================
# ELLIT SGSI MONITOR – MÓDULO COMPLETO (BLOQUE 1/3)
# ==========================================================
# Incluye:
# - Dashboard SGSI con KPIs y Radar
# - Registro histórico completo
# - Integración con Ellit Cognitive Core
# - Diseño corporativo profesional
# ==========================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import uuid
import base64
from datetime import datetime
from math import pi

from app import get_conn
from cognitive_core import (
    analyze_kpi_drift,
    classify_evidence,
    sgsi_gap_analysis
)

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
    margin-top: 4px;
}
.evidence-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 16px;
    margin-bottom: 10px;
}
.evidence-meta {
    font-size: 12px;
    color: #64748B;
}
.table-clean thead tr th {
    background-color: #F1F5F9;
    font-size: 13px;
    padding: 6px;
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
# BASE DE DATOS – CONSULTAS
# ==========================================================
def db_get_kpis(tenant_id):
    conn = get_conn()
    df = pd.read_sql_query("""
        SELECT fecha, kpi, valor, usuario
        FROM sgsi_kpi_history
        WHERE tenant_id = ?
        ORDER BY fecha ASC
    """, conn, params=(tenant_id,))
    conn.close()
    return df


def db_insert_kpi(tenant_id, kpi_name, valor, usuario):
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        INSERT INTO sgsi_kpi_history (id, tenant_id, fecha, kpi, valor, usuario)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        str(uuid.uuid4()),
        tenant_id,
        datetime.now().strftime("%Y-%m-%d %H:%M"),
        kpi_name,
        valor,
        usuario
    ))
    conn.commit()
    conn.close()


def db_delete_kpi(kpi_id):
    conn = get_conn()
    conn.execute("DELETE FROM sgsi_kpi_history WHERE id = ?", (kpi_id,))
    conn.commit()
    conn.close()


# ==========================================================
# RADAR CHART
# ==========================================================
def radar_fig(kpis):
    labels = list(kpis.keys())
    values = list(kpis.values())

    values += values[:1]
    num = len(labels)
    angles = [(n / num) * 2 * pi for n in range(num)]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={"polar": True})
    ax.fill(angles, values, alpha=0.20, color="#00B4FF")
    ax.plot(angles, values, linewidth=2, color="#00B4FF")

    ax.set_ylim(0, 100)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=10)

    return fig


# ==========================================================
# PANEL GENERAL – DASHBOARD SGSI
# ==========================================================
def render_sgsi_monitor_dashboard():

    st.markdown(CARD_STYLE, unsafe_allow_html=True)

    tenant_id = get_active_tenant()
    tenant_color = st.session_state.get("primary_color", "#0048FF")
    user_email = st.session_state.get("user_email", "usuario")

    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg,{tenant_color} 0%, #00B4FF 100%);
            padding:18px;border-radius:16px;color:white;text-align:center;
            margin-bottom:20px;">
            <h2 style="margin:0;">Monitorización SGSI — Panel General</h2>
            <p style="opacity:0.85;margin:0;">KPIs, gráficas y análisis inteligente</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Cargar KPIs
    df = db_get_kpis(tenant_id)

    if df.empty:
        st.warning("No existen KPIs aún para este tenant.")
        st.info("Puedes agregar KPIs desde el módulo de Registro Histórico.")
        return

    # Selección de KPI
    kpi_selected = st.selectbox("Selecciona una métrica para analizar", sorted(df["kpi"].unique()))

    df_kpi = df[df["kpi"] == kpi_selected]

    # TARJETAS
    c1, c2, c3 = st.columns(3)
    with c1:
        metric_card("Valor actual", f"{df_kpi['valor'].iloc[-1]:.0f}%")
    with c2:
        metric_card("Promedio histórico", f"{df_kpi['valor'].mean():.1f}%")
    with c3:
        metric_card("Total registros", len(df_kpi))

    # GRÁFICA DE TENDENCIA
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.plot(df_kpi["fecha"], df_kpi["valor"], marker="o", linewidth=2, color=tenant_color)
    ax.set_ylim(0, 100)
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)

    st.markdown("---")

    # RADAR CHART – KPIs normalizadas
    st.subheader("Radar de Madurez SGSI")

    pivot = df.pivot_table(index="kpi", values="valor", aggfunc="last")
    radar_data = {k: float(v) for k, v in zip(pivot.index, pivot["valor"])}

    st.pyplot(radar_fig(radar_data))

    st.markdown("---")

    # ANÁLISIS COGNITIVO
    st.subheader("Inteligencia del SGSI — Ellit Cognitive Core")

    with st.spinner("Analizando comportamiento histórico..."):
        result = analyze_kpi_drift(df, kpi_selected)

    if result:
        st.info(result)
    else:
        st.info("No se detectaron anomalías relevantes.")


# ==========================================================
# REGISTRO HISTÓRICO – CRUD COMPLETO
# ==========================================================
def render_sgsi_monitor_history():

    st.markdown(CARD_STYLE, unsafe_allow_html=True)

    tenant_id = get_active_tenant()
    user_email = st.session_state.get("user_email", "usuario")

    st.markdown("## Registro histórico SGSI")

    df = db_get_kpis(tenant_id)

    # -----------------------------
    # FORMULARIO DE NUEVO KPI
    # -----------------------------
    with st.expander("Añadir nueva métrica KPI"):
        kpi_name = st.text_input("Nombre de la KPI", placeholder="Ej: Disponibilidad Operativa")
        valor = st.slider("Valor (%)", 0, 100, 80)

        if st.button("Guardar KPI"):
            if not kpi_name:
                st.warning("Debes introducir un nombre.")
            else:
                db_insert_kpi(tenant_id, kpi_name, valor, user_email)
                st.success("KPI guardada.")
                st.experimental_rerun()

    st.markdown("---")

    if df.empty:
        st.info("Aún no existen KPIs registradas.")
        return

    # -----------------------------
    # FILTROS
    # -----------------------------
    col1, col2 = st.columns(2)
    with col1:
        filtro_kpi = st.selectbox("Filtrar por KPI", ["Todas"] + sorted(df["kpi"].unique()))
    with col2:
        filtro_usuario = st.selectbox("Filtrar por usuario", ["Todos"] + sorted(df["usuario"].unique()))

    df_filtered = df.copy()
    if filtro_kpi != "Todas":
        df_filtered = df_filtered[df_filtered["kpi"] == filtro_kpi]
    if filtro_usuario != "Todos":
        df_filtered = df_filtered[df_filtered["usuario"] == filtro_usuario]

    # -----------------------------
    # TABLA
    # -----------------------------
    st.dataframe(df_filtered)

    # -----------------------------
    # EXPORTAR CSV
    # -----------------------------
    csv = df_filtered.to_csv(index=False).encode("utf-8")
    st.download_button("Exportar CSV", csv, "historico_kpis.csv")

    # -----------------------------
    # BORRAR REGISTRO
    # -----------------------------
    st.markdown("### Borrar registro")
    ids = st.selectbox("Selecciona ID", df["fecha"].index)

    if st.button("Eliminar registro seleccionado"):
        db_delete_kpi(df.iloc[ids]["id"])
        st.success("Registro eliminado.")
        st.experimental_rerun()

# ===============================================================
# BLOQUE 2 — DASHBOARD PRINCIPAL DE MONITORIZACIÓN SGSI
# ===============================================================

def render_sgsi_monitor_dashboard(tenant_id: str):
    """
    Panel principal del sistema de monitorización SGSI.
    Presenta KPIs agregados, comparativas, tendencias
    y gráficos tipo SAAS para visualización ejecutiva.
    """

    st.markdown("""
        <h2 style='margin-bottom:10px;'>Panel de monitorización SGSI</h2>
        <p style='color:#A0AEC0;margin-top:-10px;'>Visión ejecutiva del estado del sistema de gestión de seguridad.</p>
    """, unsafe_allow_html=True)

    # -----------------------------------------
    # 1) Cargar datos desde la base de datos
    # -----------------------------------------
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
        SELECT kpi_date, kpi_name, kpi_value
        FROM sgsi_kpis
        WHERE tenant_id = ?
        ORDER BY kpi_date ASC
    """, (tenant_id,))

    rows = c.fetchall()
    conn.close()

    if not rows:
        st.info("No existen datos de KPIs del SGSI aún para este tenant.")
        st.write("Introduce tus primeros valores en el apartado 'Evidencias y mantenimiento'.")
        return

    # Convertir a DataFrame
    df = pd.DataFrame(rows, columns=["fecha", "kpi", "valor"])
    df["fecha"] = pd.to_datetime(df["fecha"])
    df = df.sort_values("fecha")

    # KPIs principales (último valor registrado)
    latest = df.groupby("kpi").tail(1).set_index("kpi")["valor"].to_dict()

    # -----------------------------------------
    # 2) Cards ejecutivas superiores
    # -----------------------------------------
    kpi1 = latest.get("Disponibilidad operativa (%)", 0)
    kpi2 = latest.get("Incidentes críticos (últimos 30 días)", 0)
    kpi3 = latest.get("Tiempo medio de respuesta (min)", 0)
    kpi4 = latest.get("Controles implementados (%)", 0)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Disponibilidad operativa", f"{kpi1}%")
    with c2:
        st.metric("Incidentes críticos", int(kpi2))
    with c3:
        st.metric("Tiempo medio de respuesta", f"{kpi3} min")
    with c4:
        st.metric("Controles implementados", f"{kpi4}%")

    st.markdown("---")

    # -----------------------------------------
    # 3) Gráficos tipo SAAS (líneas de tendencia)
    # -----------------------------------------
    st.subheader("Tendencias del Sistema SGSI")

    kpis_unicos = df["kpi"].unique()

    for k in kpis_unicos:
        subdf = df[df["kpi"] == k]

        st.markdown(f"### {k}")

        fig, ax = plt.subplots(figsize=(6.5, 2.8))
        ax.plot(subdf["fecha"], subdf["valor"], linewidth=2)

        ax.set_title(k, loc="left", fontsize=10)
        ax.set_xlabel("")
        ax.set_ylabel("")
        ax.grid(True, alpha=0.2)

        st.pyplot(fig)

        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("---")

    # -----------------------------------------
    # 4) Comparativa normativa (ENS / ISO / NIST / NIS2)
    # -----------------------------------------

    st.subheader("Comparativa normativa ENS / ISO 27001 / NIST / NIS2")

    comp_data = {
        "ENS": latest.get("ENS Gap (%)", 0),
        "ISO 27001": latest.get("ISO Gap (%)", 0),
        "NIST CSF": latest.get("NIST Gap (%)", 0),
        "NIS2": latest.get("NIS2 Gap (%)", 0)
    }

    labels = list(comp_data.keys())
    values = list(comp_data.values())

    fig2, ax2 = plt.subplots(figsize=(6.5, 3))
    bars = ax2.bar(labels, values)

    for bar in bars:
        height = bar.get_height()
        ax2.text(
            bar.get_x() + bar.get_width() / 2,
            height + 1,
            f"{height:.0f}%",
            ha='center', fontsize=10
        )

    ax2.set_ylim(0, 100)
    ax2.set_ylabel("Nivel de cumplimiento (%)")
    ax2.grid(axis='y', alpha=0.2)

    st.pyplot(fig2)

    st.markdown("---")

    # -----------------------------------------
    # 5) Análisis de IA
    # ----------------------
    st.subheader("Análisis automático del Ellit Cognitive Core")

    resumen_ia = generate_sgsi_ai_summary(latest)

    st.info(resumen_ia)

# ===============================================================
# BLOQUE 3 — REGISTRO HISTÓRICO Y EVIDENCIAS DEL SGSI
# ===============================================================

# ---------------------------------------------------------------
# 1) HISTÓRICO DE KPIs (Tabla + Exportación)
# ---------------------------------------------------------------
def render_sgsi_monitor_history():
    st.markdown("<h2>Registro histórico del SGSI</h2>", unsafe_allow_html=True)

    tenant_id = st.session_state.get("tenant_id")

    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        SELECT kpi_date, kpi_name, kpi_value
        FROM sgsi_kpis
        WHERE tenant_id = ?
        ORDER BY kpi_date DESC
    """, (tenant_id,))
    rows = c.fetchall()
    conn.close()

    if not rows:
        st.info("Aún no existen registros históricos para este tenant.")
        return

    df = pd.DataFrame(rows, columns=["Fecha", "KPI", "Valor"])
    df["Fecha"] = pd.to_datetime(df["Fecha"])

    # Filtros
    col1, col2 = st.columns(2)
    with col1:
        filtro_kpi = st.selectbox("Filtrar por KPI", ["Todos"] + sorted(df["KPI"].unique().tolist()))
    with col2:
        filtro_fecha = st.date_input("Fecha mínima", None)

    filtered = df.copy()

    if filtro_kpi != "Todos":
        filtered = filtered[filtered["KPI"] == filtro_kpi]

    if filtro_fecha:
        filtered = filtered[filtered["Fecha"] >= pd.to_datetime(filtro_fecha)]

    st.dataframe(filtered, use_container_width=True)

    # Exportación
    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Exportar CSV",
        csv,
        "sgsi_history_export.csv",
        "text/csv"
    )


# ---------------------------------------------------------------
# 2) FORMULARIO DE EVIDENCIAS + REGISTRO DE KPIs
# ---------------------------------------------------------------
def render_sgsi_monitor_evidences():
    st.markdown("<h2>Evidencias y mantenimiento del SGSI</h2>", unsafe_allow_html=True)

    tenant_id = st.session_state.get("tenant_id")

    st.markdown("### Registrar nueva evidencia")

    col1, col2 = st.columns(2)

    with col1:
        evidencia = st.text_area(
            "Descripción de la evidencia",
            placeholder="Ej: Auditoría interna realizada el 03/02/2025 con 2 no conformidades menores..."
        )
        normativa = st.selectbox(
            "Marco aplicable",
            ["ISO 27001", "ENS", "NIST CSF", "NIS2", "GDPR", "SOC 2", "PCI DSS"]
        )

    with col2:
        hallazgos = st.text_area(
            "Hallazgos detectados",
            placeholder="Ej: Incumplimiento en control de accesos remotos, MFA no aplicado..."
        )
        acciones = st.text_area(
            "Acciones correctivas propuestas",
            placeholder="Ej: Implementar MFA en VPN antes del 30/03/2025."
        )

    st.markdown("### Actualización de KPIs del SGSI")

    # KPIs editables desde el panel
    kpi1 = st.slider("Disponibilidad operativa (%)", 0, 100, 95)
    kpi2 = st.number_input("Incidentes críticos (últimos 30 días)", 0, 999, 1)
    kpi3 = st.number_input("Tiempo medio de respuesta (min)", 0, 9999, 45)
    kpi4 = st.slider("Controles implementados (%)", 0, 100, 80)

    # Gaps normativos
    gap_iso = st.slider("ISO 27001 Gap (%)", 0, 100, 20)
    gap_ens = st.slider("ENS Gap (%)", 0, 100, 25)
    gap_nist = st.slider("NIST Gap (%)", 0, 100, 30)
    gap_nis2 = st.slider("NIS2 Gap (%)", 0, 100, 40)

    if st.button("Guardar evidencia y KPIs"):
        conn = get_conn()
        c = conn.cursor()

        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Guardar KPIs
        kpis = {
            "Disponibilidad operativa (%)": kpi1,
            "Incidentes críticos (últimos 30 días)": kpi2,
            "Tiempo medio de respuesta (min)": kpi3,
            "Controles implementados (%)": kpi4,
            "ISO Gap (%)": gap_iso,
            "ENS Gap (%)": gap_ens,
            "NIST Gap (%)": gap_nist,
            "NIS2 Gap (%)": gap_nis2
        }

        for k, v in kpis.items():
            c.execute("""
                INSERT INTO sgsi_kpis (tenant_id, kpi_date, kpi_name, kpi_value)
                VALUES (?, ?, ?, ?)
            """, (tenant_id, fecha, k, v))

        # Guardar evidencia
        c.execute("""
            INSERT INTO sgsi_evidences (tenant_id, ev_date, evidence, findings, actions, framework)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (tenant_id, fecha, evidencia, hallazgos, acciones, normativa))

        conn.commit()
        conn.close()

        st.success("Evidencia y KPIs guardados correctamente.")


# ---------------------------------------------------------------
# 3) MOTOR DE ANÁLISIS IA (RESUMEN EJECUTIVO DEL SGSI)
# ---------------------------------------------------------------
def generate_sgsi_ai_summary(latest_kpis: dict) -> str:
    """
    Recibe los últimos KPIs del tenant y genera
    un análisis ejecutivo automático.
    """

    try:
        prompt = f"""
Eres Ellit Cognitive Core, módulo ejecutivo de análisis SGSI.

Analiza estos KPIs y genera un resumen profesional:

KPIs:
{json.dumps(latest_kpis, indent=2)}

Genera:
- Estado general del SGSI
- Riesgos principales
- Áreas más débiles
- Acciones recomendadas a 30, 90 y 180 días
- Conclusión ejecutiva

Extensión: 12 líneas máximo.
"""
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[{"role": "system", "content": "Analista SGSI senior."},
                      {"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content.strip()

    except Exception:
        return "No fue posible generar el análisis automático en este momento."


