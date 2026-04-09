# --- (Mantén todo el código anterior igual hasta la sección 7) ---

if opcion == "📊 Tablero de Control":
    st.write("---")
    # ... (Tus métricas/KPIs se mantienen igual) ...

    st.markdown("### 📋 Gestión de Cartera y Cobranza")

    # 1. Definimos la función de colores
    def color_estado(val):
        if val == "VENCIDO":
            return 'background-color: #701010; color: white' # Rojo oscuro profesional
        elif val == "AL DÍA":
            return 'background-color: #155123; color: white' # Verde oscuro profesional
        return ''

    # 2. Aplicamos el estilo al DataFrame
    # Aplicamos el color solo a la columna 'Estado' o a toda la fila
    df_estilado = df.style.applymap(color_estado, subset=['Estado'])

    # 3. Mostramos la tabla con el estilo aplicado
    st.dataframe(
        df_estilado, 
        use_container_width=True, 
        hide_index=True,
        column_config={
            "Acción": st.column_config.LinkColumn(
                "Enviar WhatsApp",
                display_text="📲 Enviar Mensaje"
            ),
            "Saldo (USD)": st.column_config.NumberColumn(format="$ %d")
        }
    )
    
    st.info("💡 Los colores permiten identificar rápidamente el estado de cada cliente.")
