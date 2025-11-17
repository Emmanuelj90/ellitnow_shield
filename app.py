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
