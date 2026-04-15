import streamlit as st
import pandas as pd
import urllib.parse
from fpdf import FPDF
from datetime import datetime
import PIL.Image as Image

# 1. Configuración de la página
st.set_page_config(page_title="AutoGestion Pro URU v2.1", layout="wide")

# 2. Función de Seguridad (Login)
def check_password():
    """Retorna True si el usuario ingresó la contraseña correcta."""
    def password_entered():
        if st.session_state["username"] == "admin" and st.session_state["password"] == "paga2026":
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # No guardar la contraseña
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # Pantalla de Bienvenida y Login
        st.markdown("<h1 style='text-align: center;'>AutoGestion Pro URU</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Sistema de Gestión Automotriz Profesional</p>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.text_input("Usuario", key="username")
            st.text_input("Contraseña", type="password", key="password")
            st.button("Entrar al Sistema", on_click=password_entered)
        if "password_correct" in st.session_state and not st.session_state["password_correct"]:
            st.error("😕 Usuario o contraseña incorrectos")
        return False
    else:
        return st.session_state["password_correct"]

# 3. Solo ejecutamos el resto si el login es exitoso
if check_password():

    # Estética Profesional (Modo Oscuro SaaS)
    st.markdown("""
        <style>
            .stApp { background-color: #0E1117; color: white; }
            [data-testid="stSidebar"] { background-color: #161B22; }
            [data-testid="stSidebar"] * { color: white !important; }
            .card {
                background-color: #1E2329;
                padding: 15px;
                border-radius: 10px;
                border-top: 4px solid #55acee;
                text-align: center;
                margin-bottom: 10px;
            }
            .titulo-central {
                text-align: center;
                color: white;
                font-size: 2.2rem;
                font-weight: bold;
                margin-top: -20px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Cargar Datos (Simulados para Demo)
    @st.cache_data
    def cargar_datos():
        data = {
            "Cliente": ["Federico Rossi", "María Gonzalez", "Juan Castro", "Ana Ledesma", "Roberto Peña"],
            "Vehículo": ["Mercedes Benz A200", "Toyota Hilux", "VW Gol Trend", "Fiat Cronos", "Ford Ranger"],
            "Vencimiento": ["2026-03-30", "2026-04-10", "2026-04-15", "2026-03-25", "2026-05-01"],
            "Estado": ["VENCIDO", "AL DÍA", "AL DÍA", "VENCIDO", "AL DÍA"],
            "Cuota (USD)": [450, 600, 300, 320, 800],
            "Score": [2, 5, 4, 1, 5],
            "latitude": [-32.31, -32.32, -32.30, -32.33, -32.31],
            "longitude": [-58.08, -58.07, -58.09, -58.08, -58.10]
        }
        df = pd.DataFrame(data)
        df["Mora"] = df.apply(lambda x: round(x["Cuota (USD)"] * 0.02, 2) if x["Estado"] == "VENCIDO" else 0, axis=1)
        df["Total"] = df["Cuota (USD)"] + df["Mora"]
        
        def link_wa(fila):
            msg = f"Gestión Automotriz: Estimado {fila['Cliente']}, recordamos que su cuota del {fila['Vehículo']} está {fila['Estado']}. Total: ${fila['Total']}."
            return f"https://wa.me/59899000000?text={urllib.parse.quote(msg)}"
        
        df["WhatsApp"] = df.apply(link_wa, axis=1)
        return df

    df = cargar_datos()

    # Sidebar
    with st.sidebar:
        try:
            logo = Image.open("logo.png")
            st.image(logo, use_container_width=True)
        except:
            st.info("AutoGestion Pro URU")
        
        opcion = st.radio("Navegación:", [
            "📊 Inteligencia de Negocio", 
            "💰 Gestión de Cobros", 
            "🔍 Buscador",
            "📄 Contratos & Simulador",
            "📍 Mapa de Cartera"
        ])
        if st.button("Cerrar Sesión"):
            del st.session_state["password_correct"]
            st.rerun()

    st.markdown('<div class="titulo-central">GESTIÓN INTELIGENTE AUTOMOTRIZ</div>', unsafe_allow_html=True)

    # Módulos (Exactamente como antes, sin cambios en funcionalidad)
    if opcion == "📊 Inteligencia de Negocio":
        st.write("---")
        c1, c2, c3 = st.columns(3)
        c1.markdown('<div class="card"><h3>Efectividad</h3><h2 style="color:#00ff00">84%</h2></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="card"><h3>Mora Ganada</h3><h2 style="color:#55acee">${df["Mora"].sum()}</h2></div>', unsafe_allow_html=True)
        c3.markdown('<div class="card"><h3>Riesgo</h3><h2 style="color:#ff4b4b">BAJO</h2></div>', unsafe_allow_html=True)
        st.line_chart({"Ventas": [10, 15, 8, 22], "Cobros": [12, 11, 14, 18]})

    elif opcion == "💰 Gestión de Cobros":
        st.title("💸 Control de Cobranza")
        def color_estado(val):
            if val == "VENCIDO": return 'background-color: #701010;'
            return 'background-color: #155123;'
        st.dataframe(df.style.map(color_estado, subset=['Estado']), use_container_width=True, hide_index=True)

    elif opcion == "🔍 Buscador":
        st.title("🔍 Archivo de Clientes")
        search = st.text_input("Buscar...")
        if search:
            res = df[df["Cliente"].str.contains(search, case=False)]
            st.write(res)

    elif opcion == "📄 Contratos & Simulador":
        st.title("📄 Herramientas")
        tab1, tab2 = st.tabs(["PDF", "Simulador"])
        with tab1:
            st.write("Seleccione cliente para generar recibo PDF.")
            st.selectbox("Cliente", df["Cliente"])
            st.button("Descargar PDF (Demo)")
        with tab2:
            monto = st.number_input("Monto USD", value=1000)
            st.write(f"Cuota sugerida (3 meses): USD {round(monto*1.1/3, 2)}")

    elif opcion == "📍 Mapa de Cartera":
        st.title("🗺️ Mapa Paysandú")
        df_map = df.rename(columns={'latitude': 'lat', 'longitude': 'lon'})
        st.map(df_map)
