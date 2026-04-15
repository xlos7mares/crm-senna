import streamlit as st
from PIL import Image

# 1. Configuración de la página (esto siempre debe ir primero)
st.set_page_config(
    page_title="CRM SENNA - 2026",
    page_icon="🏎️",
    layout="wide"
)

# 2. Cargar y mostrar el logo
try:
    # Usamos el nombre exacto que aparece en tu GitHub
    logo = Image.open('logocrm2026jpg.jpg')
    
    # Creamos columnas para centrar el logo y que no ocupe toda la pantalla
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(logo, use_container_width=True)
except:
    st.error("No se pudo cargar el logo. Verifica que el nombre sea exacto.")

# 3. Título y separador
st.markdown("---")
st.title("Sistema de Gestión Inteligente")

# Aquí continúa tu código actual...
