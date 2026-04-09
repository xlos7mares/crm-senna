import streamlit as st

# 1. Configuración de la página
st.set_page_config(page_title="Control & Gestión de Cartera", layout="wide")

# 2. CSS para forzar el Modo Oscuro y textos blancos
st.markdown(
    """
    <style>
        /* Fondo principal de la app */
        .stApp {
            background-color: #0E1117;
            color: white;
        }
        
        /* Fondo del Sidebar */
        [data-testid="stSidebar"] {
            background-color: #161B22;
        }

        /* Texto del Sidebar en blanco */
        [data-testid="stSidebar"] * {
            color: white !important;
        }

        /* Estilo para el título central */
        .titulo-central {
            text-align: center;
            color: white;
            font-size: 2.2rem;
            font-weight: bold;
            margin-top: -20px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# 3. Logo y Título Centrados
col1, col2, col3 = st.columns([1, 1.5, 1])

with col2:
    # Mostramos el logo que acabas de subir
    st.image("logo.png", use_container_width=True)
    st.markdown('<div class="titulo-central">CONTROL & GESTIÓN DE CARTERA</div>', unsafe_allow_html=True)

# 4. Menú Lateral (Sidebar)
with st.sidebar:
    st.markdown("### MENÚ")
    
    opcion = st.radio(
        "Navegación:",
        ["📊 Tablero de Control", "🔍 Buscador Inteligente", "➕ Nuevo Registro"],
        index=0
    )
    
    st.write("---")
    # Pie de página en el sidebar
    st.markdown("<p style='color: #55acee; font-size: 0.8rem;'>Sistema v1.1 | 2026 © Automotora Otormín - Paysandú</p>", unsafe_allow_html=True)

# 5. Lógica de las secciones (Ejemplo para el Tablero)
if opcion == "📊 Tablero de Control":
    st.write("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("EN MORA", "6 Clientes", "-$2,530", delta_color="inverse")
    with c2:
        st.metric("A COBRAR (7 DÍAS)", "9 Clientes", "$3,050")
    with c3:
        st.metric("TOTAL CARTERA", "20 Registros", "$7,680")

    st.markdown("### ⚠️ Acciones de Cobranza Prioritaria")
    st.error("**VENCIDO** | Federico Rossi - Mercedes Benz A200 (Vence: 2026-03-30)")
