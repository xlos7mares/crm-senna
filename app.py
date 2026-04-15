import streamlit as st
import pandas as pd
import urllib.parse
from fpdf import FPDF
from datetime import datetime
import PIL.Image as Image

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="CRM SENNA 2026",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. ESTADO DE SESIÓN
if "logueado" not in st.session_state:
    st.session_state["logueado"] = False

# --- ESTILOS VISUALES (Basados en tus capturas) ---
st.markdown("""
    <style>
        .stApp { background-color: #0E1117; color: white; }
        [data-testid="stSidebar"] { background-color: #161B22; min-width: 260px !important; }
        .card {
            background-color: #1E2329;
            padding: 20px;
            border-radius: 10px;
            border-top: 4px solid #55acee;
            text-align: center;
            margin-bottom: 20px;
        }
        .titulo-central {
            text-align: center;
            font-size: 2.2rem;
            font-weight: bold;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# 3. PANTALLA DE LOGIN
if not st.session_state["logueado"]:
    _, col_centro, _ = st.columns([1, 1.5, 1])
    with col_centro:
        st.write("#")
        st.markdown("<h1 style='text-align: center; color: #55acee;'>🏎️ CRM SENNA 2026</h1>", unsafe_allow_html=True)
        with st.form("login_form"):
            user = st.text_input("Usuario")
            password = st.text_input("Contraseña", type="password")
            if st.form_submit_button("INGRESAR"):
                if user == "Leo" and password == "Senna2026":
                    st.session_state["logueado"] = True
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas")

# 4. SISTEMA COMPLETO (Solo si está logueado)
else:
    # --- BARRA LATERAL (Sidebar) ---
    # Colocamos el menú aquí para forzar que aparezca siempre
    with st.sidebar:
        try:
            st.image("logo.png", use_container_width=True)
        except:
            st.markdown("<h2 style='color:#55acee; text-align:center;'>SENNA</h2>", unsafe_allow_html=True)
        
        st.markdown("### 🛠️ MENÚ PRINCIPAL")
        opcion = st.radio("Módulos del Sistema:", [
            "📊 Tablero de Control", 
            "💰 Gestión de Cobros", 
            "🔍 Buscador Inteligente",
            "📄 Documentos y PDF",
            "📍 Mapa de Cartera"
        ])
        st.write("---")
        if st.button("🚪 Cerrar Sesión"):
            st.session_state["logueado"] = False
            st.rerun()
        st.info("Conectado como: Leo")

    # --- CONTENIDO CENTRAL ---
    st.markdown('<div class="titulo-central">CRM SENNA 2026</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8899A6;'>Sistema de Gestión Automotriz Profesional</p>", unsafe_allow_html=True)
    st.write("---")

    # Datos demo para que la tabla no esté vacía
    data = {
        "Cliente": ["Federico Rossi", "María Gonzalez", "Juan Castro", "Ana Ledesma", "Roberto Peña"],
        "Vehículo": ["Mercedes Benz A200", "Toyota Hilux", "VW Gol Trend", "Fiat Cronos", "Ford Ranger"],
        "Vencimiento": ["2026-03-30", "2026-04-10", "2026-04-15", "2026-03-25", "2026-05-01"],
        "Estado": ["VENCIDO", "AL DÍA", "AL DÍA", "VENCIDO", "AL DÍA"],
        "Saldo (USD)": [450, 0, 0, 320, 0]
    }
    df = pd.DataFrame(data)

    if opcion == "📊 Tablero de Control":
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown('<div class="card"><h3 style="color:#8899A6">EN MORA</h3><h2 style="color:#ff4b4b">5</h2><p>USD 2.210</p></div>', unsafe_allow_html=True)
        with c2: st.markdown('<div class="card"><h3 style="color:#8899A6">A COBRAR</h3><h2 style="color:#55acee">4</h2><p>USD 1.850</p></div>', unsafe_allow_html=True)
        with c3: st.markdown('<div class="card"><h3 style="color:#8899A6">TOTAL CARTERA</h3><h2>20</h2><p>USD 15.400</p></div>', unsafe_allow_html=True)
        st.subheader("📈 Rendimiento Semanal")
        st.line_chart({"Cobros": [10, 25, 15, 30]})

    elif opcion == "💰 Gestión de Cobros":
        st.markdown("### 📋 Cartera de Clientes")
        def color_estado(val):
            if val == "VENCIDO": return 'background-color: #701010; color: white'
            if val == "AL DÍA": return 'background-color: #155123; color: white'
            return ''
        
        st.dataframe(
            df.style.map(color_estado, subset=['Estado']),
            use_container_width=True, hide_index=True
        )

    elif opcion == "📍 Mapa de Cartera":
        st.markdown("### 📍 Ubicación de Clientes (Paysandú)")
        map_data = pd.DataFrame({
            'lat': [-32.31, -32.32, -32.30],
            'lon': [-58.08, -58.07, -58.09]
        })
        st.map(map_data)
