# ==============================
# AI Executive Shield — EllitNow Cognitive Core Edition
# VERSIÓN AUTH REFACTORED — MINIMAL & CLEAN
# ==============================

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
from components.ellit_leaflet.ellit_leaflet import show_map

st.subheader("Mapa de prueba")
show_map({"mensaje": "hola"}, key="demo1")


# ==========================
# MAPA GLOBAL ELLIT THREAT
# ==========================
with st.container():
    st.subheader("🌍 Ellit Global Threat Intelligence Map")

    threat_data = {
        "countries": [
            {"country": "Spain", "lat": 40.4, "lng": -3.7, "risk": 70, "cves": 15},
            {"country": "USA", "lat": 38.0, "lng": -97.0, "risk": 85, "cves": 22},
        ]
    }

    show_map({"countries": threat_countries}, key="threatmap01")


# Inicializar cliente de OpenAI (asegúrate que exista en secrets.toml)
client = init_openai(st.secrets["OPENAI_API_KEY"])

st.markdown("""
    <style>
    
    /* 1️⃣ Evitar scroll horizontal global */
    html, body, [data-testid="stAppViewContainer"] {
        overflow-x: hidden !important;
    }

    /* 2️⃣ Centrar el contenido y limitar su ancho */
    div.block-container {
        max-width: 1250px;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }

    /* 3️⃣ Sidebar elegante sin romper el layout */
    section[data-testid="stSidebar"] {
        width: 220px !important;
        min-width: 220px !important;
        padding-right: 10px !important;
        padding-left: 10px !important;
        overflow-x: hidden !important;
    }

    /* 4️⃣ Prevenir desbordes de gráficos o contenedores */
    .element-container, .stPlotlyChart, .stPlot {
        max-width: 100% !important;
        overflow-x: hidden !important;
    }

    </style>
""", unsafe_allow_html=True)


# ==============================
# CONFIGURACIÓN DE PÁGINA
# ==============================
st.set_page_config(
    page_title="AI Executive Shield — EllitNow Cognitive Core",
    page_icon="🧠",
    layout="wide",
)

# ==============================
# ESTILO GLOBAL ELLIT SHIELD UI PRO
# ==============================
st.markdown("""
    <style>
    /* Fuente global */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
        background-color: #FFFFFF;
        color: #0F172A;
    }

    /* Sidebar corporativo fijo */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg,#0048FF 0%,#001F7F 100%);
        color: white;
        padding-top: 25px;
        border-right: 1px solid #eaeaea;
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] p {
        color: white !important;
    }
    section[data-testid="stSidebar"] a {
        color: #fff !important;
        text-decoration: none !important;
    }

    /* Contenedor principal */
    .main-container {
        background: #FFFFFF;
        border-radius: 20px;
        padding: 35px;
        margin-top: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        border: 1px solid #E2E8F0;
    }

    /* Cards de métricas */
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

    /* Títulos */
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

    /* Botones */
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

    /* Inputs y selects */
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

    /* Tabs */
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

    /* Tablas */
    .stDataFrame, .stTable {
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        border: 1px solid #E2E8F0;
        overflow: hidden;
    }

    /* Dashboard cards */
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

    hr {
        border: none;
        border-top: 1px solid #E2E8F0;
        margin: 25px 0;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================
# CONSTANTES / SESIÓN
# ==============================
SUPERADMIN_EMAIL = "admin@ellitnow.com"
SUPERADMIN_NAME = "Ellit Super Admin"
DEMO_EMAIL = "demo@ellitnow.com"
DEMO_PASSWORD = "Demo2025!g*E"
DEMO_TENANT_NAME = "DEMO - Ellit Shield"

for k, v in {
    "auth_status": None,      # super_admin, partner, client, demo, impersonated
    "user_role": None,        # rol real: super_admin, partner, client_admin, client_user, demo
    "user_id": None,
    "tenant_id": None,
    "tenant_name": None,
    "user_email": None,
    "primary_color": "#FF0080",
}.items():
    st.session_state.setdefault(k, v)

# ==============================
# BASE DE DATOS
# ==============================
TENANTS_DB = os.path.join(os.path.expanduser("~"), "ellit_tenants.db")

def get_conn():
    return sqlite3.connect(TENANTS_DB, check_same_thread=False)

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = ON;")

    # Tenants
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

    # Users
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            tenant_id TEXT,
            email TEXT UNIQUE NOT NULL,
            name TEXT,
            role TEXT NOT NULL,
            password_hash TEXT,
            is_active INTEGER DEFAULT 1,
            first_access_token TEXT,
            reset_token TEXT,
            reset_token_expiry TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (tenant_id) REFERENCES tenants(id)
        )
    """)

    conn.commit()

    # Super Admin: solo se gestiona por SUPER_ADMIN_KEY, pero creamos tenant interno si no existe
    c.execute("SELECT id FROM tenants WHERE email = ?", (SUPERADMIN_EMAIL,))
    row = c.fetchone()
    if not row:
        super_tenant_id = str(uuid.uuid4())
        c.execute("""
            INSERT INTO tenants (id, name, email, active, predictive, primary_color)
            VALUES (?, ?, ?, 1, 1, '#FF0080')
        """, (super_tenant_id, SUPERADMIN_NAME, SUPERADMIN_EMAIL))

    # Tenant y usuario DEMO
    c.execute("SELECT id FROM tenants WHERE email = ?", (DEMO_EMAIL,))
    row = c.fetchone()
    if row:
        demo_tenant_id = row[0]
    else:
        demo_tenant_id = str(uuid.uuid4())
        c.execute("""
            INSERT INTO tenants (id, name, email, active, predictive, primary_color)
            VALUES (?, ?, ?, 1, 1, '#0048FF')
        """, (demo_tenant_id, DEMO_TENANT_NAME, DEMO_EMAIL))

    c.execute("SELECT id FROM users WHERE email = ?", (DEMO_EMAIL,))
    row = c.fetchone()
    if not row:
        pwd_hash = bcrypt.hashpw(DEMO_PASSWORD.encode(), bcrypt.gensalt(12)).decode()
        demo_user_id = str(uuid.uuid4())
        c.execute("""
            INSERT INTO users (id, tenant_id, email, name, role, password_hash, is_active)
            VALUES (?, ?, ?, ?, ?, ?, 1)
        """, (demo_user_id, demo_tenant_id, DEMO_EMAIL, "Demo Comercial", "demo", pwd_hash))

    conn.commit()
    conn.close()

# Inicializar DB
init_db()

# ==============================
# UTILIDADES PDF CORPORATIVO
# ==============================
def generate_corporate_pdf(title: str, tenant_name: str, content: str, filename: str = "EllitNow_Report.pdf"):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    fuchsia = Color(1, 0, 0.5)
    blue = Color(0, 0.7, 1)

    # Fondo degradado
    for i in range(100):
        c = Color(1 - i/120, 0 + i/150, 0.5 + i/200)
        pdf.setFillColor(c)
        pdf.rect(0, (i/100)*height, width, height/100, stroke=0, fill=1)

    # Logo / branding
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

    # Título
    pdf.setFont("Helvetica-Bold", 18)
    pdf.setFillColor(fuchsia)
    pdf.drawString(40, height - 150, title)
    pdf.setFont("Helvetica", 11)
    pdf.setFillColorRGB(1, 1, 1)
    pdf.drawString(40, height - 170, f"Cliente: {tenant_name}")
    pdf.drawString(40, height - 185, f"Fecha: {_dt.datetime.now().strftime('%d/%m/%Y %H:%M')}")

    # Contenido
    pdf.setFont("Helvetica", 11)
    text_obj = pdf.beginText(40, height - 220)
    text_obj.setFillColorRGB(1, 1, 1)
    text_obj.setLeading(16)
    for line in content.split("\n"):
        text_obj.textLine(line)
    pdf.drawText(text_obj)

    pdf.setFont("Helvetica-Oblique", 9)
    pdf.setFillColor(blue)
    pdf.drawString(40, 40, "© 2025 EllitNow Cognitive Core — Confidential Document")
    pdf.drawRightString(width - 40, 40, "Página 1 de 1")

    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return buffer

def download_pdf_button(title, tenant_name, content, filename):
    pdf_buffer = generate_corporate_pdf(title, tenant_name, content, filename)
    st.download_button(
        label=f"Descargar {title}",
        data=pdf_buffer,
        file_name=filename,
        mime="application/pdf",
    )

# ==============================
# AUTENTICACIÓN / USUARIOS
# ==============================
def get_user_by_email(email: str):
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        SELECT u.id, u.email, u.name, u.role, u.tenant_id, u.password_hash, u.is_active,
               t.name, t.primary_color
        FROM users u
        LEFT JOIN tenants t ON u.tenant_id = t.id
        WHERE u.email = ?
        LIMIT 1
    """, (email,))
    row = c.fetchone()
    conn.close()
    if not row:
        return None
    return {
        "id": row[0],
        "email": row[1],
        "name": row[2],
        "role": row[3],
        "tenant_id": row[4],
        "password_hash": row[5],
        "is_active": bool(row[6]),
        "tenant_name": row[7] or "AI Executive Shield",
        "primary_color": row[8] or "#FF0080",
    }

def create_tenant_with_admin(name: str, email: str, tenant_type: str, parent_tenant_id: str | None = None):
    """
    Crea un tenant y un usuario admin asociado
    tenant_type: 'partner' o 'client'
    """
    conn = get_conn()
    c = conn.cursor()
    tenant_id = str(uuid.uuid4())
    primary_color = "#0048FF" if tenant_type == "partner" else "#FF0080"
    c.execute("""
        INSERT INTO tenants (id, name, email, active, predictive, primary_color, parent_tenant_id)
        VALUES (?, ?, ?, 1, 0, ?, ?)
    """, (tenant_id, name, email, primary_color, parent_tenant_id))

    user_id = str(uuid.uuid4())
    first_token = secrets.token_urlsafe(16)
    role = "partner" if tenant_type == "partner" else "client_admin"
    c.execute("""
        INSERT INTO users (id, tenant_id, email, name, role, is_active, first_access_token)
        VALUES (?, ?, ?, ?, ?, 0, ?)
    """, (user_id, tenant_id, email, f"Admin {name}", role, first_token))

    conn.commit()
    conn.close()
    return tenant_id, user_id, first_token

def activate_user_first_access(email: str, token: str, new_password: str) -> bool:
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        SELECT id, first_access_token FROM users
        WHERE email = ? AND is_active = 0
    """, (email,))
    row = c.fetchone()
    if not row:
        conn.close()
        return False
    user_id, stored_token = row
    if not stored_token or stored_token != token:
        conn.close()
        return False
    pwd_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt(12)).decode()
    c.execute("""
        UPDATE users
        SET password_hash = ?, is_active = 1, first_access_token = NULL
        WHERE id = ?
    """, (pwd_hash, user_id))
    conn.commit()
    conn.close()
    return True

def map_role_to_auth_status(role: str) -> str:
    if role == "super_admin":
        return "super_admin"
    if role == "partner":
        return "partner"
    if role in ("client_admin", "client_user"):
        return "client"
    if role == "demo":
        return "demo"
    return "demo"

# ==============================
# LOGIN SCREEN
# ==============================
def login_screen():
    st.markdown("""
        <div style="
            background: linear-gradient(135deg, #FF0080 0%, #00B4FF 100%);
            padding: 40px;
            border-radius: 18px;
            text-align: center;
            color: white;
            box-shadow: 0 10px 30px rgba(0,0,0,0.25);
            margin-top: 20px;
            margin-bottom: 20px;">
            <h2>Ellit Cognitive Core — Acceso Seguro</h2>
            <p>Acceso para Super Admin, partners, clientes y entorno demo.</p>
        </div>
    """, unsafe_allow_html=True)

    tab_login, tab_first, tab_reset = st.tabs(["Acceso Ellit", "Primer acceso", "Recuperar contraseña"])

    # Acceso normal
    with tab_login:
        col1, col2 = st.columns(2)

        # Super Admin por SUPER_ADMIN_KEY
        with col1:
            st.subheader("Super Admin")
            super_key = st.text_input("SUPER_ADMIN_KEY", type="password")
            if st.button("Entrar como Super Admin"):
                secret_key = st.secrets.get("SUPER_ADMIN_KEY", "")
                if super_key and super_key == secret_key:
                    st.session_state.update({
                        "auth_status": "super_admin",
                        "user_role": "super_admin",
                        "user_id": "superadmin",
                        "tenant_id": None,
                        "tenant_name": "Ellit Super Admin",
                        "user_email": SUPERADMIN_EMAIL,
                        "primary_color": "#FF0080",
                    })
                    st.success("Acceso concedido como Super Admin.")
                    st.rerun()
                else:
                    st.error("Clave de Super Admin incorrecta.")

        # Usuarios normales
        with col2:
            st.subheader("Usuarios Ellit (partners, clientes, demo)")

            with st.form("login_user_form"):
                email = st.text_input("Email corporativo")
                password = st.text_input("Contraseña", type="password")
                submitted = st.form_submit_button("Entrar")

            if submitted:
                if not email or not password:
                    st.error("Introduce email y contraseña.")
                else:
                    user = get_user_by_email(email.strip())
                    if not user:
                        st.error("Usuario no encontrado.")
                    elif not user["is_active"] or not user["password_hash"]:
                        st.error("Usuario no activado o sin contraseña. Usa 'Primer acceso'.")
                    else:
                        try:
                            if bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
                                auth_status = map_role_to_auth_status(user["role"])
                                st.session_state.update({
                                    "auth_status": auth_status,
                                    "user_role": user["role"],
                                    "user_id": user["id"],
                                    "tenant_id": user["tenant_id"],
                                    "tenant_name": user["tenant_name"],
                                    "user_email": user["email"],
                                    "primary_color": user["primary_color"],
                                })
                                st.success("Acceso correcto.")
                                st.rerun()
                            else:
                                st.error("Contraseña incorrecta.")
                        except Exception:
                            st.error("Error verificando contraseña.")

    # Primer acceso
    with tab_first:
        st.subheader("Activar usuario por primera vez")
        st.write("Introduce el email y el token de primer acceso proporcionado por tu administrador.")
        with st.form("first_access_form"):
            email_f = st.text_input("Email corporativo")
            token_f = st.text_input("Token de primer acceso")
            new_pwd = st.text_input("Nueva contraseña", type="password")
            new_pwd2 = st.text_input("Repite la nueva contraseña", type="password")
            submitted_f = st.form_submit_button("Activar cuenta")

        if submitted_f:
            if not email_f or not token_f or not new_pwd or not new_pwd2:
                st.error("Rellena todos los campos.")
            elif new_pwd != new_pwd2:
                st.error("Las contraseñas no coinciden.")
            else:
                ok = activate_user_first_access(email_f.strip(), token_f.strip(), new_pwd)
                if ok:
                    st.success("Cuenta activada correctamente. Ahora puedes iniciar sesión desde la pestaña 'Acceso Ellit'.")
                else:
                    st.error("No se pudo activar la cuenta. Revisa email y token.")

    # Reset de contraseña (stub simple)
    with tab_reset:
        st.subheader("Recuperar contraseña")
        st.info("La recuperación de contraseña se implementará enviando un token al correo corporativo. Por ahora, contacta con el administrador para un nuevo token de primer acceso.")


# ==============================
# ROLES / IMPERSONACIÓN
# ==============================
def get_partner_clients(partner_id):
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
    if st.session_state.get("auth_status") != "super_admin":
        st.error("No tienes permiso para impersonar tenants.")
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
        st.session_state["tenant_id"] = tenant[0]
        st.session_state["tenant_name"] = tenant[1]
        st.session_state["primary_color"] = tenant[3] or "#FF0080"
        st.success(f"Ahora estás viendo como: {tenant[1]}")
        st.rerun()
    else:
        st.error("Tenant no encontrado.")

def stop_impersonation():
    if "impersonated_tenant" in st.session_state:
        del st.session_state["impersonated_tenant"]
    st.session_state["auth_status"] = "super_admin"
    st.sidebar.success("Volviste al modo Super Admin")
    st.rerun()

def render_role_controls():
    role = st.session_state.get("auth_status")
    st.sidebar.markdown("---")

    # SUPER ADMIN
    if role == "super_admin":
        st.sidebar.markdown("### Impersonación de Tenants")
        conn = get_conn()
        tenants_df = pd.read_sql_query("SELECT id, name FROM tenants ORDER BY name ASC", conn)
        conn.close()

        if tenants_df.empty:
            st.sidebar.info("No hay tenants disponibles.")
        else:
            tenant_options = {row["name"]: row["id"] for _, row in tenants_df.iterrows()}
            target = st.sidebar.selectbox(
                "Selecciona un tenant para ver como",
                list(tenant_options.keys()),
                key=f"impersonation_selectbox_{uuid.uuid4()}"
            )
            if st.sidebar.button("Ver como este tenant"):
                impersonate_tenant(tenant_options[target])

        st.sidebar.markdown("---")
        st.sidebar.markdown("### Crear nuevo tenant")

        with st.sidebar.form("create_tenant_form"):
            tipo_tenant = st.selectbox("Tipo", ["Partner", "Cliente directo"])
            nombre = st.text_input("Nombre del cliente")
            email = st.text_input("Email administrador")
            submitted = st.form_submit_button("Crear tenant")

        if submitted:
            if not nombre or not email:
                st.sidebar.error("Nombre y email son obligatorios.")
            else:
                tenant_type = "partner" if tipo_tenant == "Partner" else "client"
                parent_id = None
                tenant_id, user_id, token = create_tenant_with_admin(nombre, email, tenant_type, parent_id)
                st.sidebar.success(f"Tenant '{nombre}' creado correctamente.")
                st.sidebar.write("Token de primer acceso para el administrador:")
                st.sidebar.code(token, language="bash")

    # IMPERSONATED
    elif role == "impersonated":
        tenant = st.session_state.get("impersonated_tenant", {})
        st.sidebar.markdown(f"### Modo Impersonación\nViendo como: **{tenant.get('name','')}**")
        if st.sidebar.button("Volver a Super Admin"):
            stop_impersonation()

    # PARTNER
    elif role == "partner":
        st.sidebar.markdown("### Tus clientes")
        partner_id = st.session_state.get("tenant_id")
        clients = get_partner_clients(partner_id)
        if clients:
            for c in clients:
                status = "Activo" if c[3] == 1 else "Inactivo"
                st.sidebar.write(f"{c[1]} — {status}")
        else:
            st.sidebar.info("Aún no tienes clientes asociados.")

        st.sidebar.markdown("---")
        st.sidebar.subheader("Crear cliente")
        with st.sidebar.form("create_client_form"):
            name = st.text_input("Nombre del cliente")
            email = st.text_input("Correo administrador")
            submitted = st.form_submit_button("Crear cliente")
        if submitted and name and email:
            tenant_id, user_id, token = create_tenant_with_admin(name, email, "client", parent_tenant_id=partner_id)
            st.sidebar.success(f"Cliente '{name}' creado correctamente.")
            st.sidebar.write("Token de primer acceso del administrador:")
            st.sidebar.code(token, language="bash")

    # DEMO
    elif role == "demo":
        st.sidebar.markdown("### Modo demo")
        st.sidebar.info("Estás usando el entorno de demostración comercial.")
        if st.sidebar.button("Cerrar sesión demo"):
            for k in ["auth_status", "user_role", "user_id", "tenant_id", "tenant_name", "user_email"]:
                st.session_state[k] = None
            st.rerun()


# ==============================
# PANEL PRINCIPAL
# ==============================
def render_panel():
    role = st.session_state.get("auth_status", "demo")
    tenant_name = st.session_state.get("tenant_name", "AI Executive Shield")
    primary_color = st.session_state.get("primary_color", "#FF0080")

    # Super Admin: selector de tenant activo
    if role == "super_admin":
        conn = get_conn()
        tenants = conn.execute("SELECT id, name FROM tenants ORDER BY name ASC").fetchall()
        conn.close()
        if tenants:
            tenant_map = {t[1]: t[0] for t in tenants}
            st.markdown("### Seleccionar tenant activo (modo Super Admin)")
            chosen_tenant = st.selectbox("Tenant activo", list(tenant_map.keys()))
            st.session_state["tenant_id"] = tenant_map[chosen_tenant]
            st.session_state["tenant_name"] = chosen_tenant
            tenant_name = chosen_tenant
        else:
            st.warning("No existen tenants disponibles. Crea uno desde el panel de administración.")

    # Encabezado
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, {primary_color} 0%, #00B4FF 100%);
            color:white; padding:25px; text-align:center; border-radius:15px;">
            <h1>{tenant_name}</h1>
            <p>{role.title()} • Ellit Cognitive Core 2025</p>
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Radar IA", 
        "Panel de Continuidad de Negocio", 
        "Políticas IA", 
        "Predictive", 
        "Licencias"
    ])

    # ------------------------------------------------------------------
    # TAB 1 — Radar IA
    # ------------------------------------------------------------------
    with tab1:
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
                Radar IA — Cognitive Risk Engine
            </h2>
            <p style="font-size:15px; color:rgba(255,255,255,0.9); margin:0;">
                Evaluación cognitiva avanzada de madurez, cumplimiento y resiliencia organizacional.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Perfil de la organización")
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
            responsable = st.text_input("CISO / Responsable de seguridad", "Anónimo")

        riesgos = st.text_area("Riesgos principales detectados",
                               placeholder="Ejemplo: ransomware, fuga de datos, cumplimiento GDPR, dependencias críticas...")
        certificaciones = st.text_area("Certificaciones y marcos aplicables",
                                       placeholder="Ejemplo: ISO 27001, ENS Medio, NIST CSF, SOC 2 Tipo II...")

        # INTEGRACIÓN DEL NUEVO MOTOR COGNITIVO
        if st.button("Analizar con Ellit Cognitive Core", key="analizar_radar_ia"):
            with st.spinner("Analizando contexto organizacional..."):

                context = {
                    "organizacion": nombre_org,
                    "sector": sector,
                    "nivel_ens": nivel_ens,
                    "tamano": tamano,
                    "region": region,
                    "responsable": responsable,
                    "riesgos_detectados": riesgos,
                    "certificaciones": certificaciones
                }

                try:
                    data = analyze_radar_ia(client, context)

                    if data is not None:
                        st.session_state["radar_data"] = data
                        st.success("Análisis completado correctamente.")
                    else:
                        st.error("No se pudo interpretar la respuesta del motor cognitivo.")

                except Exception as e:
                    st.error(f"Error al procesar el análisis: {str(e)}")

        else:
            data = st.session_state.get("radar_data", None)

        # Presentación del informe si existe
        if data:
            st.markdown("### Evaluación global de madurez y riesgo")

            indicadores = data.get("indicadores", {})
            if indicadores:
                c1, c2 = st.columns(2)
                with c1:
                    st.subheader("Madurez del SGSI")
                    from matplotlib.patches import Wedge, Circle
                    madurez = indicadores.get("Madurez SGSI", 0)
                    fig, ax = plt.subplots(figsize=(5, 3))
                    ax.add_patch(Circle((0, 0), 1, color='white', ec='none'))
                    ax.add_patch(Wedge((0, 0), 1, 180, 260, facecolor='#FF4B4B'))
                    ax.add_patch(Wedge((0, 0), 1, 260, 300, facecolor='#FFD93D'))
                    ax.add_patch(Wedge((0, 0), 1, 300, 360, facecolor='#6DFF8C'))
                    ang = 180 + (madurez * 180 / 100)
                    x = np.cos(np.deg2rad(ang))
                    y = np.sin(np.deg2rad(ang))
                    ax.plot([0, x], [0, y], color='#333', lw=3)
                    ax.plot(0, 0, 'o', color='#333', markersize=8)
                    ax.text(0, -0.2, f"{int(madurez)}", ha='center', va='center', fontsize=32, fontweight='bold', color='#444')
                    ax.text(0, -0.4, "Nivel de madurez", ha='center', fontsize=10, color='#666')
                    ax.set_xlim(-1.2, 1.2)
                    ax.set_ylim(-0.2, 1.1)
                    ax.axis('off')
                    st.pyplot(fig)

                with c2:
                    st.subheader("Radar ENS–ISO–NIST")
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

                st.markdown("---")
                c3, c4 = st.columns(2)
                with c3:
                    st.subheader("Distribución general de controles")
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

                with c4:
                    st.subheader("Riesgo comparativo del sector")
                    riesgo_sector = np.random.randint(30, 90)
                    riesgo_org = 100 - indicadores.get("Madurez SGSI", 0)
                    categorias = ["Media del sector", "Organización"]
                    valores = [riesgo_sector, riesgo_org]
                    fig4, ax4 = plt.subplots(figsize=(4.5, 3))
                    colores = ["#00B4FF", "#FF0080"]
                    ax4.bar(categorias, valores, color=colores)
                    for i, v in enumerate(valores):
                        ax4.text(i, v + 2, f"{v}%", ha='center', fontsize=11, fontweight='bold')
                    ax4.set_ylim(0, 100)
                    ax4.set_ylabel("Nivel de riesgo (%)")
                    st.pyplot(fig4)

            analisis = data.get("analisis", "")
            if analisis:
                st.markdown("### Análisis ejecutivo")
                st.info(analisis)

            acciones = data.get("acciones", {})
            if acciones:
                st.markdown("### Acciones prioritarias")
                for horizonte, tareas in acciones.items():
                    with st.expander(horizonte):
                        for t in tareas:
                            st.markdown(f"- {t}")

            recomendaciones = data.get("recomendaciones", [])
            if recomendaciones:
                st.markdown("### Recomendaciones estratégicas")
                for r in recomendaciones:
                    st.markdown(f"- {r}")

            alertas = data.get("alertas", [])
            if alertas:
                st.markdown("### Alertas críticas")
                for a in alertas:
                    st.error(a)

        st.markdown("---")
        st.markdown("### Exportar informe PDF")
        estilo = st.selectbox("Estilo del informe PDF", ["Clásico", "Corporativo", "Ellit"], index=2)
        if st.button("Generar informe PDF"):
            try:
                radar_data = st.session_state.get("radar_data", None)
                if radar_data is None:
                    st.warning("Primero ejecuta el análisis con Ellit Cognitive Core.")
                else:
                    resumen = radar_data.get("analisis", "Sin análisis generado.")
                    indicadores = radar_data.get("indicadores", {})
                    partes = [f"Informe Radar IA — {nombre_org}", "", f"Sector: {sector}", f"Nivel ENS actual: {nivel_ens}", f"Tamaño: {tamano}", f"Región: {region}", "", "Resumen ejecutivo:", resumen, "", "Indicadores clave:"]
                    for k, v in indicadores.items():
                        partes.append(f"- {k}: {v}%")
                    content = "\n".join(partes)
                    pdf_name = f"RadarIA_Report_{nombre_org.replace(' ', '_')}.pdf"
                    download_pdf_button("Informe Radar IA", nombre_org, content, pdf_name)
            except Exception:
                st.error("Error al generar el PDF.")


    # ------------------------------------------------------------------
    # TAB 2 — Panel de Continuidad de Negocio (BCP + SGSI)
    # ------------------------------------------------------------------
    with tab2:
        st.subheader("Generador de Plan de Continuidad ISO 22301 / ENS OP.BCP")

        tenant_name_input = st.text_input("Nombre de la organización", placeholder="Ej: Fraudfense")
        procesos_criticos = st.text_area(
            "Procesos críticos del negocio",
            "Facturación, Atención al cliente, Plataforma web, Operaciones TI"
        )
        infraestructura = st.text_area(
            "Infraestructura disponible",
            "2 CPDs en Madrid, Cloud Azure, VPN corporativa, Firewalls redundantes"
        )
        dependencias = st.text_area(
            "Dependencias tecnológicas y humanas",
            "ERP SAP, Microsoft 365, API de clientes, Proveedor ISP Telefónica"
        )
        rto = st.slider("RTO (tiempo máximo de recuperación, horas)", 1, 72, 6)
        rpo = st.slider("RPO (pérdida máxima aceptable de datos, horas)", 0, 24, 1)

        st.markdown("### Análisis cognitivo del contexto de continuidad")
        contexto_libre = st.text_area(
            "Describe el contexto o el problema de continuidad que deseas analizar",
            placeholder=(
                "Ejemplo: Tengo dos CPDs pero están en la misma ciudad. "
                "¿Qué debería hacer para mejorar la resiliencia?"
            )
        )

        if st.button("Generar plan de continuidad con Ellit Cognitive Core"):
            org_name = tenant_name_input or tenant_name
            bcp_input = {
                "organizacion": org_name,
                "procesos_criticos": procesos_criticos,
                "infraestructura": infraestructura,
                "dependencias": dependencias,
                "rto_horas": rto,
                "rpo_horas": rpo,
                "contexto_adicional": contexto_libre,
            }

            try:
                with st.spinner("Generando plan de continuidad con Ellit Cognitive Core..."):
                    plan_text = generate_bcp_plan(client, bcp_input)

                if plan_text:
                    st.text_area("Vista previa del plan", plan_text, height=420)
                    pdf_filename = f"Plan_BCP_{org_name.replace(' ', '_')}.pdf"
                    download_pdf_button(
                        f"Plan_BCP_{org_name}",
                        org_name,
                        plan_text,
                        pdf_filename
                    )
                else:
                    st.error("No se pudo generar el plan de continuidad.")
            except Exception as e:
                st.error(f"Error al generar el plan de continuidad: {str(e)}")

        st.markdown("---")
        st.subheader("Simulador de crisis BCP")

        escenario = st.text_input(
            "Describe el escenario de crisis a simular",
            placeholder="Ejemplo: Pérdida total de conectividad entre CPDs durante 12 horas"
        )
        ubicacion = st.text_input(
            "Ubicación o entorno afectado",
            placeholder="Ej: CPD Madrid o sede principal"
        )
        duracion = st.slider("Duración estimada de la interrupción (horas)", 1, 72, 8)
        impacto = st.select_slider("Nivel de impacto", ["Bajo", "Medio", "Alto"], value="Alto")

        if st.button("Simular escenario de crisis"):
            if not tenant_name_input:
                cliente_sim = tenant_name
            else:
                cliente_sim = tenant_name_input

            if "CPD" in escenario or "conectividad" in escenario.lower():
                estrategia = "Activar replicación en región secundaria y habilitar conexión VPN temporal."
            elif "ransomware" in escenario.lower():
                estrategia = "Aislar servidores afectados y restaurar desde copias inmutables."
            elif "inundación" in escenario.lower() or "incendio" in escenario.lower():
                estrategia = "Trasladar operaciones al sitio alternativo y priorizar funciones críticas."
            elif "personal" in escenario.lower() or "empleados" in escenario.lower():
                estrategia = "Activar protocolo de contingencia de recursos humanos y teletrabajo."
            else:
                estrategia = "Aplicar protocolo general de continuidad ajustado a dependencias críticas."

            plan_sim = f"""
SIMULACIÓN DE ESCENARIO BCP — ELLIT COGNITIVE CORE

Cliente: {cliente_sim}
Escenario: {escenario}
Ubicación afectada: {ubicacion}
Duración estimada: {duracion} horas
Impacto: {impacto}

ESTRATEGIA DE RECUPERACIÓN RECOMENDADA
{estrategia}

© 2025 Ellit Cognitive Core — Simulador de continuidad
"""
            st.text_area("Resultado de la simulación", plan_sim, height=320)
            pdf_name_sim = f"Simulacion_BCP_{cliente_sim.replace(' ', '_')}.pdf"
            download_pdf_button(
                f"Simulacion_BCP_{cliente_sim}",
                cliente_sim,
                plan_sim,
                pdf_name_sim
            )

        st.markdown("---")
        st.subheader("Evaluación rápida de madurez SGSI (ENS / ISO 27001 / NIST CSF)")

        evidencias_text = st.text_area(
            "Evidencias disponibles (auditorías, informes, KPIs, hallazgos)",
            placeholder="Ejemplo: Informe auditoría interna 2024, revisión de accesos, análisis de vulnerabilidades..."
        )
        controles_text = st.text_area(
            "Controles implementados (resumen ejecutivo)",
            placeholder="Ejemplo: Controles de acceso RBAC, cifrado en reposo, SOC 24x7, bastionado de servidores..."
        )

        if st.button("Calcular madurez SGSI con Ellit Cognitive Core"):
            if not evidencias_text.strip() and not controles_text.strip():
                st.warning("Introduce al menos evidencias o controles para poder evaluar.")
            else:
                try:
                    with st.spinner("Calculando madurez del SGSI..."):
                        sgsi_result = compute_sgsi_maturity(client, evidencias_text, controles_text)

                    if sgsi_result:
                        madurez_val = sgsi_result.get("madurez", 0) or 0
                        nivel_val = sgsi_result.get("nivel", "No determinado")

                        st.markdown(f"**Nivel de madurez:** {nivel_val} ({madurez_val}%)")

                        col_s1, col_s2 = st.columns(2)
                        with col_s1:
                            st.markdown("**Fortalezas**")
                            for f_item in sgsi_result.get("fortalezas", []):
                                st.markdown(f"- {f_item}")
                        with col_s2:
                            st.markdown("**Debilidades**")
                            for d_item in sgsi_result.get("debilidades", []):
                                st.markdown(f"- {d_item}")

                        acciones_req = sgsi_result.get("acciones_requeridas", [])
                        if acciones_req:
                            st.markdown("**Acciones requeridas prioritarias**")
                            for a_item in acciones_req:
                                st.markdown(f"- {a_item}")
                    else:
                        st.error("No se pudo interpretar la respuesta del motor de madurez SGSI.")
                except Exception as e:
                    st.error(f"Error al calcular la madurez SGSI: {str(e)}")


    # ------------------------------------------------------------------
    # TAB 3 — Generador de Políticas (multinormativo)
    # ------------------------------------------------------------------
    with tab3:
        st.markdown("""
        <div style="background: linear-gradient(135deg,#FF0080 0%,#00B4FF 100%);
                    padding:18px;border-radius:16px;color:white;text-align:center;">
            <h2>Generador de políticas corporativas — Ellit Cognitive Core</h2>
            <p>Redacta políticas y procedimientos multinormativos listos para auditoría.</p>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            tipo = st.text_input("Tipo de política", "Gestión de accesos físicos")
        with c2:
            normativa = st.selectbox(
                "Normativa principal",
                ["ISO 27001", "ENS", "NIST CSF", "SOC 2", "GDPR", "COBIT", "PCI DSS"]
            )
        with c3:
            detalle = st.slider("Nivel de detalle del documento", 1, 5, 3)

        if st.button("Generar política con Ellit Cognitive Core"):
            try:
                org_name = tenant_name
                st.info("Generando documento corporativo con Ellit Cognitive Core...")

                policy_text = generate_policy(
                    client=client,
                    tipo=tipo,
                    normativa=normativa,
                    organizacion=org_name,
                    detalle=detalle
                )

                if "policy_history" not in st.session_state:
                    st.session_state["policy_history"] = []
                st.session_state["policy_history"].insert(0, {
                    "tipo": tipo,
                    "normativa": normativa,
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "organizacion": org_name,
                    "contenido": policy_text
                })
                st.session_state["policy_history"] = st.session_state["policy_history"][:10]

                st.success(f"Política corporativa de {tipo} generada bajo {normativa}.")

                with st.expander("Vista previa del documento"):
                    st.markdown(policy_text)

                with st.expander("Recomendaciones del Cognitive Core"):
                    st.info(
                        f"Se recomienda validar esta política con los controles aplicables de {normativa} "
                        "y mantener revisión anual por el Comité de Seguridad."
                    )

                fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
                encabezado = f"""
POLÍTICA CORPORATIVA — {tipo.upper()}
Organización: {org_name}
Normativa base: {normativa}
Fecha: {fecha_actual}
Ellit Cognitive Core — Documento generado automáticamente
------------------------------------------------------------

"""
                documento_final = encabezado + policy_text
                pdf_filename = f"Politica_{tipo.replace(' ', '_')}.pdf"
                download_pdf_button(f"Politica_{tipo}", org_name, documento_final, pdf_filename)

            except Exception as e:
                st.error(f"Error generando la política: {str(e)}")

        if "policy_history" in st.session_state and st.session_state["policy_history"]:
            st.markdown("---")
            st.markdown("### Historial de políticas generadas")
            for item in st.session_state["policy_history"]:
                tipo_item = item.get("tipo", "Sin tipo")
                normativa_item = item.get("normativa", "Sin normativa")
                fecha_item = item.get("fecha", "Sin fecha")
                org_item = item.get("organizacion", tenant_name)
                st.markdown(f"""
                <div style="background:#F8FAFC;
                            padding:12px;
                            border-radius:10px;
                            margin-bottom:8px;
                            border:1px solid #E2E8F0;">
                    <b>{tipo_item}</b> — {normativa_item}<br>
                    {fecha_item} | {org_item}
                </div>
                """, unsafe_allow_html=True)

    # ------------------------------------------------------------------
    # TAB 4 — Ellit Predictive Intelligence (Leaflet + Cognitive Core)
    # ------------------------------------------------------------------
    with tab4:

        st.markdown("""
        <style>
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
            <div class="dashboard-title">Ellit Predictive Intelligence</div>
            <div class="dashboard-sub">Panel ejecutivo de inteligencia viva para CISOs</div>
        </div>
        """, unsafe_allow_html=True)

        # ----------------------------------------------------------------------
        # Filters
        # ----------------------------------------------------------------------
        col1_p, col2_p, col3_p = st.columns(3)

        with col1_p:
            sector_p = st.selectbox(
                "Sector",
                [
                    "Banca y Finanzas", "Salud", "Educación",
                    "Energía", "Retail y E-commerce",
                    "Tecnología", "Industria",
                    "Defensa", "Sector Público"
                ]
            )

        with col2_p:
            pais = st.text_input("País / Región", "España")

        with col3_p:
            madurez_p = st.slider("Madurez ENS/ISO (percepción interna)", 1, 5, 3)

        base_costos = {
            "Banca y Finanzas": 520000,
            "Salud": 480000,
            "Educación": 250000,
            "Energía": 600000,
            "Retail y E-commerce": 310000,
            "Tecnología": 400000,
            "Industria": 350000,
            "Defensa": 700000,
            "Sector Público": 300000,
        }

        costo_promedio = base_costos.get(sector_p, 350000)

        predictive_input = {
            "sector": sector_p,
            "region": pais,
            "madurez": madurez_p,
            "costo_medio_sector": costo_promedio,
            "tenant": tenant_name,
        }

        riesgo_sectorial_val = None
        impacto_estimado_val = None
        amenazas_emergentes = []
        tendencias_list = []
        recomendaciones_list = []

        # ----------------------------------------------------------------------
        # Predictive Intelligence Engine
        # ----------------------------------------------------------------------
        try:
            with st.spinner("Generando análisis predictivo con Ellit Cognitive Core..."):
                predictive_data = generate_predictive_analysis(client, predictive_input)

            if predictive_data:
                raw_riesgo = predictive_data.get("riesgo_sectorial", "")
                nums = re.findall(r"\d+", str(raw_riesgo))
                riesgo_sectorial_val = int(nums[0]) if nums else random.randint(60, 95)

                raw_impacto = predictive_data.get("impacto_estimado", "")
                nums_i = re.findall(r"\d+", str(raw_impacto).replace(".", "").replace(",", ""))

                impacto_estimado_val = (
                    float(nums_i[0])
                    if nums_i
                    else costo_promedio * (riesgo_sectorial_val / 100) * (1.2 - (madurez_p / 10))
                )

                amenazas_emergentes = predictive_data.get("amenazas_emergentes", []) or []
                tendencias_list = predictive_data.get("tendencias", []) or []
                recomendaciones_list = predictive_data.get("recomendaciones", []) or []

            else:
                riesgo_sectorial_val = random.randint(60, 95)
                impacto_estimado_val = costo_promedio * (riesgo_sectorial_val / 100)

        except Exception:
            riesgo_sectorial_val = random.randint(60, 95)
            impacto_estimado_val = costo_promedio * (riesgo_sectorial_val / 100)

        riesgo_sectorial_val = riesgo_sectorial_val or random.randint(60, 95)

        # ----------------------------------------------------------------------
        # Session State
        # ----------------------------------------------------------------------
        st.session_state["riesgo_sectorial_val"] = riesgo_sectorial_val
        st.session_state["impacto_estimado_val"] = impacto_estimado_val
        st.session_state["amenazas_emergentes"] = amenazas_emergentes
        st.session_state["tendencias_list"] = tendencias_list
        st.session_state["recomendaciones_list"] = recomendaciones_list

        # ----------------------------------------------------------------------
        # KPI Cards
        # ----------------------------------------------------------------------
        st.markdown('<div class="section-title">Indicadores clave de riesgo</div>', unsafe_allow_html=True)
        k1, k2, k3, k4 = st.columns(4)

        indicadores_top = [
            ("Riesgo sectorial estimado", f"{riesgo_sectorial_val:.0f}%"),
            ("Madurez declarada", f"{madurez_p}/5"),
            ("Coste medio sectorial (€)", f"{costo_promedio:,.0f}"),
            ("Impacto potencial (€)", f"{impacto_estimado_val:,.0f}"),
        ]

        for col, (label, val) in zip([k1, k2, k3, k4], indicadores_top):
            with col:
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{val}</div>
                </div>
                """, unsafe_allow_html=True)

        # ----------------------------------------------------------------------
        # Leaflet + Cognitive Core Intelligence
        # ----------------------------------------------------------------------
        c1_p2, c2_p2 = st.columns([2, 1])

        with c1_p2:
            st.markdown(
                '<div class="section-title">Mapa global de inteligencia de amenazas</div>',
                unsafe_allow_html=True
            )

            threat_countries = [
                {
                    "country": "España",
                    "lat": 40.4168,
                    "lng": -3.7038,
                    "risk": riesgo_sectorial_val,
                    "cves": random.randint(30, 90),
                    "ransomware": random.randint(5, 20),
                    "supply_chain": random.randint(3, 15),
                    "critical": random.randint(3, 12),
                },
                {
                    "country": "Estados Unidos",
                    "lat": 38.9072,
                    "lng": -77.0369,
                    "risk": random.randint(70, 95),
                    "cves": random.randint(110, 180),
                    "ransomware": random.randint(20, 40),
                    "supply_chain": random.randint(15, 30),
                    "critical": random.randint(15, 35),
                }
            ]

            show_map({"countries": threat_countries}, key="ellit_map_sectorial")

        with c2_p2:
            st.markdown(
                '<div class="section-title">Inteligencia del Cognitive Core</div>',
                unsafe_allow_html=True
            )

            if amenazas_emergentes:
                st.markdown("**Amenazas emergentes sectoriales**")
                for a in amenazas_emergentes:
                    st.markdown(f"- {a}")

            if tendencias_list:
                st.markdown("**Tendencias globales relevantes**")
                for t in tendencias_list:
                    st.markdown(f"- {t}")

            if recomendaciones_list:
                st.markdown("**Recomendaciones estratégicas**")
                for r in recomendaciones_list:
                    st.markdown(f"- {r}")

    # ------------------------------------------------------------------
    # TAB 5 — Licencias y Suscripciones
    # ------------------------------------------------------------------
    with tab5:
        render_licencias_tab()


# ==============================
# LICENCIAS / STRIPE
# ==============================
def render_stripe_checkout():
    stripe_key = st.secrets.get("STRIPE_SECRET_KEY")
    app_url = st.secrets.get("APP_URL", "https://ellitnow.com")

    if not stripe_key:
        st.error("Stripe no está configurado correctamente.")
        return

    stripe.api_key = stripe_key

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
                Activación de licencias EllitNow Shield
            </h2>
            <p style="font-size:15px; color:rgba(255,255,255,0.9); margin:0;">
                Selecciona un plan para tu organización.
            </p>
        </div>
    """, unsafe_allow_html=True)

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
        </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            <div class="license-card">
                <div class="license-title">Enterprise Edition</div>
                <div class="license-desc">Licencia anual completa</div>
                <div class="license-price">4.900 €/año</div>
                <div class="license-features">Radar IA • Simulador BCP • Políticas ejecutivas</div>
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
                st.success("Redirigiendo a Stripe Checkout...")
                st.markdown(f"[Haz clic aquí para completar el pago en Stripe]({session.url})", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error al crear sesión Stripe: {e}")

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
                st.success("Redirigiendo a Stripe Checkout...")
                st.markdown(f"[Haz clic aquí para completar el pago en Stripe]({session.url})", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error al crear sesión Stripe: {e}")

    st.markdown("---")
    st.caption("Pagos seguros con Stripe • EllitNow Cognitive Core © 2025")

def render_licencias_tab():
    st.subheader("Licencias y suscripciones — gestión de tenants y activaciones")
    st.write("Administra o activa tus licencias reales a través de Stripe Checkout.")

    conn = get_conn()
    tenants_df = pd.read_sql_query("""
        SELECT name AS Tenant, email AS Email,
               CASE WHEN active = 1 THEN 'Activo' ELSE 'Inactivo' END AS Estado,
               datetime(created_at) AS 'Fecha de registro'
        FROM tenants ORDER BY created_at DESC
    """, conn)
    conn.close()

    if not tenants_df.empty:
        st.dataframe(tenants_df, use_container_width=True)
    else:
        st.info("No hay tenants registrados aún.")

    st.markdown("### Activación de licencias")
    render_stripe_checkout()

# ==============================
# EJECUCIÓN PRINCIPAL
# ==============================
if st.session_state.get("auth_status"):
    # Banner de impersonación si aplica
    if st.session_state.get("auth_status") == "impersonated":
        tenant = st.session_state.get("impersonated_tenant", {})
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #FF0080 0%, #00B4FF 100%);
                    color:white; padding:15px; border-radius:12px; text-align:center;
                    font-size:16px; font-weight:bold; margin-bottom:20px; position:sticky; top:0; z-index:1000;">
            Estás viendo como: <b>{tenant.get('name', 'Cliente')}</b>
        </div>
        """, unsafe_allow_html=True)

    render_panel()

    if st.session_state.auth_status in ["super_admin", "impersonated", "partner"]:
        render_role_controls()
else:
    login_screen()
