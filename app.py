import streamlit as st

# 1. Configuración de la página (opcional, ayuda con el layout)
st.set_page_config(page_title="Control & Gestión de Cartera", layout="wide")

# 2. CSS para poner el texto del Sidebar en Blanco
st.markdown(
    """
    <style>
        /* Cambia el color de todo el texto en el sidebar */
        [data-testid="stSidebar"] {
            color: white;
        }
        /* Cambia el color de las etiquetas de radio o texto específico */
        [data-testid="stSidebar"] .st-emotion-cache-17l6f7f {
            color: white;
        }
        /* Asegura que los títulos del menú se vean blancos */
        section[data-testid="stSidebar"] h1, 
        section[data-testid="stSidebar"] h2, 
        section[data-testid="stSidebar"] h3 {
            color: white !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# 3. Mostrar el Logo arriba
# Reemplaza 'logo.png' por el nombre real de tu archivo
try:
    # use_container_width hace que se ajuste al ancho de la columna
    st.image("logo.png", width=200) 
except:
    st.error("No se encontró el archivo 'logo.png'. Verifica que esté en la carpeta del proyecto.")

# Título Principal
st.markdown("<h1 style='text-align: center;'>CONTROL & GESTIÓN DE CARTERA</h1>", unsafe_allow_html=True)

# --- Contenido del Sidebar ---
with st.sidebar:
    st.title("MENÚ")
    opcion = st.radio(
        "Seleccione una opción:",
        ["📊 Tablero de Control", "🔍 Buscador Inteligente", "➕ Nuevo Registro"],
        index=0
    )
    
    st.write("---")
    # Texto de versión al pie del sidebar
    st.markdown("<p style='color: #55acee;'>Sistema v1.1 | 2026 © Automotora Otormín - Paysandú</p>", unsafe_allow_html=True)
