# ==============================
# AI Executive Shield — EllitNow Cognitive Core Edition
# VERSIÓN AUTH REFACTORED — CLEAN & STABLE
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

# --- Módulos externos ---
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

# lenguaje UI
from language import translate, set_language

# DB helper
from core.database import get_conn

# Desactivar componentes viejos
st.components.v1.declare_component = lambda *args, **kwargs: None

# Cliente Cognitivo
st.session_state["client"] = EllitCognitiveCore(st.secrets["OPENAI_API_KEY"])

# ==============================
# CONFIGURACIÓN DE PÁGINA
# ==============================
st.set_page_config(
    page_title="AI Executive Shield — Ellit Cognitive Core",
    page_icon="https://i.ibb.co/h19Y9KKG/logo-white-background.jpg",
    layout="wide",
)

# ============================================================
# ESTILO GLOBAL BASE (NO MENÚ)
# ============================================================

st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #FFFFFF;
    color: #0F172A;
}

div.block-container {
    max-width: 1250px;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    margin-left: auto !important;
    margin-right: auto !important;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# CONSTANTES
# ============================================================

SUPERADMIN_EMAIL = "admin@ellitnow.com"
SUPERADMIN_NAME = "Ellit Super Admin"

DEMO_EMAIL = "demo@ellitnow.com"
DEMO_PASSWORD = "Demo2025!g*E"
DEMO_TENANT_NAME = "DEMO — Ellit Shield"

# ============================================================
# IDs INTERNOS (ÚNICA FUENTE DE VERDAD)
# ============================================================

MENU_IDS = {
    "RADAR": "radar",
    "SGSI": "sgsi",
    "BCP": "bcp",
    "POLICIES": "policies",
    "PREDICTIVE": "predictive",
    "LICENSES": "licenses",
}

SUBMENU_IDS = {
    "radar": {
        "KPIS": "kpis",
        "PROFILE": "profile",
        "COGNITIVE": "cognitive",
        "MATURITY": "maturity",
        "PDF": "pdf",
    },
    "sgsi": {
        "DASHBOARD": "dashboard",
        "HISTORY": "history",
        "EVIDENCE": "evidence",
    },
    "bcp": {
        "GENERATOR": "generator",
        "ANALYSIS": "analysis",
        "SIMULATOR": "simulator",
        "ALERT_TREE": "alert_tree",
    },
    "policies": {
        "GENERATOR": "generator",
    },
    "predictive": {
        "STANDARD": "standard",
        "PRIME": "prime",
    },
    "licenses": {
        "MANAGEMENT": "management",
    },
}

# ============================================================
# SESIÓN — ESTADO BASE
# ============================================================

DEFAULT_SESSION_STATE = {
    "auth_status": None,
    "user_role": None,
    "user_id": None,
    "tenant_id": None,
    "tenant_name": None,
    "user_email": None,
    "primary_color": "#FF0080",
    "tenant_enterprise": False,
    "tenant_prime": False,
    "menu": None,
    "submenu": None,
}

for key, value in DEFAULT_SESSION_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ============================================================
# CLIENTE COGNITIVO (UNA SOLA INSTANCIA)
# ============================================================

if "client" not in st.session_state:
    st.session_state["client"] = EllitCognitiveCore(
        st.secrets.get("OPENAI_API_KEY")
    )

# ============================================================
# BASE DE DATOS — INIT
# ============================================================

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = ON;")

    c.execute("""
    CREATE TABLE IF NOT EXISTS tenants (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        active INTEGER DEFAULT 1,
        enterprise INTEGER DEFAULT 0,
        prime INTEGER DEFAULT 0,
        primary_color TEXT DEFAULT '#FF0080',
        parent_tenant_id TEXT,
        created_at TEXT DEFAULT (datetime('now'))
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        tenant_id TEXT,
        email TEXT UNIQUE NOT NULL,
        name TEXT,
        role TEXT NOT NULL,
        password_hash TEXT,
        is_active INTEGER DEFAULT 1,
        created_at TEXT DEFAULT (datetime('now')),
        FOREIGN KEY (tenant_id) REFERENCES tenants(id)
    )
    """)

    conn.commit()

    # === SUPER ADMIN ===
    c.execute("SELECT id FROM tenants WHERE email = ?", (SUPERADMIN_EMAIL,))
    if not c.fetchone():
        super_id = str(uuid.uuid4())
        c.execute("""
        INSERT INTO tenants (id, name, email, active, enterprise, prime)
        VALUES (?, ?, ?, 1, 1, 1)
        """, (super_id, SUPERADMIN_NAME, SUPERADMIN_EMAIL))

    # === DEMO TENANT ===
    c.execute("SELECT id FROM tenants WHERE email = ?", (DEMO_EMAIL,))
    row = c.fetchone()

    if row:
        demo_tenant_id = row[0]
    else:
        demo_tenant_id = str(uuid.uuid4())
        c.execute("""
        INSERT INTO tenants (id, name, email, active, enterprise, prime, primary_color)
        VALUES (?, ?, ?, 1, 1, 1, '#0048FF')
        """, (demo_tenant_id, DEMO_TENANT_NAME, DEMO_EMAIL))

    c.execute("SELECT id FROM users WHERE email = ?", (DEMO_EMAIL,))
    if not c.fetchone():
        pwd_hash = bcrypt.hashpw(
            DEMO_PASSWORD.encode(),
            bcrypt.gensalt(12)
        ).decode()

        c.execute("""
        INSERT INTO users (id, tenant_id, email, name, role, password_hash, is_active)
        VALUES (?, ?, ?, ?, 'demo', ?, 1)
        """, (
            str(uuid.uuid4()),
            demo_tenant_id,
            DEMO_EMAIL,
            "Demo Comercial",
            pwd_hash,
        ))

    conn.commit()
    conn.close()

init_db()

# ============================================================
# HELPERS — LICENCIAS
# ============================================================

def load_tenant_license_flags(tenant_id: str | None):
    if not tenant_id:
        st.session_state["tenant_enterprise"] = False
        st.session_state["tenant_prime"] = False
        return

    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "SELECT enterprise, prime FROM tenants WHERE id = ?",
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
# PARTE 2 — SIDEBAR & MENÚ PREMIUM
# ============================================================

from language import translate, set_language

# ============================================================
# SIDEBAR — ESTILO PREMIUM (UNIFORME)
# ============================================================

st.markdown("""
<style>

/* === SIDEBAR CONTENEDOR === */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#0B2A55 0%,#061A36 100%);
    border-right: 1px solid #1E3A8A;
    padding-top: 16px;
}

/* === HEADER SIDEBAR === */
.ellit-sidebar-header {
    padding: 12px 16px 18px 16px;
    border-bottom: 1px solid #1E3A8A;
    margin-bottom: 12px;
}

.ellit-sidebar-title {
    color: #FFFFFF;
    font-size: 18px;
    font-weight: 700;
    margin: 0;
}

.ellit-sidebar-subtitle {
    color: #94A3B8;
    font-size: 13px;
    margin: 4px 0 0 0;
}

/* === MENÚ PRINCIPAL === */
.ellit-menu-item {
    display: flex;
    align-items: center;
    height: 48px;
    padding: 0 16px;
    margin: 4px 10px;
    border-radius: 12px;
    cursor: pointer;
    color: #E5E7EB;
    font-size: 14px;
    font-weight: 500;
    background: transparent;
    transition: background 0.15s ease, color 0.15s ease;
}

.ellit-menu-item:hover {
    background: #1E3A8A;
    color: #FFFFFF;
}

.ellit-menu-item-active {
    background: #FF0080;
    color: #FFFFFF;
    font-weight: 700;
}

/* === SUBMENÚ === */
.ellit-submenu-item {
    display: flex;
    align-items: center;
    height: 40px;
    padding: 0 16px 0 32px;
    margin: 2px 14px;
    border-radius: 10px;
    cursor: pointer;
    color: #CBD5F5;
    font-size: 13px;
    background: transparent;
    transition: background 0.15s ease, color 0.15s ease;
}

.ellit-submenu-item:hover {
    background: rgba(255,255,255,0.06);
    color: #FFFFFF;
}

.ellit-submenu-item-active {
    color: #FF0080;
    font-weight: 700;
    background: rgba(255,0,128,0.12);
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# DEFINICIÓN MENÚ (LABELS SOLO UI)
# ============================================================

MENU_UI = {
    "radar": translate("Radar IA", "AI Radar"),
    "sgsi": translate("Monitorización SGSI", "ISMS Monitoring"),
    "bcp": translate("Continuidad de Negocio (BCP)", "Business Continuity"),
    "policies": translate("Políticas IA", "AI Policies"),
    "predictive": translate("Predictive Intelligence", "Predictive Intelligence"),
    "licenses": translate("Licencias", "Licenses"),
}

SUBMENU_UI = {
    "radar": {
        "kpis": translate("Cuadro de mando (KPIs)", "Dashboard KPIs"),
        "profile": translate("Perfil de la organización", "Organization Profile"),
        "cognitive": translate("Radar Cognitivo", "Cognitive Radar"),
        "maturity": translate("Madurez SGSI", "ISMS Maturity"),
        "pdf": translate("Informe PDF", "PDF Report"),
    },
    "sgsi": {
        "dashboard": translate("Panel general", "General Dashboard"),
        "history": translate("Registro histórico", "History Log"),
        "evidence": translate("Evidencias y mantenimiento", "Evidence & Maintenance"),
    },
    "bcp": {
        "generator": translate("Generador BCP", "BCP Generator"),
        "analysis": translate("Análisis cognitivo", "Cognitive Analysis"),
        "simulator": translate("Simulador de crisis", "Crisis Simulator"),
        "alert_tree": translate(
            "ELLIT ALERT TREE – Crisis Communication Demo",
            "ELLIT ALERT TREE – Crisis Communication Demo"
        ),
    },
    "policies": {
        "generator": translate(
            "Generador multinormativo",
            "Multistandard Policy Generator"
        ),
    },
    "predictive": {
        "standard": translate("Predicción estándar", "Standard Prediction"),
        "prime": translate("Predicción Prime", "Prime Prediction"),
    },
    "licenses": {
        "management": translate("Gestión de licencias", "License Management"),
    },
}

# ============================================================
# SIDEBAR — RENDER
# ============================================================

with st.sidebar:
    set_language()

    # Header
    st.markdown("""
        <div class="ellit-sidebar-header">
            <div class="ellit-sidebar-title">Ellit Cognitive Core</div>
            <div class="ellit-sidebar-subtitle">AI Executive Shield</div>
        </div>
    """, unsafe_allow_html=True)

    # Estado inicial
    if not st.session_state.menu:
        st.session_state.menu = "radar"
        st.session_state.submenu = list(SUBMENU_IDS["radar"].values())[0]

    # Render menú
    for menu_id, label in MENU_UI.items():

        is_active = (menu_id == st.session_state.menu)
        menu_css = (
            "ellit-menu-item ellit-menu-item-active"
            if is_active else
            "ellit-menu-item"
        )

        if st.button(label, key=f"menu_{menu_id}"):
            st.session_state.menu = menu_id
            st.session_state.submenu = list(
                SUBMENU_IDS.get(menu_id, {}).values()
            )[0]
            st.rerun()

        st.markdown(
            f"<div class='{menu_css}'>{label}</div>",
            unsafe_allow_html=True
        )

        # Submenú desplegable
        if is_active and menu_id in SUBMENU_UI:
            for sub_id, sub_label in SUBMENU_UI[menu_id].items():

                is_sub_active = (sub_id == st.session_state.submenu)
                sub_css = (
                    "ellit-submenu-item ellit-submenu-item-active"
                    if is_sub_active else
                    "ellit-submenu-item"
                )

                if st.button(sub_label, key=f"submenu_{menu_id}_{sub_id}"):
                    st.session_state.submenu = sub_id
                    st.rerun()

                st.markdown(
                    f"<div class='{sub_css}'>{sub_label}</div>",
                    unsafe_allow_html=True
                )
# ============================================================
# PARTE 3 — CONTENT DISPATCH (ROUTER FINAL)
# ============================================================

# --- IMPORTS DE MÓDULOS ---
from modules.radar_ia import (
    render_radar_kpis,
    render_radar_profile,
    render_radar_cognitivo,
    render_radar_madurez,
    render_radar_pdf,
)

from modules.sgsi_monitoring import (
    render_sgsi_monitor_dashboard,
    render_sgsi_monitor_history,
    render_sgsi_monitor_evidences,
)

from modules.bcp import (
    render_bcp_generator,
    render_bcp_analisis,
    render_bcp_simulador,
    render_bcp_alert_tree,
)

from modules.policies import render_policies_generator

from modules.predictive import (
    render_predictive_standard,
    render_predictive_prime,
)

# ============================================================
# PANEL SUPERIOR (HEADER)
# ============================================================

def render_top_panel():
    tenant = st.session_state.get("tenant_name") or "Ellit Cognitive Core"
    role = st.session_state.get("auth_status") or "demo"
    color = st.session_state.get("primary_color", "#FF0080")

    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg,{color} 0%,#00B4FF 100%);
            padding:20px;
            border-radius:14px;
            color:white;
            text-align:center;
            margin-bottom:18px;
        ">
            <h1 style="margin:0;">{tenant}</h1>
            <div style="opacity:0.85;font-size:13px;">
                {role.title()} · Ellit Cognitive Core
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# CONTENT DISPATCH
# ============================================================

if st.session_state.get("auth_status"):

    # Header superior
    render_top_panel()

    content = st.container()

    menu = st.session_state.get("menu")
    submenu = st.session_state.get("submenu")

    # --------------------------------------------------------
    # RADAR IA
    # --------------------------------------------------------
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

    # --------------------------------------------------------
    # SGSI MONITORING
    # --------------------------------------------------------
    elif menu == "sgsi":

        require_enterprise()

        with content:
            if submenu == "dashboard":
                render_sgsi_monitor_dashboard()

            elif submenu == "history":
                render_sgsi_monitor_history()

            elif submenu == "evidence":
                render_sgsi_monitor_evidences()

    # --------------------------------------------------------
    # BCP
    # --------------------------------------------------------
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

    # --------------------------------------------------------
    # POLÍTICAS IA
    # --------------------------------------------------------
    elif menu == "policies":

        require_enterprise()

        with content:
            if submenu == "generator":
                render_policies_generator()

    # --------------------------------------------------------
    # PREDICTIVE INTELLIGENCE
    # --------------------------------------------------------
    elif menu == "predictive":

        with content:
            if submenu == "standard":
                require_enterprise()
                render_predictive_standard()

            elif submenu == "prime":
                require_prime()
                render_predictive_prime()

    # --------------------------------------------------------
    # LICENCIAS
    # --------------------------------------------------------
    elif menu == "licenses":

        with content:
            from app import render_licencias_tab
            render_licencias_tab()

else:
    # --------------------------------------------------------
    # LOGIN / NO SESSION
    # --------------------------------------------------------
    login_screen()
