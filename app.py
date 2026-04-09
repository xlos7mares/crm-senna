import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- (Mantén tu configuración de página y CSS anterior aquí) ---

# 1. Simulación de Datos (20 Clientes)
data = {
    "Cliente": [
        "Federico Rossi", "María Gonzalez", "Juan Castro", "Ana Ledesma", "Roberto Peña",
        "Lucía Méndez", "Carlos Paez", "Elena Solari", "Diego Lugano", "Sonia Britos",
        "Martín Sosa", "Valentina Ríos", "Jorge Blanco", "Carmen Díaz", "Raúl Martínez",
        "Patricia Sosa", "Gabriel Vera", "Natalia Luna", "Oscar Duarte", "Silvia Pereyra"
    ],
    "Vehículo": [
        "Mercedes Benz A200", "Toyota Hilux", "VW Gol Trend", "Fiat Cronos", "Ford Ranger",
        "Chevrolet Onix", "Hyundai HB20", "Peugeot 208", "Suzuki Vitara", "Renault Kwid",
        "Honda Civic", "Nissan Frontier", "Jeep Renegade", "BMW 320i", "Ford Ka",
        "Citroen C3", "VW Amarok", "Toyota Corolla", "Fiat Toro", "Chevrolet Cruze"
    ],
    "Cuota N°": [5, 10, 3, 12, 8, 2, 6, 1, 9, 4, 7, 11, 5, 3, 8, 10, 2, 6, 4, 12],
    "Vencimiento": [
        "2026-03-30", "2026-04-10", "2026-04-15", "2026-03-25", "2026-05-01",
        "2026-04-20", "2026-03-28", "2026-04-05", "2026-04-12", "2026-04-18",
        "2026-03-20", "2026-04-25", "2026-04-30", "2026-05-05", "2026-04-02",
        "2026-04-08", "2026-03-15", "2026-04-22", "2026-04-28", "2026-05-10"
    ],
    "Estado": [
        "VENCIDO", "AL DÍA", "AL DÍA", "VENCIDO", "AL DÍA",
        "AL DÍA", "VENCIDO", "AL DÍA", "AL DÍA", "AL DÍA",
        "VENCIDO", "AL DÍA", "AL DÍA", "AL DÍA", "AL DÍA",
        "AL DÍA", "VENCIDO", "AL DÍA", "AL DÍA", "AL DÍA"
    ],
    "Saldo Pendiente (USD)": [450, 0, 0, 320, 0, 0, 280, 0, 0, 0, 550, 0, 0, 0, 0, 0, 610, 0, 0, 0]
}

df = pd.DataFrame(data)

# --- (Aquí va la parte de Logo y Título que ya tienes) ---

# 2. Lógica del Tablero
if opcion == "📊 Tablero de Control":
    st.write("---")
    
    # KPIs Superiores
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("EN MORA", "5 Clientes", "-$2,210", delta_color="inverse")
    with c2:
        st.metric("A COBRAR (7 DÍAS)", "4 Clientes", "$1,850")
    with c3:
        st.metric("TOTAL CARTERA", "20 Registros", "$15,400")

    st.markdown("### ⚠️ Acciones de Cobranza Prioritaria")
    
    # Filtramos solo los vencidos para las alertas rápidas
    vencidos = df[df["Estado"] == "VENCIDO"]
    for _, row in vencidos.iterrows():
        st.error(f"**VENCIDO** | {row['Cliente']} - {row['Vehículo']} (Vence: {row['Vencimiento']}) - Saldo: ${row['Saldo Pendiente (USD)']}")

    st.write("---")
    st.markdown("### 📋 Listado Completo de Cartera")
    
    # Mostramos la tabla interactiva
    # Agregamos un buscador rápido arriba de la tabla
    busqueda = st.text_input("Filtrar por nombre o vehículo:", "")
    
    if busqueda:
        df_filtrado = df[df['Cliente'].str.contains(busqueda, case=False) | df['Vehículo'].str.contains(busqueda, case=False)]
    else:
        df_filtrado = df

    # Estilizar la tabla para que se vea bien en modo oscuro
    st.dataframe(
        df_filtrado, 
        use_container_width=True,
        hide_index=True,
        column_config={
            "Saldo Pendiente (USD)": st.column_config.NumberColumn(format="$ %d"),
            "Estado": st.column_config.TextColumn("Estado", help="Situación del pago")
        }
    )

    # Botón para descargar reporte (para que vea que es profesional)
    st.download_button(
        label="📥 Descargar Reporte Excel",
        data=df.to_csv().encode('utf-8'),
        file_name='cartera_otormin.csv',
        mime='text/csv',
    )
