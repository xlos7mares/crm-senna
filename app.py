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

# 2. INICIALIZACIÓN DEL ESTADO DE SESIÓN
if "logueado" not in st.session_state:
    st.session_state["logueado"] = False

# --- PANTALLA DE ACCESO (LOGIN) ---
if not st.session_state["logueado"]:
    st.markdown("<style>.stApp { background-color: #0E1117; color: white; }</style>", unsafe_allow_html=True)
    _, col_centro, _ = st.columns([1, 1.5, 1])
    with col_centro:
        st.write("#")
        try:
            logo_login = Image.open("logo.png")
            st.image(logo_login, use_container_width=True)
        except:
            st.markdown("<h1 style='text-align: center; color: #55acee;'>🏎️ CRM SENNA</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center;'>🔐 Acceso al Sistema</h2>", unsafe_allow_html=True)
        with st.form("login_form"):
            user = st.text_input("Usuario")
            password = st.text_input("Contraseña", type="password")
            if st.form_submit_button("INGRESAR"):
                if user == "Leo" and password == "Senna2026":
                    st.session_state["logueado"] = True
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas")

# --- PANTALLA PRINCIPAL (TODO EL CONTENIDO PROFESIONAL) ---
else:
    st.markdown("""
        <style>
            .stApp { background-color: #0E1117; color: white; }
            [data-testid="stSidebar"] { background-color: #161B22; }
            [data-testid="stSidebar"] * { color: white !important; }
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
                color: white;
                font-size: 2.2rem;
                font-weight: bold;
                margin-top: -20px;
            }
        </style>
    """, unsafe_allow_html=True)

    @st.cache_data
    def cargar_datos():
        data = {
            "Cliente": ["Federico Rossi", "María Gonzalez", "Juan Castro", "Ana Ledesma", "Roberto Peña"],
            "Vehículo": ["Mercedes Benz A200", "Toyota Hilux", "VW Gol Trend", "Fiat Cronos", "Ford Ranger"],
            "Vencimiento": ["2026-03-30", "2026-04-10", "2026-04-15", "2026-03-25", "2026-05-01"],
            "Estado": ["VENCIDO", "AL DÍA", "AL DÍA", "VENCIDO", "AL DÍA"],
            "Saldo (USD)": [450, 0, 0, 320, 0],
            "lat": [-32.31, -32.32, -32.30, -32.33, -32.31],
            "lon": [-58.08, -58.07, -58.09, -58.08, -58.10]
        }
        df = pd.DataFrame(data)
        def link_wa(fila):
            msg = f"CRM Senna Informa: {fila['Cliente']}, cuota {fila['Vehículo']} {fila['Estado']}. Saludos."
            return f"https://wa.me/59899000000?text={urllib.parse.quote(msg)}"
        df["Enviar Mensaje"] = df.apply(link_wa, axis=1)
        return df

    df = cargar_datos()

    with st.sidebar:
        try:
            st.image("logo.png", use_container_width=True)
        except: pass
        st.markdown("### MENÚ")
        opcion = st.radio("Navegación:", ["📊 Tablero de Control", "🔍 Buscador Inteligente", "➕ Nuevo Registro"])
        st.write("---")
        if st.button("🚪 Cerrar Sesión"):
            st.session_state["logueado"] = False
            st.rerun()

    st.markdown('<div class="titulo-central">CRM SENNA 2026</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8899A6;'>Control Total de Cartera Automotriz</p>", unsafe_allow_html=True)

    if opcion == "📊 Tablero de Control":
        st.write("---")
        # Tarjetas idénticas a la captura
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown('<div class="card"><h3 style="color:#8899A6">EN MORA</h3><h2 style="color:#ff4b4b">5 Clientes</h2><p>USD 2.210</p></div>', unsafe_allow_html=True)
        with c2: st.markdown('<div class="card"><h3 style="color:#8899A6">A COBRAR (7 DÍAS)</h3><h2 style="color:#55acee">4 Clientes</h2><p>USD 1.850</p></div>', unsafe_allow_html=True)
        with c3: st.markdown('<div class="card"><h3 style="color:#8899A6">TOTAL CARTERA</h3><h2 style="color:white">20 Registros</h2><p>USD 15.400</p></div>', unsafe_allow_html=True)

        st.markdown("### 📋 Gestión de Cartera y Cobranza")
        
        # Estilo de tabla igual a la captura
        def color_estado(val):
            if val == "VENCIDO": return 'background-color: #701010; color: white'
            if val == "AL DÍA": return 'background-color: #155123; color: white'
            return ''

        # MOSTRAMOS SOLO LAS COLUMNAS DE LA CAPTURA
        columnas_visibles = ["Cliente", "Vehículo", "Vencimiento", "Estado", "Saldo (USD)", "Enviar Mensaje"]
        
        st.dataframe(
            df[columnas_visibles].style.map(color_estado, subset=['Estado']),
            use_container_width=True, hide_index=True,
            column_config={
                "Enviar Mensaje": st.column_config.LinkColumn(display_text="📲 WhatsApp"),
                "Saldo (USD)": st.column_config.NumberColumn(format="$ %d")
            }
        )

    elif opcion == "🔍 Buscador Inteligente":
        st.title("🔍 Buscador")
        busqueda = st.text_input("Buscar cliente...")
        if busqueda:
            res = df[df['Cliente'].str.contains(busqueda, case=False)]
            st.dataframe(res[["Cliente", "Vehículo", "Estado", "Saldo (USD)"]], use_container_width=True, hide_index=True)

    elif opcion == "➕ Nuevo Registro":
        st.title("➕ Cargar Nuevo Cliente")
        with st.form("nuevo"):
            st.text_input("Nombre")
            st.text_input("Auto")
            if st.form_submit_button("Guardar"):
                st.success("Guardado")
