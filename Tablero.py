import streamlit as st
from streamlit_drawable_canvas import st_canvas

st.title("🎨 Zona Creativa: Dibuja lo que imagines")

with st.sidebar:
    st.subheader("Propiedades del Tablero")

    # Canvas dimensions (más grande)
    st.subheader("Dimensiones del Tablero")
    canvas_width = st.slider("Ancho del tablero", 600, 1200, 900, 50)
    canvas_height = st.slider("Alto del tablero", 400, 900, 600, 50)

    # Drawing mode selector
    drawing_mode = st.selectbox(
        "Herramienta de Dibujo:",
        ("freedraw", "line", "rect", "circle", "transform", "polygon", "point"),
    )

    # Stroke width slider
    stroke_width = st.slider("Selecciona el ancho de línea", 1, 30, 15)

    # Selector de color (solo blanco y morado)
    color_option = st.selectbox("Color de trazo", ("Blanco", "Morado"))
    stroke_color = "#FFFFFF" if color_option == "Blanco" else "#8000FF"

    # Background color
    bg_color = st.color_picker("Color de fondo", "#000000")

# Create a canvas component with dynamic key
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=canvas_height,
    width=canvas_width,
    drawing_mode=drawing_mode,
    key=f"canvas_{canvas_width}_{canvas_height}",
)
