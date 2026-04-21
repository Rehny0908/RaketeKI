import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# ------------------------
# Physik-Klasse
# ------------------------
class Rocket:
    def __init__(self):
        self.y = 100.0   # Höhe (m)
        self.vy = 0.0    # Geschwindigkeit (m/s)

    def step(self, thrust, dt):
        g = 9.81
        mass = 1.0

        ay = (thrust / mass) - g

        self.vy += ay * dt
        self.y += self.vy * dt

        if self.y < 0:
            self.y = 0


# ------------------------
# Streamlit UI
# ------------------------
st.title("🚀 Raketen-Simulation (Phase 1)")

thrust = st.slider("Schub (Newton)", 0.0, 20.0, 10.0)
dt = st.slider("Zeitschritt (dt)", 0.01, 0.2, 0.05)

start = st.button("Simulation starten")
reset = st.button("Reset")

# Session State (wichtig für Streamlit)
if "rocket" not in st.session_state:
    st.session_state.rocket = Rocket()
    st.session_state.history = []
    st.session_state.running = False

if reset:
    st.session_state.rocket = Rocket()
    st.session_state.history = []
    st.session_state.running = False

if start:
    st.session_state.running = True

# Platzhalter für Plot
plot_placeholder = st.empty()

# ------------------------
# Simulation Loop
# ------------------------
if st.session_state.running:
    for _ in range(200):
        rocket = st.session_state.rocket

        rocket.step(thrust, dt)
        st.session_state.history.append(rocket.y)

        # Plot
        fig, ax = plt.subplots()
        ax.plot(st.session_state.history)
        ax.set_xlabel("Zeit")
        ax.set_ylabel("Höhe (m)")
        ax.set_title("Raketenhöhe")

        plot_placeholder.pyplot(fig)
        plt.close(fig)

        # Stop wenn Boden erreicht
        if rocket.y <= 0:
            st.warning("Rakete gelandet / gecrasht")
            st.session_state.running = False
            break

        time.sleep(0.05)

# Statusanzeige
rocket = st.session_state.rocket
st.write(f"Höhe: {rocket.y:.2f} m")
st.write(f"Geschwindigkeit: {rocket.vy:.2f} m/s")
