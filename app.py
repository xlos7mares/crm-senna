elif opcion == "📍 Mapa de Cartera":
        st.subheader("📍 Geolocalización de Deudores (Paysandú)")
        
        # Preparamos una copia de los datos específica para el mapa
        df_mapa = df.copy()
        
        # Renombramos las columnas correctamente antes de pasarlas al mapa
        df_mapa = df_mapa.rename(columns={'lat': 'latitude', 'lon': 'longitude'})
        
        # Verificamos que no haya valores vacíos que rompan el mapa
        df_mapa = df_mapa.dropna(subset=['latitude', 'longitude'])
        
        # Mostramos el mapa con un color que resalte (Rojo Senna)
        st.map(df_mapa, color="#ff4b4b", size=40)
        
        st.info("💡 Los puntos indican la ubicación aproximada de los clientes en cartera.")
