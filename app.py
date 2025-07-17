import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

st.set_page_config(page_title="Calculadora de alojamiento - Lund", layout="centered")
st.title("📊 Calculadora de probabilidad de alojamiento en Lund (AF Böstader)")
st.markdown("""
Selecciona la **fecha y hora que te tocó en el sorteo**, ajusta el **% estimado de solicitantes activos**, y observa tus probabilidades de estar en el **Top 1, 2 o 3** en al menos una habitación.
""")

fecha_inicio = datetime(2025, 7, 10, 0, 0)
fecha = st.date_input("📅 Día que te tocó", datetime(2025, 7, 11).date())
hora = st.time_input("⏰ Hora que te tocó", datetime(2025, 7, 11, 6, 7).time(),step=timedelta(minutes=1))
fecha_usuario = datetime.combine(fecha, hora)
porcentaje_activos = st.slider("🔢 Porcentaje de solicitantes activos antes que tú", 10, 100, 70, 5)
col1, col2, col3 = st.columns([1, 6, 1])
with col1:
    st.markdown("**10%**")
with col2:
    porcentaje = st.slider(
        "% de solicitantes activos",
        min_value=10,
        max_value=100,
        value=70,
        step=5,
        label_visibility="collapsed"
    )
with col3:
    st.markdown("**100%**")
st.markdown("""
💡 *Como no podemos saber cuántas personas que están por delante de ti siguen buscando alojamiento, puedes ajustar esta estimación con el porcentaje de arriba. Esto afecta al número total de solicitudes que se esperan por habitación.*
""")
habitaciones_disponibles = st.number_input("🏠 Número de habitaciones restantes", 50, 700, 572)

# Cálculos
minutos_diferencia = (fecha_usuario - fecha_inicio).total_seconds() / 60
posicion_usuario = int(round(minutos_diferencia)) + 1
personas_mejor_hora = posicion_usuario - 1
# Ajuste por personas con alojamiento
habitaciones_iniciales = 900
personas_con_alojamiento = habitaciones_iniciales - habitaciones_disponibles

# No pueden quedar menos de 0
personas_utiles = max(personas_mejor_hora - personas_con_alojamiento, 0)
if personas_utiles <= 0:
    st.success("🎉 ¡Tu posición en la cola es muy buena! Seguramente ya hayas conseguido alojamiento.")

# Personas activas tras ajuste
personas_activas = round(personas_utiles * porcentaje_activos / 100)
solicitudes_totales = personas_activas * 3

habitaciones = np.arange(0, 901)
prob_top1, prob_top2, prob_top3 = [], [], []

for h in habitaciones:
    lam = solicitudes_totales / h
    p0 = np.exp(-lam)
    p1 = lam * np.exp(-lam)
    p2 = (lam**2 / 2) * np.exp(-lam)
    prob_top1.append(1 - (1 - p0) ** h)
    prob_top2.append(1 - (1 - (p0 + p1)) ** h)
    prob_top3.append(1 - (1 - (p0 + p1 + p2)) ** h)

# Resultados
st.markdown(f"📍 Tu posición en el sorteo es: **{posicion_usuario}**")
st.markdown(f"👥 Personas activas antes que tú: **{personas_activas}**")
st.markdown(f"📨 Solicitudes estimadas: **{solicitudes_totales}**")

st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)

# Interpolamos la probabilidad exacta en el número actual de habitaciones
idx = np.where(habitaciones == habitaciones_disponibles)[0]
if len(idx) > 0:
    i = idx[0]
    p1_actual = prob_top1[i]
    p2_actual = prob_top2[i]
    p3_actual = prob_top3[i]

    st.markdown(f"""
    <div style="text-align: center; padding: 1rem; background-color: #f7f7f7; border-radius: 10px; width: 100%;">
    <h3>🎯 Probabilidades en {habitaciones_disponibles} habitaciones:</h3>
    <p style="font-size: 18px;">🥇 <strong>Top 1</strong>: {p1_actual:.1%}</p>
    <p style="font-size: 18px;">🥈 <strong>Top ≤2</strong>: {p2_actual:.1%}</p>
    <p style="font-size: 18px;">🥉 <strong>Top ≤3</strong>: {p3_actual:.1%}</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.warning("El número de habitaciones introducido no está en el rango calculado.")

st.markdown("<div style='margin-top: 35px;'></div>", unsafe_allow_html=True)

fig, ax = plt.subplots()
ax.plot(habitaciones, prob_top1, label='Top 1', linewidth=2)
ax.plot(habitaciones, prob_top2, label='Top ≤2', linewidth=2)
ax.plot(habitaciones, prob_top3, label='Top ≤3', linewidth=2)
ax.axvline(x=habitaciones_disponibles, color='gray', linestyle='--', label='Habitaciones actuales')
ax.axhline(y=0.8, color='black', linestyle='--', label='80% probabilidad')
ax.set_xlabel("Número de habitaciones")
ax.set_ylabel("Probabilidad")
ax.set_title("Probabilidad de estar en el top N en al menos una habitación")
ax.grid(True)
ax.legend()
st.pyplot(fig)

st.markdown("""
<style>
.footer {
    position: fixed;
    bottom: 10px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 14px;
    color: #888888;
}
</style>
<div class="footer">Pablo Montoro · 2025</div>
""", unsafe_allow_html=True)