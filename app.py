import streamlit as st
import pandas as pd
import urllib.parse

# 1. Configuración de la página
st.set_page_config(page_title="Control & Gestión de Cartera | Otormín", layout="wide")

# 2. CSS Maestro para Modo Oscuro y Estética
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
        /* Estilo para las fichas del buscador */
        .ficha-cliente {
            background-color: #1E2329;
            padding: 15px;
            border-radius: 10px;
            border-left: 5px solid #55acee;
            margin-bottom: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# 3. Datos de la Automotora (20 Registros)
@st.cache_data
def cargar_datos():
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
    
    # Generar links de WhatsApp
    def link_wa(fila):
        msg = f"Hola {fila['Cliente']}, le recordamos que su cuota del {fila['Vehículo']} vence el {fila['Vencimiento']}. Saludos de Automotora Otormín."
        return f"https://wa.me/59899000000?text={urllib.parse.quote(msg)}"
    
    df["Acción"] = df.apply(link_wa, axis=1)
    return df

df = cargar_datos()

# 4. Sidebar (Menú)
with st.sidebar:
    st.markdown("### MENÚ")
    opcion = st.radio("Navegación:", ["📊 Tablero de Control", "🔍 Buscador Inteligente", "➕ Nuevo Registro"])
    st.write("---")
    st.markdown("<p style='color: #55acee; font-size: 0.8rem;'>Sistema v1.1 | 2026 © Automotora Otormín</p>", unsafe_allow_html=True)

# 5. Logo y Título
col1, col2, col3 = st.columns([1, 1.5, 1])
with col2:
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.warning("⚠️ Logo no encontrado. Sube 'logo.png' a GitHub.")
    st.markdown('<div class="titulo-central">CONTROL & GESTIÓN DE CARTERA</div>', unsafe_allow_html=True)

# 6. Lógica de Secciones
if opcion == "📊 Tablero de Control":
    st.write("---")
    c1, c2, c3 = st.columns(3)
    c1.metric("EN MORA", "5 Clientes", "-$2,210", delta_color="inverse")
    c2.metric("A COBRAR (7 DÍAS)", "4 Clientes", "$1,850")
    c3.metric("TOTAL CARTERA", "20 Registros", "$15,400")

    st.markdown("### 📋 Listado General")
    
    def color_estado(val):
        if val == "VENCIDO": return 'background-color: #701010; color: white'
        if val == "AL DÍA": return 'background-color: #155123; color: white'
        return ''

    st.dataframe(
        df.style.map(color_estado, subset=['Estado']), 
        use_container_width=True, 
        hide_index=True,
        column_config={
            "Acción": st.column_config.LinkColumn("WhatsApp", display_text="📲 Enviar"),
            "Saldo (USD)": st.column_config.NumberColumn(format="$ %d")
        }
    )

elif opcion == "🔍 Buscador Inteligente":
    st.write("---")
    st.markdown("### 🔍 Buscador de Clientes")
    busqueda = st.text_input("Buscar por nombre o vehículo...", placeholder="Ej: Federico")

    if busqueda:
        res = df[df['Cliente'].str.contains(busqueda, case=False) | df['Vehículo'].str.contains(busqueda, case=False)]
        if not res.empty:
            for i, row in res.iterrows():
                with st.container():
                    st.markdown(f"""
                    <div class="ficha-cliente">
                        <h4>{row['Cliente']}</h4>
                        <p>🚗 <b>Vehículo:</b> {row['Vehículo']} | 📅 <b>Vencimiento:</b> {row['Vencimiento']}</p>
                        <p>💰 <b>Saldo:</b> ${row['Saldo (USD)']} | <b>Estado:</b> {row['Estado']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.link_button(f"📲 Notificar a {row['Cliente']}", row['Acción'])
        else:
            st.warning("No hay resultados.")
    else:
        st.info("Ingresa un nombre para buscar.")
        st.bar_chart(df['Estado'].value_counts())

elif opcion == "➕ Nuevo Registro":
    st.write("---")
    st.subheader("➕ Cargar Nuevo Cliente")
    with st.form("nuevo_cliente"):
        nombre = st.text_input("Nombre Completo")
        auto = st.text_input("Vehículo")
        vence = st.date_input("Fecha de Vencimiento")
        if st.form_submit_button("Guardar Registro"):
            st.success(f"Registro de {nombre} guardado correctamente (Simulación).")
