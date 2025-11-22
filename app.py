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
import json
import os
from math import pi
from datetime import datetime
from io import BytesIO

# --- Visualización ---
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# --- Auxiliares ---
import stripe
import traceback

# --- PDF (corporativo) ---
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color
from reportlab.lib.utils import ImageReader
import datetime as _dt

# --- Ellit Cognitive Core ---
from core.cognitive_core import EllitCognitiveCore, extract_json


# --- Módulo Radar IA ---
from modules.radar_ia import (
    render_radar_kpis,
    render_radar_profile,
    render_radar_cognitivo,
    render_radar_madurez,
    render_radar_pdf,
 #    render_radar_normativa_inteligente
)


# --- Módulo BCP ---
from modules.bcp import (
    render_bcp_generator,
    render_bcp_analisis,
    render_bcp_simulador,
    render_bcp_alert_tree
)
from modules.predictive import (
    render_predictive_standard,
    render_predictive_prime
)
from modules.policies import render_policies_generator
# lenguaje UI
from language import translate, set_language

# SGSI Monitoring (faltaban!)
from modules.sgsi_monitoring import (
    render_sgsi_monitor_dashboard,
    render_sgsi_monitor_history,
    render_sgsi_monitor_evidences
)
from core.database import get_conn

# Desactivar carga de componentes externos antiguos
st.components.v1.declare_component = lambda *args, **kwargs: None

# Inicializar cliente de OpenAI (asegúrate que exista en secrets.toml)
st.session_state["client"] = EllitCognitiveCore(st.secrets["OPENAI_API_KEY"])

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
# ESTILO GLOBAL ELLIT SHIELD UI PRO — COLORES CORREGIDOS
# ==============================
st.markdown("""
    <style>
    /* Fuente global */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
        background-color: #FFFFFF;
        color: #FFFFFF;
    }

    /* Sidebar corporativo fijo */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg,#0B2A55 0%,#061A36 100%);
        color: white;
        padding-top: 25px;
        border-right: 1px solid #4C5D7A;
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
        background: #0B2A55;
        border-radius: 20px;
        padding: 35px;
        margin-top: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.25);
        border: 1px solid #4C5D7A;
        color: #FFFFFF;
    }

    /* Cards de métricas */
    .metric-card {
        background-color: #0F355F;
        border-radius: 14px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.25);
        border: 1px solid #4C5D7A;
        padding: 20px;
        margin-bottom: 16px;
        text-align: center;
        transition: all 0.2s ease;
        color: #FFFFFF;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.35);
    }
    .metric-value {
        font-size: 26px;
        font-weight: 700;
        color: #D8278A;
    }
    .metric-label {
        font-size: 13px;
        color: #E2E8F0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Títulos */
    h1, h2, h3, h4 {
        font-weight: 700 !important;
        color: #FFFFFF !important;
        margin-bottom: 10px;
    }
    .section-title {
        font-weight: 600;
        font-size: 18px;
        color: #FFFFFF;
        margin-bottom: 12px;
    }

    /* Botones */
    .stButton>button {
        background: linear-gradient(135deg,#D8278A 0%,#0B2A55 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 30px;
        font-weight: 600;
        transition: 0.2s ease;
        padding: 12px 28px;
        font-size: 16px;
    }
    .stButton>button:hover {
        filter: brightness(1.1);
        transform: translateY(-2px);
    }

    /* Inputs y selects */
    .stTextInput>div>div>input, .stTextArea textarea {
        border-radius: 10px !important;
        border: 1px solid #4C5D7A !important;
        background-color: #0F355F !important;
        color: #FFFFFF !important;
        padding: 10px 12px !important;
    }
    .stSelectbox>div>div {
        background-color: #0F355F !important;
        border-radius: 10px !important;
        border: 1px solid #4C5D7A !important;
        color: #FFFFFF !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        justify-content: center;
    }
    .stTabs [data-baseweb="tab"] {
        background: #0F355F;
        border-radius: 10px;
        color: #E2E8F0;
        font-weight: 500;
        padding: 10px 18px;
        transition: 0.2s;
        border: 1px solid #4C5D7A;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg,#D8278A 0%,#0B2A55 100%);
        color: white !important;
        font-weight: 600;
    }

    /* Tablas */
    .stDataFrame, .stTable {
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.25);
        border: 1px solid #4C5D7A;
        overflow: hidden;
        color: #FFFFFF;
    }

    /* Dashboard cards */
    .dashboard-card {
        background: #0F355F;
        border-radius: 18px;
        padding: 25px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.25);
        margin-bottom: 25px;
        border: 1px solid #4C5D7A;
        color: #FFFFFF;
    }
    .dashboard-title {
        font-size: 24px;
        font-weight: 600;
        color: #FFFFFF;
    }
    .dashboard-sub {
        font-size: 14px;
        color: #E2E8F0;
        margin-top: -8px;
    }

    hr {
        border: none;
        border-top: 1px solid #4C5D7A;
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

    # ==========================================
    # TENANTS
    # ==========================================
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
    # ==========================================
    # MIGRACIÓN — NUEVOS CAMPOS DE LICENCIA
    # ==========================================
    # enterprise → 1 si el tenant ha adquirido el plan Enterprise anual
    # prime → 1 si el tenant ha adquirido el add-on Predictive Intelligence

    try:
        c.execute("ALTER TABLE tenants ADD COLUMN enterprise INTEGER DEFAULT 0")
    except:
        pass

    try:
        c.execute("ALTER TABLE tenants ADD COLUMN prime INTEGER DEFAULT 0")
    except:
        pass

    # ==========================================
    # USERS
    # ==========================================
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

    # ==========================================
    # SGSI — HISTÓRICO DE KPIS
    # ==========================================
    c.execute("""
        CREATE TABLE IF NOT EXISTS sgsi_kpi_history (
            id TEXT PRIMARY KEY,
            tenant_id TEXT NOT NULL,
            user_id TEXT,
            fecha TEXT NOT NULL,
            kpi TEXT NOT NULL,
            valor REAL NOT NULL,
            metadata TEXT,
            FOREIGN KEY (tenant_id) REFERENCES tenants(id)
        )
    """)

    # ==========================================
    # SGSI — EVIDENCIAS (ARCHIVOS)
    # ==========================================
    c.execute("""
        CREATE TABLE IF NOT EXISTS sgsi_evidences (
            id TEXT PRIMARY KEY,
            tenant_id TEXT NOT NULL,
            user_id TEXT,
            fecha TEXT NOT NULL,
            nombre_archivo TEXT NOT NULL,
            tipo_archivo TEXT NOT NULL,
            contenido BLOB,
            descripcion TEXT,
            FOREIGN KEY (tenant_id) REFERENCES tenants(id)
        )
    """)

    # ==========================================
    # SGSI — MANTENIMIENTOS
    # ==========================================
    c.execute("""
        CREATE TABLE IF NOT EXISTS sgsi_maintenance (
            id TEXT PRIMARY KEY,
            tenant_id TEXT NOT NULL,
            user_id TEXT,
            fecha TEXT NOT NULL,
            actividad TEXT NOT NULL,
            responsable TEXT,
            impacto TEXT,
            FOREIGN KEY (tenant_id) REFERENCES tenants(id)
        )
    """)

    conn.commit()

    # ==========================================
    # SUPER ADMIN (tenant interno)
    # ==========================================
    c.execute("SELECT id FROM tenants WHERE email = ?", (SUPERADMIN_EMAIL,))
    row = c.fetchone()
    if not row:
        super_tenant_id = str(uuid.uuid4())
        c.execute("""
            INSERT INTO tenants (id, name, email, active, predictive, primary_color)
            VALUES (?, ?, ?, 1, 1, '#FF0080')
        """, (super_tenant_id, SUPERADMIN_NAME, SUPERADMIN_EMAIL))

    # ==========================================
    # TENANT Y USUARIO DEMO
    # ==========================================
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


# ==========================================
# Cargar licencias del tenant en session_state
# ==========================================
def load_tenant_license_flags(tenant_id: str):
    """
    Carga en session_state los flags de licencia Enterprise / Prime
    del tenant autenticado.
    """
    if not tenant_id:
        st.session_state["tenant_enterprise"] = False
        st.session_state["tenant_prime"] = False
        return

    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        SELECT enterprise, prime
        FROM tenants
        WHERE id = ?
        LIMIT 1
    """, (tenant_id,))
    row = c.fetchone()
    conn.close()

    if not row:
        st.session_state["tenant_enterprise"] = False
        st.session_state["tenant_prime"] = False
        return

    enterprise, prime = row

    # Guardar automáticamente en session_state
    st.session_state["tenant_enterprise"] = bool(enterprise)
    st.session_state["tenant_prime"] = bool(prime)


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

    # =========================================================
    # ACCESO NORMAL
    # =========================================================
    with tab_login:
        col1, col2 = st.columns(2)

        # ----------------------------
        # SUPER ADMIN por SUPER_ADMIN_KEY
        # ----------------------------
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

                    # 🔥 Cargar flags Enterprise / Prime (aunque no tenga tenant)
                    load_tenant_license_flags(st.session_state["tenant_id"])

                    st.success("Acceso concedido como Super Admin.")
                    st.rerun()
                else:
                    st.error("Clave de Super Admin incorrecta.")

        # ----------------------------
        # USUARIOS NORMALES
        # ----------------------------
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

                                # 🔥 Cargar flags Enterprise / Prime
                                load_tenant_license_flags(user["tenant_id"])

                                st.success("Acceso correcto.")
                                st.rerun()
                            else:
                                st.error("Contraseña incorrecta.")
                        except Exception:
                            st.error("Error verificando contraseña.")

    # =========================================================
    # PRIMER ACCESO
    # =========================================================
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

    # =========================================================
    # RESET PASSWORD
    # =========================================================
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
# PANEL PRINCIPAL (NAVEGACIÓN LATERAL PRO)
# ==============================
def render_panel():
    role = st.session_state.get("auth_status", "demo")
    tenant_name = st.session_state.get("tenant_name", "AI Executive Shield")
    primary_color = st.session_state.get("primary_color", "#FF0080")

    # ---------------------------------------
    # HEADER
    # ---------------------------------------
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, {primary_color} 0%, #00B4FF 100%);
            color:white; padding:25px; text-align:center; border-radius:15px;">
            <h1>{tenant_name}</h1>
            <p>{role.title()} • Ellit Cognitive Core 2025</p>
        </div>
    """, unsafe_allow_html=True)
    
    # ---------- Breadcrumb ----------
    if "breadcrumb" in st.session_state:
        st.markdown(f"""
            <div style="margin-top:10px; margin-bottom:20px;
                        font-size:13px; color:#E2E8F0;">
                {st.session_state['breadcrumb']}
            </div>
        """, unsafe_allow_html=True)


# ===============================================================
# SIDEBAR CORPORATIVO — MENÚ + SUBMENÚ
# ===============================================================
with st.sidebar:

    set_language()

    st.markdown(
        """
        <div style='padding:15px; margin-bottom:10px;
            background:linear-gradient(180deg, #0048FF 0%, #001F7F 100%);
            border-radius:12px; color:white;'>
            <h3 style='margin:0; color:white;'>Ellit Cognitive Core</h3>
            <p style='margin:0; opacity:0.8; font-size:13px;'>AI Executive Shield</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    menu = st.radio(
        translate("Navegación", "Navigation"),
        [
            translate("Radar IA", "AI Radar"),
            translate("Monitorización SGSI", "ISMS Monitoring"),
            translate("Continuidad de Negocio (BCP)", "Business Continuity"),
            translate("Políticas IA", "AI Policies"),
            translate("Predictive Intelligence", "Predictive Intelligence"),
            translate("Licencias", "Licenses")
        ],
        label_visibility="collapsed"
    )

    submenu = None

    if menu == translate("Radar IA", "AI Radar"):
        submenu = st.radio(
            translate("Opciones", "Options"),
            [
                translate("Cuadro de mando (KPIs)", "Dashboard KPIs"),
                translate("Perfil de la organización", "Organization Profile"),
                translate("Radar Cognitivo", "Cognitive Radar"),
                translate("Madurez SGSI", "ISMS Maturity"),
                translate("Informe PDF", "PDF Report")
            ],
            label_visibility="collapsed"
        )

    elif menu == translate("Monitorización SGSI", "ISMS Monitoring"):
        submenu = st.radio(
            translate("Opciones", "Options"),
            [
                translate("Panel general", "General Dashboard"),
                translate("Registro histórico", "History Log"),
                translate("Evidencias y mantenimiento", "Evidence & Maintenance")
            ],
            label_visibility="collapsed"
        )

    elif menu == translate("Continuidad de Negocio (BCP)", "Business Continuity"):
        submenu = st.radio(
            translate("Opciones", "Options"),
            [
                translate("Generador BCP", "BCP Generator"),
                translate("Análisis cognitivo", "Cognitive Analysis"),
                translate("Simulador de crisis", "Crisis Simulator"),
                translate("ELLIT ALERT TREE – Crisis Communication Demo", "ELLIT ALERT TREE – Crisis Communication Demo")
            ],
            label_visibility="collapsed"
        )

    elif menu == translate("Políticas IA", "AI Policies"):
        submenu = st.radio(
            translate("Opciones", "Options"),
            [
                translate("Generador multinormativo", "Multistandard Policy Generator")
            ],
            label_visibility="collapsed"
        )

    elif menu == translate("Predictive Intelligence", "Predictive Intelligence"):
        submenu = st.radio(
            translate("Opciones", "Options"),
            [
                translate("Predicción estándar", "Standard Prediction"),
                translate("Predicción Prime", "Prime Prediction")
            ],
            label_visibility="collapsed"
        )

    elif menu == translate("Licencias", "Licenses"):
        submenu = st.radio(
            translate("Opciones", "Options"),
            [
                translate("Gestión de licencias", "License Management")
            ],
            label_visibility="collapsed"
        )


# ==============================================================
# VALIDACIÓN DE LICENCIAS — ENTERPRISE & PRIME
# ==============================================================

def require_enterprise():
    """
    Bloquea acceso si el tenant NO tiene Enterprise.
    Super Admin e impersonated SIEMPRE tienen acceso.
    """
    role = st.session_state.get("auth_status")

    # super_admin e impersonated siempre pueden usarlo
    if role in ["super_admin", "impersonated"]:
        return

    if not st.session_state.get("tenant_enterprise", False):
        st.error("🚫 Este módulo requiere una licencia **Enterprise** activa.")
        st.stop()


def require_prime():
    """
    Bloquea acceso si el tenant NO tiene PRIME add-on.
    Super Admin e impersonated SIEMPRE tienen acceso.
    """
    role = st.session_state.get("auth_status")

    if role in ["super_admin", "impersonated"]:
        return

    if not st.session_state.get("tenant_prime", False):
        st.warning("🔒 Este módulo requiere la suscripción **Prime - Predictive Intelligence**.")
        st.stop()

# ===============================================================
# RENDER DEL CONTENIDO
# ===============================================================
content_area = st.container()
# ---------------------------------------------------------------
# BREADCRUMB DINÁMICO
# ---------------------------------------------------------------
if menu and submenu:
    st.session_state["breadcrumb"] = f"{menu} → {submenu}"

# ---------------------------
# RADAR IA (requiere Enterprise)
# ---------------------------
if menu == translate("Radar IA", "AI Radar"):

    require_enterprise()  # 🔒 IMPORTANTE

    if submenu == translate("Cuadro de mando (KPIs)", "Dashboard KPIs"):
        with content_area: 
            render_radar_kpis()

    elif submenu == translate("Perfil de la organización", "Organization Profile"):
        with content_area: 
            render_radar_profile()

    elif submenu == translate("Radar Cognitivo", "Cognitive Radar"):
        with content_area: 
            render_radar_cognitivo()

    elif submenu == translate("Madurez SGSI", "ISMS Maturity"):
        with content_area: 
            render_radar_madurez()

    elif submenu == translate("Informe PDF", "PDF Report"):
        with content_area: 
            render_radar_pdf()


# ---------------------------
# SGSI Monitoring (Enterprise)
# ---------------------------
elif menu == translate("Monitorización SGSI", "ISMS Monitoring"):

    require_enterprise()  # 🔒 IMPORTANTE

    if submenu == translate("Panel general", "General Dashboard"):
        with content_area: 
            render_sgsi_monitor_dashboard()

    elif submenu == translate("Registro histórico", "History Log"):
        with content_area: 
            render_sgsi_monitor_history()

    elif submenu == translate("Evidencias y mantenimiento", "Evidence & Maintenance"):
        with content_area: 
            render_sgsi_monitor_evidences()


# ---------------------------
# BCP (Enterprise)
# ---------------------------
elif menu == translate("Continuidad de Negocio (BCP)", "Business Continuity"):

    require_enterprise()  # 🔒 IMPORTANTE

    if submenu == translate("Generador BCP", "BCP Generator"):
        with content_area: render_bcp_generator()

    elif submenu == translate("Análisis cognitivo", "Cognitive Analysis"):
        with content_area: render_bcp_analisis()

    elif submenu == translate("Simulador de crisis", "Crisis Simulator"):
        with content_area: render_bcp_simulador()

    elif submenu == translate("ELLIT ALERT TREE – Crisis Communication Demo", "ELLIT ALERT TREE – Crisis Communication Demo"):
        with content_area: render_bcp_alert_tree()

# ---------------------------
# POLÍTICAS IA (Enterprise)
# ---------------------------
elif menu == translate("Políticas IA", "AI Policies"):

    require_enterprise()  # 🔒 IMPORTANTE

    if submenu == translate("Generador multinormativo", "Multistandard Policy Generator"):
        with content_area: render_policies_generator()

# ---------------------------
# PREDICTIVE INTELLIGENCE
# ---------------------------
elif menu == translate("Predictive Intelligence", "Predictive Intelligence"):

    if submenu == translate("Predicción estándar", "Standard Prediction"):
        require_enterprise()  # standard prediction requiere enterprise
        with content_area: render_predictive_standard()

    elif submenu == translate("Predicción Prime", "Prime Prediction"):
        require_prime()  # 🔮 Prime add-on
        with content_area: render_predictive_prime()

# ---------------------------
# LICENCIAS
# ---------------------------
elif menu == translate("Licencias", "Licenses"):

    # Solo super_admin, partner o client_admin
    if st.session_state.get("user_role") not in ["super_admin", "partner", "client_admin"]:
        st.warning("⚠️ No tienes permisos para gestionar licencias.")
        st.stop()

    if submenu == translate("Gestión de licencias", "License Management"):
        with content_area: render_licencias_tab()


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

    render_panel()   # SE RENDERIZA PRIMERO EL PANEL

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

    # Controles de rol
    if st.session_state.auth_status in ["super_admin", "impersonated", "partner"]:
        render_role_controls()

else:
    login_screen()

