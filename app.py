import streamlit as st
import pandas as pd
import urllib.parse
from fpdf import FPDF
from datetime import datetime
import PIL.Image as Image

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="CRM SENNA 2026 - Sistema de Control",
    page_icon="🏎️",
    layout="wide"
)

# 2. ESTÉTICA PROFESIONAL (Modo Oscuro SENNA)
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

# 3. INICIALIZACIÓN DEL CONTROL DE ACCESO
if "logueado" not in st.session_state:
    st.session_state["logueado"] = False

# --- PANTALLA DE ACCESO (LOGIN) ---
if not st.session_state["logueado"]:
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
            user = st.text_input("Usuario", placeholder="Tu nombre")
            password = st.text_input("Contraseña", type="password")
            btn_login = st.form_submit_button("INGRESAR AL PANEL DE CONTROL")
            
            if btn_login:
                if user == "Leo" and password == "Senna2026":
                    st.session_state["logueado"] = True
                    st.rerun()
                else:
                    st.error("❌ Credenciales incorrectas.")

# --- PANTALLA PRINCIPAL (Contenido Protegido) ---
else:
    # 4. Datos con Inteligencia y Geolocalización
    @st.cache_data
    def cargar_todo():
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
            # Mensaje actualizado a CRM SENNA
            msg = f"CRM SENNA 2026 Informa: {fila['Cliente']}, cuota {fila['Vehículo']} {fila['Estado']}. Total: ${fila['Total']}. Saludos."
            return f"https://wa.me/59899000000?text={urllib.parse.quote(msg)}"
        
        df["WhatsApp"] = df.apply(link_wa, axis=1)
        return df

    df = cargar_todo()

    # 5. Función PDF Real
    def generar_pdf(cliente, vehiculo, monto, tipo):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="CRM SENNA - AUTOMOTORA", ln=True, align='C')
        pdf.ln(10)
        pdf.set_font("Arial", '', 12)
        pdf.cell(200, 10, txt=f"Cliente: {cliente}", ln=True)
        pdf.cell(200, 10, txt=f"Vehículo: {vehiculo}", ln=True)
        pdf.cell(200, 10, txt=f"Total Liquidado: USD {monto}", ln=True)
        pdf.cell(200, 10, txt=f"Fecha: {datetime.now().strftime('%d/%m/%Y')}", ln=True)
        return pdf.output(dest='S').encode('latin-1')

    # 6. Sidebar (Menú Lateral de la Izquierda)
    with st.sidebar:
        try:
            logo_side = Image.open("logo.png")
            st.image(logo_side, use_container_width=True)
        except:
            st.markdown("<h1 style='color: #55acee;'>🏎️ SENNA</h1>", unsafe_allow_html=True)
        
        st.markdown(f"### 👤 ADMIN: **Leo**")
        st.write("---")
        
        opcion = st.radio("MÓDULOS:", [
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
        
        st.markdown("v2.2 | **SENNA 2026**")

    # 7. Cabecera Central
    st.markdown('<div class="titulo-central">CONTROL & GESTIÓN CRM SENNA</div>', unsafe_allow_html=True)

    # 8. Lógica de Módulos (Exactamente como tu código v1.6)
    if opcion == "📊 Inteligencia de Negocio":
        st.write("---")
        c1, c2, c3 = st.columns(3)
        c1.markdown('<div class="card"><h3>Cobranza</h3><h2 style="color:#00ff00">84%</h2></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="card"><h3>Intereses</h3><h2 style="color:#55acee">${df["Mora"].sum()}</h2></div>', unsafe_allow_html=True)
        c3.markdown('<div class="card"><h3>Riesgo</h3><h2 style="color:#ff4b4b">BAJO</h2></div>', unsafe_allow_html=True)
        st.subheader("📈 Proyección Semanal")
        st.line_chart({"Semana": ["S1", "S2", "S3", "S4"], "Ingresos (USD)": [2400, 3100, 1800, 4200]})

    elif opcion == "💰 Gestión de Cobros":
        st.title("💸 Operaciones de Cobranza")
        def color_estado(val):
            if val == "VENCIDO": return 'background-color: #701010; color: white'
            if val == "AL DÍA": return 'background-color: #155123; color: white'
            return ''
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
                    st.file_uploader(f"Adjuntar documento para {r['Cliente']}", key=r['Cliente'])

    elif opcion == "📄 Contratos y Simulador":
        st.title("📄 Herramientas de Cierre")
        tab1, tab2 = st.tabs(["📄 Generar Recibo", "🧮 Simulador"])
        with tab1:
            sel = st.selectbox("Cliente:", df["Cliente"])
            row = df[df["Cliente"] == sel].iloc[0]
            # Generación real de PDF
            pdf_data = generar_pdf(sel, row["Vehículo"], row["Total"], "Recibo Oficial")
            st.download_button(f"📥 Descargar Recibo {sel}", data=pdf_data, file_name=f"recibo_{sel}.pdf", mime="application/pdf")
        with tab2:
            monto = st.number_input("Deuda USD", value=500.0)
            cuotas = st.slider("Meses", 1, 12, 3)
            st.metric("Cuota Mensual", f"USD {round((monto*1.1)/cuotas, 2)}")

    elif opcion == "📍 Mapa de Cartera":
        st.title("🗺️ Mapa de Cobranza")
        df_map = df.copy()
        df_map["color"] = df_map["Estado"].apply(lambda x: "#FF0000" if x == "VENCIDO" else "#0000FF")
        st.map(df_map, color="color", size=40)
        st.info("🔴 Rojo: Vencidos | 🔵 Azul: Al día")
