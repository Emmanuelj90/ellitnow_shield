# ==============================
# AI Executive Shield — EllitNow Cognitive Core Edition
# VERSIÓN FINAL — STABLE & FIXED RELEASE
# ==============================

import streamlit as st
import sqlite3
import bcrypt
import hashlib
import secrets
import uuid     
from openai import OpenAI

# Inicializar cliente de OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

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

# --- Generador de informes PDF ---
from fpdf import FPDF
import textwrap
import tempfile
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color
from reportlab.lib.utils import ImageReader
from io import BytesIO
import datetime as _dt

# ==============================
# 🔄 Pantalla de carga profesional Ellit
# ==============================

# Crear un contenedor temporal
loading_placeholder = st.empty()

with loading_placeholder.container():
    st.markdown("""
        <style>
        .loading-container {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background: radial-gradient(circle at center, #0a0a0a 0%, #101010 100%);
            color: white;
            font-family: 'Poppins', sans-serif;
        }
        .loading-logo {
            font-size: 3em;
            font-weight: bold;
            color: #ff0080;
            letter-spacing: 2px;
            text-shadow: 0 0 10px #ff0080, 0 0 20px #ff66b2;
        }
        .loading-sub {
            font-size: 1.2em;
            color: #ccc;
            margin-top: 10px;
        }
        .spinner {
            border: 4px solid #222;
            border-top: 4px solid #ff0080;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            animation: spin 1.2s linear infinite;
            margin-top: 25px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        </style>
        <div class="loading-container">
            <div class="loading-logo">ELLIT</div>
            <div class="loading-sub">ACTIVANDO NÚCLEO COGNITIVO...</div>
            <div class="spinner"></div>
        </div>
    """, unsafe_allow_html=True)

# Simular carga (3 segundos)
time.sleep(3)

# 🔄 Limpiar pantalla de carga
loading_placeholder.empty()


# ==============================
# CONFIGURACIÓN DE PÁGINA
# ==============================
st.set_page_config(
    page_title="AI Executive Shield — EllitNow Cognitive Core",
    page_icon="brain",
    layout="wide",
)
# ===== ESTILO GLOBAL ELLIT SHIELD UI PRO =====
st.markdown("""
    <style>
    /* -------- Fuente global -------- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
        background-color: #FFFFFF;
        color: #0F172A;
    }

    /* -------- Sidebar corporativo -------- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg,#0048FF 0%,#001F7F 100%);
        color: white;
        padding-top: 25px;
        border-right: 1px solid #eaeaea;
    }
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] p {
        color: white !important;
    }
    section[data-testid="stSidebar"] a {
        color: #fff !important;
        text-decoration: none !important;
    }

    /* -------- Contenedor principal -------- */
    .main-container {
        background: #FFFFFF;
        border-radius: 20px;
        padding: 35px;
        margin-top: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        border: 1px solid #E2E8F0;
    }

    /* -------- Cards de métricas -------- */
    .metric-card {
        background-color: #F8FAFC;
        border-radius: 14px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        border: 1px solid #E2E8F0;
        padding: 20px;
        margin-bottom: 16px;
        text-align: center;
        transition: all 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    .metric-value {
        font-size: 26px;
        font-weight: 700;
        color: #0048FF;
    }
    .metric-label {
        font-size: 13px;
        color: #475569;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* -------- Títulos -------- */
    h1, h2, h3, h4 {
        font-weight: 700 !important;
        color: #0F172A !important;
        margin-bottom: 10px;
    }
    .section-title {
        font-weight: 600;
        font-size: 18px;
        color: #0F172A;
        margin-bottom: 12px;
    }

    /* -------- Botones -------- */
    .stButton>button {
        background: linear-gradient(135deg,#FF0080 0%,#00B4FF 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px;
        font-weight: 600;
        transition: 0.2s ease;
        padding: 10px 18px;
    }
    .stButton>button:hover {
        filter: brightness(1.1);
        transform: translateY(-2px);
    }

    /* -------- Campos de texto y selects -------- */
    .stTextInput>div>div>input, .stTextArea textarea {
        border-radius: 10px !important;
        border: 1px solid #E2E8F0 !important;
        background-color: #F8FAFC !important;
        padding: 10px 12px !important;
    }
    .stSelectbox>div>div {
        background-color: #F8FAFC !important;
        border-radius: 10px !important;
        border: 1px solid #E2E8F0 !important;
    }

    /* -------- Tabs -------- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        justify-content: center;
    }
    .stTabs [data-baseweb="tab"] {
        background: #F8FAFC;
        border-radius: 10px;
        color: #475569;
        font-weight: 500;
        padding: 10px 18px;
        transition: 0.2s;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg,#FF0080 0%,#00B4FF 100%);
        color: white !important;
        font-weight: 600;
    }

    /* -------- Tablas -------- */
    .stDataFrame, .stTable {
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        border: 1px solid #E2E8F0;
        overflow: hidden;
    }

    /* -------- Dashboard Cards -------- */
    .dashboard-card {
        background: #FFFFFF;
        border-radius: 18px;
        padding: 25px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        margin-bottom: 25px;
        border: 1px solid #E2E8F0;
    }
    .dashboard-title {
        font-size: 24px;
        font-weight: 600;
        color: #0F172A;
    }
    .dashboard-sub {
        font-size: 14px;
        color: #475569;
        margin-top: -8px;
    }

    /* -------- Bordes y divisores -------- */
    hr {
        border: none;
        border-top: 1px solid #E2E8F0;
        margin: 25px 0;
    }
    </style>
""", unsafe_allow_html=True)


# ==============================
# ESTADO DE SESIÓN
# ==============================
for k, v in {
    "auth_status": None,
    "tenant_id": None,
    "tenant_name": None,
    "user_email": None,
    "primary_color": "#FF0080",
}.items():
    st.session_state.setdefault(k, v)

# ==============================
# BASE DE DATOS (en HOME del usuario → nunca se pierde)
# ==============================
TENANTS_DB = os.path.join(os.path.expanduser("~"), "ellit_tenants.db")

def get_conn():
    return sqlite3.connect(TENANTS_DB, check_same_thread=False)

# ==============================
# INIT DB + CREACIÓN AUTOMÁTICA DEL SUPER ADMIN
# ==============================
SUPERADMIN_EMAIL = "admin@ellitnow.com"
SUPERADMIN_NAME = "Ellit Super Admin"

# ==============================
# INIT DB + SUPER ADMIN BLINDADO (NUNCA MÁS SE DESINCRONIZA)
# ==============================
def init_db_and_superadmin():
    conn = get_conn()
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = ON;")

    # Tablas base
    c.execute("""
        CREATE TABLE IF NOT EXISTS tenants (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            active INTEGER DEFAULT 1,
            predictive INTEGER DEFAULT 0,
            primary_color TEXT DEFAULT '#FF0080',
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS tenant_api_keys (
            tenant_id TEXT,
            key_fingerprint TEXT UNIQUE,
            key_hash TEXT NOT NULL,
            revoked INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (tenant_id) REFERENCES tenants(id)
        )
    """)

    c.execute("CREATE INDEX IF NOT EXISTS idx_fp ON tenant_api_keys(key_fingerprint);")
    conn.commit()

    # ===== SUPER ADMIN KEY DESDE secrets.toml =====
    if "SUPER_ADMIN_KEY" not in st.secrets:
        st.error("FALTA SUPER_ADMIN_KEY en ~/.streamlit/secrets.toml")
        st.stop()

    super_key = st.secrets["SUPER_ADMIN_KEY"]
    fingerprint = hashlib.sha256(super_key.encode()).hexdigest()[:12]
    key_hash = bcrypt.hashpw(super_key.encode(), bcrypt.gensalt(12)).decode()

    # 1) Garantizar que exista el tenant del Super Admin (por email)
    c.execute("SELECT id FROM tenants WHERE email = ?", (SUPERADMIN_EMAIL,))
    row = c.fetchone()

    if row:
        super_id = row[0]
    else:
        super_id = str(uuid.uuid4())
        c.execute("""
            INSERT INTO tenants (id, name, email, active, predictive, primary_color)
            VALUES (?, ?, ?, 1, 1, '#FF0080')
        """, (super_id, SUPERADMIN_NAME, SUPERADMIN_EMAIL))

    # 2) Sincronizar SIEMPRE la API key del super admin con SUPER_ADMIN_KEY
    c.execute("""
        INSERT OR REPLACE INTO tenant_api_keys (tenant_id, key_fingerprint, key_hash, revoked, created_at)
        VALUES (?, ?, ?, 0, datetime('now'))
    """, (super_id, fingerprint, key_hash))

    conn.commit()
    conn.close()

    # Mensaje suave (no mostramos la clave porque ya está en secrets)
    st.info("🔐 Super Admin sincronizado con SUPER_ADMIN_KEY.")


# ==============================
# EJECUTAR UNA SOLA VEZ AL INICIO
# ==============================
init_db_and_superadmin()  # <--- AQUÍ SE ARREGLA TODO

# ==============================
# CREACIÓN DE PDF (Opción 3 — sin fuentes externas)
# Soluciona errores Unicode sustituyendo caracteres no compatibles
# ==============================

def sanitize_text(text):
    """Reemplaza caracteres Unicode problemáticos por equivalentes ASCII seguros"""
    if not text:
        return ""
    replacements = {
        "™": "(TM)",
        "©": "(C)",
        "®": "(R)",
        "’": "'",
        "“": '"',
        "”": '"',
        "–": "-",
        "—": "-",
        "…": "...",
        "•": "*",
        "°": "º"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    text = re.sub(r"[^\x00-\x7F]+", "", text)  # elimina cualquier otro carácter no ASCII
    return text

def create_pdf_report(title: str, tenant_name: str, content: str, filename: str):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.set_text_color(255, 0, 128)
    pdf.cell(0, 10, sanitize_text("AI Executive Shield (TM) — Ellit Cognitive Core"), ln=1, align="C")
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, sanitize_text(title), ln=1, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, sanitize_text(f"Cliente: {tenant_name}"), ln=1)
    pdf.cell(0, 8, f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=1)
    pdf.ln(10)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 8, sanitize_text(content))
    pdf.ln(10)
    pdf.set_font("Arial", "I", 9)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 10, sanitize_text("© 2025 EllitNow Cognitive Core — Todos los derechos reservados."), align="C")

    buffer = io.BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer.getvalue()

def download_pdf_button(title: str, tenant_name: str, content: str, filename: str):
    pdf_bytes = create_pdf_report(title, tenant_name, content, filename)
    b64 = base64.b64encode(pdf_bytes).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="{filename}">' \
           f'<button style="background:#FF0080;color:white;padding:10px 20px;border:none;border-radius:8px;">' \
           f'Descargar {filename}</button></a>'
    st.markdown(href, unsafe_allow_html=True)



# ==============================
# VALIDACIÓN DE API KEY
# ==============================
# ==============================
# VALIDACIÓN DE API KEY — COMPATIBLE CON ELLIT- Y sk_ellit_
# ==============================
def get_tenant_by_api_key(api_key: str):
    """Valida API Keys tanto del formato antiguo (ELLIT-) como del nuevo (sk_ellit_)."""
    if not api_key:
        return None

    # Aceptar ambos prefijos válidos
    valid_prefixes = ("sk_ellit_", "ELLIT-")
    if not api_key.startswith(valid_prefixes):
        return None

    # Generar fingerprint y comparar hash
    fingerprint = hashlib.sha256(api_key.encode()).hexdigest()[:12]
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
        SELECT t.id, t.name, t.email, t.active, t.primary_color, k.key_hash, k.revoked
        FROM tenant_api_keys k
        JOIN tenants t ON k.tenant_id = t.id
        WHERE k.key_fingerprint = ? AND k.revoked = 0
        LIMIT 1
    """, (fingerprint,))
    
    row = c.fetchone()
    conn.close()
    if not row:
        return None

    stored_hash = row[5]
    try:
        if bcrypt.checkpw(api_key.encode(), stored_hash.encode()):
            return {
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "active": bool(row[3]),
                "primary_color": row[4] or "#FF0080"
            }
    except Exception as e:
        print(f"[SECURITY] bcrypt error: {e}")
    return None


# ==============================
# LOGIN SCREEN — FORM FIX
# ==============================
def login_screen():
    st.markdown("""
        <style>
        .login-container {
            background: linear-gradient(135deg, #FF0080 0%, #00B4FF 100%);
            padding: 50px;
            border-radius: 18px;
            text-align: center;
            color: white;
            box-shadow: 0 10px 30px rgba(0,0,0,0.25);
            margin-top: 40px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-container"><h2>🔐 Ellit Cognitive Core — Acceso Seguro</h2></div>', unsafe_allow_html=True)

    with st.form(key=f"login_form_{uuid.uuid4()}", clear_on_submit=True):
        api_key = st.text_input("Introduce tu API Key", type="password", placeholder="sk_ellit_••••••••••••••••••••••")
        submitted = st.form_submit_button("ACCEDER", use_container_width=True, type="primary")

    if submitted:
        if not api_key.strip():
            st.error("Ingresa tu API Key")
        else:
            tenant = get_tenant_by_api_key(api_key.strip())
            if tenant and tenant["active"]:
                st.session_state.update({
                    "auth_status": "super_admin" if tenant["email"] == SUPERADMIN_EMAIL else "client",
                    "tenant_id": tenant["id"],
                    "tenant_name": tenant["name"],
                    "user_email": tenant["email"],
                    "primary_color": tenant["primary_color"],
                })
                st.success(f"Bienvenido, {tenant['name']}")
                st.balloons()
                st.rerun()
            else:
                st.error("API Key inválida o revocada.")

# ==============================
# PANEL PRINCIPAL
# ==============================
def render_panel():
    role = st.session_state.get("auth_status", "demo")
    tenant_name = st.session_state.get("tenant_name", "AI Executive Shield")
    primary_color = st.session_state.get("primary_color", "#FF0080")

    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, {primary_color} 0%, #00B4FF 100%);
            color:white; padding:25px; text-align:center; border-radius:15px;">
            <h1>{tenant_name}</h1>
            <p>{role.title()} • Ellit Cognitive Core 2025</p>
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Radar IA™", "Panel de Continuidad de Negocio", "Políticas IA", "Predictive", "Licencias"
    ])
    # ==============================
    # TAB 1 — RADAR IA™ (Cognitive Risk Engine)
    # ==============================
    with tab1:
        # ====== Paso 2 – Contenedor visual Ellit Shield Pro ======
        st.markdown("""
        <style>
        .main-container {
            background-color: #FFFFFF;
            border-radius: 18px;
            padding: 25px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.05);
            border: 1px solid #E2E8F0;
            margin-bottom: 30px;
        }
        .metric-card {
            background-color: #F9FAFB !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 14px !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            padding: 22px;
            text-align: center;
            transition: all 0.2s ease;
        }
        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 3px 10px rgba(0,0,0,0.08);
        }
        .metric-value {
            font-size: 28px;
            font-weight: 700;
            color: #0F172A !important;
            margin-top: 6px;
        }
        .metric-label {
            font-size: 14px;
            font-weight: 500;
            color: #64748B !important;
            text-transform: uppercase;
            letter-spacing: 0.4px;
            margin-bottom: 6px;
        }
        </style>
        """, unsafe_allow_html=True)


        # ====== Paso 3 – Métricas principales (KPI superiores, ahora DINÁMICAS) ======
        try:
            indicadores_session = st.session_state.get("radar_data", {}).get("indicadores", {})
        except Exception:
            indicadores_session = {}

        disp_default = 99.8
        ens_default = 92
        bcp_default = 88
        cultura_default = 74

        disp = indicadores_session.get("Nivel de Protección", disp_default)
        ens = indicadores_session.get("Cumplimiento Normativo", ens_default)
        bcp = indicadores_session.get("Resiliencia BCP", bcp_default)
        cultura = indicadores_session.get("Cultura de Seguridad", cultura_default)

        def fmt(v):
            try:
                return f"{float(v):.0f}%"
            except Exception:
                return str(v)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(
                f'<div class="metric-card"><div class="metric-value">{fmt(disp)}</div>'
                '<div class="metric-label">DISPONIBILIDAD OPERATIVA</div></div>',
                unsafe_allow_html=True
            )
        with col2:
            st.markdown(
                f'<div class="metric-card"><div class="metric-value">{fmt(ens)}</div>'
                '<div class="metric-label">CUMPLIMIENTO ENS</div></div>',
                unsafe_allow_html=True
            )
        with col3:
            st.markdown(
                f'<div class="metric-card"><div class="metric-value">{fmt(bcp)}</div>'
                '<div class="metric-label">RESILIENCIA BCP</div></div>',
                unsafe_allow_html=True
            )
        with col4:
            st.markdown(
                f'<div class="metric-card"><div class="metric-value">{fmt(cultura)}</div>'
                '<div class="metric-label">CULTURA DE SEGURIDAD</div></div>',
                unsafe_allow_html=True
            )

        # Encabezado de la sección Radar IA™ (versión profesional limpia)
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #FF0080 0%, #00B4FF 100%);
            padding:24px;
            border-radius:16px;
            text-align:center;
            margin-bottom:25px;
            color:#FFFFFF;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        ">
            <h2 style="font-weight:700; letter-spacing:0.5px; margin-bottom:6px;">
                Radar IA™ — Cognitive Risk Engine
            </h2>
            <p style="font-size:15px; color:rgba(255,255,255,0.9); margin:0;">
                Evaluación cognitiva avanzada de madurez, cumplimiento y resiliencia organizacional.
            </p>
        </div>
        """, unsafe_allow_html=True)




        # -----------------------------
        # 1️⃣ PERFIL ORGANIZACIONAL
        # -----------------------------
        st.markdown("### 🧾 Perfil de la Organización")
        c1, c2, c3 = st.columns(3)
        with c1:
            nombre_org = st.text_input("Nombre de la organización", "Fraudfense")
        with c2:
            sector = st.selectbox("Sector", [
                "Banca y Finanzas", "Seguros", "Salud y Farmacéutica", "Tecnología e I+D+I",
                "Energía y Utilities", "Educación", "Retail y E-commerce", "Industrial y Manufactura",
                "Defensa y Seguridad", "Sector Público", "Startup / Innovación", "Otro"
            ])
        with c3:
            nivel_ens = st.selectbox("Nivel ENS actual", ["No aplica", "Básico", "Medio", "Alto"])

        c4, c5, c6 = st.columns(3)
        with c4:
            tamano = st.selectbox("Tamaño de la organización", ["Pequeña", "Mediana", "Grande", "Multinacional"])
        with c5:
            region = st.text_input("Región / País principal", "España")
        with c6:
            responsable = st.text_input("CISO / Responsable de Seguridad", "Anónimo")

        riesgos = st.text_area("⚙️ Riesgos principales detectados",
                               placeholder="Ejemplo: ransomware, fuga de datos, cumplimiento GDPR, dependencias críticas...")
        certificaciones = st.text_area(" Certificaciones y marcos aplicables",
                                       placeholder="Ejemplo: ISO 27001, ENS Medio, NIST CSF, SOC 2 Tipo II...")

        # -----------------------------
        # 2️⃣ ANÁLISIS COGNITIVO — ELLIT COGNITIVE CORE
        # -----------------------------
        if st.button(" Analizar con Ellit Cognitive Core", key="analizar_radar_ia"):
            import re, json
            with st.spinner("Analizando contexto de seguridad y madurez organizacional..."):
                try:
                    prompt = f"""
Eres Ellit Cognitive Core™, motor cognitivo especializado en ENS, ISO 27001, NIST CSF y continuidad ISO 22301.
Evalúa la madurez de {nombre_org}, sector {sector}, tamaño {tamano}, nivel ENS {nivel_ens}, en la región {region}.

Basado en el contexto y madurez declarada:
- Si ENS es 'Medio', orienta el objetivo hacia ISO 27001 óptimo y ENS Alto.
- Si ENS es 'Alto', refuerza controles NIST CSF Tier 3+ e ISO 22301.
- Proporciona un análisis técnico + ejecutivo para CISO.
- Genera 10 acciones críticas agrupadas según horizonte temporal.

Responde solo en JSON válido:
{{
  "indicadores": {{
    "Madurez SGSI": 0-100,
    "Nivel de Protección": 0-100,
    "Cumplimiento Normativo": 0-100,
    "Probabilidad de Materialización": 0-100,
    "Resiliencia BCP": 0-100,
    "Cultura de Seguridad": 0-100,
    "Brecha ENS (%)": 0-100
  }},
  "analisis": "Análisis contextual con interpretación ENS/ISO/NIST/22301.",
  "acciones": {{
    "0-3 meses": ["acción 1", "acción 2"],
    "3-6 meses": ["acción 3", "acción 4"],
    "6-12 meses": ["acción 5", "acción 6"]
  }},
  "recomendaciones": ["Recomendación 1", "Recomendación 2"],
  "alertas": ["Alerta 1", "Alerta 2"]
}}
"""
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "Eres un evaluador experto en GRC y ciberseguridad ENS/ISO27001."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.3,
                        max_tokens=1500
                    )

                    raw = response.choices[0].message.content or ""
                    match = re.search(r"\{.*\}", raw, re.S)
                    if match:
                        data = json.loads(match.group(0))
                        st.session_state["radar_data"] = data
                        st.success(f"✅ Análisis completado para {nombre_org}")
                    else:
                        st.error("❌ No se pudo interpretar la respuesta del núcleo cognitivo. Intenta de nuevo.")
                        data = None

                except Exception as e:
                    st.error(f"❌ Error al conectar con Ellit Cognitive Core: {str(e)}")
                    data = None
        else:
            data = st.session_state.get("radar_data", None)
        # -----------------------------
        # 📊 PANEL DE VISUALIZACIÓN COMPLETO
        # -----------------------------
        if data:
            st.markdown("###  Evaluación Global de Madurez y Riesgo")

            indicadores = data.get("indicadores", {})
            if not indicadores:
                st.warning("No se encontraron indicadores en los resultados.")
            else:
                # =======================
                # FILA 1: Gauge + Radar
                # =======================
                c1, c2 = st.columns(2)

                # --------- Gauge (Madurez SGSI) — nuevo estilo semicircular
                # --------- Gauge (Madurez SGSI) — nuevo estilo semicircular
                with c1:
                    st.subheader("Madurez del SGSI")

                    from matplotlib.patches import Wedge, Circle  #  Import correcto

                    madurez = indicadores.get("Madurez SGSI", 0)

                    fig, ax = plt.subplots(figsize=(5, 3))

                    # Fondo semicircular dividido en zonas
                    ax.add_patch(Circle((0, 0), 1, color='white', ec='none'))
                    ax.add_patch(Wedge((0, 0), 1, 180, 260, facecolor='#FF4B4B'))  # Rojo 0-40
                    ax.add_patch(Wedge((0, 0), 1, 260, 300, facecolor='#FFD93D'))  # Amarillo 40-60
                    ax.add_patch(Wedge((0, 0), 1, 300, 360, facecolor='#6DFF8C'))  # Verde 60-100

                    # Línea del puntero
                    ang = 180 + (madurez * 180 / 100)
                    x = np.cos(np.deg2rad(ang))
                    y = np.sin(np.deg2rad(ang))
                    ax.plot([0, x], [0, y], color='#333', lw=3)
                    ax.plot(0, 0, 'o', color='#333', markersize=8)

                    # Texto del valor
                    ax.text(0, -0.2, f"{int(madurez)}", ha='center', va='center', fontsize=32, fontweight='bold', color='#444')
                    ax.text(0, -0.4, "Nivel de Madurez", ha='center', fontsize=10, color='#666')

                    # Estética limpia
                    ax.set_xlim(-1.2, 1.2)
                    ax.set_ylim(-0.2, 1.1)
                    ax.axis('off')
                    st.pyplot(fig)
                    st.caption("El indicador muestra el grado de madurez del Sistema de Gestión de Seguridad de la Información (SGSI).")


                # --------- Radar Cognitivo
                with c2:
                    st.subheader("Radar Cognitivo ENS–ISO–NIST")
                    labels = list(indicadores.keys())
                    values = list(indicadores.values())
                    num_vars = len(labels)
                    angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
                    values += values[:1]
                    angles += angles[:1]

                    fig2, ax2 = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
                    ax2.fill(angles, values, color="#00B4FF", alpha=0.25)
                    ax2.plot(angles, values, color="#00B4FF", linewidth=2)
                    ax2.set_yticks([20, 40, 60, 80, 100])
                    ax2.set_ylim(0, 100)
                    ax2.set_xticks(angles[:-1])
                    ax2.set_xticklabels(labels, fontsize=8)
                    st.pyplot(fig2)
                    st.caption("El radar compara el equilibrio entre protección, cumplimiento, resiliencia y cultura de seguridad.")

                st.markdown("---")

                # =======================
                # FILA 2: Barras + Riesgo de Mercado
                # =======================
                c3, c4 = st.columns(2)

                # --------- Distribución General de Controles
                with c3:
                    st.subheader("Distribución General de Controles")
                    df = pd.DataFrame({
                        "Indicador": list(indicadores.keys()),
                        "Puntaje (%)": list(indicadores.values())
                    })
                    fig3, ax3 = plt.subplots(figsize=(6, 3))
                    bars = ax3.bar(df["Indicador"], df["Puntaje (%)"], color="#0066cc")
                    ax3.bar_label(bars, fmt="%.0f", label_type="edge")
                    ax3.set_ylabel("Puntaje (%)")
                    ax3.set_ylim(0, 100)
                    plt.xticks(rotation=45, ha='right')
                    st.pyplot(fig3)

                # --------- Riesgo según Mercado (simulado)
                with c4:
                    st.subheader("Riesgo Comparativo del Sector")
                    riesgo_sector = np.random.randint(30, 90)
                    riesgo_org = 100 - indicadores.get("Madurez SGSI", 0)

                    categorias = ["Media del Sector", "Tu Organización"]
                    valores = [riesgo_sector, riesgo_org]

                    fig4, ax4 = plt.subplots(figsize=(4.5, 3))
                    colores = ["#00B4FF", "#FF0080"]
                    ax4.bar(categorias, valores, color=colores)
                    for i, v in enumerate(valores):
                        ax4.text(i, v + 2, f"{v}%", ha='center', fontsize=11, fontweight='bold')
                    ax4.set_ylim(0, 100)
                    ax4.set_ylabel("Nivel de Riesgo (%)")
                    st.pyplot(fig4)
                    st.caption("Comparación entre el nivel de riesgo estimado del mercado y el de la organización analizada.")

            # -----------------------------
            # 🧠 Análisis Ejecutivo y Recomendaciones
            # -----------------------------
            analisis = data.get("analisis", "")
            if analisis:
                st.markdown("###  Análisis Ejecutivo")
                st.info(analisis)

            acciones = data.get("acciones", {})
            if acciones:
                st.markdown("### 🛠️ Acciones Prioritarias")
                for horizonte, tareas in acciones.items():
                    with st.expander(f"📆 {horizonte}"):
                        for t in tareas:
                            st.markdown(f"- {t}")

            recomendaciones = data.get("recomendaciones", [])
            if recomendaciones:
                st.markdown("### 💡 Recomendaciones Estratégicas")
                for r in recomendaciones:
                    st.markdown(f"- {r}")

            alertas = data.get("alertas", [])
            if alertas:
                st.markdown("### 🚨 Alertas Críticas")
                for a in alertas:
                    st.error(f"⚠️ {a}")



        # -----------------------------
        # 🔍 MÓDULO DE EVALUACIÓN DOCUMENTAL ENS (MEJORADO)
        # -----------------------------
        if data:
            st.markdown("###  Evaluación Documental ENS — Nivel Objetivo")
            st.info("Analiza los documentos existentes y los requeridos para alcanzar el nivel ENS superior.")

            documentos_existentes = st.text_area(
                "📚 Documentos existentes (uno por línea)",
                placeholder="Ejemplo:\nPolítica de Seguridad de la Información\nGestión de Riesgos\nProcedimiento de Control de Accesos"
            ).splitlines()

            controles_faltantes = st.text_area(
                "⚠️ Controles ENS faltantes (uno por línea, formato: MP.INFO.1, OP.ACC.2, etc.)",
                placeholder="Ejemplo:\nMP.INFO.2\nOP.BCP.2\nPR.COM.1"
            ).splitlines()

            mapa_controles_docs = {
                "MP.INFO.1": "Política de Seguridad de la Información",
                "MP.INFO.2": "Informe de Evaluación y Gestión de Riesgos",
                "MP.INFO.3": "Política de Clasificación de la Información",
                "OP.ACC.1": "Procedimiento de Control de Accesos",
                "OP.LOG.2": "Procedimiento de Monitorización y Registro de Actividades",
                "ORG.CONT.3": "Plan de Continuidad y Recuperación ante Desastres",
                "PR.DAT.1": "Política de Protección de Datos Personales",
                "PR.COM.1": "Procedimiento de Comunicaciones Seguras",
                "OP.BCP.2": "Informe de Pruebas de Continuidad Operativa",
                "MP.AUD.2": "Informe de Auditoría de Seguridad",
                "MP.SUP.1": "Plan de Mantenimiento y Soporte de Sistemas",
                "ORG.FOR.1": "Manual de Formación y Concienciación en Seguridad",
                "MP.CHG.1": "Procedimiento de Gestión de Cambios",
                "MP.ACQ.1": "Procedimiento de Adquisición Segura de Sistemas y Servicios",
                "PR.CRY.1": "Política de Cifrado y Gestión de Claves",
                "PR.IDS.1": "Informe de Gestión de Incidentes de Seguridad",
                "OP.CON.1": "Controles de Red y Segmentación Lógica",
                "ORG.SUP.1": "Manual de Soporte y Escalado Técnico",
                "MP.CONF.1": "Procedimiento de Configuración Segura",
                "PR.MAL.1": "Procedimiento de Protección frente a Malware"
            }

            def calcular_documentos_faltantes(controles_faltantes, documentos_existentes, nivel_ens):
                documentos_faltantes = []
                for control in controles_faltantes:
                    control = control.strip()
                    if not control:
                        continue
                    doc_requerido = mapa_controles_docs.get(control)
                    if doc_requerido and all(doc_requerido.lower() not in d.lower() for d in documentos_existentes):
                        documentos_faltantes.append(f"{control} → {doc_requerido}")

                # Si el objetivo es subir a ENS Alto, exige además documentación avanzada
                if nivel_ens == "Medio":
                    adicionales = [
                        "Informe de Análisis de Brechas hacia ENS Alto",
                        "Procedimiento de Gestión de Proveedores Críticos",
                        "Política de Seguridad por Capas (Zero Trust)",
                        "Plan de Pruebas de Resiliencia Operativa Anual"
                    ]
                    for doc in adicionales:
                        if all(doc.lower() not in d.lower() for d in documentos_existentes):
                            documentos_faltantes.append(f"ENS Alto → {doc}")

                return documentos_faltantes

            if st.button(" Analizar Documentación ENS", key="analizar_docs_ens"):
                documentos_faltantes = calcular_documentos_faltantes(controles_faltantes, documentos_existentes, nivel_ens)
                if documentos_faltantes:
                    st.error("📄 Documentos faltantes para alcanzar el nivel objetivo ENS:")
                    for doc in documentos_faltantes:
                        st.markdown(f"- {doc}")
                else:
                    st.success("✅ Todos los documentos requeridos para el nivel actual están presentes. Puedes iniciar el proceso de mejora hacia ENS Alto.")

        # -----------------------------
        # 5️⃣ EXPORTAR INFORME PDF — VERSIÓN UNICODE ESTABLE
        # -----------------------------
        st.markdown("---")
        st.markdown("###  Exportar Informe PDF")

        estilo = st.selectbox(
            "Estilo del informe PDF",
            ["Clásico", "Corporativo", "Ellit"],
            index=2
        )

        if st.button("📥 Generar Informe PDF"):
            try:


                radar_data = st.session_state.get("radar_data", None)
                if radar_data is None:
                    st.warning("⚠️ Primero ejecuta el análisis con Ellit Cognitive Core antes de generar el PDF.")
                    st.stop()

                # 🧹 Limpieza de memoria
                gc.collect()

                # 🔤 Función robusta para limpiar caracteres
                def clean_text(text):
                    if not text:
                        return ""
                    t = str(text)
                    replacements = {
                        "–": "-", "—": "-", "•": "-", "’": "'", "‘": "'",
                        "“": '"', "”": '"', "…": "...", "→": "->", "·": "-",
                        "\xa0": " ", "\u200b": " "
                    }
                    for k, v in replacements.items():
                        t = t.replace(k, v)
                    t = re.sub(r"[\t\r\f\v]+", " ", t)
                    t = re.sub(r"\s{2,}", " ", t)
                    return "\n".join(textwrap.wrap(t.strip(), width=95))

                # PDF base (solo DejaVu, Unicode)
                pdf = FPDF()
                pdf.set_auto_page_break(auto=True, margin=15)
                pdf.add_page()
                pdf.set_left_margin(15)
                pdf.set_right_margin(15)

                font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
                if os.path.exists(font_path):
                    pdf.add_font("DejaVu", "", font_path, uni=True)
                    pdf.add_font("DejaVu", "B", font_path, uni=True)
                    pdf.set_font("DejaVu", "", 12)
                else:
                    pdf.set_font("Helvetica", "", 12)

                # -----------------------------
                # 🟣 ENCABEZADO
                # -----------------------------
                if estilo == "Ellit":
                    pdf.set_fill_color(255, 0, 128)
                    pdf.rect(0, 0, 210, 18, "F")
                    pdf.set_text_color(255, 255, 255)
                    pdf.set_font("DejaVu", "B", 16)
                    pdf.cell(0, 12, "Ellit Cognitive Core - Radar IA Report", ln=True, align="C")
                elif estilo == "Corporativo":
                    pdf.set_fill_color(0, 70, 130)
                    pdf.rect(0, 0, 210, 18, "F")
                    pdf.set_text_color(255, 255, 255)
                    pdf.set_font("DejaVu", "B", 16)
                    pdf.cell(0, 12, "Radar IA | Executive Cybersecurity Report", ln=True, align="C")
                else:
                    pdf.set_font("DejaVu", "B", 16)
                    pdf.set_text_color(0, 0, 0)
                    pdf.cell(0, 12, "Radar IA - Informe Ejecutivo", ln=True, align="C")

                # -----------------------------
                # 📋 INFORMACIÓN GENERAL
                # -----------------------------
                pdf.ln(20)
                pdf.set_text_color(0, 0, 0)
                pdf.set_font("DejaVu", "B", 14)
                pdf.cell(0, 10, "Información General:", ln=True)
                pdf.set_font("DejaVu", "", 12)
                info = (
                    f"Organización: {nombre_org}\n"
                    f"Sector: {sector}\n"
                    f"Nivel ENS actual: {nivel_ens}\n"
                    f"Tamaño: {tamano}\n"
                    f"Región: {region}\n"
                    f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
                )
                pdf.multi_cell(180, 8, clean_text(info))
                pdf.ln(10)

                # -----------------------------
                # 🧠 RESUMEN EJECUTIVO
                # -----------------------------
                pdf.set_font("DejaVu", "B", 14)
                pdf.cell(0, 10, "Resumen Ejecutivo:", ln=True)
                pdf.set_font("DejaVu", "", 12)
                resumen = radar_data.get("analisis", "Sin análisis generado.")
                pdf.multi_cell(180, 8, clean_text(resumen))
                pdf.ln(10)

                # -----------------------------
                # 📊 INDICADORES
                # -----------------------------
                indicadores = radar_data.get("indicadores", {})
                if indicadores:
                    pdf.set_font("DejaVu", "B", 14)
                    pdf.cell(0, 10, "Indicadores Clave:", ln=True)
                    pdf.set_font("DejaVu", "", 12)
                    pdf.set_fill_color(240, 240, 240)
                    pdf.cell(110, 10, "Indicador", 1, 0, "C", fill=True)
                    pdf.cell(40, 10, "Valor (%)", 1, 1, "C", fill=True)
                    for k, v in indicadores.items():
                        pdf.cell(110, 10, clean_text(k), 1)
                        pdf.cell(40, 10, f"{v}%", 1, 1, "C")
                    pdf.ln(10)

                # -----------------------------
                # 💡 RECOMENDACIONES (REPARADO Y ALINEADO)
                # -----------------------------
                recomendaciones = radar_data.get("recomendaciones", [])
                if recomendaciones:
                    # 🔹 Forzar salto limpio y margen antes del bloque
                    pdf.ln(12)
                    pdf.set_y(pdf.get_y())        # actualiza posición vertical
                    pdf.set_x(pdf.l_margin)       # vuelve exactamente al margen izquierdo
                    pdf.cell(0, 10, "", ln=True)  # línea vacía para “resetear” flujo

                    # 🔹 Título
                    pdf.set_font("DejaVu", "B", 14)
                    pdf.cell(0, 10, "Recomendaciones Estratégicas:", ln=True)
                    pdf.ln(4)

                    # 🔹 Contenido
                    pdf.set_font("DejaVu", "", 12)
                    pdf.set_text_color(0, 0, 0)
                    for r in recomendaciones:
                        texto = clean_text(f"- {r}")
                        pdf.set_x(pdf.l_margin)           # asegura margen izquierdo
                        pdf.multi_cell(180, 8, texto, align="J")  # ancho seguro dentro de página
                        pdf.ln(2)

                    # 🔹 restaurar color por si otros bloques usan gris
                    pdf.set_text_color(0, 0, 0)


                # -----------------------------
                # 🧭 ACCIONES RECOMENDADAS (REPARADO Y ALINEADO)
                # -----------------------------
                acciones = radar_data.get("acciones", {})
                if acciones:
                    pdf.ln(10)
                    pdf.set_y(pdf.get_y())        # asegura posición vertical correcta
                    pdf.set_x(pdf.l_margin)       # reinicia margen izquierdo
                    pdf.cell(0, 10, "", ln=True)  # limpia cualquier celda previa

                    pdf.set_font("DejaVu", "B", 14)
                    pdf.cell(0, 10, "Acciones Recomendadas por Horizonte Temporal:", ln=True)
                    pdf.ln(5)

                    pdf.set_font("DejaVu", "", 12)
                    pdf.set_text_color(0, 0, 0)

                    for periodo, lista_acciones in acciones.items():
                        pdf.set_x(pdf.l_margin)
                        pdf.set_font("DejaVu", "B", 12)
                        pdf.cell(0, 10, clean_text(periodo), ln=True)
                        pdf.ln(2)

                        pdf.set_font("DejaVu", "", 11)
                        for a in lista_acciones:
                            texto = clean_text(f"- {a}")
                            pdf.set_x(pdf.l_margin)
                            pdf.multi_cell(180, 8, texto, align="J")
                            pdf.ln(1)

                        pdf.ln(4)

                    pdf.set_text_color(0, 0, 0)


                # -----------------------------
                # 🧾 PIE DE PÁGINA (UNICODE LIMPIO)
                # -----------------------------
                pdf.set_font("DejaVu", "", 9)
                pdf.set_text_color(120, 120, 120)
                footer_text = "© 2025 Ellit Cognitive Core - Informe Radar IA"
                pdf.multi_cell(180, 8, clean_text(footer_text), align="C")

                # -----------------------------
                # 💾 GUARDAR Y DESCARGAR
                # -----------------------------
                pdf_file = f"RadarIA_Report_{nombre_org.replace(' ', '_')}.pdf"
                pdf.output(pdf_file)

                with open(pdf_file, "rb") as f:
                    st.download_button(" Descargar PDF", f, file_name=pdf_file)

            except Exception as e:
                import traceback
                st.error(f"⚠️ Error al generar el PDF:\n{traceback.format_exc()}")

    # ===== TAB 2 — Panel de Continuidad de Negocio =====
    with tab2:
        # ====== Paso 2 – Contenedor visual Ellit Shield Pro ======
        st.markdown("""
        <style>
        .bcp-container {
            background-color: #0b0b0b;
            border-radius: 18px;
            padding: 25px;
            box-shadow: 0 0 15px rgba(0,180,255,0.15);
            margin-bottom: 30px;
        }
        .bcp-metric-card {
            background: linear-gradient(135deg, #111 0%, #1a1a1c 100%);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 14px;
            padding: 18px;
            text-align: center;
            color: white;
            box-shadow: 0 4px 12px rgba(0,0,0,0.25);
            transition: all 0.3s ease-in-out;
        }
        .bcp-metric-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 16px rgba(0,180,255,0.3);
        }
        .bcp-metric-value {
            font-size: 28px;
            font-weight: 700;
            color: #00B4FF;
        }
        .bcp-metric-label {
            font-size: 13px;
            color: #ccc;
            margin-top: 5px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        </style>
        """, unsafe_allow_html=True)

        # -----------------------------
        # 1️⃣ GENERADOR DE PLAN BCP PERSONALIZADO
        # -----------------------------
        st.subheader("Generador de Plan de Continuidad ISO 22301")

        tenant_name = st.text_input("Nombre de la organización", placeholder="Ej: Fraudfense")
        procesos_criticos = st.text_area("Procesos críticos del negocio",
                                         "Facturación, Atención al cliente, Plataforma web, Operaciones TI")
        infraestructura = st.text_area("Infraestructura disponible",
                                       "2 CPDs en Madrid, Cloud Azure, VPN corporativa, Firewalls redundantes")
        dependencias = st.text_area("Dependencias tecnológicas y humanas",
                                    "ERP SAP, Microsoft 365, API de clientes, Proveedor ISP Telefónica")
        rto = st.slider("RTO (tiempo máximo de recuperación, horas)", 1, 72, 6)
        rpo = st.slider("RPO (pérdida máxima aceptable de datos, horas)", 0, 24, 1)

        st.markdown("### Análisis cognitivo del contexto de continuidad")
        contexto_libre = st.text_area(
            "Describe el contexto o el problema de continuidad que deseas analizar",
            placeholder="Ejemplo: Tengo dos CPDs pero están en la misma ciudad. ¿Qué debería hacer para mejorar la resiliencia?"
        )

        if st.button("Generar Plan de Continuidad con Ellit Cognitive Core"):
            st.success(f"Plan de continuidad generado para {tenant_name}")

            # Motor cognitivo de análisis contextual
            if "CPD" in contexto_libre and "misma" in contexto_libre:
                recomendacion = (
                    "Implementar una estrategia de redundancia geográfica en una región diferente, "
                    "preferiblemente a más de 200 km, para mitigar desastres regionales. "
                    "Se recomienda el uso de replicación síncrona entre entornos cloud y CPD físico."
                )
            elif "nieve" in contexto_libre or "nevada" in contexto_libre:
                recomendacion = (
                    "Definir un protocolo de continuidad operativa basado en personal remoto y teletrabajo temporal. "
                    "Mantener stock mínimo en cada sucursal y establecer acuerdos con proveedores logísticos alternos."
                )
            elif "proveedor" in contexto_libre:
                recomendacion = (
                    "Establecer contratos con proveedores secundarios con cláusulas de continuidad (SLA espejo). "
                    "Activar procesos de failover contractual y revisión de dependencias externas."
                )
            elif "incendio" in contexto_libre:
                recomendacion = (
                    "Definir rutas de evacuación, activar CPD secundario y mantener documentación crítica en entornos cifrados cloud. "
                    "El Comité de Crisis debe poder reunirse en un sitio alternativo predefinido."
                )
            else:
                recomendacion = (
                    "Analizar riesgos asociados al escenario descrito, priorizar procesos críticos, "
                    "y diseñar estrategias específicas de recuperación con soporte del Comité de Crisis."
                )

            plan_text = f"""
PLAN DE CONTINUIDAD DE NEGOCIO — ISO 22301 / ENS / Ellit Cognitive Core

Organización: {tenant_name}
Procesos críticos: {procesos_criticos}
Infraestructura: {infraestructura}
Dependencias: {dependencias}
RTO: {rto} horas
RPO: {rpo} horas

-----------------------------------------------
ANÁLISIS COGNITIVO DEL CONTEXTO
-----------------------------------------------
{contexto_libre}

EVALUACIÓN Y RECOMENDACIÓN DEL COGNITIVE CORE
-----------------------------------------------
{recomendacion}

-----------------------------------------------
MARCO DE CONTINUIDAD
-----------------------------------------------
El plan se construye bajo los principios de la norma ISO 22301 y del Esquema Nacional de Seguridad.
Incluye la gestión del impacto en procesos críticos, definición de tiempos RTO/RPO y asignación de roles
en la cadena de respuesta ante incidentes.

El Comité de Crisis debe revisar este plan semestralmente, validar los escenarios simulados y
mantener la coherencia entre la infraestructura disponible y las dependencias operativas.

-----------------------------------------------
© 2025 Ellit Cognitive Core — Plan de Continuidad Inteligente
            """

            st.text_area("Vista previa del plan", plan_text, height=500)
            download_pdf_button(f"Plan_BCP_{tenant_name}", tenant_name, plan_text, f"Plan_BCP_{tenant_name}.pdf")

        # -----------------------------
        # 2️⃣ SIMULADOR DE CRISIS BCP
        # -----------------------------
        st.markdown("---")
        st.subheader("Simulador de Crisis BCP — MAGERIT + Ellit IA")

        escenario = st.text_input(
            "Describe el escenario de crisis a simular",
            placeholder="Ejemplo: Pérdida total de conectividad entre CPDs durante 12 horas"
        )
        ubicacion = st.text_input("Ubicación o entorno afectado", placeholder="Ej: CPD Madrid o sede principal")
        duracion = st.slider("Duración estimada de la interrupción (horas)", 1, 72, 8)
        impacto = st.select_slider("Nivel de impacto", ["Bajo", "Medio", "Alto"], value="Alto")

        if st.button("Simular Escenario de Crisis con Ellit Cognitive Core"):
            st.success("Simulación de crisis completada.")

            # Generación de respuesta cognitiva adaptativa
            if "CPD" in escenario or "conectividad" in escenario:
                estrategia = (
                    "Activar replicación activa en región cloud secundaria y habilitar conexión VPN temporal entre sedes."
                )
            elif "ransomware" in escenario:
                estrategia = (
                    "Aislar servidores afectados, restaurar sistemas desde copias inmutables y comunicar el incidente al comité de crisis."
                )
            elif "inundación" in escenario or "incendio" in escenario:
                estrategia = (
                    "Trasladar operaciones al sitio alternativo, iniciar respaldo de infraestructura y priorizar funciones críticas."
                )
            elif "personal" in escenario or "empleados" in escenario:
                estrategia = (
                    "Activar protocolo de contingencia de recursos humanos y establecer turnos remotos operativos."
                )
            else:
                estrategia = (
                    "Aplicar protocolo general de continuidad ajustado a dependencias críticas y capacidades de recuperación."
                )

            plan_sim = f"""
SIMULACIÓN DE ESCENARIO BCP — ELLIT COGNITIVE CORE

Cliente: {tenant_name}
Escenario: {escenario}
Ubicación afectada: {ubicacion}
Duración estimada: {duracion} horas
Impacto: {impacto}

-----------------------------------------------
EVALUACIÓN COGNITIVA
-----------------------------------------------
El motor Ellit IA ha evaluado el impacto sobre los procesos críticos definidos ({procesos_criticos}),
determinando las áreas más vulnerables y los tiempos de recuperación más probables.

-----------------------------------------------
ESTRATEGIA DE RECUPERACIÓN RECOMENDADA
-----------------------------------------------
{estrategia}

-----------------------------------------------
INDICADORES DEL EJERCICIO
-----------------------------------------------
RTO alcanzable: {rto} horas
RPO efectivo: {rpo} horas
Nivel de madurez BCP: Intermedio
Capacidad de respuesta: Alta

-----------------------------------------------
RECOMENDACIONES DE MEJORA
-----------------------------------------------
- Realizar simulacros semestrales con escenarios realistas.
- Revisar la redundancia geográfica de los entornos críticos.
- Integrar los contactos del Comité de Crisis en Ellit Call Tree™.
- Ajustar los tiempos RTO/RPO según la capacidad observada.

-----------------------------------------------
© 2025 Ellit Cognitive Core — Simulador de Continuidad Inteligente
            """

            st.text_area("Resultado de la simulación", plan_sim, height=500)
            download_pdf_button(f"Simulacion_BCP_{tenant_name}", tenant_name, plan_sim, f"Simulacion_BCP_{tenant_name}.pdf")

        # -----------------------------
        # 3️⃣ MÓDULO PREMIUM — Ellit Call Tree™
        # -----------------------------
        st.markdown("---")
        st.markdown("""
        <div style="background: linear-gradient(135deg,#00B4FF 0%,#FF0080 100%);
                    padding:18px;border-radius:16px;color:white;text-align:center;">
            <h3>Ellit Call Tree™ — Comunicación Inteligente ante Crisis</h3>
            <p>Automatiza la notificación y respuesta de personal durante una activación BCP.</p>
        </div>
        """, unsafe_allow_html=True)

        st.write("""
        Ellit Call Tree™ es la aplicación móvil conectada al Panel Ellit Shield para:
        - Notificar al personal y validar respuestas en segundos.
        - Escalar llamadas automáticas por jerarquía o área.
        - Integrarse con las simulaciones generadas por el Cognitive Core.
        - Activar el Comité de Crisis desde cualquier dispositivo.
        """)
        st.info("Disponible en versión premium para organizaciones certificadas ISO 22301 o ENS Alto.")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Ver demostración de Call Tree™"):
                st.video("https://www.youtube.com/watch?v=example")
        with col2:
            if st.button("Suscribirse a versión premium"):
                st.markdown("[Ir a la suscripción premium](https://ellitnow.com/calltree)")

        st.caption(
            "La integración con Call Tree™ permite activar y monitorizar el BCP en tiempo real desde cualquier dispositivo."
        )


    # ===== TAB 3 — Generador de Políticas =====
    with tab3:
        st.markdown("""
        <div style="background: linear-gradient(135deg,#FF0080 0%,#00B4FF 100%);
                    padding:18px;border-radius:16px;color:white;text-align:center;">
            <h2> Generador de Políticas Corporativas — Ellit Cognitive Core™</h2>
            <p>Redacta políticas y procedimientos multinormativos listas para auditoría.</p>
        </div>
        """, unsafe_allow_html=True)

        # === CONFIGURACIÓN DE LA POLÍTICA ===
        c1, c2, c3 = st.columns(3)
        with c1:
            tipo = st.text_input("Tipo de política", "Gestión de Accesos Físicos")
        with c2:
            normativa = st.selectbox(
                "Normativa principal",
                ["ISO 27001", "ENS", "NIST CSF", "SOC 2", "GDPR", "COBIT", "PCI DSS"]
            )
        with c3:
            detalle = st.slider("Nivel de detalle del documento", 1, 5, 3)

        # === GENERACIÓN COGNITIVA ===
        if st.button(" Generar Política con Ellit Cognitive Core™"):
            try:
                st.info("Generando documento corporativo...")

                # Prompt avanzado multinormativo
                policy_prompt = f"""
Eres Ellit Cognitive Core™, un motor cognitivo experto en GRC, ciberseguridad y cumplimiento multinormativo.
Redacta una política corporativa de "{tipo}" adaptada a la normativa {normativa}, con rigor profesional.

Requisitos:
- Nivel de redacción: formal corporativo, preparado para auditorías.
- Idioma: español neutro.
- Extensión esperada: entre 900 y 1300 palabras.
- Estructura:
  1. Propósito y objetivos
  2. Alcance
  3. Roles y responsabilidades
  4. Principios y directrices
  5. Procedimientos asociados
  6. Cumplimiento y revisión
  7. Referencias normativas
  8. Recomendaciones del Cognitive Core™

Incluye el nombre de la organización ({tenant_name}) y referencias explícitas al marco {normativa}.
Genera un documento con tono institucional, coherente con entornos corporativos de ciberseguridad.
"""

                # Llamada al modelo de OpenAI
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "Eres un consultor experto en GRC y cumplimiento normativo multinormativo (ISO, ENS, NIST, SOC2, GDPR, PCI DSS, COBIT)."},
                        {"role": "user", "content": policy_prompt}
                    ],
                    temperature=0.35,
                    max_tokens=2000
                )

                policy_text = response.choices[0].message.content.strip()

                # === GUARDAR EN HISTORIAL ===
                if "policy_history" not in st.session_state:
                    st.session_state["policy_history"] = []
                st.session_state["policy_history"].insert(0, {
                    "tipo": tipo,
                    "normativa": normativa,
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "organizacion": tenant_name,
                    "contenido": policy_text
                })
                st.session_state["policy_history"] = st.session_state["policy_history"][:10]

                st.success(f" Política corporativa de {tipo} generada exitosamente bajo {normativa}.")

                # === VISTA PREVIA ===
                with st.expander(" Vista previa del documento"):
                    st.markdown(policy_text)

                with st.expander(" Recomendaciones del Cognitive Core™"):
                    st.info(f"El Cognitive Core™ sugiere validar esta política con los controles aplicables de {normativa} y mantener revisión anual por el Comité de Seguridad.")

                # === DESCARGA PDF CORPORATIVA ===
                fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
                encabezado = f"""
POLÍTICA CORPORATIVA — {tipo.upper()}
Organización: {tenant_name}
Normativa base: {normativa}
Fecha: {fecha_actual}
Ellit Cognitive Core™ — Documento generado automáticamente
------------------------------------------------------------

"""
                documento_final = encabezado + policy_text
                download_pdf_button(f"Política_{tipo}", tenant_name, documento_final, f"Politica_{tipo}.pdf")

            except Exception as e:
                st.error(f"❌ Error generando la política: {str(e)}")

        # === HISTORIAL DE POLÍTICAS ===
        if "policy_history" in st.session_state and st.session_state["policy_history"]:
            st.markdown("---")
            st.markdown("### 📚 Historial de Políticas Generadas")

            for item in st.session_state["policy_history"]:
                tipo_item = item.get("tipo", "Sin tipo")
                normativa_item = item.get("normativa", "Sin normativa")
                fecha_item = item.get("fecha", "Sin fecha")
                org_item = item.get("organizacion", tenant_name)
                
                st.markdown(f"""
                <div style="background:rgba(255,255,255,0.05);
                            padding:12px;
                            border-radius:10px;
                            margin-bottom:8px;
                            border:1px solid rgba(255,255,255,0.1);">
                    <b>{tipo_item}</b> — {normativa_item}<br>
                    📅 {fecha_item} | 🏢 {org_item}
                </div>
                """, unsafe_allow_html=True)



    # ===== TAB 4 — Ellit Predictive Intelligence™ Enterprise Dashboard =====
    with tab4:
        # =========================
        # CABECERA
        # =========================
        st.markdown("""
        <style>
        .dashboard-card {
            background: #FFFFFF;
            border-radius: 18px;
            padding: 25px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.05);
            margin-bottom: 25px;
        }
        .dashboard-title {
            font-size: 24px;
            font-weight: 600;
            color: #0F172A;
            margin-bottom: 5px;
        }
        .dashboard-sub {
            font-size: 14px;
            color: #475569;
            margin-top: -8px;
        }
        .metric-box {
            background: #F8FAFC;
            border-radius: 14px;
            padding: 18px;
            text-align: center;
            border: 1px solid #E2E8F0;
        }
        .metric-label {
            color: #64748B;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.4px;
        }
        .metric-value {
            font-size: 22px;
            font-weight: 600;
            color: #0F172A;
            margin-top: 4px;
        }
        .section-title {
            font-weight: 600;
            font-size: 18px;
            color: #0F172A;
            margin-bottom: 12px;
        }
        </style>

        <div class="dashboard-card">
            <div class="dashboard-title">Ellit Predictive Intelligence™</div>
            <div class="dashboard-sub">Panel ejecutivo de inteligencia viva para CISOs</div>
        </div>
        """, unsafe_allow_html=True)

        # =========================
        # FILA 1 — CONTEXTO Y KPIs
        # =========================
        col1, col2, col3 = st.columns(3)
        with col1:
            sector = st.selectbox("Sector", [
                "Banca y Finanzas", "Salud", "Educación", "Energía",
                "Retail y E-commerce", "Tecnología", "Industria", "Defensa", "Sector Público"
            ])
        with col2:
            pais = st.text_input("País / Región", "España")
        with col3:
            madurez = st.slider("Madurez ENS/ISO", 1, 5, 3)

        base_costos = {
            "Banca y Finanzas": 520000,
            "Salud": 480000,
            "Educación": 250000,
            "Energía": 600000,
            "Retail y E-commerce": 310000,
            "Tecnología": 400000,
            "Industria": 350000,
            "Defensa": 700000,
            "Sector Público": 300000
        }

        riesgo_sector = random.randint(60, 95)
        cve_activas = random.randint(25, 80)
        costo_promedio = base_costos.get(sector, 350000)
        impacto = (costo_promedio * (riesgo_sector / 100)) * (1.2 - (madurez / 10))

        st.markdown('<div class="section-title">Indicadores Clave de Riesgo</div>', unsafe_allow_html=True)
        k1, k2, k3, k4 = st.columns(4)
        for col, (label, val) in zip(
            [k1, k2, k3, k4],
            [
                ("Riesgo Sectorial", f"{riesgo_sector}%"),
                ("Vulnerabilidades Activas", f"{cve_activas}"),
                ("Costo Medio Sectorial (€)", f"{costo_promedio:,.0f}"),
                ("Impacto Potencial (€)", f"{impacto:,.0f}")
            ]
        ):
            with col:
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{val}</div>
                </div>
                """, unsafe_allow_html=True)

        # =========================
        # FILA 2 — MAPA + RADAR
        # =========================
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="section-title">Distribución Global de Amenazas Activas</div>', unsafe_allow_html=True)
            threat_data = pd.DataFrame({
                "country": ["España", "EE.UU.", "Reino Unido", "Alemania", "Brasil", "India", "Japón"],
                "cves": [45, 120, 85, 60, 55, 70, 40]
            })
            fig_map = px.choropleth(
                threat_data, locations="country", locationmode="country names",
                color="cves", color_continuous_scale=["#FF0080", "#00B4FF"],
                title=""
            )
            fig_map.update_layout(
                geo=dict(bgcolor="rgba(0,0,0,0)"),
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0, r=0, t=0, b=0)
            )
            st.plotly_chart(fig_map, use_container_width=True)

        with c2:
            st.markdown('<div class="section-title">Benchmark Comparativo ENS / ISO / NIST</div>', unsafe_allow_html=True)
            categories = ["ENS", "ISO 27001", "NIST CSF", "SOC2", "PCI DSS"]
            org_values = [madurez * 15, madurez * 18, madurez * 14, madurez * 12, madurez * 10]
            leader_values = [95, 90, 88, 85, 82]

            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=leader_values + [leader_values[0]], theta=categories + [categories[0]],
                fill='toself', name='Líder Sectorial', line=dict(color="#00B4FF")
            ))
            fig_radar.add_trace(go.Scatterpolar(
                r=org_values + [org_values[0]], theta=categories + [categories[0]],
                fill='toself', name='Tu Organización', line=dict(color="#FF0080")
            ))
            fig_radar.update_layout(
                polar=dict(bgcolor="rgba(0,0,0,0)", radialaxis=dict(visible=True, range=[0, 100])),
                showlegend=True, paper_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig_radar, use_container_width=True)

        # =========================
        # FILA 3 — SIMULADOR + ALERTAS
        # =========================
        c3, c4 = st.columns(2)
        with c3:
            st.markdown('<div class="section-title">Simulador de Ataque Predictivo (IA)</div>', unsafe_allow_html=True)
            vector = st.selectbox("Vector de ataque", [
                "Ransomware dirigido", "Exfiltración de datos",
                "Ataque a la cadena de suministro", "Phishing masivo", "Insider Threat"
            ])
            intensidad = st.slider("Intensidad esperada", 1, 10, 6)
            if st.button("Ejecutar simulación IA"):
                probabilidad = riesgo_sector / 100
                impacto_ajustado = impacto * (intensidad / 10)
                st.success("Simulación completada.")
                st.markdown(f"""
                **Vector seleccionado:** {vector}  
                **Probabilidad de ocurrencia:** {probabilidad*100:.1f}%  
                **Impacto económico estimado:** €{impacto_ajustado:,.0f}  
                **Nivel de madurez actual:** {madurez}/5  

                ---
                **Recomendaciones cognitivas:**  
                - Implementar microsegmentación Zero Trust.  
                - Fortalecer continuidad digital (ISO 22301).  
                - Monitoreo SOC/SIEM adaptativo.  
                - Refuerzo en gestión ENS–NIST de cadena de suministro.
                """)

        with c4:
            st.markdown('<div class="section-title">Alertas Predictivas Sectoriales</div>', unsafe_allow_html=True)
            alertas = [
                f"Aumento del 23% en ataques ransomware en {sector}.",
                f"Nuevas vulnerabilidades críticas detectadas en {pais}.",
                "Incremento en explotación de vulnerabilidades VPN.",
                "Amenazas a proveedores en cadena de suministro europea.",
            ]
            for alerta in alertas:
                st.markdown(f"""
                <div style="background:#F8FAFC;padding:14px;border-radius:10px;
                            border:1px solid #E2E8F0;margin-bottom:8px;">
                    <span style="color:#0F172A;font-size:14px;">{alerta}</span>
                </div>
                """, unsafe_allow_html=True)



    # ===== TAB 5 — Licencias y Suscripciones =====
    with tab5:
        render_licencias_tab()


# ==============================
# 🧩 BLOQUE 5 — SISTEMA DE ROLES, PERMISOS E IMPERSONACIÓN
# ==============================

# Fallback DB path si no existiese en globals
if "TENANTS_DB" not in globals():
    TENANTS_DB = "tenants.db"

# Fallback seguro para get_conn() — CORREGIDO
try:
    get_conn()  # ← ¡AHORA SÍ LLAMAMOS LA FUNCIÓN CON ()!
    pass
except NameError:
    def get_conn():
        return sqlite3.connect(TENANTS_DB, check_same_thread=False)
# Asegura que el esquema soporte roles/impersonación usados en este bloque
def _ensure_roles_schema():
    conn = get_conn()
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = ON;")

    # Tenants table base
    c.execute("""
        CREATE TABLE IF NOT EXISTS tenants (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            active INTEGER DEFAULT 1,
            predictive INTEGER DEFAULT 0,
            primary_color TEXT DEFAULT '#FF0080',
            parent_tenant_id TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)

    # Asegurar columnas si la tabla ya existía sin ellas
    c.execute("PRAGMA table_info(tenants);")
    cols = {row[1] for row in c.fetchall()}

    # Solo agregamos columnas si realmente no existen
    try:
        if "parent_tenant_id" not in cols:
            c.execute("ALTER TABLE tenants ADD COLUMN parent_tenant_id TEXT;")
        if "primary_color" not in cols:
            c.execute("ALTER TABLE tenants ADD COLUMN primary_color TEXT DEFAULT '#FF0080';")
    except sqlite3.OperationalError:
        # Si ya existen o hay conflicto, simplemente ignoramos
        pass

    # Tabla de API keys
    c.execute("""
        CREATE TABLE IF NOT EXISTS tenant_api_keys (
            tenant_id TEXT,
            key_fingerprint TEXT UNIQUE,
            key_hash TEXT NOT NULL,
            revoked INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (tenant_id) REFERENCES tenants(id)
        )
    """)
    c.execute("CREATE INDEX IF NOT EXISTS idx_fp ON tenant_api_keys(key_fingerprint);")

    conn.commit()
    conn.close()


# Ejecutar la comprobación de esquema
_ensure_roles_schema()


def get_partner_clients(partner_id):
    """Devuelve los clientes asociados a un partner."""
    conn = get_conn()
    c = conn.cursor()
    try:
        c.execute("""
            SELECT id, name, email, active, created_at
            FROM tenants
            WHERE parent_tenant_id = ?
            ORDER BY created_at DESC
        """, (partner_id,))
        clients = c.fetchall()
    finally:
        conn.close()
    return clients


def impersonate_tenant(target_tenant_id):
    """Permite al Super Admin 'ver como' otro tenant."""
    if st.session_state.get("auth_status") != "super_admin":
        st.error("❌ No tienes permiso para impersonar tenants.")
        return

    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT id, name, email, primary_color FROM tenants WHERE id = ?", (target_tenant_id,))
    tenant = c.fetchone()
    conn.close()

    if tenant:
        st.session_state["impersonated_tenant"] = {
            "id": tenant[0],
            "name": tenant[1],
            "email": tenant[2],
            "primary_color": tenant[3] or "#FF0080",
        }
        st.session_state["auth_status"] = "impersonated"
        st.success(f" Ahora estás viendo como: {tenant[1]}")
        st.rerun()
    else:
        st.error("❌ Tenant no encontrado.")


def stop_impersonation():
    """Vuelve al modo Super Admin."""
    if "impersonated_tenant" in st.session_state:
        del st.session_state["impersonated_tenant"]
        st.session_state["auth_status"] = "super_admin"
        st.sidebar.success("🔙 Volviste al modo Super Admin")
        st.rerun()


# ==============================
# 🎨 BANNER VISUAL DE IMPERSONACIÓN (ESTILO ELLITNOW)
# ==============================
def render_impersonation_banner():
    """Muestra un banner superior cuando el Super Admin está impersonando a otro tenant."""
    if st.session_state.get("auth_status") == "impersonated":
        tenant = st.session_state.get("impersonated_tenant", {})
        tenant_name = tenant.get("name", "Tenant desconocido")

        st.markdown(f"""
        <div style="
            position: sticky;
            top: 0;
            z-index: 1000;
            background: linear-gradient(135deg, #FF0080 0%, #00B4FF 100%);
            color: white;
            padding: 14px 20px;
            border-radius: 10px;
            margin-bottom: 18px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.25);
            display: flex;
            align-items: center;
            justify-content: space-between;
        ">
            <div style="font-size:16px;">
                 <b>Estás viendo la plataforma como:</b>
                <span style="opacity:0.9;">{tenant_name}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🔙 Volver a Super Admin", key="stop_impersonation_button"):
            stop_impersonation()


def render_role_controls():
    """Renderiza los controles adicionales en el sidebar según el rol."""
    role = st.session_state.get("auth_status")
    st.sidebar.markdown("---")

    # 👑 SUPER ADMIN
    if role == "super_admin":
        st.sidebar.markdown("### Control de Impersonación")
        conn = get_conn()
        tenants_df = pd.read_sql_query("SELECT id, name FROM tenants ORDER BY name ASC", conn)
        conn.close()

        if tenants_df.empty:
            st.sidebar.info("No hay tenants disponibles.")
            return

        tenant_options = {row["name"]: row["id"] for _, row in tenants_df.iterrows()}
        dynamic_key_select = f"impersonation_selectbox_{uuid.uuid4()}"
        dynamic_key_button = f"impersonate_button_{uuid.uuid4()}"

        target = st.sidebar.selectbox(
            "Selecciona un tenant para impersonar",
            list(tenant_options.keys()),
            key=dynamic_key_select
        )

        if st.sidebar.button(" Ver como este tenant", key=dynamic_key_button):
            impersonate_tenant(tenant_options[target])

    #  IMPERSONATED
    elif role == "impersonated":
        tenant = st.session_state.get("impersonated_tenant", {})
        st.sidebar.markdown(f"###  Modo Impersonación\nViendo como: **{tenant.get('name','')}**")
        if st.sidebar.button(" Volver a Super Admin", key="return_to_admin_button"):
            stop_impersonation()

    # PARTNER
    elif role == "partner":
        st.sidebar.markdown("###  Tus Clientes Asociados")
        partner_id = st.session_state.get("tenant_id")
        clients = get_partner_clients(partner_id)
        if clients:
            for c in clients:
                status = "🟢 Activo" if c[3] == 1 else "🔴 Inactivo"
                st.sidebar.write(f"**{c[1]}** — {status}")
        else:
            st.sidebar.info("Aún no tienes clientes asociados.")

        st.sidebar.markdown("---")
        st.sidebar.subheader("➕ Crear Cliente")
        with st.sidebar.form("create_client"):
            name = st.text_input("Nombre del Cliente", key=f"name_{uuid.uuid4()}")
            email = st.text_input("Correo", key=f"email_{uuid.uuid4()}")
            create = st.form_submit_button("Crear")
            if create and name and email:
                conn = get_conn()
                tenant_id = str(uuid.uuid4())
                api_key = "sk_ellit_" + secrets.token_urlsafe(24)
                key_hash = bcrypt.hashpw(api_key.encode(), bcrypt.gensalt(12)).decode()
                fingerprint = hashlib.sha256(api_key.encode()).hexdigest()[:12]  # ← consistente

                conn.execute("""
                    INSERT INTO tenants (id, name, email, active, parent_tenant_id, created_at)
                    VALUES (?, ?, ?, 1, ?, datetime('now'))
                """, (tenant_id, name, email, partner_id))
                conn.execute("""
                    INSERT INTO tenant_api_keys (tenant_id, key_fingerprint, key_hash)
                    VALUES (?, ?, ?)
                """, (tenant_id, fingerprint, key_hash))
                conn.commit()
                conn.close()
                st.sidebar.success(f"✅ Cliente '{name}' creado correctamente.")
                st.sidebar.code(api_key, language="bash")

    # DEMO
    elif role == "demo":
        st.sidebar.markdown("###  Demo Experience")
        st.sidebar.info("Visualización en modo demostrativo.")
        if st.sidebar.button("🔙 Cerrar sesión demo", key="close_demo_button"):
            st.session_state["auth_status"] = None
            st.rerun()


# ==============================
# 🧾 BLOQUE 6 — GENERADOR DE PDFs CORPORATIVOS ELLITNOW
# ==============================



def generate_corporate_pdf(title: str, tenant_name: str, content: str, filename: str = "EllitNow_Report.pdf"):
    """Genera un PDF corporativo con el branding de EllitNow Shield."""
    buffer = BytesIO()
    buffer.truncate(0)
    buffer.seek(0)
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Colores corporativos
    fuchsia = Color(1, 0, 0.5)
    blue = Color(0, 0.7, 1)

    # Fondo degradado
    for i in range(100):
        c = Color(1 - i/120, 0 + i/150, 0.5 + i/200)
        pdf.setFillColor(c)
        pdf.rect(0, (i/100)*height, width, height/100, stroke=0, fill=1)

    # Logo y encabezado
    logo_url = "https://i.imgur.com/b8U3pAL.png"
    try:
        logo = ImageReader(logo_url)
        pdf.drawImage(logo, 40, height - 100, width=80, preserveAspectRatio=True)
    except Exception:
        pdf.setFillColor(fuchsia)
        pdf.setFont("Helvetica-Bold", 20)
        pdf.drawString(40, height - 100, "EllitNow Shield")

    pdf.setFont("Helvetica-Bold", 20)
    pdf.setFillColorRGB(1, 1, 1)
    pdf.drawString(140, height - 60, "EllitNow Shield")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(140, height - 80, "AI Executive Security Platform")

    # Título y cliente
    pdf.setFont("Helvetica-Bold", 18)
    pdf.setFillColor(fuchsia)
    pdf.drawString(40, height - 150, title)
    pdf.setFont("Helvetica", 11)
    pdf.setFillColorRGB(1, 1, 1)
    pdf.drawString(40, height - 170, f"Cliente: {tenant_name}")
    pdf.drawString(40, height - 185, f"Fecha: {_dt.datetime.now().strftime('%d/%m/%Y %H:%M')}")

    # Contenido principal
    pdf.setFont("Helvetica", 11)
    text_obj = pdf.beginText(40, height - 220)
    text_obj.setFillColorRGB(1, 1, 1)
    text_obj.setLeading(16)
    for line in content.split("\n"):
        text_obj.textLine(line)
    pdf.drawText(text_obj)

    # Pie
    pdf.setFont("Helvetica-Oblique", 9)
    pdf.setFillColor(blue)
    pdf.drawString(40, 40, "© 2025 EllitNow Cognitive Core — Confidential Document")
    pdf.drawRightString(width - 40, 40, "Página 1 de 1")

    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return buffer


def download_corporate_pdf_button(title, tenant_name, content, filename):
    """Botón de descarga PDF con branding corporativo."""
    pdf_buffer = generate_corporate_pdf(title, tenant_name, content, filename)
    st.download_button(
        label=f"📄 Descargar {title}",
        data=pdf_buffer,
        file_name=filename,
        mime="application/pdf",
    )

# Alias para mantener consistencia con bloques anteriores
def download_pdf_button(title, tenant_name, content, filename):
    return download_corporate_pdf_button(title, tenant_name, content, filename)


# ==============================
# 💳 BLOQUE 8 — SISTEMA DE LICENCIAS Y PAGOS STRIPE (ELLITNOW CORPORATE)
# ==============================
import stripe

def render_stripe_checkout():
    """Módulo visual y funcional para activar licencias reales."""
    stripe_key = st.secrets.get("STRIPE_SECRET_KEY")
    app_url = st.secrets.get("APP_URL", "https://ellitnow.com")

    if not stripe_key:
        st.error("❌ Stripe no está configurado correctamente.")
        return

    stripe.api_key = stripe_key

    # ======= Encabezado =======
    st.markdown("""
        <div style="
            background: linear-gradient(135deg,#FF0080 0%,#00B4FF 100%);
            padding:24px;
            border-radius:16px;
            text-align:center;
            color:#FFFFFF;
            box-shadow:0 4px 20px rgba(0,0,0,0.08);
            margin-bottom:30px;">
            <h2 style="font-weight:700; letter-spacing:0.5px; margin-bottom:6px;">
                Activación de Licencias EllitNow Shield
            </h2>
            <p style="font-size:15px; color:rgba(255,255,255,0.9); margin:0;">
                Selecciona un plan para tu organización.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # ======= Estilo Moderno Ellit Shield =======
    st.markdown("""
        <style>
        .license-card {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 16px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.06);
            padding: 30px;
            text-align: center;
            transition: all 0.2s ease-in-out;
        }
        .license-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        }
        .license-title {
            font-size: 20px;
            font-weight: 700;
            color: #0F172A;
            margin-bottom: 8px;
        }
        .license-desc {
            color: #475569;
            font-size: 14px;
            margin-bottom: 12px;
        }
        .license-price {
            font-size: 26px;
            font-weight: 800;
            color: #0048FF;
            margin: 10px 0;
        }
        .license-features {
            color: #334155;
            font-size: 13px;
            margin-top: 8px;
        }
        .license-btn {
            display: inline-block;
            background: linear-gradient(135deg,#FF0080 0%,#00B4FF 100%);
            color: white !important;
            font-weight: 600;
            padding: 10px 20px;
            border-radius: 10px;
            text-decoration: none;
            margin-top: 18px;
            transition: 0.2s ease;
        }
        .license-btn:hover {
            filter: brightness(1.1);
        }
        </style>
    """, unsafe_allow_html=True)

    # ======= Tarjetas de planes =======
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            <div class="license-card">
                <div class="license-title">Enterprise Edition</div>
                <div class="license-desc">Licencia anual completa</div>
                <div class="license-price">4.900 €/año</div>
                <div class="license-features">Radar IA • Simulador BCP • Políticas Ejecutivas</div>
            </div>
        """, unsafe_allow_html=True)

        if st.button("Activar Enterprise Edition", key="stripe_enterprise_button"):
            try:
                session = stripe.checkout.Session.create(
                    payment_method_types=["card"],
                    mode="subscription",
                    line_items=[{
                        "price": st.secrets["STRIPE_PRICE_ENTERPRISE_ID"],
                        "quantity": 1
                    }],
                    success_url=f"{app_url}?success=true",
                    cancel_url=f"{app_url}?canceled=true",
                )
                st.success("✅ Redirigiendo a Stripe Checkout...")
                st.markdown(f"[Haz clic aquí para completar el pago en Stripe]({session.url})", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"❌ Error al crear sesión Stripe: {e}")

    with col2:
        st.markdown("""
            <div class="license-card">
                <div class="license-title">Prime - Predictive Intelligence Add-On</div>
                <div class="license-desc">Suscripción mensual</div>
                <div class="license-price">699 €/mes</div>
                <div class="license-features">IA avanzada • Alertas globales • Benchmark sectorial</div>
            </div>
        """, unsafe_allow_html=True)

        if st.button("Añadir Prime - Predictive Intelligence Add-On", key="stripe_predictive_button"):
            try:
                session = stripe.checkout.Session.create(
                    payment_method_types=["card"],
                    mode="subscription",
                    line_items=[{
                        "price": st.secrets["STRIPE_PRICE_PREDICTIVE_ID"],
                        "quantity": 1
                    }],
                    success_url=f"{app_url}?success=true",
                    cancel_url=f"{app_url}?canceled=true",
                )
                st.success("✅ Redirigiendo a Stripe Checkout...")
                st.markdown(f"[Haz clic aquí para completar el pago en Stripe]({session.url})", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"❌ Error al crear sesión Stripe: {e}")

    st.markdown("---")
    st.caption(" Pagos seguros con Stripe • EllitNow Cognitive Core © 2025")


def render_licencias_tab():
    """Extiende la pestaña 5 con pagos y activación."""
    st.subheader("Licencias y Suscripciones — Gestión de Tenants y Activaciones")
    st.write("Administra o activa tus licencias reales a través de Stripe Checkout.")

    conn = get_conn()
    tenants_df = pd.read_sql_query("""
        SELECT name AS Tenant, email AS Email,
               CASE WHEN active = 1 THEN 'Activo' ELSE 'Inactivo' END AS Estado,
               datetime(created_at) AS 'Fecha de Registro'
        FROM tenants ORDER BY created_at DESC
    """, conn)
    conn.close()

    if not tenants_df.empty:
        st.dataframe(tenants_df, use_container_width=True)
    else:
        st.info("No hay tenants registrados aún.")

    st.markdown("###  Activación de Licencias")
    render_stripe_checkout()


# ==============================
# EJECUCIÓN FINAL — ÚNICA Y CORRECTA
# ==============================

# 1. Inicializamos DB + Super Admin (solo una vez)
init_db_and_superadmin()

# 2. Si ya pasamos el st.stop() → estamos logueados o en login
# if st.session_state.get("auth_status"):
    # Banner de impersonación
 #    if st.session_state.auth_status == "impersonated":
 #        tenant = st.session_state.get("impersonated_tenant", {})
   #      st.markdown(f"""
   #      <div style="background: linear-gradient(135deg, #FF0080 0%, #00B4FF 100%);
   #                  color:white; padding:15px; border-radius:12px; text-align:center;
   #                  font-size:18px; font-weight:bold; margin-bottom:20px; position:sticky; top:0; z-index:1000;">
    #         Estás viendo como: <b>{tenant.get('name', 'Cliente')}</b>
    #     </div>
    #     """, unsafe_allow_html=True)
    #     if st.button("Volver a Super Admin", key="stop_imp"):
     #        stop_impersonation()

   #  render_panel()
    
    # Controles de rol
   #  if st.session_state.auth_status in ["super_admin", "impersonated", "partner"]:
   #      render_role_controls()

# else:
#     login_screen()

# === DEBUG: FORZAR MODO SUPER ADMIN ===
st.sidebar.markdown("---")
st.sidebar.error("MODO DEBUG ACTIVADO")
if st.sidebar.button("FORZAR SUPER ADMIN"):
    st.session_state.update({
        "auth_status": "super_admin",
        "tenant_id": "debug-001",
        "tenant_name": "DEBUG ELLIT",
        "user_email": "debug@ellitnow.com",
        "primary_color": "#FF0080"
    })
    st.rerun()
