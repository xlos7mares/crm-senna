import streamlit as st

# 1. Configuración de página con tema oscuro forzado
st.set_page_config(page_title="Control & Gestión de Cartera", layout="wide")

# 2. CSS Maestro: Fondo oscuro y textos blancos
st.markdown(
    """
    <style>
        /* Fondo de la aplicación principal */
        .stApp {
            background-color: #0E1117;
            color: white;
        }
        
        /* Fondo del Sidebar */
        [data-testid="stSidebar"] {
            background-color: #161B22;
        }

        /* Color de los textos en el Sidebar */
        [data-testid="stSidebar"] section[data-testid="stSidebarNav"] span,
        [data-testid="stSidebar"] .stText,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] p {
            color: white !important;
        }

        /* Título principal centrado */
        .titulo-central {
            text-align: center;
            color: white;
            font-weight: bold;
            font-size: 2.5rem;
            margin-bottom: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# 3. Encabezado con Logo y Título
# Creamos tres columnas para centrar el logo y el título
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Intenta cargar la imagen. Si falla, no muestra error feo, solo un espacio.
    try:
        # PRUEBA ESTO: Si tu archivo se llama distinto, cámbialo aquí
        st.image("logo.png", use_container_width=True)
    except:
        st.warning("⚠️ Sube el archivo 'logo.png' a la carpeta raíz en GitHub.")
    
    st.markdown('<div class="titulo-central">CONTROL & GESTIÓN DE CARTERA</div>', unsafe_allow_html=True)

# 4. Sidebar con diseño corregido
with st.sidebar:
    st.markdown("## MENÚ")
    
    opcion = st.radio(
        "Seleccione una opción:",
        ["📊 Tablero de Control", "🔍 Buscador Inteligente", "➕ Nuevo Registro"],
        index=0
    )
    
    st.markdown("---")
    # Texto inferior con color celeste para que resalte
    st.markdown("<p style='color: #55acee; font-size: 0.8rem;'>Sistema v1.1 | 2026 © Automotora Otormín - Paysandú</p>", unsafe_allow_html=True)

# 5. Ejemplo de tarjetas (KPIs) para que veas cómo queda
if opcion == "📊 Tablero de Control":
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("EN MORA", "6 Clientes", "-$2,530")
    with c2:
        st.metric("A COBRAR (7 DÍAS)", "9 Clientes", "$3,050")
    with c3:
        st.metric("TOTAL CARTERA", "20 Registros", "$7,680")
