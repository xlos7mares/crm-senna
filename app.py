import streamlit as st
from PIL import Image
import pandas as pd

# 1. CONFIGURACIÓN DE PÁGINA (Debe ser la primera instrucción de Streamlit)
st.set_page_config(
    page_title="CRM SENNA - Dashboard",
    page_icon="🏎️",
    layout="wide"
)

# 2. INICIALIZACIÓN DEL ESTADO DE SESIÓN (Control de acceso)
if "logueado" not in st.session_state:
    st.session_state["logueado"] = False

# --- PANTALLA DE ACCESO (LOGIN) ---
if not st.session_state["logueado"]:
    # Centramos el formulario de login
    _, col_centro, _ = st.columns([1, 2, 1])
    
    with col_centro:
        try:
            # Intentamos cargar el logo transparente que subiste
            # IMPORTANTE: Verifica que el nombre sea exacto al de tu GitHub
            logo = Image.open('logocrm2026.png')
            st.image(logo, use_container_width=True)
        except:
            st.info("Cargando sistema... (Verifica si logocrm2026.png está en la raíz de tu GitHub)")
        
        st.markdown("<h2 style='text-align: center;'>🔐 Acceso CRM SENNA 2026</h2>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            user = st.text_input("Usuario", placeholder="Ingresa tu nombre")
            password = st.text_input("Contraseña", type="password")
            btn_login = st.form_submit_button("INGRESAR AL PANEL DE CONTROL")
            
            if btn_login:
                # Credenciales de acceso
                if user == "Leo" and password == "Senna2026":
                    st.session_state["logueado"] = True
                    st.rerun()
                else:
                    st.error("❌ Credenciales incorrectas. Intenta de nuevo.")

# --- PANTALLA PRINCIPAL (Solo visible tras el Login) ---
else:
    # Barra Lateral (Sidebar)
    with st.sidebar:
        try:
            logo_side = Image.open('logocrm2026.png')
            st.image(logo_side, use_container_width=True)
        except:
            pass
        st.markdown(f"### 👤 Usuario: **Leo**")
        st.markdown("---")
        if st.button("🚪 Cerrar Sesión"):
            st.session_state["logueado"] = False
            st.rerun()

    # Título Principal y Banner de IA
    st.title("🚀 CRM SENNA - Automotora Otormín")
    st.markdown("#### **Plataforma Inteligente de Control Total - Nivel 2026**")
    st.info("IA Activa: Analizando flujo de caja y vencimientos de cuotas.")

    # ORGANIZACIÓN POR PESTAÑAS (TABS)
    tab_dashboard, tab_stock, tab_cuotas = st.tabs([
        "📊 Dashboard General", 
        "🚘 Inventario de Vehículos", 
        "📅 Control de Cuotas"
    ])

    # CONTENIDO: PESTAÑA 1 - DASHBOARD
    with tab_dashboard:
        st.subheader("Estado del Negocio en Tiempo Real")
        c1, c2, c3 = st.columns(3)
        c1.metric("Unidades en Stock", "24", "+2 esta semana")
        c2.metric("Cobros del Mes", "$12.500", "Meta: $20k")
        c3.metric("Ventas Mensuales", "8", "+15% vs mes anterior")
        
        st.markdown("### Rendimiento de Ventas")
        # Gráfico simple de ejemplo
        st.area_chart({"Ventas": [4, 6, 5, 8, 7, 9, 10]})

    # CONTENIDO: PESTAÑA 2 - INVENTARIO
    with tab_stock:
        st.subheader("Gestión de Stock de Vehículos")
        # Base de datos de ejemplo (esto se conectará a Sheets después)
        df_stock = pd.DataFrame({
            'Vehículo': ['Toyota Hilux', 'Chevrolet Cruze', 'VW Gol', 'Fiat Cronos'],
            'Año': [2022, 2024, 2020, 2023],
            'Estado': ['Disponible', 'Vendido', 'Taller', 'Disponible'],
            'Precio (USD)': [45000, 22000, 12500, 18900]
        })
        st.dataframe(df_stock, use_container_width=True)
        
        if st.button("➕ Cargar Nuevo Auto al Stock"):
            st.info("Función de carga en desarrollo para conexión con base de datos.")

    # CONTENIDO: PESTAÑA 3 - CUOTAS
    with tab_cuotas:
        st.subheader("Vencimientos y Cobranza")
        st.warning("🔔 Alerta IA: 3 Clientes tienen vencimientos en las próximas 48hs.")
        
        # Ejemplo de datos de cuotas
        df_cuotas = pd.DataFrame({
            'Cliente': ['José Ignacio Otormín', 'Rafael G.', 'Gustavo S.'],
            'Vehículo': ['Toyota Hilux', 'VW Gol', 'Fiat Cronos'],
            'Cuota N°': ['5/12', '10/24', '2/36'],
            'Vencimiento': ['2026-04-18', '2026-04-20', '2026-04-22'],
            'Monto': [1200, 450, 600]
        })
        st.table(df_cuotas)
        st.success("Sugerencia IA: Enviar recordatorio por WhatsApp a José Ignacio Otormín.")
