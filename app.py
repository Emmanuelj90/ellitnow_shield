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
    page_title="AI Executive Shield — EllitNow Cognitive Core",
    page_icon="🧠",
    layout="wide",
)

# ==============================
# ESTILO GLOBAL
# ==============================
st.markdown("""<style>
html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
    background-color: #FFFFFF;
    color: #FFFFFF;
}
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#0B2A55 0%,#061A36 100%);
    padding-top: 25px;
    border-right: 1px solid #4C5D7A;
    color: white;
}
div.block-container {
    max-width: 1250px;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    margin-left: auto !important;
    margin-right: auto !important;
}
</style>""", unsafe_allow_html=True)

# ==============================
# CONSTANTES / SESIÓN
# ==============================
SUPERADMIN_EMAIL = "admin@ellitnow.com"
SUPERADMIN_NAME = "Ellit Super Admin"
DEMO_EMAIL = "demo@ellitnow.com"
DEMO_PASSWORD = "Demo2025!g*E"
DEMO_TENANT_NAME = "DEMO - Ellit Shield"

default_session = {
    "auth_status": None,
    "user_role": None,
    "user_id": None,
    "tenant_id": None,
    "tenant_name": None,
    "user_email": None,
    "primary_color": "#FF0080",
    "tenant_enterprise": False,
    "tenant_prime": False,
}

for k, v in default_session.items():
    st.session_state.setdefault(k, v)

# ==============================
# BASE DE DATOS
# ==============================
TENANTS_DB = os.path.join(os.path.expanduser("~"), "ellit_tenants.db")

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = ON;")

    # TENANTS
    c.execute("""
        CREATE TABLE IF NOT EXISTS tenants (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            active INTEGER DEFAULT 1,
            predictive INTEGER DEFAULT 0,
            primary_color TEXT DEFAULT '#FF0080',
            parent_tenant_id TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            enterprise INTEGER DEFAULT 0,
            prime INTEGER DEFAULT 0
        )
    """)

    # USERS
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

    # SGSI – KPI HISTORY
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

    # SGSI – EVIDENCES
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

    # SGSI – MAINTENANCE
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

    # SUPER ADMIN
    c.execute("SELECT id FROM tenants WHERE email=?", (SUPERADMIN_EMAIL,))
    if not c.fetchone():
        super_id = str(uuid.uuid4())
        c.execute("""
            INSERT INTO tenants (id,name,email,active,predictive,primary_color,enterprise,prime)
            VALUES (?, ?, ?, 1, 1, '#FF0080', 1, 1)
        """, (super_id, SUPERADMIN_NAME, SUPERADMIN_EMAIL))

    # DEMO
    c.execute("SELECT id FROM tenants WHERE email=?", (DEMO_EMAIL,))
    row = c.fetchone()
    if row:
        demo_tenant_id = row[0]
    else:
        demo_tenant_id = str(uuid.uuid4())
        c.execute("""
            INSERT INTO tenants (id,name,email,active,predictive,primary_color,enterprise,prime)
            VALUES (?, ?, ?, 1, 1, '#0048FF', 1, 1)
        """, (demo_tenant_id, DEMO_TENANT_NAME, DEMO_EMAIL))

    c.execute("SELECT id FROM users WHERE email=?", (DEMO_EMAIL,))
    if not c.fetchone():
        pwd_hash = bcrypt.hashpw(DEMO_PASSWORD.encode(), bcrypt.gensalt(12)).decode()
        c.execute("""
            INSERT INTO users (id,tenant_id,email,name,role,password_hash,is_active)
            VALUES (?, ?, ?, ?, 'demo', ?, 1)
        """, (str(uuid.uuid4()), demo_tenant_id, DEMO_EMAIL, "Demo Comercial", pwd_hash))

    conn.commit()
    conn.close()

init_db()

# ==============================
# AUTENTICACIÓN
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

def load_tenant_license_flags(tenant_id):
    if not tenant_id:
        st.session_state["tenant_enterprise"] = False
        st.session_state["tenant_prime"] = False
        return

    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT enterprise, prime FROM tenants WHERE id=?", (tenant_id,))
    row = c.fetchone()
    conn.close()

    st.session_state["tenant_enterprise"] = bool(row[0]) if row else False
    st.session_state["tenant_prime"] = bool(row[1]) if row else False

def map_role_to_auth_status(role: str):
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

    # =========================================================
    # ACCESO NORMAL
    # =========================================================
    with tab_login:
        col1, col2 = st.columns(2)

        # SUPER ADMIN (clave de emergencia)
        with col1:
            st.subheader("Super Admin")
            super_key = st.text_input("SUPER_ADMIN_KEY", type="password")

            if st.button("Entrar como Super Admin"):
                secret_key = st.secrets.get("SUPER_ADMIN_KEY", "")

                if super_key == secret_key:
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
                    st.success("Acceso concedido como Super Admin.")
                    st.rerun()
                else:
                    st.error("Clave de Super Admin incorrecta.")

        # USUARIOS NORMALES
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
                    elif not user["is_active"]:
                        st.error("Usuario no activado. Usa 'Primer acceso'.")
                    else:
                        if bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
                            st.session_state.update({
                                "auth_status": map_role_to_auth_status(user["role"]),
                                "user_role": user["role"],
                                "user_id": user["id"],
                                "tenant_id": user["tenant_id"],
                                "tenant_name": user["tenant_name"],
                                "user_email": user["email"],
                                "primary_color": user["primary_color"],
                            })

                            # cargar licencias
                            load_tenant_license_flags(user["tenant_id"])

                            st.success("Acceso correcto.")
                            st.rerun()
                        else:
                            st.error("Contraseña incorrecta.")

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
            new_pwd2 = st.text_input("Repite contraseña", type="password")
            submitted_f = st.form_submit_button("Activar cuenta")

        if submitted_f:
            if not email_f or not token_f or not new_pwd:
                st.error("Rellena todos los campos.")
            elif new_pwd != new_pwd2:
                st.error("Las contraseñas no coinciden.")
            else:
                ok = activate_user_first_access(email_f.strip(), token_f.strip(), new_pwd)
                if ok:
                    st.success("Cuenta activada. Ya puedes iniciar sesión.")
                else:
                    st.error("No se pudo activar la cuenta. Revisa email y token.")

    # =========================================================
    # RESET PASSWORD
    # =========================================================
    with tab_reset:
        st.subheader("Recuperar contraseña")
        st.info("La recuperación se habilitará por correo. Contacta a soporte temporalmente.")


# ==============================
# IMPERSONACIÓN / ROLES
# ==============================
def get_partner_clients(partner_id):
    conn = get_conn()
    df = pd.read_sql_query("""
        SELECT id, name, email, active, created_at
        FROM tenants
        WHERE parent_tenant_id = ?
        ORDER BY created_at DESC
    """, conn, params=(partner_id,))
    conn.close()
    return df


def impersonate_tenant(target_tenant_id):
    if st.session_state.get("auth_status") != "super_admin":
        st.error("No tienes permiso para impersonar tenants.")
        return

    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        SELECT id, name, email, primary_color
        FROM tenants WHERE id = ?
    """, (target_tenant_id,))
    tenant = c.fetchone()
    conn.close()

    if tenant:
        st.session_state.update({
            "auth_status": "impersonated",
            "impersonated_tenant": {
                "id": tenant[0],
                "name": tenant[1],
                "email": tenant[2],
                "primary_color": tenant[3]
            },
            "tenant_id": tenant[0],
            "tenant_name": tenant[1],
            "primary_color": tenant[3]
        })

        load_tenant_license_flags(tenant[0])
        st.success(f"Ahora estás viendo como: {tenant[1]}")
        st.rerun()
    else:
        st.error("Tenant no encontrado.")


def stop_impersonation():
    if "impersonated_tenant" in st.session_state:
        del st.session_state["impersonated_tenant"]

    st.session_state.update({
        "auth_status": "super_admin",
        "tenant_id": None,
        "tenant_name": "Ellit Super Admin",
        "primary_color": "#FF0080",
    })

    st.success("Has vuelto al modo Super Admin.")
    st.rerun()


# ==============================
# CONTROLES LATERALES DEL ROL
# ==============================
def render_role_controls():
    role = st.session_state.get("auth_status")
    st.sidebar.markdown("---")

    # SUPER ADMIN
    if role == "super_admin":
        st.sidebar.subheader("Impersonar Tenant")

        conn = get_conn()
        tenants_df = pd.read_sql_query("SELECT id, name FROM tenants ORDER BY name", conn)
        conn.close()

        if tenants_df.empty:
            st.sidebar.info("No hay tenants.")
        else:
            names = tenants_df["name"].tolist()
            tenant_map = dict(zip(names, tenants_df["id"]))

            selected = st.sidebar.selectbox(
                "Selecciona tenant",
                names,
                key="imperson_selector"
            )

            if st.sidebar.button("Ver como tenant seleccionado"):
                impersonate_tenant(tenant_map[selected])

        st.sidebar.markdown("---")
        st.sidebar.subheader("Crear nuevo tenant")

        with st.sidebar.form("new_tenant_form"):
            tipo = st.selectbox("Tipo", ["Partner", "Cliente directo"])
            nombre = st.text_input("Nombre")
            email = st.text_input("Email administrador")
            ok = st.form_submit_button("Crear")

        if ok:
            if nombre and email:
                tenant_type = "partner" if tipo == "Partner" else "client"
                tenant_id, user_id, token = create_tenant_with_admin(
                    nombre, email, tenant_type
                )
                st.sidebar.success(f"Tenant '{nombre}' creado.")
                st.sidebar.code(token)
            else:
                st.sidebar.error("Nombre y email requeridos.")

    # IMPERSONATED
    elif role == "impersonated":
        t = st.session_state.get("impersonated_tenant", {})
        st.sidebar.info(f"Modo impersonación: {t.get('name')}")
        if st.sidebar.button("Salir de impersonación"):
            stop_impersonation()

    # PARTNER
    elif role == "partner":
        st.sidebar.subheader("Tus clientes")

        partner_id = st.session_state.get("tenant_id")
        df = get_partner_clients(partner_id)

        if df.empty:
            st.sidebar.info("No tienes clientes.")
        else:
            for _, row in df.iterrows():
                st.sidebar.write(f"• {row['name']}")

        st.sidebar.markdown("---")
        st.sidebar.subheader("Crear cliente directo")

        with st.sidebar.form("new_client_form"):
            name = st.text_input("Nombre del cliente")
            email = st.text_input("Email admin")
            ok = st.form_submit_button("Crear cliente")

        if ok and name and email:
            tenant_id, user_id, token = create_tenant_with_admin(
                name, email, "client", parent_tenant_id=partner_id
            )
            st.sidebar.success(f"Cliente '{name}' creado.")
            st.sidebar.code(token)

    # DEMO
    elif role == "demo":
        st.sidebar.info("Modo demo activo.")
        if st.sidebar.button("Cerrar demo"):
            for key in ["auth_status","user_role","user_id","tenant_id","tenant_name","user_email"]:
                st.session_state[key] = None
            st.rerun()


# ==============================
# PANEL SUPERIOR
# ==============================
def render_panel():
    role = st.session_state.get("auth_status", "demo")
    tenant = st.session_state.get("tenant_name", "AI Executive Shield")
    color = st.session_state.get("primary_color", "#FF0080")

    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg,{color} 0%,#00B4FF 100%);
            padding:20px;
            color:white;
            border-radius:12px;
            text-align:center;">
            <h1>{tenant}</h1>
            <p>{role.title()} • Ellit Cognitive Core</p>
        </div>
    """, unsafe_allow_html=True)

    if "menu" in st.session_state and "submenu" in st.session_state:
        st.session_state["breadcrumb"] = (
            f"{st.session_state['menu']} → {st.session_state['submenu']}"
        )

    if "breadcrumb" in st.session_state:
        st.markdown(
            f"<div style='margin-top:10px;font-size:13px;color:#E2E8F0;'>"
            f"{st.session_state['breadcrumb']}</div>",
            unsafe_allow_html=True
        )


# ==============================
# VALIDACIONES DE LICENCIAS
# ==============================
def require_enterprise():
    if st.session_state.get("auth_status") in ["super_admin", "impersonated"]:
        return
    if not st.session_state.get("tenant_enterprise", False):
        st.error("🚫 Este módulo requiere licencia **Enterprise**.")
        st.stop()

def require_prime():
    if st.session_state.get("auth_status") in ["super_admin", "impersonated"]:
        return
    if not st.session_state.get("tenant_prime", False):
        st.warning(" Este módulo requiere **Prime - Predictive Intelligence**.")
        st.stop()


# ==============================
# STRIPE / ACTIVACIÓN DE LICENCIAS
# ==============================
def render_stripe_checkout():
    stripe_key = st.secrets.get("STRIPE_SECRET_KEY")
    app_url = st.secrets.get("APP_URL", "https://ellitnow.com")

    if not stripe_key:
        st.error("Falta STRIPE_SECRET_KEY.")
        return

    stripe.api_key = stripe_key

    st.markdown("""
        <h3 style='text-align:center;color:#FF0080;'>Activar licencias EllitNow Shield</h3>
        <p style='text-align:center;color:#E2E8F0;'>
            Selecciona un plan y completa el checkout.
        </p>
    """, unsafe_allow_html=True)

    colE, colP = st.columns(2)

    # PLAN ENTERPRISE
    with colE:
        st.markdown("""
            <div style="
                background:#0F355F;padding:20px;border-radius:15px;
                border:1px solid #4C5D7A;color:white;
                text-align:center;">
                <h4>Enterprise Edition</h4>
                <p>4.900 €/año</p>
            </div>
        """, unsafe_allow_html=True)

        if st.button("Activar Enterprise"):
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
                st.markdown(
                    f"<a href='{session.url}' target='_blank'>Continuar en Stripe</a>",
                    unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {e}")

    # PLAN PRIME
    with colP:
        st.markdown("""
            <div style="
                background:#0F355F;padding:20px;border-radius:15px;
                border:1px solid #4C5D7A;color:white;text-align:center;">
                <h4>Prime — Predictive Intelligence</h4>
                <p>699 €/mes</p>
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
                st.markdown(
                    f"<a href='{session.url}' target='_blank'>Completar pago</a>",
                    unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {e}")


# ==============================
# GESTIÓN DE LICENCIAS TAB COMPLETO
# ==============================
def render_licencias_tab():
    st.subheader("Gestión de licencias y tenants")

    conn = get_conn()
    df = pd.read_sql_query("""
        SELECT name,email,
               CASE WHEN active=1 THEN 'Activo' ELSE 'Inactivo' END AS Estado,
               created_at
        FROM tenants
        ORDER BY created_at DESC
    """, conn)
    conn.close()

    if df.empty:
        st.info("No hay tenants.")
    else:
        st.dataframe(df, use_container_width=True)

    st.markdown("### Activar Licencias")
    render_stripe_checkout()
        # ===============================
        # MENÚ PRINCIPAL CONFIG
        # ===============================
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
                translate("ELLIT ALERT TREE – Crisis Communication Demo", "ELLIT ALERT TREE – Crisis Communication Demo")
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

        # Estado inicial seguro
        if "menu" not in st.session_state:
            st.session_state.menu = main_options[0]

        if "submenu" not in st.session_state:
            st.session_state.submenu = submenu_map[st.session_state.menu][0]

        # ===============================
        # ESTILOS (CSS)
        # ===============================
        st.markdown("""
        <style>
        .ellit-menu-btn {
            width: 100%;
            padding: 10px 14px;
            border-radius: 10px;
            margin-bottom: 6px;
            border: 1px solid #1A4472;
            background: #0F355F;
            color: white;
            font-weight: 500;
            text-align: left;
        }
        .ellit-menu-btn:hover {
            background: #1A4472;
        }
        .ellit-menu-btn-active {
            background: #D8278A;
            border-color: #FF0080;
            font-weight: 700;
            color: white;
        }
        .ellit-submenu-item {
            padding: 6px 10px;
            margin-left: 12px;
            border-left: 2px solid #1A4472;
            color: #E2E8F0;
        }
        .ellit-submenu-item:hover {
            color: white;
        }
        .ellit-submenu-active {
            color: #FF0080;
            font-weight: 700;
            border-left: 2px solid #FF0080;
        }
        </style>
        """, unsafe_allow_html=True)

        # ===============================
        # MENÚ PRINCIPAL
        # ===============================
        for opt in main_options:
            active = (opt == st.session_state.menu)
            css_class = "ellit-menu-btn-active" if active else "ellit-menu-btn"

            if st.button(opt, key=f"menu_{opt}"):
                st.session_state.menu = opt
                st.session_state.submenu = submenu_map[opt][0]
                st.rerun()

            st.markdown(f"<div class='{css_class}'>{opt}</div>", unsafe_allow_html=True)

        # ===============================
        # SUBMENÚ
        # ===============================
        for sub in submenu_map[st.session_state.menu]:
            is_active = (sub == st.session_state.submenu)
            css_sub = "ellit-submenu-item ellit-submenu-active" if is_active else "ellit-submenu-item"

            if st.button(sub, key=f"submenu_{sub}"):
                st.session_state.submenu = sub
                st.rerun()

            st.markdown(f"<div class='{css_sub}'>{sub}</div>", unsafe_allow_html=True)

        # ===============================
        # CONTROLES DE ROL
        # ===============================
        render_role_controls()


    # ==============================
    # PANEL SUPERIOR
    # ==============================
    render_panel()

    # ==============================
    # CONTENIDO PRINCIPAL
    # ==============================
    content_area = st.container()

    menu = st.session_state.get("menu")
    submenu = st.session_state.get("submenu")

    if menu and submenu:
        st.session_state["breadcrumb"] = f"{menu} → {submenu}"

    # =====================================
    # RADAR IA (Enterprise)
    # =====================================
    if menu == translate("Radar IA", "AI Radar"):

        require_enterprise()

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

    # =====================================
    # SGSI MONITORING (Enterprise)
    # =====================================
    elif menu == translate("Monitorización SGSI", "ISMS Monitoring"):

        require_enterprise()

        if submenu == translate("Panel general", "General Dashboard"):
            with content_area:
                render_sgsi_monitor_dashboard()

        elif submenu == translate("Registro histórico", "History Log"):
            with content_area:
                render_sgsi_monitor_history()

        elif submenu == translate("Evidencias y mantenimiento", "Evidence & Maintenance"):
            with content_area:
                render_sgsi_monitor_evidences()

    # =====================================
    # BCP (Enterprise)
    # =====================================
    elif menu == translate("Continuidad de Negocio (BCP)", "Business Continuity"):

        require_enterprise()

        if submenu == translate("Generador BCP", "BCP Generator"):
            with content_area:
                render_bcp_generator()

        elif submenu == translate("Análisis cognitivo", "Cognitive Analysis"):
            with content_area:
                render_bcp_analisis()

        elif submenu == translate("Simulador de crisis", "Crisis Simulator"):
            with content_area:
                render_bcp_simulador()

        elif submenu == translate("ELLIT ALERT TREE – Crisis Communication Demo",
                                  "ELLIT ALERT TREE – Crisis Communication Demo"):
            with content_area:
                render_bcp_alert_tree()

    # =====================================
    # POLITICAS IA (Enterprise)
    # =====================================
    elif menu == translate("Políticas IA", "AI Policies"):

        require_enterprise()

        if submenu == translate("Generador multinormativo", "Multistandard Policy Generator"):
            with content_area:
                render_policies_generator()

    # =====================================
    # PREDICTIVE INTELLIGENCE
    # =====================================
    elif menu == translate("Predictive Intelligence", "Predictive Intelligence"):

        if submenu == translate("Predicción estándar", "Standard Prediction"):
            require_enterprise()
            with content_area:
                render_predictive_standard()

        elif submenu == translate("Predicción Prime", "Prime Prediction"):
            require_prime()
            with content_area:
                render_predictive_prime()

    # =====================================
    # LICENCIAS
    # =====================================
    elif menu == translate("Licencias", "Licenses"):

        if st.session_state.get("user_role") not in ["super_admin", "partner", "client_admin"]:
            st.warning("No tienes permisos para gestionar licencias.")
            st.stop()

        if submenu == translate("Gestión de licencias", "License Management"):
            with content_area:
                render_licencias_tab()

else:
    # Si no hay sesión iniciar login
    login_screen()

