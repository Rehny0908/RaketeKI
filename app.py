import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

# ------------------------
# Setup
# ------------------------
st.set_page_config(page_title="Rocket Sim", layout="centered")

st.title("🚀 Rocket Landing Simulator")

st.markdown("Simple physics sandbox for thrust control")

# ------------------------
# Rocket Model
# ------------------------
class Rocket:
    def __init__(self):
        self.y = 100.0
        self.vy = 0.0

    def step(self, thrust, dt):
        g = 9.81
        mass = 1.0

        ay = (thrust / mass) - g

        self.vy += ay * dt
        self.y += self.vy * dt

        if self.y < 0:
            self.y = 0


# ------------------------
# UI Controls
# ------------------------
thrust = st.slider("Thrust (N)", 0.0, 25.0, 10.0)
dt = st.slider("Time step", 0.01, 0.2, 0.05)

col1, col2 = st.columns(2)
start = col1.button("Start 🚀")
reset = col2.button("Reset 🔄")

# ------------------------
# Session State
# ------------------------
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


rocket = st.session_state.rocket
history = st.session_state.history

# ------------------------
# Plot placeholder
# ------------------------
chart = st.empty()

# ------------------------
# Simulation Loop
# ------------------------
if st.session_state.running:
    for _ in range(200):

        rocket.step(thrust, dt)
        history.append(rocket.y)

        # ------------------------
        # Plotly Figure (clean look)
        # ------------------------
        fig = go.Figure()

        # Ground
        fig.add_shape(
            type="line",
            x0=0, x1=1,
            y0=0, y1=0,
            line=dict(color="brown", width=3),
            xref="paper"
        )

        # Rocket position (latest point)
        fig.add_trace(go.Scatter(
            x=[0.5],
            y=[rocket.y],
            mode="markers",
            marker=dict(size=20, color="red"),
            name="Rocket"
        ))

        # Trail
        fig.add_trace(go.Scatter(
            x=[0.5]*len(history),
            y=history,
            mode="lines",
            line=dict(color="orange"),
            name="Trajectory"
        ))

        fig.update_layout(
            height=500,
            showlegend=False,
            yaxis=dict(range=[0, 120]),
            xaxis=dict(visible=False),
            title="Rocket Flight"
        )

        chart.plotly_chart(fig, use_container_width=True)

        # Stop condition
        if rocket.y <= 0:
            st.error("💥 Crash / Landing detected")
            st.session_state.running = False
            break

        time.sleep(0.05)

# ------------------------
# Stats
# ------------------------
st.metric("Altitude", f"{rocket.y:.2f} m")
st.metric("Vertical Speed", f"{rocket.vy:.2f} m/s")
