# ============================================================
#  EllitNow Shield — AI Executive Security Platform
#  UI Corporativa (Azul #10305C + Fucsia #E43480)
#  Versión completa y profesional — 2025
# ============================================================

import streamlit as st
import sqlite3
import bcrypt
import hashlib
import secrets
import uuid
from openai import OpenAI

# --- Librerías de análisis y visualización ---
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
import tempfile

# --- Librerías auxiliares ---
import stripe
import random
import base64
import json
import re
import io
import os
import gc
import time
import traceback
from math import pi
from datetime import datetime
from io import BytesIO

# --- Librerías de análisis y visualización ---
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
import tempfile

# --- ReportLab para PDF corporativo ---
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color
from reportlab.lib.utils import ImageReader
import datetime as _dt
from fpdf import FPDF
import textwrap
import tempfile
from io import BytesIO
import datetime as _dt
from core.cognitive_core import (
    init_openai,
    extract_json,
    analyze_radar_ia,
    generate_policy,
    generate_bcp_plan,
    generate_predictive_analysis,
    compute_sgsi_maturity,
)
client = init_openai(st.secrets["OPENAI_API_KEY"])

# ============================================================
# SISTEMA DE ESTILO CORPORATIVO
# ============================================================

ELLIT_BLUE = "#10305C"
ELLIT_BLUE_DARK = "#0D2D5A"
ELLIT_FUCHSIA = "#E43480"
ELLIT_WHITE = "#FFFFFF"

st.set_page_config(
    page_title="EllitNow Shield — Cognitive Security",
    layout="wide",
)

# ============================================================
# ESTILOS GLOBALES (AZUL + FUCSIA CORPORATIVO)
# ============================================================

st.markdown(f"""
<style>

html, body, [data-testid="stAppViewContainer"] {{
    overflow-x: hidden !important;
}}

div.block-container {{
    max-width: 1300px !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}}

section[data-testid="stSidebar"] {{
    background: {ELLIT_BLUE};
    padding: 1.5rem 0.8rem;
}}

section[data-testid="stSidebar"] .stMarkdown, 
section[data-testid="stSidebar"] label {{
    color: #FFFFFF !important;
}}

.sidebar-title {{
    font-size: 20px;
    font-weight: 600;
    color: #FFFFFF;
    margin-bottom: 15px;
}}

.ellit-hero {{
    background: linear-gradient(135deg, {ELLIT_BLUE} 0%, {ELLIT_BLUE_DARK} 40%, {ELLIT_FUCHSIA} 100%);
    padding: 70px 40px;
    border-radius: 22px;
    color: white;
    margin-top: 15px;
    margin-bottom: 35px;
}}

.ellit-hero h1 {{
    font-size: 42px;
    font-weight: 700;
}}

.ellit-hero p {{
    font-size: 18px;
    margin-top: -10px;
}}

.hero-btn {{
    background: {ELLIT_FUCHSIA};
    padding: 16px 36px;
    border-radius: 40px;
    color: white !important;
    font-weight: 600;
    border: none;
}}

.section-title {{
    font-size: 24px;
    font-weight: 700;
    margin-top: 10px;
    margin-bottom: 15px;
    color: {ELLIT_BLUE_DARK};
}}

.metric-box {{
    background: #F8FAFC;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #E2E8F0;
    text-align: center;
}}

.metric-label {{
    color: #64748B;
    font-size: 13px;
}}

.metric-value {{
    font-size: 22px;
    font-weight: 600;
    color: {ELLIT_BLUE};
}}

</style>
""", unsafe_allow_html=True)

# ============================================================
# BASE DE DATOS (LOGIN SEGURO)
# ============================================================

def init_db():
    conn = sqlite3.connect("ellit_users.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            password BLOB,
            tenant TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

def register_user(email, password, tenant):
    conn = sqlite3.connect("ellit_users.db")
    c = conn.cursor()
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
        c.execute("INSERT INTO users (email, password, tenant) VALUES (?, ?, ?)",
                  (email, hashed, tenant))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def login_user(email, password):
    conn = sqlite3.connect("ellit_users.db")
    c = conn.cursor()
    c.execute("SELECT password, tenant FROM users WHERE email = ?", (email,))
    row = c.fetchone()
    conn.close()

    if row:
        stored, tenant = row
        if bcrypt.checkpw(password.encode(), stored):
            return True, tenant
    return False, None

# ============================================================
# LOGIN / REGISTER UI
# ============================================================

if "logged" not in st.session_state:
    st.session_state["logged"] = False

if not st.session_state["logged"]:
    menu = st.sidebar.selectbox("Acceso", ["Iniciar sesión", "Registrarse"])

    if menu == "Registrarse":
        st.title("Crear cuenta EllitNow Shield")
        email = st.text_input("Correo corporativo")
        pwd = st.text_input("Contraseña", type="password")
        tenant = st.text_input("Nombre de empresa")

        if st.button("Registrar", use_container_width=True):
            if register_user(email, pwd, tenant):
                st.success("Cuenta creada. Ahora inicia sesión.")
            else:
                st.error("Error: este correo ya existe.")

    else:
        st.title("Acceso a EllitNow Shield")
        email = st.text_input("Correo")
        pwd = st.text_input("Contraseña", type="password")

        if st.button("Iniciar sesión", use_container_width=True):
            ok, tenant = login_user(email, pwd)
            if ok:
                st.session_state["logged"] = True
                st.session_state["tenant"] = tenant
                st.rerun()
            else:
                st.error("Credenciales incorrectas")

    st.stop()

tenant_name = st.session_state.get("tenant", "Organización")

# ============================================================
# HERO CORPORATIVO INICIAL (como tu imagen)
# ============================================================

st.markdown(f"""
<div class="ellit-hero">
    <h1>CYBERSECURITY & COMPLIANCE</h1>
    <p>We help your organization implement and maintain security frameworks such as ISO 27001, ENS, NIST and best practices.</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# TABS PRINCIPALES
# ============================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "Executive Overview",
    "Continuidad & Políticas",
    "Radar de Ciberinteligencia",
    "Predictive Intelligence"
])

# ============================================================
# TAB 1 — Executive Overview (🟦 incluye Evaluación SGSI)
# ============================================================

with tab1:

    st.markdown('<div class="section-title">Evaluación rápida de madurez SGSI</div>',
                unsafe_allow_html=True)

    col_m1, col_m2, col_m3 = st.columns(3)

    with col_m1:
        p_gob = st.slider("Gobernanza", 1, 5, 3)

    with col_m2:
        p_ops = st.slider("Operación y control", 1, 5, 3)

    with col_m3:
        p_risk = st.slider("Gestión de riesgos", 1, 5, 3)

    maturity_input = {
        "gobernanza": p_gob,
        "operacion": p_ops,
        "riesgos": p_risk,
        "tenant": tenant_name,
    }

    if st.button("Calcular madurez SGSI", type="primary"):
        with st.spinner("Procesando con Cognitive Core..."):
            result = compute_sgsi_maturity(client, maturity_input)

        st.subheader("Resultado SGSI (ENS / ISO 27001 / NIST CSF)")
        st.write(result)
# ============================================================
# TAB 2 — Continuidad & Políticas (con submenús en el sidebar)
# ============================================================

with tab2:

    st.markdown('<div class="section-title">Continuidad del Negocio & Gobierno</div>',
                unsafe_allow_html=True)

    st.sidebar.markdown("---")
    st.sidebar.markdown('<div class="sidebar-title">Continuidad & Políticas</div>', unsafe_allow_html=True)

    submenu = st.sidebar.radio(
        "Selecciona un módulo",
        [
            "Generador de Plan de Continuidad (ISO 22301 / ENS OP.BCP)",
            "Análisis cognitivo del contexto de continuidad",
            "Simulador de crisis BCP",
            "Generador avanzado de políticas",
        ]
    )

    # =======================================================
    # 1. Generador de Plan de Continuidad ISO 22301 / ENS
    # =======================================================
    if submenu == "Generador de Plan de Continuidad (ISO 22301 / ENS OP.BCP)":
        st.markdown("##  Generador de Plan de Continuidad ISO 22301 / ENS")

        col1, col2 = st.columns(2)

        with col1:
            objetivo = st.text_input("Objetivo del Plan", "Mantener la operación ante incidentes críticos.")
            alcance = st.text_area("Alcance", "Procesos esenciales, infraestructura crítica y personal clave.")
            criticidad = st.selectbox("Nivel de criticidad", ["Alta", "Media", "Baja"])

        with col2:
            rto = st.number_input("RTO objetivo (horas)", 1, 120, 24)
            rpo = st.number_input("RPO objetivo (horas)", 1, 120, 8)
            pais_bcp = st.text_input("Ubicación/Región", tenant_name)

        inputs_bcp = {
            "objetivo": objetivo,
            "alcance": alcance,
            "criticidad": criticidad,
            "rto": rto,
            "rpo": rpo,
            "region": pais_bcp,
            "tenant": tenant_name,
        }

        if st.button("Generar Plan BCP", use_container_width=True):
            with st.spinner("Generando plan de continuidad con Ellit Cognitive Core..."):
                plan = generate_bcp_plan(client, inputs_bcp)

            st.markdown("###  Resultado del Plan de Continuidad")
            st.write(plan)

    # =======================================================
    # 2. Análisis Cognitivo del Contexto de Continuidad
    # =======================================================
    elif submenu == "Análisis cognitivo del contexto de continuidad":
        st.markdown("##  Análisis Cognitivo del Contexto de Continuidad")

        desc_org = st.text_area(
            "Describe la situación organizacional",
            "Infraestructura crítica distribuida, dependencias en terceros, modelos híbridos…"
        )

        amenazas = st.text_area(
            "Describe amenazas relevantes",
            "Interrupción eléctrica, ransomware, fallos de terceros, desastres naturales…"
        )

        insumos_ctx = {
            "descripcion": desc_org,
            "amenazas": amenazas,
            "tenant": tenant_name
        }

        if st.button("Analizar contexto", use_container_width=True):
            with st.spinner("Procesando contexto estratégico..."):
                ctx = analyze_radar_ia(client, insumos_ctx)

            st.subheader(" Inteligencia contextual generada")
            st.write(ctx)

    # =======================================================
    # 3. Simulador de Crisis BCP
    # =======================================================
    elif submenu == "Simulador de crisis BCP":
        st.markdown("##  Simulador de Crisis — Business Continuity")

        escenario = st.selectbox(
            "Escenario de crisis",
            [
                "Ransomware total en infraestructura",
                "Pérdida total de CPD / Data Center",
                "Caída de proveedor crítico",
                "Brecha masiva de datos",
                "Interrupción eléctrica prolongada",
                "Desastre natural",
            ]
        )

        tiempo = st.slider("Duración estimada del incidente (horas)", 1, 240, 12)

        insumos_sim = {
            "escenario": escenario,
            "duracion": tiempo,
            "tenant": tenant_name,
        }

        if st.button("Ejecutar simulación", use_container_width=True):
            with st.spinner("Ejecutando simulación predictiva..."):
                sim = generate_predictive_analysis(client, insumos_sim)

            st.subheader(" Simulación de impacto y respuesta")
            st.write(sim)

    # =======================================================
    # 4. Generador de Políticas Automáticas (ISO/ENS/GDPR)
    # =======================================================
    elif submenu == "Generador avanzado de políticas":
        st.markdown("##  Generador Automático de Políticas")

        tipo = st.selectbox(
            "Tipo de política a generar",
            [
                "Política de Seguridad de la Información (ISO 27001 / ENS)",
                "Política de Protección de Datos (GDPR)",
                "Política de Continuidad del Negocio",
                "Política de Gestión de Incidentes",
                "Política de Gestión de Riesgos",
                "Política de Control de Acceso",
            ]
        )

        detalles = st.text_area(
            "Contexto / personalización",
            "Añade detalles específicos del negocio, regulaciones o requisitos."
        )

        insumos_pol = {
            "tipo": tipo,
            "detalles": detalles,
            "tenant": tenant_name,
        }

        if st.button("Generar política", use_container_width=True):
            with st.spinner("Generando documentación oficial..."):
                pol = generate_policy(client, insumos_pol)

            st.subheader(" Política generada")
            st.write(pol)
# ============================================================
# TAB 3 — Radar de Ciberinteligencia (con submenús)
# ============================================================

with tab3:

    st.markdown('<div class="section-title">Radar de Ciberinteligencia</div>',
                unsafe_allow_html=True)

    st.sidebar.markdown("---")
    st.sidebar.markdown('<div class="sidebar-title">Ciberinteligencia</div>', unsafe_allow_html=True)

    submenu_cyb = st.sidebar.radio(
        "Selecciona un módulo",
        [
            "Radar global de amenazas",
            "Análisis cognitivo de indicadores (IoCs)",
            "Resumen ejecutivo para CISO",
        ]
    )

    # =======================================================
    # 1. Radar global de amenazas
    # =======================================================
    if submenu_cyb == "Radar global de amenazas":
        st.markdown("##  Radar Global de Amenazas — Cognitive Core")

        st.info(
            "Este radar analiza amenazas globales basadas en riesgo, intensidad y proximidad sectorial."
        )

        # Entradas para análisis
        col1, col2, col3 = st.columns(3)

        with col1:
            industria = st.selectbox(
                "Industria",
                [
                    "Banca", "Salud", "Retail", "Energía", "Tecnología",
                    "Manufactura", "Gobierno", "Educación"
                ]
            )
        with col2:
            region_radar = st.text_input("Región", "Europa")
        with col3:
            horizonte = st.selectbox(
                "Horizonte de análisis",
                ["1 mes", "3 meses", "6 meses", "12 meses"]
            )

        insumos_radar = {
            "industria": industria,
            "region": region_radar,
            "horizonte": horizonte,
            "tenant": tenant_name
        }

        if st.button("Generar Radar", use_container_width=True):
            with st.spinner("Analizando amenazas globales..."):
                radar = analyze_radar_ia(client, insumos_radar)

            st.markdown("###  Resultados del Radar")
            st.write(radar)

    # =======================================================
    # 2. Análisis cognitivo de indicadores (IoCs)
    # =======================================================
    elif submenu_cyb == "Análisis cognitivo de indicadores (IoCs)":

        st.markdown("##  Análisis Cognitivo de IoCs")

        st.write("Carga indicadores técnicos (IPs, hashes, dominios, URLs) para un análisis contextual avanzado.")

        iocs_raw = st.text_area(
            "Introduce IoCs (uno por línea)",
            "malicious-domain.com\n45.178.23.1\nb6f8c24ea7d4..."
        )

        if st.button("Analizar IoCs", use_container_width=True):
            lista_iocs = [line.strip() for line in iocs_raw.split("\n") if line.strip()]

            insumos_iocs = {
                "iocs": lista_iocs,
                "tenant": tenant_name
            }

            with st.spinner("Procesando inteligencia contextual..."):
                resultado_iocs = analyze_radar_ia(client, insumos_iocs)

            st.subheader(" Análisis cognitivo de los IoCs")
            st.write(resultado_iocs)

    # =======================================================
    # 3. Resumen ejecutivo para el CISO
    # =======================================================
    elif submenu_cyb == "Resumen ejecutivo para CISO":

        st.markdown("##  Resumen Ejecutivo para CISO")

        st.write(
            "Genera un resumen ejecutivo automatizado basado en tu industria, región y perfil de riesgo."
        )

        col1, col2 = st.columns(2)

        with col1:
            sector_exec = st.selectbox(
                "Sector",
                [
                    "Banca", "Seguros", "Salud", "Gobierno",
                    "Telecomunicaciones", "Retail", "Tecnología"
                ]
            )

        with col2:
            region_exec = st.text_input("Región", "Europa")

        insumos_exec = {
            "sector": sector_exec,
            "region": region_exec,
            "tenant": tenant_name
        }

        if st.button("Generar Resumen Ejecutivo", use_container_width=True):
            with st.spinner("Generando informe ejecutivo..."):
                resumen = generate_predictive_analysis(client, insumos_exec)

            st.subheader("📄 Resumen Ejecutivo del Radar")
            st.write(resumen)
# ============================================================
# TAB 4 — Ellit Predictive Intelligence Suite
# ============================================================

with tab4:

    # ============================================================
    # Barra lateral — Submenús profesionales
    # ============================================================
    st.sidebar.markdown("---")
    st.sidebar.markdown('<div class="sidebar-title">Predictive Intelligence</div>', unsafe_allow_html=True)

    submenu_pred = st.sidebar.radio(
        "Selecciona un módulo",
        [
            "Análisis Predictivo Principal",
            "Benchmark sectorial",
            "Insights y Recomendaciones",
        ]
    )

    # ============================================================
    # 1. ANÁLISIS PREDICTIVO PRINCIPAL
    # ============================================================
    if submenu_pred == "Análisis Predictivo Principal":

        st.markdown("""
        <div class="section-title">Ellit Predictive Intelligence — Cognitive Core</div>
        """, unsafe_allow_html=True)

        st.write(
            "Genera un análisis predictivo basado en sector, región y nivel actual de madurez para obtener un panorama de riesgo futuro."
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            sector_p = st.selectbox(
                "Sector",
                [
                    "Banca y Finanzas",
                    "Seguros",
                    "Salud",
                    "Tecnología",
                    "Retail",
                    "Energía",
                    "Telecomunicaciones",
                    "Gobierno",
                    "Educación",
                    "Manufactura",
                ]
            )

        with col2:
            region_p = st.text_input("Región", "Europa")

        with col3:
            madurez_p = st.slider("Madurez ENS/ISO declarada", 1, 5, 3)

        base_costos = {
            "Banca y Finanzas": 520000,
            "Seguros": 350000,
            "Salud": 480000,
            "Tecnología": 400000,
            "Retail": 310000,
            "Energía": 600000,
            "Telecomunicaciones": 450000,
            "Gobierno": 300000,
            "Educación": 250000,
            "Manufactura": 370000,
        }

        costo_promedio = base_costos.get(sector_p, 350000)

        predictive_input = {
            "sector": sector_p,
            "region": region_p,
            "madurez": madurez_p,
            "costo_medio_sector": costo_promedio,
            "tenant": tenant_name,
        }

        if st.button("Generar análisis predictivo", use_container_width=True):
            with st.spinner("Analizando datos sectoriales..."):
                predictive_data = generate_predictive_analysis(client, predictive_input)

            if predictive_data:

                riesgo_raw = predictive_data.get("riesgo_sectorial", "")
                riesgo_num = re.findall(r"\d+", str(riesgo_raw))
                riesgo_sectorial = int(riesgo_num[0]) if riesgo_num else random.randint(60, 95)

                impacto_raw = predictive_data.get("impacto_estimado", "")
                impacto_num = re.findall(r"\d+", str(impacto_raw).replace(".", ""))
                impacto_valor = (
                    int(impacto_num[0]) if impacto_num else costo_promedio * (riesgo_sectorial / 100)
                )

                st.session_state["riesgo_sectorial_pred"] = riesgo_sectorial
                st.session_state["impacto_sectorial_pred"] = impacto_valor
                st.session_state["amenazas_pred"] = predictive_data.get("amenazas_emergentes", [])
                st.session_state["tendencias_pred"] = predictive_data.get("tendencias", [])
                st.session_state["recomendaciones_pred"] = predictive_data.get("recomendaciones", [])

                st.success("Análisis Predictivo generado correctamente.")

        if "riesgo_sectorial_pred" in st.session_state:

            r_val = st.session_state["riesgo_sectorial_pred"]
            i_val = st.session_state["impacto_sectorial_pred"]

            st.markdown("### 📊 Indicadores Clave de Riesgo (KPIs)")

            k1, k2, k3, k4 = st.columns(4)

            k1.metric("Riesgo sectorial", f"{r_val}%")
            k2.metric("Madurez declarada", f"{madurez_p}/5")
            k3.metric("Coste medio sectorial", f"{costo_promedio:,.0f} €")
            k4.metric("Impacto estimado", f"{i_val:,.0f} €")

            st.markdown("---")
            st.markdown("###  Panel Predictivo")

            col_pred1, col_pred2 = st.columns([2, 1])

            # ============================================================
            # Gráfico principal — Impacto vs Madurez
            # ============================================================
            with col_pred1:
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=[madurez_p],
                    y=[i_val],
                    mode="markers",
                    marker=dict(size=20, color="#D93B8A"),
                    name="Tu organización"
                ))

                fig.update_layout(
                    title="Impacto estimado vs Madurez actual",
                    xaxis_title="Madurez ENS/ISO",
                    yaxis_title="Impacto (€)",
                    height=420,
                    template="plotly_white"
                )
                st.plotly_chart(fig, use_container_width=True)

            # ============================================================
            # Inteligencia cognitiva — lado derecho
            # ============================================================
            with col_pred2:
                st.markdown("###  Inteligencia del Cognitive Core")

                for threat in st.session_state.get("amenazas_pred", []):
                    st.markdown(f"⚠️ **{threat}**")

                st.markdown("###  Tendencias")
                for trend in st.session_state.get("tendencias_pred", []):
                    st.markdown(f"- {trend}")

                st.markdown("###  Recomendaciones Estratégicas")
                for rec in st.session_state.get("recomendaciones_pred", []):
                    st.markdown(f"- {rec}")

    # ============================================================
    # 2. BENCHMARK SECTORIAL
    # ============================================================
    elif submenu_pred == "Benchmark sectorial":

        st.markdown('<div class="section-title">Benchmark Sectorial — Cognitive Core</div>',
                    unsafe_allow_html=True)

        st.write("Compara tu madurez y riesgo frente al promedio de tu industria.")

        sector_b = st.selectbox(
            "Selecciona tu sector",
            [
                "Banca y Finanzas",
                "Seguros",
                "Salud",
                "Tecnología",
                "Retail",
                "Energía",
                "Gobierno",
                "Educación",
                "Manufactura"
            ]
        )

        madurez_org = st.slider("Tu nivel de madurez", 1, 5, 3)

        comparativa = {
            "Banca y Finanzas": 4,
            "Seguros": 3,
            "Salud": 3,
            "Tecnología": 4,
            "Retail": 2,
            "Energía": 4,
            "Gobierno": 3,
            "Educación": 2,
            "Manufactura": 3,
        }

        media_sector = comparativa.get(sector_b, 3)

        st.markdown("###  Comparativa de madurez")
        c1, c2 = st.columns(2)

        with c1:
            st.metric("Tu organización", f"{madurez_org}/5")

        with c2:
            st.metric("Media del sector", f"{media_sector}/5")

        st.markdown("---")

        fig_b = go.Figure(data=[
            go.Bar(
                name="Tu organización",
                x=["Madurez"],
                y=[madurez_org],
                marker_color="#D93B8A"
            ),
            go.Bar(
                name="Sector",
                x=["Madurez"],
                y=[media_sector],
                marker_color="#0B2951"
            )
        ])

        fig_b.update_layout(
            title="Comparativa de madurez",
            barmode="group",
            height=420,
            template="plotly_white"
        )

        st.plotly_chart(fig_b, use_container_width=True)

    # ============================================================
    # 3. INSIGHTS Y RECOMENDACIONES
    # ============================================================
    elif submenu_pred == "Insights y Recomendaciones":

        st.markdown('<div class="section-title">Insights Avanzados para CISOs</div>',
                    unsafe_allow_html=True)

        st.write(
            "Obtén insights estratégicos generados en tiempo real basados en amenazas, tendencias y nivel de madurez."
        )

        ins_input = st.text_area(
            "Describe tu situación actual",
            "Ejemplo: Nuestro SOC no trabaja 24x7, tenemos dependencias críticas externas..."
        )

        if st.button("Generar Insights", use_container_width=True):
            with st.spinner("Generando insights con Cognitive Core..."):
                insights = generate_predictive_analysis(
                    client,
                    {"contexto": ins_input, "tenant": tenant_name}
                )

            st.write("###  Insights del Cognitive Core")
            st.write(insights)
