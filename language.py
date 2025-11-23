# ================================
# Language module — Ellit
# ================================

import streamlit as st

# Traducciones simples
translations = {
    "es": {
        "Navegación": "Navegación",
        "Radar IA": "Radar IA",
        "Monitorización SGSI": "Monitorización SGSI",
        "Continuidad de Negocio (BCP)": "Continuidad de Negocio (BCP)",
        "Políticas IA": "Políticas IA",
        "Predictive Intelligence": "Inteligencia Predictiva",
        "Licencias": "Licencias",
        "Opciones": "Opciones",
        "Cuadro de mando (KPIs)": "Cuadro de mando (KPIs)",
        "Perfil de la organización": "Perfil de la organización",
        "Radar Cognitivo": "Radar Cognitivo",
        "Madurez SGSI": "Madurez SGSI",
        "Informe PDF": "Informe PDF",
        "Panel general": "Panel general",
        "Registro histórico": "Registro histórico",
        "Evidencias y mantenimiento": "Evidencias y mantenimiento",
        "Generador BCP": "Generador BCP",
        "Análisis cognitivo": "Análisis cognitivo",
        "Simulador de crisis": "Simulador de crisis",
        "ELLIT ALERT TREE – Crisis Communication Demo": "ELLIT ALERT TREE – Crisis Communication Demo",
        "Generador multinormativo": "Generador multinormativo",
        "Predicción estándar": "Predicción estándar",
        "Predicción Prime": "Predicción Prime",
        "Gestión de licencias": "Gestión de licencias",
    },
    "en": {
        "Navegación": "Navigation",
        "Radar IA": "AI Radar",
        "Monitorización SGSI": "ISMS Monitoring",
        "Continuidad de Negocio (BCP)": "Business Continuity",
        "Políticas IA": "AI Policies",
        "Predictive Intelligence": "Predictive Intelligence",
        "Licencias": "Licenses",
        "Opciones": "Options",
        "Cuadro de mando (KPIs)": "Dashboard KPIs",
        "Perfil de la organización": "Organization Profile",
        "Radar Cognitivo": "Cognitive Radar",
        "Madurez SGSI": "ISMS Maturity",
        "Informe PDF": "PDF Report",
        "Panel general": "General Dashboard",
        "Registro histórico": "History Log",
        "Evidencias y mantenimiento": "Evidence & Maintenance",
        "Generador BCP": "BCP Generator",
        "Análisis cognitivo": "Cognitive Analysis",
        "Simulador de crisis": "Crisis Simulator",
        "ELLIT ALERT TREE – Crisis Communication Demo": "ELLIT ALERT TREE – Crisis Communication Demo",
        "Generador multinormativo": "Multistandard Policy Generator",
        "Predicción estándar": "Standard Prediction",
        "Predicción Prime": "Prime Prediction",
        "Gestión de licencias": "License Management",
    }
}

def translate(text, fallback=None):
    lang = st.session_state.get("language", "es")
    return translations.get(lang, {}).get(text, fallback or text)

def set_language():
    lang = st.selectbox("🌍 Idioma / Language", ["es", "en"], index=0)
    st.session_state["language"] = lang
