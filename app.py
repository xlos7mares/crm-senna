# --- AGREGAR AL FINAL DEL ARCHIVO ---

elif opcion == "➕ Nuevo Registro":
    # Mantenemos lo que tenías y agregamos la herramienta de cierre
    st.write("---")
    st.subheader("📝 Cargar Nuevo Cliente")
    with st.form("nuevo_cliente"):
        nombre = st.text_input("Nombre Completo")
        auto = st.text_input("Vehículo")
        vence = st.date_input("Fecha de Vencimiento")
        if st.form_submit_button("Guardar Registro"):
            st.success(f"Registro de {nombre} guardado correctamente.")

    st.write("---")
    st.subheader("🧮 Simulador de Refinanciación (Para cerrar acuerdos)")
    st.info("Usa esta herramienta cuando el cliente no puede pagar el total y quiere cuotas.")
    
    col_sim1, col_sim2 = st.columns(2)
    with col_sim1:
        deuda_total = st.number_input("Monto Adeudado (USD)", min_value=0.0, value=500.0)
        num_cuotas = st.slider("Cantidad de cuotas", 1, 12, 3)
    with col_sim2:
        interes_ref = st.number_input("Interés mensual (%)", value=2.0)
        
        # Cálculo de cuota fija (Simulado)
        total_con_interes = deuda_total * (1 + (interes_ref/100 * num_cuotas))
        cuota_mensual = total_con_interes / num_cuotas
        
        st.metric("Cuota Mensual", f"USD {round(cuota_mensual, 2)}")
        st.write(f"**Total a cobrar al final:** USD {round(total_con_interes, 2)}")

    if st.button("Generar Plan de Pagos PDF"):
        st.warning("Función Pro: Imprime el plan de cuotas para que el cliente lo firme ya.")
