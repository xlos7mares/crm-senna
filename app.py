import streamlit as st
import pandas as pd
import urllib.parse
from fpdf import FPDF
from datetime import datetime
import PIL.Image as Image

# 1. CONFIGURACIÓN DE PÁGINA (Layout idéntico a tus capturas)
st.set_page_config(
    page_title="CRM SENNA 2026",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. INICIALIZACIÓN DEL ESTADO DE SESIÓN (Login)
if "logueado" not in st.session_state:
    st.session_state["logueado"] = False

# --- PANTALLA DE ACCESO (LOGIN) ---
if not st.session_state["logueado"]:
    st.markdown("<style>.stApp { background-color: #0E1117; color: white; }</style>", unsafe_allow_html=True)
    _, col_centro, _ = st.columns([1, 1.5, 1])
    with col_centro:
        st.write("#")
        st.markdown("<h1 style='text-align: center; color: #55acee;'>🏎️ CRM SENNA 2026</h1>", unsafe_allow_html=True)
        with st.form("login_form"):
            user = st.text_input("Usuario", placeholder="Leo")
            password = st.text_input("Contraseña", type="password", placeholder="Senna2026")
            if st.form_submit_button("INGRESAR AL SISTEMA"):
                if user == "Leo" and password == "Senna2026":
                    st.session_state["logueado"] = True
                    st.rerun()
                else:
                    st.error("❌ Credenciales incorrectas")

# --- PANTALLA PRINCIPAL (TODO EL CONTENIDO DE LAS CAPTURAS) ---
else:
    # Estética Profesional SENNA (Modo Oscuro)
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

    # Datos cargados exactamente como en la tabla de tus fotos
    @st.cache_data
    def cargar_datos():
        data = {
            "Cliente": ["Federico Rossi", "María Gonzalez", "Juan Castro", "Ana Ledesma", "Roberto Peña"],
            "Vehículo": ["Mercedes Benz A200", "Toyota Hilux", "VW Gol Trend", "Fiat Cronos", "Ford Ranger"],
            "Vencimiento": ["2026-03-30", "2026-04-10", "2026-04-15", "2026-03-25", "2026-05-01"],
            "Estado": ["VENCIDO", "AL DÍA", "AL DÍA", "VENCIDO", "AL DÍA"],
            "Cuota (USD)": [450, 600, 300, 320, 800],
            "Confianza": [2, 5, 4, 1, 5],
            "latitude": [-32.31, -32.32, -32.30, -32.33, -32.31],
            "longitude": [-58.08, -58.07, -58.09, -58.08, -58.10]
        }
        df = pd.DataFrame(data)
        df["Mora"] = df.apply(lambda x: round(x["Cuota (USD)"] * 0.02, 2) if x["Estado"] == "VENCIDO" else 0, axis=1)
        df["Total"] = df["Cuota (USD)"] + df["Mora"]
        
        def link_wa(fila):
            msg = f"CRM Senna 2026: Hola {fila['Cliente']}, cuota {fila['Vehículo']} {fila['Estado']}. Saldo: ${fila['Total']}."
            return f"https://wa.me/59899000000?text={urllib.parse.quote(msg)}"
        
        df["WhatsApp"] = df.apply(link_wa, axis=1)
        return df

    df = cargar_datos()

    # --- BARRA LATERAL (Los 5 Módulos de tus capturas) ---
    with st.sidebar:
        try:
            st.image("logo.png", use_container_width=True)
        except:
            st.markdown("<h2 style='color:#55acee'>🏎️ SENNA</h2>", unsafe_allow_html=True)
        
        st.markdown("### 🔐 ACCESO: ADMIN")
        opcion = st.radio("Módulos:", [
            "📊 Inteligencia de Negocio", 
            "💰 Gestión de Cobros", 
            "🔍 Buscador y Archivo",
            "📄 Contratos y Simulador",
            "📍 Mapa de Cartera"
        ])
        st.write("---")
        if st.button("🚪 Cerrar Sesión"):
            st.session_state["logueado"] = False
            st.rerun()
        st.markdown("v1.6 | **Premium Edition**")

    # Título Central
    st.markdown('<div class="titulo-central">CONTROL & GESTIÓN CRM SENNA</div>', unsafe_allow_html=True)
    st.write("---")

    # --- LÓGICA DE MÓDULOS ---

    if opcion == "📊 Inteligencia de Negocio":
        # Las 3 tarjetas de tus capturas
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown('<div class="card"><h3>Cobranza</h3><h2 style="color:#00ff00">84%</h2></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="card"><h3>Intereses</h3><h2 style="color:#55acee">${df["Mora"].sum()}</h2></div>', unsafe_allow_html=True)
        with c3: st.markdown('<div class="card"><h3>Riesgo</h3><h2 style="color:#ff4b4b">BAJO</h2></div>', unsafe_allow_html=True)
        
        st.subheader("📈 Proyección Semanal")
        st.line_chart({"Ingresos (USD)": [2400, 3100, 1800, 4200]})

    elif opcion == "💰 Gestión de Cobros":
        st.title("💸 Operaciones de Cobranza")
        def color_estado(val):
            if val == "VENCIDO": return 'background-color: #701010; color: white'
            if val == "AL DÍA": return 'background-color: #155123; color: white'
            return ''
        
        # Tabla completa con barra de progreso de Confianza (Estrellas)
        st.dataframe(
            df.style.map(color_estado, subset=['Estado']),
            use_container_width=True, hide_index=True,
            column_config={
                "WhatsApp": st.column_config.LinkColumn("Notificar", display_text="📲 WhatsApp"),
                "Confianza": st.column_config.ProgressColumn("Confianza", min_value=1, max_value=5, format="%d ⭐")
            }
        )

    elif opcion == "🔍 Buscador y Archivo":
        st.title("🔍 Archivo Digital")
        search = st.text_input("Buscar cliente...")
        if search:
            res = df[df["Cliente"].str.contains(search, case=False)]
            for _, r in res.iterrows():
                with st.expander(f"👤 {r['Cliente']} - Ficha"):
                    st.write(f"Auto: {r['Vehículo']} | Score: {r['Confianza']}/5")
                    st.file_uploader(f"Adjuntar documento para {r['Cliente']}")

    elif opcion == "📄 Contratos y Simulador":
        st.title("📄 Herramientas de Cierre")
        t1, t2 = st.tabs(["📄 Generar Recibo", "🧮 Simulador"])
        with t1:
            sel = st.selectbox("Cliente:", df["Cliente"])
            if st.button("Generar PDF"):
                st.success("Recibo generado.")
        with t2:
            monto = st.number_input("Deuda USD", value=500.0)
            st.metric("Cuota Mensual (3 meses)", f"USD {round(monto*1.1/3, 2)}")

    elif opcion == "📍 Mapa de Cartera":
        st.title("📍 Mapa de Cobranza")
        df_map = df.rename(columns={'latitude': 'lat', 'longitude': 'lon'})
        st.map(df_map, color="#ff4b4b", size=40)
        st.info("Visualización de clientes en Paysandú.")
