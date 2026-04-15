import streamlit as st
import pandas as pd
import urllib.parse
from fpdf import FPDF
from datetime import datetime
import PIL.Image as Image

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="CRM SENNA 2026", layout="wide", initial_sidebar_state="expanded")

# 2. SESIÓN
if "logueado" not in st.session_state:
    st.session_state["logueado"] = False

# --- PANTALLA DE LOGIN ---
if not st.session_state["logueado"]:
    st.markdown("<style>.stApp { background-color: #0E1117; color: white; }</style>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.write("#")
        st.markdown("<h1 style='text-align: center; color: #55acee;'>🏎️ CRM SENNA 2026</h1>", unsafe_allow_html=True)
        with st.form("login"):
            u = st.text_input("Usuario")
            p = st.text_input("Contraseña", type="password")
            if st.form_submit_button("INGRESAR"):
                if u == "Leo" and p == "Senna2026":
                    st.session_state["logueado"] = True
                    st.rerun()
                else: st.error("Acceso Denegado")

# --- SISTEMA ACTIVO ---
else:
    # Datos (Aseguramos nombres de columnas para el mapa)
    @st.cache_data
    def cargar_datos():
        data = {
            "Cliente": ["Federico Rossi", "María Gonzalez", "Juan Castro", "Ana Ledesma", "Roberto Peña"],
            "Vehículo": ["Mercedes Benz A200", "Toyota Hilux", "VW Gol Trend", "Fiat Cronos", "Ford Ranger"],
            "Vencimiento": ["2026-03-30", "2026-04-10", "2026-04-15", "2026-03-25", "2026-05-01"],
            "Estado": ["VENCIDO", "AL DÍA", "AL DÍA", "VENCIDO", "AL DÍA"],
            "Saldo (USD)": [450, 0, 0, 320, 0],
            "latitude": [-32.31, -32.32, -32.30, -32.33, -32.31],
            "longitude": [-58.08, -58.07, -58.09, -58.08, -58.10]
        }
        df = pd.DataFrame(data)
        def link_wa(fila):
            msg = f"CRM Senna Informa: {fila['Cliente']}, cuota {fila['Vehículo']} {fila['Estado']}. Saldo: ${fila['Saldo (USD)']}. Saludos."
            return f"https://wa.me/59899000000?text={urllib.parse.quote(msg)}"
        df["WhatsApp"] = df.apply(link_wa, axis=1)
        return df

    df = cargar_datos()

    # Barra Lateral
    with st.sidebar:
        st.title("SENNA")
        st.markdown("### 🛠️ MENÚ PRINCIPAL")
        opcion = st.radio("Módulos:", ["📊 Tablero", "💰 Cobros", "🔍 Buscador", "📄 Documentos", "📍 Mapa"])
        if st.button("🚪 Cerrar Sesión"):
            st.session_state["logueado"] = False
            st.rerun()

    # Cabecera
    st.markdown(f"<h1 style='text-align: center;'>CRM SENNA - {opcion.upper()}</h1>", unsafe_allow_html=True)
    st.write("---")

    if opcion == "📊 Tablero":
        c1, c2, c3 = st.columns(3)
        c1.metric("EN MORA", "5 Clientes", "USD 2.210")
        c2.metric("A COBRAR", "4 Clientes", "USD 1.850")
        c3.metric("TOTAL", "20 Registros", "USD 15.400")
        st.subheader("📈 Flujo Semanal")
        st.line_chart({"Ventas": [10, 20, 15, 25], "Cobros": [5, 12, 18, 22]})

    elif opcion == "💰 Cobros":
        def color_estado(val):
            if val == "VENCIDO": return 'background-color: #701010; color: white'
            return 'background-color: #155123; color: white'
        st.dataframe(df.style.map(color_estado, subset=['Estado']), use_container_width=True, hide_index=True)

    elif opcion == "🔍 Buscador":
        busq = st.text_input("Buscar cliente...")
        if busq:
            res = df[df['Cliente'].str.contains(busq, case=False)]
            for _, r in res.iterrows():
                with st.expander(f"👤 {r['Cliente']}"):
                    st.write(f"**Auto:** {r['Vehículo']} | **Saldo:** ${r['Saldo (USD)']}")
                    st.markdown(f"[📲 Enviar WhatsApp]({r['WhatsApp']})")

    elif opcion == "📄 Documentos":
        c = st.selectbox("Cliente:", df["Cliente"])
        if st.button("Generar Recibo"):
            st.success(f"Recibo generado para {c}")

    elif opcion == "📍 Mapa":
        # Mapa arreglado con columnas correctas
        st.map(df[["latitude", "longitude"]], color="#ff4b4b", size=40)
        st.info("📍 Ubicación de deudores en Paysandú")
