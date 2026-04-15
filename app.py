import streamlit as st
import pandas as pd
import urllib.parse
from fpdf import FPDF
from datetime import datetime, timedelta
import PIL.Image as Image

# 1. CONFIGURACIÓN DE PÁGINA (Debe ser la primera instrucción)
st.set_page_config(
    page_title="CRM SENNA 2026",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. INICIALIZACIÓN DEL ESTADO DE SESIÓN (Control de acceso)
if "logueado" not in st.session_state:
    st.session_state["logueado"] = False

# --- PANTALLA DE ACCESO (LOGIN) ---
if not st.session_state["logueado"]:
    # Estética profesional para el Login (Modo Oscuro)
    st.markdown("""
        <style>
            .stApp { background-color: #0E1117; color: white; }
            .login-box {
                background-color: #161B22;
                padding: 30px;
                border-radius: 15px;
                border: 1px solid #55acee;
            }
        </style>
    """, unsafe_allow_html=True)

    # Centramos el formulario de login
    _, col_centro, _ = st.columns([1, 1.5, 1])
    
    with col_centro:
        st.write("#") # Espacio superior
        try:
            # Intentamos cargar el logo genérico 'logo.png'
            logo_login = Image.open("logo.png")
            st.image(logo_login, use_container_width=True)
        except:
            pass
        
        st.markdown("<h2 style='text-align: center;'>🔐 Acceso CRM SENNA</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #8899A6;'>Sistema de Gestión Automotriz Profesional - v2026</p>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            user = st.text_input("Usuario", placeholder="Tu usuario")
            password = st.text_input("Contraseña", type="password", placeholder="Tu contraseña")
            btn_login = st.form_submit_button("INGRESAR AL SISTEMA")
            
            if btn_login:
                # Credenciales unificadas
                if user == "Leo" and password == "Senna2026":
                    st.session_state["logueado"] = True
                    st.rerun()
                else:
                    st.error("❌ Credenciales incorrectas.")

# --- PANTALLA PRINCIPAL (Solo visible tras el Login exitoso) ---
else:
    # 3. ESTÉTICA PROFESIONAL CRM (Modo Oscuro - Tal cual las capturas)
    st.markdown("""
        <style>
            .stApp { background-color: #0E1117; color: white; }
            [data-testid="stSidebar"] { background-color: #161B22; }
            [data-testid="stSidebar"] * { color: white !important; }
            /* Estilo de Tarjetas Métricas */
            .card {
                background-color: #1E2329;
                padding: 20px;
                border-radius: 10px;
                border-top: 4px solid #55acee;
                text-align: center;
                margin-bottom: 20px;
            }
            /* Título central */
            .titulo-central {
                text-align: center;
                color: white;
                font-size: 2.2rem;
                font-weight: bold;
                margin-top: -20px;
            }
        </style>
    """, unsafe_allow_html=True)

    # 4. Datos y Lógica de Inteligencia (Ejemplo des-otormizado para Demo)
    @st.cache_data
    def cargar_datos_demo():
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
        
        # WhatsApp Genérico SaaS
        def link_wa(fila):
            msg = f"Aviso de Gestión de Cobranza Automotriz: Estimado {fila['Cliente']}, le informamos que su cuota por el {fila['Vehículo']} se encuentra en estado {fila['Estado']}. El saldo total liquidado es de ${fila['Saldo (USD)']}. Saludos cordiales."
            return f"https://wa.me/59899000000?text={urllib.parse.quote(msg)}"
        
        df["WhatsApp"] = df.apply(link_wa, axis=1)
        return df

    df = cargar_datos_demo()

    # 5. Función PDF Real
    def generar_pdf(cliente, vehiculo, monto, tipo):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="SISTEMA GESTIÓN AUTOMOTRIZ", ln=True, align='C')
        pdf.ln(10)
        pdf.set_font("Arial", '', 12)
        pdf.cell(200, 10, txt=f"Cliente: {cliente}", ln=True)
        pdf.cell(200, 10, txt=f"Vehículo: {vehiculo}", ln=True)
        pdf.cell(200, 10, txt=f"Total Liquidado: USD {monto}", ln=True)
        pdf.cell(200, 10, txt=f"Fecha: {datetime.now().strftime('%d/%m/%Y')}", ln=True)
        return pdf.output(dest='S').encode('latin-1')

    # 6. Sidebar (Navegación Unificada - Reconstruida según capturas)
    with st.sidebar:
        try:
            # Cargamos el logo genérico 'logo.png'
            logo_side = Image.open("logo.png")
            st.image(logo_side, use_container_width=True)
        except:
            pass
        
        st.markdown("### MENÚ")
        # Botones de Radio EXACTOS a las capturas que pasaste
        opcion = st.radio("Navegación:", [
            "📊 Tablero de Control", 
            "🔍 Buscador Inteligente", 
            "➕ Nuevo Registro"
        ])
        
        st.write("---")
        # Botón para cerrar sesión
        if st.button("🚪 Cerrar Sesión"):
            st.session_state["logueado"] = False
            st.rerun()
        
        st.markdown("<p style='color: #8899A6; font-size: 0.8rem;'>v2.2 | CRM SENNA 2026</p>", unsafe_allow_html=True)

    # 7. Cabecera Central
    st.markdown('<div class="titulo-central">CRM SENNA 2026</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8899A6; margin-top: -10px;'>Control Total de Cartera Automotriz</p>", unsafe_allow_html=True)
    st.write("---")

    # 8. Lógica de Módulos

    if opcion == "📊 Tablero de Control":
        # Métricas (Tarjetas con borde celeste tal cual las capturas)
        st.write("---")
        c1, c2, c3 = st.columns(3)
        c1.markdown('<div class="card"><h3>EN MORA</h3><h2 style="color:#ff4b4b">5 Clientes</h2><p>USD 2.210</p></div>', unsafe_allow_html=True)
        c2.markdown('<div class="card"><h3>A COBRAR (7 DÍAS)</h3><h2 style="color:#55acee">4 Clientes</h2><p>USD 1.850</p></div>', unsafe_allow_html=True)
        c3.markdown('<div class="card"><h3>TOTAL CARTERA</h3><h2>20 Registros</h2><p>USD 15.400</p></div>', unsafe_allow_html=True)

        st.markdown("### 📋 Gestión de Cartera y Cobranza")
        
        # Función para dar color a las celdas de Estado
        def color_estado(val):
            if val == "VENCIDO": return 'background-color: #701010; color: white'
            if val == "AL DÍA": return 'background-color: #155123; color: white'
            return ''
        
        # Mostramos la tabla principal recreando la estructura exacta
        st.dataframe(
            df.style.map(color_estado, subset=['Estado']),
            use_container_width=True, hide_index=True,
            column_config={
                "WhatsApp": st.column_config.LinkColumn("Enviar Mensaje", display_text="📲 WhatsApp"),
                "Saldo (USD)": st.column_config.NumberColumn(format="$ %d")
            }
        )

    elif opcion == "🔍 Buscador Inteligente":
        st.title("🔍 Buscador Inteligente de Clientes")
        search = st.text_input("Buscar cliente o vehículo...", placeholder="Ej: Federico Rossi")
        
        if search:
            # Filtramos los datos
            res = df[df["Cliente"].str.contains(search, case=False) | df["Vehículo"].str.contains(search, case=False)]
            
            if not res.empty:
                for _, r in res.iterrows():
                    with st.expander(f"👤 Ficha Completa: {r['Cliente']}"):
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.write(f"**Vehículo:** {r['Vehículo']}")
                            st.write(f"**Vencimiento:** {r['Vencimiento']}")
                            st.write(f"**Estado:** {r['Estado']}")
                            st.write(f"**Saldo Total:** ${r['Saldo (USD)']}")
                        with col_b:
                            st.write(f"**Score Crediticio:** {r['Score']} / 5")
                            # Botones de Acción
                            if st.button(f"📲 WhatsApp a {r['Cliente']}"):
                                st.markdown(f'<a href="{r["WhatsApp"]}" target="_blank">Abrir WhatsApp</a>', unsafe_allow_html=True)
                            
                            # PDF (Demo - sin logo anterior)
                            pdf_data = generar_pdf(r['Cliente'], r['Vehículo'], r['Saldo (USD)'], "Recibo Oficial")
                            st.download_button(f"📥 Descargar PDF {r['Cliente']}", data=pdf_data, file_name=f"recibo_{r['Cliente']}.pdf")

            else:
                st.warning("No se encontraron coincidencias.")

    elif opcion == "➕ Nuevo Registro":
        st.title("➕ Cargar Nuevo Cliente a Cartera")
        with st.form("nuevo_cliente"):
            nombre = st.text_input("Nombre Completo")
            vehiculo = st.text_input("Vehículo (Marca y Modelo)")
            vencimiento = st.date_input("Fecha de Vencimiento")
            saldo = st.number_input("Monto de Cuota (USD)")
            if st.form_submit_button("Guardar Registro"):
                st.success(f"Registro de {nombre} guardado correctamente (Simulación).")
