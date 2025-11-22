def render_radar_normativa_inteligente():
    st.markdown("""
    <div style="background: linear-gradient(135deg,#FF0080 0%,#00B4FF 100%);
                padding:22px; border-radius:14px; color:white; text-align:center;
                margin-bottom:25px;">
        <h3 style="margin:0; font-weight:700;">Selección inteligente de normativa</h3>
        <p style="margin:4px 0 0; opacity:0.9;">Ellit Cognitive Core — Detección automática basada en riesgo, contexto y madurez</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Datos analizados por el Cognitive Core")
    st.info("""
El sistema analizará automáticamente:
- Sector  
- País o región  
- Tamaño de la organización  
- Nivel ENS declarado  
- Riesgos detectados  
- Certificaciones existentes  
- Evidencias disponibles  
- Controles implementados  
- KPIs históricos del SGSI  
- Nivel de madurez previo del radar  
    """)

    # -----------------------------------------------------------
    # CAPTURA AUTOMÁTICA DE DATOS EXISTENTES DEL RADAR IA
    # -----------------------------------------------------------
    radar_data = st.session_state.get("radar_data", {})
    indicadores = radar_data.get("indicadores", {})
    analisis = radar_data.get("analisis", "")
    riesgos_detectados = radar_data.get("riesgos_detectados", "")
    certificaciones = radar_data.get("certificaciones", "")

    # Del perfil
    perfil = st.session_state.get("radar_profile", {})
    nombre_org = perfil.get("organizacion", "Organización")
    sector = perfil.get("sector", "")
    tamano = perfil.get("tamano", "")
    region = perfil.get("region", "")
    nivel_ens = perfil.get("nivel_ens", "")

    # Del módulo SGSI futuro
    kpi_sgsi = st.session_state.get("sgsi_kpis", {})

    # Inputs adicionales
    st.markdown("### Evidencias y controles disponibles")
    evidencias = st.text_area(
        "Evidencias documentales (auditorías, KPIs, revisiones, hallazgos)",
        placeholder="Ejemplo: Informe auditoría interna, revisión de accesos, pruebas de bastionado, hallazgos priorizados..."
    )
    controles = st.text_area(
        "Controles técnicos y organizativos aplicados",
        placeholder="Ejemplo: RBAC, SIEM 24x7, MFA obligatorio, cifrado AES-256, gestión de vulnerabilidades..."
    )

    if st.button("Ejecutar análisis inteligente con Ellit Cognitive Core"):
        with st.spinner("Analizando contexto normativo y obligaciones aplicables..."):

            payload = {
                "organizacion": nombre_org,
                "sector": sector,
                "region": region,
                "tamano": tamano,
                "nivel_ens": nivel_ens,
                "indicadores": indicadores,
                "riesgos_detectados": riesgos_detectados,
                "certificaciones": certificaciones,
                "evidencias": evidencias,
                "controles": controles,
                "kpi_sgsi": kpi_sgsi,
                "analisis": analisis
            }

            try:
                result = analyze_normativa_inteligente(client, payload)
                st.session_state["normativa_inteligente"] = result
                st.success("Análisis completado correctamente.")
            except Exception as e:
                st.error(f"Error en el análisis: {e}")
                return

    result = st.session_state.get("normativa_inteligente", None)
    if not result:
        return

    # -----------------------------------------------------------
    # RESULTADOS
    # -----------------------------------------------------------
    st.markdown("---")
    st.markdown("## Normativa principal aplicable")

    principal = result.get("normativa_principal", "")
    if principal:
        st.success(f"Normativa principal sugerida por el Cognitive Core: **{principal}**")

    st.markdown("### Normativas secundarias aplicables")
    for n in result.get("normativas_secundarias", []):
        st.markdown(f"- {n}")

    st.markdown("### Nivel de obligatoriedad")
    st.info(result.get("obligatoriedad", "No determinado"))

    # -----------------------------------------------------------
    # CUMPLIMIENTO Y DESVIACIONES
    # -----------------------------------------------------------
    st.markdown("## Mapa de cumplimiento inicial")
    mapa = result.get("mapa_cumplimiento", {})

    if mapa:
        df = pd.DataFrame([
            {"Control": k, "Cumplimiento (%)": v}
            for k, v in mapa.items()
        ])
        fig, ax = plt.subplots(figsize=(6, 3))
        bars = ax.bar(df["Control"], df["Cumplimiento (%)"], color="#00B4FF")
        ax.set_ylim(0, 100)
        ax.set_ylabel("Cumplimiento (%)")
        plt.xticks(rotation=45, ha="right")
        st.pyplot(fig)

    desviaciones = result.get("desviaciones", [])
    if desviaciones:
        st.markdown("### Desviaciones críticas detectadas")
        for d in desviaciones:
            st.error(f"- {d}")

    # -----------------------------------------------------------
    # ROADMAP
    # -----------------------------------------------------------
    st.markdown("## Roadmap de cumplimiento — 3 / 6 / 12 meses")

    roadmap = result.get("roadmap", {})
    for fase, tareas in roadmap.items():
        with st.expander(fase):
            for t in tareas:
                st.markdown(f"- {t}")

    # -----------------------------------------------------------
    # RECOMENDACIONES
    # -----------------------------------------------------------
    st.markdown("## Recomendaciones estratégicas")
    for r in result.get("recomendaciones", []):
        st.markdown(f"- {r}")
