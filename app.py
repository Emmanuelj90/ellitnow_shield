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

# Inicializar cliente de OpenAI (asegúrate que exista en secrets.toml)
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



# -if os.path.exists("ellit.db"):
# -    os.remove("ellit.db")
 # -   st.warning(">>> BASE DE DATOS ellit.db BORRADA (TEMPORAL) <<<")

# Ajuste visual moderno: corrige desplazamientos y desbordes
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

    /* 3️⃣ Sidebar fijo sin afectar el main */
    section[data-testid="stSidebar"] {
        min-width: 260px !important;
        max-width: 260px !important;
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
    # TAB 1 — Radar IA (toda tu lógica existente, sin iconos)
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

        # Perfil organizacional
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

        if st.button("Analizar con Ellit Cognitive Core", key="analizar_radar_ia"):
            import re as _re
            with st.spinner("Analizando contexto de seguridad y madurez organizacional..."):
                try:
                    prompt = f"""
Eres Ellit Cognitive Core, motor cognitivo especializado en ENS, ISO 27001, NIST CSF y continuidad ISO 22301.
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
                    match = _re.search(r"\{.*\}", raw, _re.S)
                    if match:
                        data = json.loads(match.group(0))
                        st.session_state["radar_data"] = data
                        st.success(f"Análisis completado para {nombre_org}")
                    else:
                        st.error("No se pudo interpretar la respuesta del núcleo cognitivo.")
                        data = None

                except Exception as e:
                    st.error(f"Error al conectar con Ellit Cognitive Core: {str(e)}")
                    data = None
        else:
            data = st.session_state.get("radar_data", None)

        if data:
            st.markdown("### Evaluación global de madurez y riesgo")

            indicadores = data.get("indicadores", {})
            if indicadores:
                # Fila 1: gauge + radar
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

        # Evaluación documental ENS (igual que tenías)
        if data:
            st.markdown("### Evaluación documental ENS — Nivel objetivo")
            st.info("Analiza los documentos existentes y los requeridos para alcanzar el nivel ENS superior.")

            documentos_existentes = st.text_area(
                "Documentos existentes (uno por línea)",
                placeholder="Ejemplo:\nPolítica de Seguridad de la Información\nGestión de Riesgos\nProcedimiento de Control de Accesos"
            ).splitlines()

            controles_faltantes = st.text_area(
                "Controles ENS faltantes (uno por línea, formato: MP.INFO.1, OP.ACC.2, etc.)",
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

            def calcular_documentos_faltantes(ctrls_f, docs_ex, nivel_ens_local):
                documentos_faltantes = []
                for control in ctrls_f:
                    control = control.strip()
                    if not control:
                        continue
                    doc_requerido = mapa_controles_docs.get(control)
                    if doc_requerido and all(doc_requerido.lower() not in d.lower() for d in docs_ex):
                        documentos_faltantes.append(f"{control} → {doc_requerido}")

                if nivel_ens_local == "Medio":
                    adicionales = [
                        "Informe de Análisis de Brechas hacia ENS Alto",
                        "Procedimiento de Gestión de Proveedores Críticos",
                        "Política de Seguridad por Capas (Zero Trust)",
                        "Plan de Pruebas de Resiliencia Operativa Anual"
                    ]
                    for doc in adicionales:
                        if all(doc.lower() not in d.lower() for d in docs_ex):
                            documentos_faltantes.append(f"ENS Alto → {doc}")
                return documentos_faltantes

            if st.button("Analizar documentación ENS", key="analizar_docs_ens"):
                documentos_falt = calcular_documentos_faltantes(controles_faltantes, documentos_existentes, nivel_ens)
                if documentos_falt:
                    st.error("Documentos faltantes para alcanzar el nivel objetivo ENS:")
                    for doc in documentos_falt:
                        st.markdown(f"- {doc}")
                else:
                    st.success("Todos los documentos requeridos para el nivel actual están presentes.")

        # Exportar informe PDF (mantengo tu lógica)
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
    # TAB 2 — Panel de Continuidad de Negocio (tu código)
    # ------------------------------------------------------------------
    with tab2:
        st.subheader("Generador de Plan de Continuidad ISO 22301")

        tenant_name_input = st.text_input("Nombre de la organización", placeholder="Ej: Fraudfense")
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

        if st.button("Generar plan de continuidad con Ellit Cognitive Core"):
            st.success(f"Plan de continuidad generado para {tenant_name_input}")
            if "CPD" in contexto_libre and "misma" in contexto_libre:
                recomendacion = (
                    "Implementar una estrategia de redundancia geográfica en una región diferente, "
                    "preferiblemente a más de 200 km, para mitigar desastres regionales."
                )
            elif "nieve" in contexto_libre or "nevada" in contexto_libre:
                recomendacion = (
                    "Definir un protocolo de continuidad basado en teletrabajo temporal "
                    "y acuerdos con proveedores logísticos alternos."
                )
            elif "proveedor" in contexto_libre:
                recomendacion = (
                    "Establecer contratos con proveedores secundarios con cláusulas de continuidad."
                )
            elif "incendio" in contexto_libre:
                recomendacion = (
                    "Definir rutas de evacuación, activar CPD secundario y mantener documentación crítica cifrada en cloud."
                )
            else:
                recomendacion = (
                    "Analizar riesgos asociados al escenario descrito, priorizar procesos críticos y diseñar "
                    "estrategias específicas de recuperación con soporte del Comité de Crisis."
                )

            plan_text = f"""
PLAN DE CONTINUIDAD DE NEGOCIO — ISO 22301 / ENS / Ellit Cognitive Core

Organización: {tenant_name_input}
Procesos críticos: {procesos_criticos}
Infraestructura: {infraestructura}
Dependencias: {dependencias}
RTO: {rto} horas
RPO: {rpo} horas

ANÁLISIS COGNITIVO DEL CONTEXTO
{contexto_libre}

EVALUACIÓN Y RECOMENDACIÓN DEL COGNITIVE CORE
{recomendacion}

© 2025 Ellit Cognitive Core — Plan de continuidad inteligente
"""
            st.text_area("Vista previa del plan", plan_text, height=400)
            download_pdf_button(f"Plan_BCP_{tenant_name_input}", tenant_name_input, plan_text, f"Plan_BCP_{tenant_name_input}.pdf")

        st.markdown("---")
        st.subheader("Simulador de crisis BCP")

        escenario = st.text_input(
            "Describe el escenario de crisis a simular",
            placeholder="Ejemplo: Pérdida total de conectividad entre CPDs durante 12 horas"
        )
        ubicacion = st.text_input("Ubicación o entorno afectado", placeholder="Ej: CPD Madrid o sede principal")
        duracion = st.slider("Duración estimada de la interrupción (horas)", 1, 72, 8)
        impacto = st.select_slider("Nivel de impacto", ["Bajo", "Medio", "Alto"], value="Alto")

        if st.button("Simular escenario de crisis"):
            st.success("Simulación de crisis completada.")
            if "CPD" in escenario or "conectividad" in escenario:
                estrategia = "Activar replicación en región secundaria y habilitar conexión VPN temporal."
            elif "ransomware" in escenario:
                estrategia = "Aislar servidores afectados y restaurar desde copias inmutables."
            elif "inundación" in escenario or "incendio" in escenario:
                estrategia = "Trasladar operaciones al sitio alternativo y priorizar funciones críticas."
            elif "personal" in escenario or "empleados" in escenario:
                estrategia = "Activar protocolo de contingencia de recursos humanos y teletrabajo."
            else:
                estrategia = "Aplicar protocolo general de continuidad ajustado a dependencias críticas."

            plan_sim = f"""
SIMULACIÓN DE ESCENARIO BCP — ELLIT COGNITIVE CORE

Cliente: {tenant_name_input}
Escenario: {escenario}
Ubicación afectada: {ubicacion}
Duración estimada: {duracion} horas
Impacto: {impacto}

ESTRATEGIA DE RECUPERACIÓN RECOMENDADA
{estrategia}

© 2025 Ellit Cognitive Core — Simulador de continuidad
"""
            st.text_area("Resultado de la simulación", plan_sim, height=400)
            download_pdf_button(f"Simulacion_BCP_{tenant_name_input}", tenant_name_input, plan_sim, f"Simulacion_BCP_{tenant_name_input}.pdf")

    # ------------------------------------------------------------------
    # TAB 3 — Generador de Políticas (multinormativo)
    # ------------------------------------------------------------------
    with tab3:
        st.markdown("""
        <div style="background: linear-gradient(135deg,#FF0080 0%,#00B4FF 100%);
                    padding:18px;border-radius:16px;color:white;text-align:center;">
            <h2>Generador de políticas corporativas — Ellit Cognitive Core</h2>
            <p>Redacta políticas y procedimientos multinormativos listas para auditoría.</p>
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
                st.info("Generando documento corporativo...")

                policy_prompt = f"""
Eres Ellit Cognitive Core, un motor cognitivo experto en GRC, ciberseguridad y cumplimiento multinormativo.
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
  8. Recomendaciones del Cognitive Core

Incluye el nombre de la organización ({tenant_name}) y referencias explícitas al marco {normativa}.
Genera un documento con tono institucional, coherente con entornos corporativos de ciberseguridad.
"""

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "Eres un consultor experto en GRC y cumplimiento normativo multinormativo."},
                        {"role": "user", "content": policy_prompt}
                    ],
                    temperature=0.35,
                    max_tokens=2000
                )

                policy_text = response.choices[0].message.content.strip()

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

                st.success(f"Política corporativa de {tipo} generada bajo {normativa}.")

                with st.expander("Vista previa del documento"):
                    st.markdown(policy_text)

                with st.expander("Recomendaciones del Cognitive Core"):
                    st.info(f"Se recomienda validar esta política con los controles aplicables de {normativa} y mantener revisión anual por el Comité de Seguridad.")

                fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
                encabezado = f"""
POLÍTICA CORPORATIVA — {tipo.upper()}
Organización: {tenant_name}
Normativa base: {normativa}
Fecha: {fecha_actual}
Ellit Cognitive Core — Documento generado automáticamente
------------------------------------------------------------

"""
                documento_final = encabezado + policy_text
                download_pdf_button(f"Politica_{tipo}", tenant_name, documento_final, f"Politica_{tipo}.pdf")

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
    # TAB 4 — Ellit Predictive Intelligence
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

        col1_p, col2_p, col3_p = st.columns(3)
        with col1_p:
            sector_p = st.selectbox("Sector", [
                "Banca y Finanzas", "Salud", "Educación", "Energía",
                "Retail y E-commerce", "Tecnología", "Industria", "Defensa", "Sector Público"
            ])
        with col2_p:
            pais = st.text_input("País / Región", "España")
        with col3_p:
            madurez_p = st.slider("Madurez ENS/ISO", 1, 5, 3)

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
        costo_promedio = base_costos.get(sector_p, 350000)
        impacto = (costo_promedio * (riesgo_sector / 100)) * (1.2 - (madurez_p / 10))

        st.markdown('<div class="section-title">Indicadores clave de riesgo</div>', unsafe_allow_html=True)
        k1, k2, k3, k4 = st.columns(4)
        for col, (label, val) in zip(
            [k1, k2, k3, k4],
            [
                ("Riesgo sectorial", f"{riesgo_sector}%"),
                ("Vulnerabilidades activas", f"{cve_activas}"),
                ("Coste medio sectorial (€)", f"{costo_promedio:,.0f}"),
                ("Impacto potencial (€)", f"{impacto:,.0f}")
            ]
        ):
            with col:
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{val}</div>
                </div>
                """, unsafe_allow_html=True)

        c1_p2, c2_p2 = st.columns(2)
        with c1_p2:
            st.markdown('<div class="section-title">Distribución global de amenazas activas</div>', unsafe_allow_html=True)
            threat_data = pd.DataFrame({
                "country": ["España", "Estados Unidos", "Reino Unido", "Alemania", "Brasil", "India", "Japón"],
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

        with c2_p2:
            st.markdown('<div class="section-title">Benchmark comparativo ENS / ISO / NIST</div>', unsafe_allow_html=True)
            categories = ["ENS", "ISO 27001", "NIST CSF", "SOC 2", "PCI DSS"]
            org_values = [madurez_p * 15, madurez_p * 18, madurez_p * 14, madurez_p * 12, madurez_p * 10]
            leader_values = [95, 90, 88, 85, 82]
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=leader_values + [leader_values[0]], theta=categories + [categories[0]],
                fill='toself', name='Líder sectorial', line=dict(color="#00B4FF")
            ))
            fig_radar.add_trace(go.Scatterpolar(
                r=org_values + [org_values[0]], theta=categories + [categories[0]],
                fill='toself', name='Organización', line=dict(color="#FF0080")
            ))
            fig_radar.update_layout(
                polar=dict(bgcolor="rgba(0,0,0,0)", radialaxis=dict(visible=True, range=[0, 100])),
                showlegend=True, paper_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig_radar, use_container_width=True)

        c3_p3, c4_p3 = st.columns(2)
        with c3_p3:
            st.markdown('<div class="section-title">Simulador de ataque predictivo</div>', unsafe_allow_html=True)
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
                Vector seleccionado: {vector}  
                Probabilidad de ocurrencia: {probabilidad*100:.1f}%  
                Impacto económico estimado: €{impacto_ajustado:,.0f}  
                Nivel de madurez actual: {madurez_p}/5  

                Recomendaciones:
                - Fortalecer controles perimetrales y segmentación Zero Trust.
                - Refuerzo en continuidad digital (ISO 22301).
                - Mejora en detección y respuesta SOC/SIEM.
                - Revisión específica de cadena de suministro bajo ENS/NIST.
                """)

        with c4_p3:
            st.markdown('<div class="section-title">Alertas predictivas sectoriales</div>', unsafe_allow_html=True)
            alertas = [
                f"Aumento relevante de ataques ransomware en {sector_p}.",
                f"Nuevas vulnerabilidades críticas detectadas en {pais}.",
                "Incremento en explotación de vulnerabilidades VPN.",
                "Amenazas a proveedores clave en cadena de suministro europea.",
            ]
            for alerta in alertas:
                st.markdown(f"""
                <div style="background:#F8FAFC;padding:14px;border-radius:10px;
                            border:1px solid #E2E8F0;margin-bottom:8px;">
                    <span style="color:#0F172A;font-size:14px;">{alerta}</span>
                </div>
                """, unsafe_allow_html=True)

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
