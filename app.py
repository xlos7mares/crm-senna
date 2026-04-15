import streamlit as st
from PIL import Image

# Configuración de página
st.set_page_config(page_title="CRM SENNA - Acceso", page_icon="🏎️", layout="centered")

# --- FUNCION DE LOGIN ---
def login():
    st.markdown("<h2 style='text-align: center;'>🔒 Control de Acceso</h2>", unsafe_allow_html=True)
    
    with st.form("login_form"):
        usuario = st.text_input("Usuario")
        clave = st.text_input("Contraseña", type="password")
        submit = st.form_submit_button("Ingresar al Sistema")
        
        if submit:
            # Aquí puedes cambiar 'admin' y '1234' por lo que tú quieras
            if usuario == "Leo" and clave == "Senna2026":
                st.session_state["logueado"] = True
                st.rerun()
            else:
                st.error("Credenciales incorrectas")

# --- LÓGICA DE NAVEGACIÓN ---
if "logueado" not in st.session_state:
    st.session_state["logueado"] = False

if not st.session_state["logueado"]:
    # Mostramos el logo también en el login para que se vea bien
    try:
        logo = Image.open('logocrm2026.png')
        st.image(logo, use_container_width=True)
    except:
        pass
    login()
else:
    # --- CONTENIDO DEL CRM (Solo si está logueado) ---
    st.sidebar.button("Cerrar Sesión", on_click=lambda: st.session_state.update({"logueado": False}))
    
    try:
        logo = Image.open('logocrm2026.png')
        st.image(logo, use_container_width=True)
    except:
        st.warning("Sube 'logocrm2026.png' a GitHub para ver el logo.")

    st.markdown("---")
    st.title("🚀 Sistema de Gestión Inteligente - Automotora")
    st.write(f"Bienvenido al panel de control, **{st.session_state.get('user', 'Leo')}**.")
    
    # Aquí va el resto de tu código de ventas, stock, etc.
    st.info("Plataforma Nivel 2026 activada.")
