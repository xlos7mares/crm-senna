elif opcion == "📍 Mapa de Cartera":
    st.title("🗺️ Mapa de Cobranza en Paysandú")
    st.write("Visualiza la ubicación de tus activos y deudores.")
    
    # Preparamos los datos para que el mapa los entienda (renombrar columnas)
    df_mapa = df.copy()
    df_mapa = df_mapa.rename(columns={'Lat': 'latitude', 'Lon': 'longitude'})
    
    # Creamos una columna de color: Rojo para Vencidos, Azul para Al Día
    df_mapa["color"] = df_mapa["Estado"].apply(lambda x: "#FF0000" if x == "VENCIDO" else "#0000FF")
    
    # Mostramos el mapa con los colores personalizados
    st.map(df_mapa, color="color", size=40)
    
    st.write("---")
    st.markdown("""
    **Leyenda del Mapa:**
    * 🔴 **Punto Rojo:** Cliente con deuda vencida.
    * 🔵 **Punto Azul:** Cliente al día.
    """)
