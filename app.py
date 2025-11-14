# app.py — Clean Minimalistic Version
# NOTE: This is a skeleton structure preserving all original tabs (1–5)
# and ready for you to paste the original tab content inside each section.
# All authentication, roles, sidebar, and layout are rebuilt cleanly.

import streamlit as st
import sqlite3, uuid, hashlib, secrets, bcrypt
import pandas as pd
import numpy as np
from io import BytesIO
import datetime as dt

# ================================================
# DATABASE CONNECTION
# ================================================
TENANTS_DB = "tenants.db"

def get_conn():
    return sqlite3.connect(TENANTS_DB, check_same_thread=False)

# ================================================
# INIT SUPER ADMIN
# ================================================
SUPERADMIN_EMAIL = "super@ellitnow.com"
SUPERADMIN_KEY = "sk_superadmin"

def init_db_and_superadmin():
    conn = get_conn()
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS tenants (id TEXT PRIMARY KEY, name TEXT, email TEXT, active INTEGER, primary_color TEXT, created_at TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS tenant_api_keys (tenant_id TEXT, key_fingerprint TEXT, key_hash TEXT, revoked INTEGER)")
    conn.commit()

    # create super-admin
    c.execute("SELECT id FROM tenants WHERE email=?", (SUPERADMIN_EMAIL,))
    if not c.fetchone():
        sid = str(uuid.uuid4())
        key_hash = bcrypt.hashpw(SUPERADMIN_KEY.encode(), bcrypt.gensalt()).decode()
        fingerprint = hashlib.sha256(SUPERADMIN_KEY.encode()).hexdigest()[:12]
        c.execute("INSERT INTO tenants VALUES (?, ?, ?, 1, '#222222', ?)", (sid, "SuperAdmin", SUPERADMIN_EMAIL, dt.datetime.now()))
        c.execute("INSERT INTO tenant_api_keys VALUES (?, ?, ?, 0)", (sid, fingerprint, key_hash))
        conn.commit()
    conn.close()

# ================================================
# AUTH
# ================================================

def verify_api_key(key):
    conn = get_conn()
    c = conn.cursor()
    fingerprint = hashlib.sha256(key.encode()).hexdigest()[:12]
    c.execute("SELECT tenant_id,key_hash FROM tenant_api_keys WHERE key_fingerprint=? AND revoked=0", (fingerprint,))
    row = c.fetchone()
    if not row:
        return None
    tenant_id, stored = row
    if bcrypt.checkpw(key.encode(), stored.encode()):
        c.execute("SELECT id,name,email,primary_color FROM tenants WHERE id=?", (tenant_id,))
        t = c.fetchone()
        conn.close()
        return t
    conn.close()
    return None

# ================================================
# SIDEBAR
# ================================================

def render_sidebar():
    st.sidebar.title("Ellit Panel")
    role = st.session_state.get("auth_status")

    if role == "super_admin":
        st.sidebar.subheader("Super Admin")
        st.sidebar.write("Gestionar Tenants, Impersonación")
    elif role == "impersonated":
        st.sidebar.subheader("Viendo como Tenant")
        st.sidebar.write(st.session_state.get("tenant_name"))
        if st.sidebar.button("Salir de Impersonación"):
            st.session_state.auth_status = "super_admin"
            st.rerun()
    else:
        st.sidebar.subheader("Tenant")
        st.sidebar.write(st.session_state.get("tenant_name"))

    st.sidebar.markdown("---")
    if st.sidebar.button("Cerrar sesión"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

# ================================================
# LOGIN
# ================================================

def login_screen():
    st.title("Acceso Ellit")
    with st.form("login_form"):
        api_key = st.text_input("API Key", type="password")
        s = st.form_submit_button("Entrar")
    if s:
        t = verify_api_key(api_key)
        if t:
            tid, name, email, color = t
            st.session_state.auth_status = "super_admin" if email == SUPERADMIN_EMAIL else "tenant"
            st.session_state.tenant_id = tid
            st.session_state.tenant_name = name
            st.session_state.primary_color = color
            st.rerun()
        else:
            st.error("Clave incorrecta")

# ================================================
# MAIN PANEL
# ================================================

def render_main_panel():
    st.title(st.session_state.get("tenant_name", "Ellit"))

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Radar", "Continuidad", "Políticas", "Predictive", "Licencias"])

    with tab1:
        st.write("TAB1 — Pegar contenido original aquí.")

    with tab2:
        st.write("TAB2 — Pegar contenido original aquí.")

    with tab3:
        st.write("TAB3 — Pegar contenido original aquí.")

    with tab4:
        st.write("TAB4 — Pegar contenido original aquí.")

    with tab5:
        st.write("TAB5 — Pegar contenido original aquí.")

# ================================================
# EXECUTION
# ================================================
init_db_and_superadmin()
render_sidebar()

if st.session_state.get("auth_status"):
    render_main_panel()
else:
    login_screen()
