# ============================================================
#  RADAR IA — BLOQUE 1: KPIs del Cuadro de Mando
# ============================================================

def render_radar_kpis():
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

    st.markdown("""
    <style>
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

# ============================================================
#  RADAR IA — BLOQUE 2: Perfil de la Organización
# ============================================================

def render_radar_profile():
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

    st.session_state["radar_profile"] = {
        "organizacion": nombre_org,
        "sector": sector,
        "nivel_ens": nivel_ens,
        "tamano": tamano,
        "region": region,
        "responsable": responsable,
        "riesgos_detectados": riesgos,
        "certificaciones": certificaciones
    }

# ============================================================
#  RADAR IA — BLOQUE 3: Radar ENS–ISO–NIST (Radar Cognitivo)
# ============================================================

def render_radar_cognitivo():
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #FF0080 0%, #00B4FF 100%);
        padding:24px;
        border-radius:16px;
        text-align:center;
        margin-bottom:25px;
        color:#FFFFFF;">
        <h2 style="font-weight:700;margin:0;">Radar IA — Cognitive Risk Engine</h2>
    </div>
    """, unsafe_allow_html=True)

    profile = st.session_state.get("radar_profile", {})
    if not profile:
        st.warning("Primero completa el perfil de la organización en la sección correspondiente.")
        return

    if st.button("Analizar con Ellit Cognitive Core", key="analizar_radar_ia"):
        with st.spinner("Analizando contexto organizacional..."):
            try:
                data = analyze_radar_ia(client, profile)
                if data:
                    st.session_state["radar_data"] = data
                    st.success("Análisis completado correctamente.")
                else:
                    st.error("No se pudo interpretar la respuesta del motor cognitivo.")
            except Exception as e:
                st.error(f"Error al procesar el análisis: {str(e)}")

    data = st.session_state.get("radar_data", None)
    if not data:
        return

    indicadores = data.get("indicadores", {})
    if indicadores:
        labels = list(indicadores.keys())
        values = list(indicadores.values())
        num_vars = len(labels)
        angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
        values += values[:1]
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
        ax.fill(angles, values, color="#00B4FF", alpha=0.25)
        ax.plot(angles, values, color="#00B4FF", linewidth=2)
        ax.set_yticks([20, 40, 60, 80, 100])
        ax.set_ylim(0, 100)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels, fontsize=8)
        st.pyplot(fig)


# ============================================================
#  RADAR IA — BLOQUE 4: Madurez del SGSI
# ============================================================

def render_radar_madurez():
    st.subheader("Evaluación rápida de madurez SGSI (ENS / ISO 27001 / NIST / NIS2)")

    evidencias_text = st.text_area(
        "Evidencias disponibles",
        placeholder="Auditorías, KPIs, análisis de vulnerabilidades, etc."
    )
    controles_text = st.text_area(
        "Controles implementados",
        placeholder="RBAC, MFA, SIEM 24x7, cifrado, etc."
    )

    if st.button("Calcular madurez SGSI con Ellit Cognitive Core"):
        if not evidencias_text.strip() and not controles_text.strip():
            st.warning("Introduce al menos evidencias o controles.")
            return

        try:
            with st.spinner("Calculando madurez..."):
                sgsi_result = compute_sgsi_maturity(client, evidencias_text, controles_text)
        except Exception as e:
            st.error(f"Error: {e}")
            return

        if not sgsi_result:
            st.error("No se pudo interpretar la respuesta.")
            return

        madurez_val = sgsi_result.get("madurez", 0)
        nivel_val = sgsi_result.get("nivel", "No determinado")

        st.markdown(f"### Nivel de madurez: {nivel_val} ({madurez_val}%)")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Fortalezas**")
            for f in sgsi_result.get("fortalezas", []):
                st.markdown(f"- {f}")

        with c2:
            st.markdown("**Debilidades**")
            for d in sgsi_result.get("debilidades", []):
                st.markdown(f"- {d}")

        acciones = sgsi_result.get("acciones_requeridas", [])
        if acciones:
            st.markdown("### Acciones prioritarias")
            for a in acciones:
                st.markdown(f"- {a}")

# ============================================================
#  RADAR IA — BLOQUE 5: Informe PDF
# ============================================================

def render_radar_pdf():
    st.markdown("### Generar informe PDF del Radar IA")

    radar_data = st.session_state.get("radar_data", None)
    profile = st.session_state.get("radar_profile", {})

    if not radar_data:
        st.warning("Primero ejecuta el análisis del Radar IA.")
        return

    estilo = st.selectbox("Estilo del informe PDF", ["Clásico", "Corporativo", "Ellit"], index=2)

    if st.button("Generar informe PDF"):
        resumen = radar_data.get("analisis", "")
        indicadores = radar_data.get("indicadores", {})

        partes = [
            f"Informe Radar IA — {profile.get('organizacion','')}",
            "",
            f"Sector: {profile.get('sector','')}",
            f"Nivel ENS actual: {profile.get('nivel_ens','')}",
            f"Tamaño: {profile.get('tamano','')}",
            f"Región: {profile.get('region','')}",
            "",
            "Resumen ejecutivo:",
            resumen,
            "",
            "Indicadores clave:"
        ]

        for k, v in indicadores.items():
            partes.append(f"- {k}: {v}%")

        content = "\n".join(partes)
        pdf_name = f"RadarIA_Report_{profile.get('organizacion','').replace(' ', '_')}.pdf"
        download_pdf_button("Informe Radar IA", profile.get('organizacion',''), content, pdf_name)

# ============================================================
#  RADAR IA — BLOQUE 6: Selección inteligente de normativa (NUEVO)
# ============================================================

def render_radar_normativa_inteligente():
    st.markdown("""
    <div style="background: linear-gradient(135deg,#FF0080 0%,#00B4FF 100%);
                padding:22px; border-radius:14px; color:white; text-align:center;
                margin-bottom:25px;">
        <h3 style="margin:0; font-weight:700;">Selección inteligente de normativa</h3>
        <p style="margin:4px 0 0; opacity:0.9;">Ellit Cognitive Core</p>
    </div>
    """, unsafe_allow_html=True)

    radar_data = st.session_state.get("radar_data", {})
    perfil = st.session_state.get("radar_profile", {})

    st.markdown("### Evidencias y controles disponibles")
    evidencias = st.text_area("Evidencias documentales")
    controles = st.text_area("Controles implementados")

    if st.button("Ejecutar análisis inteligente con Ellit Cognitive Core"):
        payload = {
            "perfil": perfil,
            "radar": radar_data,
            "evidencias": evidencias,
            "controles": controles
        }

        try:
            result = analyze_normativa_inteligente(client, payload)
            st.session_state["normativa_inteligente"] = result
            st.success("Análisis completado.")
        except Exception as e:
            st.error(f"Error: {e}")
            return

    result = st.session_state.get("normativa_inteligente", None)
    if not result:
        return

    st.markdown("### Normativa principal sugerida")
    st.success(result.get("normativa_principal","No disponible"))

    st.markdown("### Normativas secundarias")
    for n in result.get("normativas_secundarias",[]):
        st.markdown(f"- {n}")

    st.markdown("### Roadmap 3 / 6 / 12 meses")
    roadmap = result.get("roadmap",{})
    for fase, tareas in roadmap.items():
        with st.expander(fase):
            for t in tareas:
                st.markdown(f"- {t}")
