import streamlit as st
import pandas as pd
import urllib.parse

# 1. Configuración de la página
st.set_page_config(page_title="Gestión Inteligente Otormín", layout="wide")

# 2. CSS Maestro para estética profesional
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
        }
    </style>
""", unsafe_allow_html=True)

# 3. Datos Inteligentes con Cálculo de Mora
@st.cache_data
def obtener_datos():
    data = {
        "Cliente": ["Federico Rossi", "María Gonzalez", "Juan Castro", "Ana Ledesma", "Roberto Peña"],
        "Vehículo": ["Mercedes Benz A200", "Toyota Hilux", "VW Gol Trend", "Fiat Cronos", "Ford Ranger"],
        "Vencimiento": ["2026-03-30", "2026-04-10", "2026-04-15", "2026-03-25", "2026-05-01"],
        "Estado": ["VENCIDO", "AL DÍA", "AL DÍA", "VENCIDO", "AL DÍA"],
        "Cuota (USD)": [450, 600, 300, 320, 800],
        "Días de Atraso": [10, 0, 0, 15, 0]
    }
    df = pd.DataFrame(data)
    
    # Cálculo de mora (2% de recargo si está vencido)
    tasa_mora = 0.02
    df["Intereses Mora"] = df.apply(lambda x: round(x["Cuota (USD)"] * tasa_mora, 2) if x["Estado"] == "VENCIDO" else 0, axis=1)
    df["Total a Cobrar"] = df["Cuota (USD)"] + df["Intereses Mora"]
    
    # Función para link de WhatsApp con el monto detallado
    def generar_wa(fila):
        if fila["Estado"] == "VENCIDO":
            msg = f"Hola {fila['Cliente']}, le informamos que su cuota de {fila['Vehículo']} está vencida. Saldo cuota: ${fila['Cuota (USD)']} + Intereses: ${fila['Intereses Mora']}. Total a pagar: ${fila['Total a Cobrar']}. Por favor, regularice su situación."
        else:
            msg = f"Hola {fila['Cliente']}, le recordamos que su próxima cuota de {fila['Vehículo']} vence el {fila['Vencimiento']}. Saludos de Automotora Otormín."
        return f"https://wa.me/59899000000?text={urllib.parse.quote(msg)}"
    
    df["WhatsApp"] = df.apply(generar_wa, axis=1)
    return df

df = obtener_datos()

# 4. Sidebar
with st.sidebar:
    try: st.image("logo.png")
    except: pass
    st.markdown("### PANEL DE CONTROL")
    opcion = st.radio("Módulos de Gestión:", ["📊 Inteligencia de Negocio", "💰 Gestión de Cobros", "📄 Generador de Contratos"])
    st.write("---")
    st.markdown("<p style='color: #55acee;'>Sistema v1.2 | Otormín 2026</p>", unsafe_allow_html=True)

# 5. Módulo: Gestión de Cobros (Aquí está el WhatsApp potente)
if opcion == "💰 Gestión de Cobros":
    st.title("💸 Liquidación de Deuda y Cobranza")
    
    st.info("💡 Este panel liquida intereses automáticamente. El botón de WhatsApp ya incluye el cálculo de deuda actualizado.")

    # Estilo de colores para la tabla
    def resaltar_estado(val):
        if val == "VENCIDO": return 'background-color: #701010; color: white'
        if val == "AL DÍA": return 'background-color: #155123; color: white'
        return ''

    # Configuración de columnas para que el link se vea como un botón
    st.dataframe(
        df.style.map(resaltar_estado, subset=['Estado']),
        use_container_width=True,
        hide_index=True,
        column_config={
            "WhatsApp": st.column_config.LinkColumn("Acción Rápida", display_text="📲 Notificar Cobro"),
            "Cuota (USD)": st.column_config.NumberColumn(format="$ %d"),
            "Intereses Mora": st.column_config.NumberColumn(format="$ %.2f"),
            "Total a Cobrar": st.column_config.NumberColumn(format="$ %.2f")
        }
    )

# 6. Módulo: Inteligencia de Negocio
elif opcion == "📊 Inteligencia de Negocio":
    st.title("🚀 Análisis de Cartera Estratégico")
    col1, col2, col3 = st.columns(3)
    with col1: st.markdown('<div class="card"><h3>Efectividad</h3><h2 style="color:#00ff00">84%</h2></div>', unsafe_allow_html=True)
    with col2: st.markdown(f'<div class="card"><h3>Mora Generada</h3><h2 style="color:#55acee">${df["Intereses Mora"].sum()}</h2></div>', unsafe_allow_html=True)
    with col3: st.markdown('<div class="card"><h3>Riesgo</h3><h2 style="color:#ff4b4b">BAJO</h2></div>', unsafe_allow_html=True)
    
    st.write("---")
    st.subheader("📈 Proyección de Ingresos Semanales")
    st.line_chart({"Semana": ["Sem 1", "Sem 2", "Sem 3", "Sem 4"], "Ingresos (USD)": [2400, 3100, 1800, 4200]})

# 7. Módulo: Generador de Contratos
elif opcion == "📄 Generador de Contratos":
    st.title("📄 Automatización de Documentos")
    cliente_sel = st.selectbox("Seleccione Cliente:", df["Cliente"])
    tipo_doc = st.selectbox("Tipo de Documento:", ["Recibo de Pago", "Convenio de Pago", "Notificación Judicial"])
    
    if st.button("Generar y Descargar"):
        st.success(f"Documento para {cliente_sel} listo.")
        st.download_button("Descargar PDF", "Contenido Simulado", file_name="documento.pdf")
