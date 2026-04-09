import streamlit as st
import pandas as pd

# 1. Configuración de la página
st.set_page_config(page_title="Control & Gestión de Cartera", layout="wide")

# 2. CSS Maestro (Modo Oscuro y Textos Blancos)
st.markdown(
    """
    <style>
        .stApp { background-color: #0E1117; color: white; }
        [data-testid="stSidebar"] { background-color: #161B22; }
        [data-testid="stSidebar"] * { color: white !important; }
        .titulo-central {
            text-align: center;
            color: white;
            font-size: 2.2rem;
            font-weight: bold;
            margin-top: -20px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# 3. Datos de Ejemplo (20 Clientes)
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
    "Saldo (USD)": [450, 0, 0, 320, 0, 0, 280, 0, 0, 0, 550, 0, 0, 0, 0, 0, 610, 0, 0, 0]
}
df = pd.DataFrame(data)

# 4. Sidebar (AQUÍ SE DEFINE 'opcion')
with st.sidebar:
    st.markdown("### MENÚ")
    # Es muy importante que esta variable se llame EXACTAMENTE 'opcion'
    opcion = st.radio(
        "Navegación:",
        ["📊 Tablero de Control", "🔍 Buscador Inteligente", "➕ Nuevo Registro"],
        index=0
    )
    st.write("---")
    st.markdown("<p style='color: #55acee; font-size: 0.8rem;'>Sistema v1.1 | 2026 © Automotora Otormín</p>", unsafe_allow_html=True)

# 5. Encabezado Principal
col1, col2, col3 = st.columns([1, 1.5, 1])
with col2:
    try:
        st.image("logo.png", use_container_width=True)
    except:
        pass
    st.markdown('<div class="titulo-central">CONTROL & GESTIÓN DE CARTERA</div>', unsafe_allow_html=True)

# 6. Lógica de Secciones
if opcion == "📊 Tablero de Control":
    st.write("---")
    # Indicadores
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("EN MORA", "5 Clientes", "-$2,210", delta_color="inverse")
    with c2: st.metric("A COBRAR (7 DÍAS)", "4 Clientes", "$1,850")
    with c3: st.metric("TOTAL CARTERA", "20 Registros", "$15,400")

    # Alertas
    st.markdown("### ⚠️ Acciones de Cobranza Prioritaria")
    vencidos = df[df["Estado"] == "VENCIDO"]
    for _, row in vencidos.iterrows():
        st.error(f"**VENCIDO** | {row['Cliente']} - {row['Vehículo']} (Vence: {row['Vencimiento']})")

    # Tabla Completa
    st.write("---")
    st.markdown("### 📋 Listado Completo de Cartera")
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.download_button("📥 Descargar Reporte Excel", data=df.to_csv().encode('utf-8'), file_name='cartera.csv')

elif opcion == "🔍 Buscador Inteligente":
    st.subheader("Buscador de Clientes")
    # Aquí puedes agregar más lógica luego

elif opcion == "➕ Nuevo Registro":
    st.subheader("Cargar Nuevo Cliente")
    # Aquí puedes agregar el formulario luego
