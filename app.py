# ==============================
# AI Executive Shield — EllitNow Cognitive Core Edition
# PARTE 1 / 3 — CORE & AUTH (PRODUCCIÓN)
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
from core.cognitive_core import EllitCognitiveCore

# --- Módulos externos (NO SE TOCAN) ---
from modules.radar_ia import (
    render_radar_kpis,
    render_radar_profile,
    render_radar_cognitivo,
    render_radar_madurez,
    render_radar_pdf,
)

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
from modules.sgsi_monitoring import (
    render_sgsi_monitor_dashboard,
    render_sgsi_monitor_history,
    render_sgsi_monitor_evidences
)

# --- Lenguaje UI ---
from language import translate, set_language

# --- DB helper ---
from core.database import get_conn
from modules.licencias import render_licencias_tab

# Desactivar componentes legacy (seguro en prod)
st.components.v1.declare_component = lambda *args, **kwargs: None


# ============================================================
# PAGE CONFIG (BRANDING)
# ============================================================

st.set_page_config(
    page_title="Ellit Shield · AI Executive Platform",
    page_icon="https://i.ibb.co/h19Y9KKG/logo-white-background.jpg",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# GLOBAL STYLE BASE (NO SIDEBAR)
# ============================================================

st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #ffffff;
    color: #0F172A;
}
div.block-container {
    max-width: 1320px;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# CONSTANTES / IDS
# ============================================================

SUPERADMIN_EMAIL = "admin@ellitnow.com"
SUPERADMIN_NAME = "Ellit Super Admin"

DEMO_EMAIL = "demo@ellitnow.com"
DEMO_PASSWORD = "Demo2025!g*E"
DEMO_TENANT_NAME = "DEMO — Ellit Shield"

MENU_IDS = ["radar", "sgsi", "bcp", "policies", "predictive", "licenses"]


# ============================================================
# SESSION BOOTSTRAP (A PRUEBA DE STREAMLIT)
# ============================================================

DEFAULT_SESSION = {
    "auth_status": None,      # super_admin / partner / client / demo
    "user_role": None,
    "user_id": None,
    "user_email": None,

    "tenant_id": None,
    "tenant_name": None,
    "primary_color": "#123A6A",

    "tenant_enterprise": False,
    "tenant_prime": False,

    "menu": None,
    "submenu": None,
}

for key, value in DEFAULT_SESSION.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ============================================================
# COGNITIVE CORE (INSTANCIA ÚNICA, SEGURA)
# ============================================================

if "client" not in st.session_state:
    st.session_state["client"] = EllitCognitiveCore(
        st.secrets["OPENAI_API_KEY"]
    )

# ============================================================
# DATABASE INIT (TOTALMENTE COMPATIBLE)
# ============================================================

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = ON;")

    # --------------------------------------------------------
    # TENANTS
    # --------------------------------------------------------
    c.execute("""
    CREATE TABLE IF NOT EXISTS tenants (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        active INTEGER DEFAULT 1,
        predictive INTEGER DEFAULT 0,
        enterprise INTEGER DEFAULT 0,
        prime INTEGER DEFAULT 0,
        primary_color TEXT DEFAULT '#FF0080',
        parent_tenant_id TEXT,
        created_at TEXT DEFAULT (datetime('now'))
    )
    """)

    # --------------------------------------------------------
    # USERS
    # --------------------------------------------------------
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

    # --------------------------------------------------------
    # SGSI KPIs (CANONICAL)
    # --------------------------------------------------------
    c.execute("""
    CREATE TABLE IF NOT EXISTS sgsi_kpis (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        kpi_date TEXT NOT NULL,
        kpi_name TEXT NOT NULL,
        kpi_value REAL NOT NULL,
        created_at TEXT DEFAULT (datetime('now')),
        FOREIGN KEY (tenant_id) REFERENCES tenants(id)
    )
    """)

    # --------------------------------------------------------
    # SGSI KPI LOG (MONITORING)
    # --------------------------------------------------------
    c.execute("""
    CREATE TABLE IF NOT EXISTS sgsi_kpi_log (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        kpi_date TEXT NOT NULL,
        kpi_name TEXT NOT NULL,
        kpi_value REAL NOT NULL,
        created_at TEXT DEFAULT (datetime('now')),
        FOREIGN KEY (tenant_id) REFERENCES tenants(id)
    )
    """)

    # ✅ PRIMER COMMIT: ESTRUCTURA DE TABLAS
    conn.commit()

    # --------------------------------------------------------
    # SUPER ADMIN TENANT
    # --------------------------------------------------------
    c.execute("SELECT id FROM tenants WHERE email=?", (SUPERADMIN_EMAIL,))
    if not c.fetchone():
        tid = str(uuid.uuid4())
        c.execute("""
        INSERT INTO tenants (id, name, email, active, enterprise, prime)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (tid, SUPERADMIN_NAME, SUPERADMIN_EMAIL, 1, 1, 1))

    # --------------------------------------------------------
    # DEMO TENANT
    # --------------------------------------------------------
    c.execute("SELECT id FROM tenants WHERE email=?", (DEMO_EMAIL,))
    row = c.fetchone()
    if not row:
        demo_tid = str(uuid.uuid4())
        c.execute("""
        INSERT INTO tenants
        (id, name, email, active, enterprise, prime, primary_color)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            demo_tid,
            DEMO_TENANT_NAME,
            DEMO_EMAIL,
            1,
            1,
            1,
            "#0048FF"
        ))

        pwd_hash = bcrypt.hashpw(
            DEMO_PASSWORD.encode(),
            bcrypt.gensalt(12)
        ).decode()

        c.execute("""
        INSERT INTO users
        (id, tenant_id, email, name, role, password_hash, is_active)
        VALUES (?, ?, ?, ?, ?, ?, 1)
        """, (
            str(uuid.uuid4()),
            demo_tid,
            DEMO_EMAIL,
            "Demo Comercial",
            "demo",
            pwd_hash
        ))

    # ✅ COMMIT FINAL
    conn.commit()
    conn.close()


# Ejecutar init una sola vez al arranque
init_db()


# ============================================================
# LICENCIAS / HELPERS
# ============================================================

def load_tenant_license_flags(tenant_id):
    if not tenant_id:
        st.session_state["tenant_enterprise"] = False
        st.session_state["tenant_prime"] = False
        return

    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "SELECT enterprise, prime FROM tenants WHERE id=?",
        (tenant_id,)
    )
    row = c.fetchone()
    conn.close()

    st.session_state["tenant_enterprise"] = bool(row[0]) if row else False
    st.session_state["tenant_prime"] = bool(row[1]) if row else False


def require_enterprise():
    if st.session_state["auth_status"] in ("super_admin", "impersonated"):
        return
    if not st.session_state["tenant_enterprise"]:
        st.error("🚫 Este módulo requiere licencia Enterprise.")
        st.stop()


def require_prime():
    if st.session_state["auth_status"] in ("super_admin", "impersonated"):
        return
    if not st.session_state["tenant_prime"]:
        st.warning("⚠️ Este módulo requiere Prime — Predictive Intelligence.")
        st.stop()


# ============================================================
# LOGIN SCREEN (REAL, ESTABLE)
# ============================================================

def login_screen():

    st.markdown("""
    <div style="
        background: linear-gradient(135deg,#FF0080 0%,#0048FF 100%);
        padding:42px;
        border-radius:22px;
        text-align:center;
        color:white;
        box-shadow:0 20px 50px rgba(0,0,0,0.25);
        margin-top:70px;
    ">
        <h1>Ellit Shield</h1>
        <p style="opacity:.9">Cognitive Security Platform</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # SUPER ADMIN
    with col1:
        st.subheader("Super Admin")
        key = st.text_input("Clave maestra", type="password")

        if st.button("Acceder como Super Admin"):
            if key == st.secrets.get("SUPER_ADMIN_KEY"):
                st.session_state.update({
                    "auth_status": "super_admin",
                    "user_role": "super_admin",
                    "tenant_name": SUPERADMIN_NAME,
                    "primary_color": "#FF0080",
                    "menu": "radar",
                    "submenu": "kpis",
                })
                st.rerun()
            else:
                st.error("Clave incorrecta")

    # USUARIOS NORMALES
    with col2:
        st.subheader("Acceso corporativo")

        email = st.text_input("Email corporativo")
        password = st.text_input("Contraseña", type="password")

        if st.button("Entrar"):
            conn = get_conn()
            c = conn.cursor()
            c.execute("""
            SELECT u.id,u.role,u.password_hash,
                   u.tenant_id,t.name,t.primary_color
            FROM users u
            JOIN tenants t ON u.tenant_id=t.id
            WHERE u.email=? AND u.is_active=1
            """, (email,))
            row = c.fetchone()
            conn.close()

            if not row:
                st.error("Usuario no encontrado o inactivo.")
                return

            if not bcrypt.checkpw(password.encode(), row[2].encode()):
                st.error("Credenciales incorrectas.")
                return

            st.session_state.update({
                "auth_status": row[1],
                "user_role": row[1],
                "user_id": row[0],
                "tenant_id": row[3],
                "tenant_name": row[4],
                "primary_color": row[5],
                "menu": "radar",
                "submenu": "kpis",
            })

            load_tenant_license_flags(row[3])
            st.rerun()

# ============================================================
# ENTRY POINT (SEGURO)
# ============================================================

if not st.session_state.get("auth_status"):
    login_screen()
    st.stop()
# ============================================================
# PARTE 2 / 3 — SIDEBAR ACCORDION ENTERPRISE (ELLIT · FIX REAL)
# ============================================================

st.markdown("""
<style>

/* ================= SIDEBAR BASE ================= */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#0F2F57 0%,#0B2545 100%);
    border-right: 1px solid #163A63;
}

/* ================= LOGO ================= */
.ellit-logo {
    display:flex;
    justify-content:center;
    align-items:center;
    padding:20px 0;
    border-bottom:1px solid #163A63;
    margin-bottom:14px;
}
.ellit-logo img {
    width:120px;
}

/* ================= MENÚ PRINCIPAL ================= */
button[kind="secondary"].ellit-main {
    width:100% !important;
    height:48px;
    margin:6px 10px;
    padding-left:18px;

    border-radius:12px;
    border-left:4px solid transparent;
    border-top:none;
    border-right:none;
    border-bottom:none;

    background:#123A6A;
    color:#E5E7EB;

    font-size:14px;
    font-weight:600;
    text-align:left;

    display:flex;
    align-items:center;
    justify-content:space-between;

    transition:all .15s ease;
}

button[kind="secondary"].ellit-main:hover {
    background:#153A63;
    color:#FFFFFF;
}

/* ===== ACTIVO NIVEL 1 (BORDE MAGENTA) ===== */
button[kind="secondary"].ellit-main-active {
    background:#123A6A !important;
    border-left:4px solid #9D2B6B;
    color:#FFFFFF !important;
}

/* ================= SUBMENÚ CONTENEDOR ================= */
.ellit-submenu-group {
    margin:6px 10px 12px 22px;
    padding-left:12px;
    border-left:2px solid rgba(157,43,107,0.6);
    background:#0B2545;
    border-radius:8px;
}

/* ================= SUBMENÚ BOTÓN ================= */
button[kind="secondary"].ellit-sub {
    width:100% !important;
    height:34px;
    margin:4px 0;
    padding-left:6px;

    border:none;
    background:transparent;

    color:#C7D2E0;
    font-size:13px;
    font-weight:500;
    text-align:left;

    transition:all .15s ease;
}

button[kind="secondary"].ellit-sub:hover {
    color:#FFFFFF;
}

/* ===== ACTIVO SUBMENÚ ===== */
button[kind="secondary"].ellit-sub-active {
    color:#9D2B6B !important;
    font-weight:700 !important;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# MENU STRUCTURE
# ============================================================

MENU_STRUCTURE = {
    "radar": ("Radar IA", {
        "kpis": "Cuadro de mando (KPIs)",
        "profile": "Perfil de la organización",
        "cognitive": "Radar Cognitivo",
        "maturity": "Madurez SGSI",
        "pdf": "Informe PDF"
    }),
    "sgsi": ("Monitorización SGSI", {
        "dashboard": "Panel general",
        "history": "Registro histórico",
        "evidence": "Evidencias y mantenimiento"
    }),
    "bcp": ("Continuidad de Negocio (BCP)", {
        "generator": "Generador BCP",
        "analysis": "Análisis cognitivo",
        "simulator": "Simulador de crisis",
        "alert_tree": "ELLIT ALERT TREE – Crisis Communication Demo"
    }),
    "policies": ("Políticas IA", {
        "generator": "Generador multinormativo"
    }),
    "predictive": ("Predictive Intelligence", {
        "standard": "Predicción estándar",
        "prime": "Predicción Prime"
    }),
    "licenses": ("Licencias", {
        "management": "Gestión de licencias"
    }),
}

# ============================================================
# RENDER SIDEBAR
# ============================================================

with st.sidebar:

    set_language()

    st.markdown("""
    <div class="ellit-logo">
        <img src="https://i.ibb.co/h19Y9KKG/logo-white-background.jpg">
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.menu:
        st.session_state.menu = "radar"
    if not st.session_state.submenu:
        st.session_state.submenu = "kpis"

    for menu_id, (label, subs) in MENU_STRUCTURE.items():

        active_menu = (menu_id == st.session_state.menu)
        chevron = "▼" if active_menu else "▶"
        main_class = "ellit-main-active" if active_menu else "ellit-main"

        if st.button(
            f"{label} {chevron}",
            key=f"menu_{menu_id}",
            use_container_width=True
        ):
            st.session_state.menu = menu_id
            st.session_state.submenu = list(subs.keys())[0]
            st.rerun()

        # SUBMENÚS
        if active_menu:
            st.markdown("<div class='ellit-submenu-group'>", unsafe_allow_html=True)

            for sub_id, sub_label in subs.items():
                sub_active = (sub_id == st.session_state.submenu)
                sub_class = "ellit-sub-active" if sub_active else "ellit-sub"

                if st.button(
                    sub_label,
                    key=f"submenu_{menu_id}_{sub_id}",
                    use_container_width=True
                ):
                    st.session_state.submenu = sub_id
                    st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# PARTE 3 / 3 — ROUTER FINAL & CONTENIDO
# ============================================================

# ============================================================
# PANEL SUPERIOR (HEADER EJECUTIVO)
# ============================================================

def render_top_panel():
    tenant = st.session_state.get("tenant_name", "Ellit Shield")
    role = st.session_state.get("auth_status", "").replace("_", " ").title()

    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg,#0F2F57 0%,#123A6A 100%);
            padding:28px;
            border-radius:18px;
            color:white;
            margin-bottom:28px;
            box-shadow:0 12px 30px rgba(0,0,0,0.25);
        ">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <h1 style="margin:0;font-size:26px;">{tenant}</h1>
                    <div style="opacity:0.85;font-size:13px;">
                        {role} · Ellit Cognitive Core
                    </div>
                </div>
            </div>
        </div>
        """.format(tenant=tenant, role=role),
        unsafe_allow_html=True
    )


# ============================================================
# ROUTER PRINCIPAL
# ============================================================

render_top_panel()

content = st.container()

menu = st.session_state.get("menu")
submenu = st.session_state.get("submenu")

# ------------------------------------------------------------
# RADAR IA
# ------------------------------------------------------------
if menu == "radar":

    require_enterprise()

    with content:
        if submenu == "kpis":
            render_radar_kpis()
        elif submenu == "profile":
            render_radar_profile()
        elif submenu == "cognitive":
            render_radar_cognitivo()
        elif submenu == "maturity":
            render_radar_madurez()
        elif submenu == "pdf":
            render_radar_pdf()

# ------------------------------------------------------------
# SGSI
# ------------------------------------------------------------
elif menu == "sgsi":

    require_enterprise()

    with content:
        if submenu == "dashboard":
            render_sgsi_monitor_dashboard()
        elif submenu == "history":
            render_sgsi_monitor_history()
        elif submenu == "evidence":
            render_sgsi_monitor_evidences()

# ------------------------------------------------------------
# BCP
# ------------------------------------------------------------
elif menu == "bcp":

    require_enterprise()

    with content:
        if submenu == "generator":
            render_bcp_generator()
        elif submenu == "analysis":
            render_bcp_analisis()
        elif submenu == "simulator":
            render_bcp_simulador()
        elif submenu == "alert_tree":
            render_bcp_alert_tree()

# ------------------------------------------------------------
# POLÍTICAS IA
# ------------------------------------------------------------
elif menu == "policies":

    require_enterprise()

    with content:
        render_policies_generator()

# ------------------------------------------------------------
# PREDICTIVE INTELLIGENCE
# ------------------------------------------------------------
elif menu == "predictive":

    with content:
        if submenu == "standard":
            require_enterprise()
            render_predictive_standard()

        elif submenu == "prime":
            require_prime()
            render_predictive_prime()

# ------------------------------------------------------------
# LICENCIAS (MÓDULO REAL)
# ------------------------------------------------------------
elif menu == "licenses":

    with content:
        render_licencias_tab()


