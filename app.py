# ==============================
# AI Executive Shield — EllitNow Cognitive Core Edition
# VERSIÓN ORDENADA Y SIN DUPLICADOS
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
)

# --- Módulo BCP ---
from modules.bcp import (
    render_bcp_generator,
    render_bcp_analisis,
    render_bcp_simulador,
    render_bcp_alert_tree
)

# --- Predictive Intelligence ---
from modules.predictive import (
    render_predictive_standard,
    render_predictive_prime
)

# --- Políticas IA ---
from modules.policies import render_policies_generator

# --- Lenguaje UI ---
from language import translate, set_language

# --- SGSI Monitoring ---
from modules.sgsi_monitoring import (
    render_sgsi_monitor_dashboard,
    render_sgsi_monitor_history,
    render_sgsi_monitor_evidences
)

# --- Base de datos ---
from core.database import get_conn

# Desactivar componentes externos obsoletos
st.components.v1.declare_component = lambda *args, **kwargs: None

# Cliente OpenAI
st.session_state["client"] = EllitCognitiveCore(st.secrets["OPENAI_API_KEY"])


# ==============================
# CONFIGURACIÓN DE PÁGINA
# ==============================
st.set_page_config(
    page_title="AI Executive Shield — EllitNow Cognitive Core",
    page_icon="🧠",
    layout="wide",
)


# ==============================
# ESTILO UI GLOBAL — Manteniendo tu diseño
# ==============================
st.markdown("""
    <style>
    /* Centrar layout y evitar overflow */
    html, body, [data-testid="stAppViewContainer"] {
        overflow-x: hidden !important;
    }
    div.block-container {
        max-width: 1250px;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }

    /* Sidebar corporativo */
    section[data-testid="stSidebar"] {
        width: 220px !important;
        min-width: 220px !important;
        background: linear-gradient(180deg,#0B2A55 0%,#061A36 100%);
        border-right: 1px solid #4C5D7A;
        padding: 20px 10px;
        color: white !important;
    }

    /* Tipografía global */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body {
        font-family: 'Inter', sans-serif;
        color: #FFFFFF;
    }

    /* UI principal */
    .main-container {
        background: #0B2A55;
        border-radius: 20px;
        padding: 35px;
        margin-top: 20px;
        border: 1px solid #4C5D7A;
        box-shadow: 0 4px 20px rgba(0,0,0,0.25);
    }

    /* Botones */
    .stButton>button {
        background: linear-gradient(135deg,#D8278A 0%,#0B2A55 100%) !important;
        color: white !important;
        border-radius: 30px;
        font-weight: 600;
        padding: 12px 28px;
        border: none;
        transition: 0.2s;
    }
    .stButton>button:hover {
        filter: brightness(1.1);
        transform: translateY(-2px);
    }

    /* Inputs */
    .stTextInput input, .stTextArea textarea {
        background: #0F355F !important;
        color: white !important;
        border-radius: 10px !important;
        border: 1px solid #4C5D7A !important;
        padding: 10px !important;
    }

    /* Tablas */
    .stDataFrame, .stTable {
        background: #0F355F !important;
        color: white !important;
        border-radius: 10px;
        border: 1px solid #4C5D7A;
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

DEFAULT_SESSION_VALUES = {
    "auth_status": None,
    "user_role": None,
    "user_id": None,
    "tenant_id": None,
    "tenant_name": None,
    "user_email": None,
    "primary_color": "#FF0080",
}

for key, value in DEFAULT_SESSION_VALUES.items():
    st.session_state.setdefault(key, value)


# ==============================
# BASE DE DATOS (Tenant + Users)
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
            enterprise INTEGER DEFAULT 0,
            prime INTEGER DEFAULT 0,
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

    # SGSI tablas
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
    conn.close()


# Ejecutar inicialización DB
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


def load_tenant_license_flags(tenant_id: str):
    """Carga flags Enterprise / Prime al iniciar sesión."""
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

    st.session_state["tenant_enterprise"] = bool(row[0])
    st.session_state["tenant_prime"] = bool(row[1])


def create_tenant_with_admin(name: str, email: str, tenant_type: str, parent_tenant_id: str | None = None):
    """Crea un tenant + un usuario administrador asociado."""
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
    """Primer acceso para usuarios recién creados."""
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
        SELECT id, first_access_token
        FROM users
        WHERE email = ? AND is_active = 0
    """, (email,))
    row = c.fetchone()

    if not row:
        conn.close()
        return False

    user_id, stored_token = row
    if stored_token != token:
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

    tab_login, tab_first, tab_reset = st.tabs([
        "Acceso Ellit", "Primer acceso", "Recuperar contraseña"
    ])

    # --- ACCESO NORMAL ---
    with tab_login:
        col1, col2 = st.columns(2)

        # SUPER ADMIN
        with col1:
            st.subheader("Super Admin")
            super_key = st.text_input("SUPER_ADMIN_KEY", type="password")

            if st.button("Entrar como Super Admin"):
                admin_key = st.secrets.get("SUPER_ADMIN_KEY", "")
                if super_key == admin_key:
                    st.session_state.update({
                        "auth_status": "super_admin",
                        "user_role": "super_admin",
                        "user_id": "superadmin",
                        "tenant_id": None,
                        "tenant_name": "Ellit Super Admin",
                        "user_email": SUPERADMIN_EMAIL,
                        "primary_color": "#FF0080",
                    })
                    load_tenant_license_flags(None)
                    st.success("Acceso concedido.")
                    st.rerun()
                else:
                    st.error("Clave incorrecta.")

        # USUARIOS NORMALES
        with col2:
            st.subheader("Usuarios Ellit")

            with st.form("login_form"):
                email = st.text_input("Email")
                password = st.text_input("Contraseña", type="password")
                submitted = st.form_submit_button("Entrar")

            if submitted:
                if not email or not password:
                    st.error("Completa todos los campos.")
                else:
                    user = get_user_by_email(email)

                    if not user:
                        st.error("Usuario no encontrado.")
                    elif not user["is_active"]:
                        st.error("Usuario no activado. Usa Primer acceso.")
                    else:
                        if bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
                            status = map_role_to_auth_status(user["role"])

                            st.session_state.update({
                                "auth_status": status,
                                "user_role": user["role"],
                                "user_id": user["id"],
                                "tenant_id": user["tenant_id"],
                                "tenant_name": user["tenant_name"],
                                "user_email": user["email"],
                                "primary_color": user["primary_color"],
                            })

                            load_tenant_license_flags(user["tenant_id"])
                            st.success("Acceso correcto.")
                            st.rerun()
                        else:
                            st.error("Contraseña incorrecta.")

    # --- PRIMER ACCESO ---
    with tab_first:
        st.subheader("Primer acceso")
        with st.form("first_access"):
            email = st.text_input("Email corporativo")
            token = st.text_input("Token de primer acceso")
            pwd1 = st.text_input("Nueva contraseña", type="password")
            pwd2 = st.text_input("Repite la contraseña", type="password")
            ok = st.form_submit_button("Activar")

        if ok:
            if not email or not token or not pwd1 or not pwd2:
                st.error("Completa todos los campos.")
            elif pwd1 != pwd2:
                st.error("Las contraseñas no coinciden.")
            else:
                if activate_user_first_access(email, token, pwd1):
                    st.success("Cuenta activada. Ya puedes iniciar sesión.")
                else:
                    st.error("Error activando cuenta.")

    # --- RESET PASSWORD ---
    with tab_reset:
        st.subheader("Recuperar contraseña")
        st.info("Por ahora, solicita un nuevo token de acceso al administrador.")


# ==============================
# ROLES / IMPERSONACIÓN
# ==============================
def get_partner_clients(partner_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        SELECT id, name, email, active, created_at
        FROM tenants
        WHERE parent_tenant_id = ?
        ORDER BY created_at DESC
    """, (partner_id,))
    rows = c.fetchall()
    conn.close()
    return rows


def impersonate_tenant(target_id):
    if st.session_state.get("auth_status") != "super_admin":
        st.error("No autorizado.")
        return

    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        SELECT id, name, email, primary_color
        FROM tenants WHERE id = ?
    """, (target_id,))
    row = c.fetchone()
    conn.close()

    if not row:
        st.error("Tenant no encontrado.")
        return

    st.session_state["impersonated_tenant"] = {
        "id": row[0], "name": row[1], "email": row[2],
        "primary_color": row[3] or "#FF0080"
    }

    st.session_state.update({
        "auth_status": "impersonated",
        "tenant_id": row[0],
        "tenant_name": row[1],
        "primary_color": row[3] or "#FF0080",
    })

    st.rerun()


def stop_impersonation():
    if "impersonated_tenant" in st.session_state:
        del st.session_state["impersonated_tenant"]

    st.session_state["auth_status"] = "super_admin"
    st.sidebar.success("Impersonación finalizada.")
    st.rerun()


def render_role_controls():
    role = st.session_state.get("auth_status")

    st.sidebar.markdown("---")

    if role == "super_admin":
        st.sidebar.markdown("### Impersonar tenants")

        conn = get_conn()
        df = pd.read_sql_query("SELECT id, name FROM tenants ORDER BY name", conn)
        conn.close()

        if not df.empty:
            names = df["name"].tolist()
            ids = df["id"].tolist()

            selected = st.sidebar.selectbox(
                "Selecciona tenant",
                names,
                key="impersonation_select"
            )

            if st.sidebar.button("Ver como este tenant"):
                idx = names.index(selected)
                impersonate_tenant(ids[idx])

        # Crear nuevo tenant
        st.sidebar.markdown("---")
        st.sidebar.subheader("Crear tenant")

        with st.sidebar.form("new_tenant"):
            t_type = st.selectbox("Tipo", ["Partner", "Cliente directo"])
            name = st.text_input("Nombre")
            email = st.text_input("Email admin")
            submit = st.form_submit_button("Crear")

        if submit:
            if not name or not email:
                st.sidebar.error("Completa los campos.")
            else:
                t_type_key = "partner" if t_type == "Partner" else "client"
                tid, uid, token = create_tenant_with_admin(
                    name, email, t_type_key
                )
                st.sidebar.success(f"Tenant '{name}' creado.")
                st.sidebar.code(token)

    elif role == "impersonated":
        t = st.session_state.get("impersonated_tenant", {})
        st.sidebar.markdown("### Impersonando")
        st.sidebar.write(f"Tenant: **{t.get('name','')}**")

        if st.sidebar.button("Salir de impersonación"):
            stop_impersonation()

    elif role == "partner":
        st.sidebar.markdown("### Tus clientes")
        clients = get_partner_clients(st.session_state["tenant_id"])

        if clients:
            for cid, name, email, active, created in clients:
                st.sidebar.write(f"{name} — {'Activo' if active else 'Inactivo'}")
        else:
            st.sidebar.info("Sin clientes asignados.")

        st.sidebar.markdown("---")
        st.sidebar.subheader("Crear cliente")

        with st.sidebar.form("new_client"):
            name = st.text_input("Nombre del cliente")
            email = st.text_input("Email admin")
            submit = st.form_submit_button("Crear")

        if submit:
            tid, uid, token = create_tenant_with_admin(
                name, email, "client",
                parent_tenant_id=st.session_state["tenant_id"]
            )
            st.sidebar.success(f"Cliente '{name}' creado.")
            st.sidebar.code(token)

    elif role == "demo":
        st.sidebar.markdown("### Modo demo")
        if st.sidebar.button("Cerrar sesión demo"):
            for k in [
                "auth_status", "user_role", "user_id",
                "tenant_id", "tenant_name", "user_email"
            ]:
                st.session_state[k] = None
            st.rerun()


# ==============================
# PANEL PRINCIPAL
# ==============================
def render_panel():
    role = st.session_state.get("auth_status", "demo")
    tenant = st.session_state.get("tenant_name", "AI Executive Shield")
    color = st.session_state.get("primary_color", "#FF0080")

    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg,{color} 0%,#00B4FF 100%);
            padding:25px; border-radius:15px; text-align:center; color:white;">
            <h1>{tenant}</h1>
            <p>{role.title()} • Ellit Cognitive Core 2025</p>
        </div>
    """, unsafe_allow_html=True)

    if "menu" in st.session_state and "submenu" in st.session_state:
        st.session_state["breadcrumb"] = (
            f"{st.session_state.menu} → {st.session_state.submenu}"
        )

    if "breadcrumb" in st.session_state:
        st.markdown(
            f"""
                <div style="margin-top:10px; font-size:13px; color:#E2E8F0;">
                    {st.session_state['breadcrumb']}
                </div>
            """,
            unsafe_allow_html=True
        )
# ==============================
# VALIDACIÓN DE LICENCIAS
# ==============================
def require_enterprise():
    """Restringe módulos que requieren Enterprise."""
    role = st.session_state.get("auth_status")

    if role in ["super_admin", "impersonated"]:
        return

    if not st.session_state.get("tenant_enterprise", False):
        st.error("🚫 Este módulo requiere una licencia **Enterprise** activa.")
        st.stop()


def require_prime():
    """Restringe módulo Predictive Intelligence Prime."""
    role = st.session_state.get("auth_status")

    if role in ["super_admin", "impersonated"]:
        return

    if not st.session_state.get("tenant_prime", False):
        st.warning("🔒 Este módulo requiere la suscripción **Prime**.")
        st.stop()


# ===============================================================
# RENDER DEL CONTENIDO SEGÚN MENÚ Y SUBMENÚ
# ===============================================================

menu = st.session_state.get("menu")
submenu = st.session_state.get("submenu")

# Si no hay menú = usuario no ha iniciado sesión
if not menu:
    st.stop()

content_area = st.container()

# Breadcrumb dinámico
if menu and submenu:
    st.session_state["breadcrumb"] = f"{menu} → {submenu}"


# ===============================================================
# ➤  RADAR IA (Enterprise)
# ===============================================================
if menu == translate("Radar IA", "AI Radar"):

    require_enterprise()

    if submenu == translate("Cuadro de mando (KPIs)", "Dashboard KPIs"):
        with content_area: render_radar_kpis()

    elif submenu == translate("Perfil de la organización", "Organization Profile"):
        with content_area: render_radar_profile()

    elif submenu == translate("Radar Cognitivo", "Cognitive Radar"):
        with content_area: render_radar_cognitivo()

    elif submenu == translate("Madurez SGSI", "ISMS Maturity"):
        with content_area: render_radar_madurez()

    elif submenu == translate("Informe PDF", "PDF Report"):
        with content_area: render_radar_pdf()


# ===============================================================
# ➤  SGSI MONITORING (Enterprise)
# ===============================================================
elif menu == translate("Monitorización SGSI", "ISMS Monitoring"):

    require_enterprise()

    if submenu == translate("Panel general", "General Dashboard"):
        with content_area: render_sgsi_monitor_dashboard()

    elif submenu == translate("Registro histórico", "History Log"):
        with content_area: render_sgsi_monitor_history()

    elif submenu == translate("Evidencias y mantenimiento", "Evidence & Maintenance"):
        with content_area: render_sgsi_monitor_evidences()


# ===============================================================
# ➤  BCP — Continuidad de Negocio (Enterprise)
# ===============================================================
elif menu == translate("Continuidad de Negocio (BCP)", "Business Continuity"):

    require_enterprise()

    if submenu == translate("Generador BCP", "BCP Generator"):
        with content_area: render_bcp_generator()

    elif submenu == translate("Análisis cognitivo", "Cognitive Analysis"):
        with content_area: render_bcp_analisis()

    elif submenu == translate("Simulador de crisis", "Crisis Simulator"):
        with content_area: render_bcp_simulador()

    elif submenu == translate("ELLIT ALERT TREE – Crisis Communication Demo",
                              "ELLIT ALERT TREE – Crisis Communication Demo"):
        with content_area: render_bcp_alert_tree()


# ===============================================================
# ➤  POLÍTICAS IA (Enterprise)
# ===============================================================
elif menu == translate("Políticas IA", "AI Policies"):

    require_enterprise()

    if submenu == translate("Generador multinormativo", "Multistandard Policy Generator"):
        with content_area: render_policies_generator()


# ===============================================================
# ➤  PREDICTIVE INTELLIGENCE (Enterprise / Prime)
# ===============================================================
elif menu == translate("Predictive Intelligence", "Predictive Intelligence"):

    if submenu == translate("Predicción estándar", "Standard Prediction"):
        require_enterprise()
        with content_area: render_predictive_standard()

    elif submenu == translate("Predicción Prime", "Prime Prediction"):
        require_prime()
        with content_area: render_predictive_prime()


# ===============================================================
# ➤  LICENCIAS (solo super_admin, partner o client_admin)
# ===============================================================
elif menu == translate("Licencias", "Licenses"):

    if st.session_state.get("user_role") not in ["super_admin", "partner", "client_admin"]:
        st.warning("⚠️ No tienes permisos para gestionar licencias.")
        st.stop()

    if submenu == translate("Gestión de licencias", "License Management"):
        with content_area: render_licencias_tab()


# ===============================================================
# STRIPE — CHECKOUT UI
# ===============================================================
def render_stripe_checkout():

    stripe_key = st.secrets.get("STRIPE_SECRET_KEY")
    app_url = st.secrets.get("APP_URL", "https://ellitnow.com")

    if not stripe_key:
        st.error("⚠️ Stripe no está configurado correctamente.")
        return

    if "STRIPE_PRICE_ENTERPRISE_ID" not in st.secrets or \
       "STRIPE_PRICE_PREDICTIVE_ID" not in st.secrets:
        st.error("⚠️ Faltan Price IDs en secrets.")
        return

    stripe.api_key = stripe_key

    st.markdown("""
        <div style="background:linear-gradient(135deg,#FF0080,#0048FF);
        padding:24px;border-radius:16px;color:white;text-align:center;
        margin-bottom:30px;">
            <h2 style="font-weight:700;margin-bottom:4px;">
                Activación de licencias EllitNow Shield
            </h2>
            <p>Selecciona un plan para tu organización</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # ENTERPRISE
    with col1:
        st.markdown("""
            <div class="license-card">
                <div class="license-title">Enterprise Edition</div>
                <div class="license-desc">Licencia anual completa</div>
                <div class="license-price">4.900 €/año</div>
                <div class="license-features">Radar IA • BCP • Políticas ejecutivas</div>
            </div>
        """, unsafe_allow_html=True)

        if st.button("Activar Enterprise Edition"):
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
                st.success("Redirigiendo a Stripe...")
                st.markdown(f"[Completar pago]({session.url})")
            except Exception as e:
                st.error(f"Stripe error: {e}")

    # PRIME
    with col2:
        st.markdown("""
            <div class="license-card">
                <div class="license-title">Prime - Predictive Intelligence</div>
                <div class="license-desc">Suscripción mensual</div>
                <div class="license-price">699 €/mes</div>
                <div class="license-features">IA avanzada • Alertas globales</div>
            </div>
        """, unsafe_allow_html=True)

        if st.button("Añadir Prime"):
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
                st.success("Redirigiendo a Stripe...")
                st.markdown(f"[Completar pago]({session.url})")
            except Exception as e:
                st.error(f"Stripe error: {e}")

    st.caption("Pagos seguros con Stripe • © EllitNow 2025")


# ===============================================================
# GESTOR DE LICENCIAS (TAB COMPLETO)
# ===============================================================
def render_licencias_tab():
    st.subheader("Licencias y suscripciones — Gestión")
    st.write("Administra tenants y activa licencias reales con Stripe.")

    conn = get_conn()
    df = pd.read_sql_query("""
        SELECT name AS Tenant, email AS Email,
               CASE WHEN active = 1 THEN 'Activo' ELSE 'Inactivo' END AS Estado,
               datetime(created_at) AS 'Creado'
        FROM tenants ORDER BY created_at DESC
    """, conn)
    conn.close()

    if df.empty:
        st.info("No hay tenants registrados.")
    else:
        st.dataframe(df, use_container_width=True)

    st.markdown("### Activación de licencias")
    render_stripe_checkout()


# ===============================================================
# EJECUCIÓN PRINCIPAL COMPLETA
# ===============================================================

if st.session_state.get("auth_status"):

    # SIDEBAR
    with st.sidebar:

        set_language()

        st.markdown("""
            <style>
            .ellit-menu-btn {
                padding:10px 14px;margin-bottom:6px;
                border-radius:10px;background:#0F355F;
                border:1px solid #1A4472;color:#E2E8F0;
                cursor:pointer;text-align:left;
            }
            .ellit-menu-btn-active {
                background:#D8278A;border-color:#FF0080;
                color:white;font-weight:700;
            }
            </style>
        """, unsafe_allow_html=True)

        st.markdown("""
            <div style="padding:12px 4px;margin-bottom:10px;">
                <h3 style="margin:0;color:white;">Ellit Cognitive Core</h3>
                <p style="margin:0;color:#E2E8F0;font-size:13px;">AI Executive Shield</p>
            </div>
        """, unsafe_allow_html=True)

        main_options = [
            translate("Radar IA", "AI Radar"),
            translate("Monitorización SGSI", "ISMS Monitoring"),
            translate("Continuidad de Negocio (BCP)", "Business Continuity"),
            translate("Políticas IA", "AI Policies"),
            translate("Predictive Intelligence", "Predictive Intelligence"),
            translate("Licencias", "Licenses")
        ]

        submenu_map = {
            translate("Radar IA", "AI Radar"): [
                translate("Cuadro de mando (KPIs)", "Dashboard KPIs"),
                translate("Perfil de la organización", "Organization Profile"),
                translate("Radar Cognitivo", "Cognitive Radar"),
                translate("Madurez SGSI", "ISMS Maturity"),
                translate("Informe PDF", "PDF Report")
            ],
            translate("Monitorización SGSI", "ISMS Monitoring"): [
                translate("Panel general", "General Dashboard"),
                translate("Registro histórico", "History Log"),
                translate("Evidencias y mantenimiento", "Evidence & Maintenance")
            ],
            translate("Continuidad de Negocio (BCP)", "Business Continuity"): [
                translate("Generador BCP", "BCP Generator"),
                translate("Análisis cognitivo", "Cognitive Analysis"),
                translate("Simulador de crisis", "Crisis Simulator"),
                translate("ELLIT ALERT TREE – Crisis Communication Demo",
                          "ELLIT ALERT TREE – Crisis Communication Demo")
            ],
            translate("Políticas IA", "AI Policies"): [
                translate("Generador multinormativo", "Multistandard Policy Generator")
            ],
            translate("Predictive Intelligence", "Predictive Intelligence"): [
                translate("Predicción estándar", "Standard Prediction"),
                translate("Predicción Prime", "Prime Prediction")
            ],
            translate("Licencias", "Licenses"): [
                translate("Gestión de licencias", "License Management")
            ]
        }

        # ESTADO INICIAL
        if "menu" not in st.session_state:
            st.session_state.menu = main_options[0]
        if "submenu" not in st.session_state:
            st.session_state.submenu = submenu_map[st.session_state.menu][0]

        # MENÚ PRINCIPAL
        for opt in main_options:
            active = (opt == st.session_state.menu)
            css = "ellit-menu-btn-active" if active else "ellit-menu-btn"

            if st.button(opt, key=f"main_{opt}"):
                st.session_state.menu = opt
                st.session_state.submenu = submenu_map[opt][0]
                st.rerun()

            st.markdown(f"<div class='{css}'>{opt}</div>", unsafe_allow_html=True)

        # SUBMENÚ
        for sub in submenu_map[st.session_state.menu]:
            sub_active = "ellit-submenu-active" if sub == st.session_state.submenu else ""
            if st.button(sub, key=f"sub_{sub}"):
                st.session_state.submenu = sub
                st.rerun()
            st.markdown(f"<a class='{sub_active}'>{sub}</a>", unsafe_allow_html=True)

        # CONTROLES DE ROL
        render_role_controls()

    # PANEL SUPERIOR
    render_panel()

else:
    login_screen()
