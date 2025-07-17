import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="Calculadora de alojamiento - Lund", layout="centered")
st.title("📊 Calculadora de probabilidad de alojamiento en Lund")

st.markdown("""
Selecciona la **fecha y hora que te tocó en el sorteo**, ajusta el **% estimado de solicitantes activos**, y observa tus probabilidades de estar en el **Top 1, 2 o 3** en al menos una habitación.
""")

fecha_inicio = datetime(2025, 7, 10, 0, 0)
fecha = st.date_input("📅 Día que te tocó", datetime(2025, 7, 11).date())
hora = st.time_input("⏰ Hora que te tocó", datetime(2025, 7, 11, 6, 7).time())
fecha_usuario = datetime.combine(fecha, hora)
porcentaje_activos = st.slider("🔢 % de solicitantes activos antes que tú", 10, 100, 70, 5)
habitaciones_disponibles = st.number_input("🏠 Número de habitaciones restantes", 50, 700, 573)

# Cálculos
minutos_diferencia = (fecha_usuario - fecha_inicio).total_seconds() / 60
posicion_usuario = int(round(minutos_diferencia)) + 1
personas_mejor_hora = posicion_usuario - 1
personas_activas = round(personas_mejor_hora * porcentaje_activos / 100)
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