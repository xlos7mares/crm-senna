elif "Buscador" in opcion:
    st.write("---")
    st.markdown("### 🔍 Buscador Inteligente de Clientes")
    
    # 1. Barra de búsqueda superior
    busqueda = st.text_input("Escribe el nombre del cliente o el modelo del vehículo...", placeholder="Ej: Federico o Toyota")

    if busqueda:
        # Filtramos los datos
        resultados = df[
            df['Cliente'].str.contains(busqueda, case=False) | 
            df['Vehículo'].str.contains(busqueda, case=False)
        ]

        if not resultados.empty:
            st.success(f"Se encontraron {len(resultados)} coincidencias:")
            
            # 2. Mostramos los resultados en columnas para que parezcan "Fichas"
            for i, row in resultados.iterrows():
                with st.container():
                    col_a, col_b, col_c = st.columns([2, 2, 1])
                    with col_a:
                        st.markdown(f"**👤 Cliente:** {row['Cliente']}")
                        st.markdown(f"**🚗 Vehículo:** {row['Vehículo']}")
                    with col_b:
                        st.markdown(f"**📅 Vencimiento:** {row['Vencimiento']}")
                        # Color dinámico para el estado en el buscador
                        color = "🔴" if row['Estado'] == "VENCIDO" else "🟢"
                        st.markdown(f"**{color} Estado:** {row['Estado']}")
                    with col_c:
                        # Botón de acción directo desde el buscador
                        st.link_button("📲 Notificar", row['Acción'])
                    st.write("---")
        else:
            st.warning("No se encontraron clientes con ese nombre o vehículo.")
    else:
        # Mensaje cuando la barra está vacía
        st.info("Ingresa un dato arriba para buscar en la base de datos de la automotora.")
        
        # Opcional: Mostrar un gráfico rápido para que no se vea vacío
        st.markdown("#### 📊 Resumen de Cartera")
        conteo_estados = df['Estado'].value_counts()
        st.bar_chart(conteo_estados)
