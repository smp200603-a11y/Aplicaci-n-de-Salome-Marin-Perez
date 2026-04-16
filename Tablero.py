import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np
import streamlit as st
from streamlit_drawable_canvas import st_canvas

# -----------------------------
# CONFIGURACIÓN
# -----------------------------
st.set_page_config(
    page_title='Reconocimiento de Dígitos',
    layout='wide'
)

# -----------------------------
# ESTILOS
# -----------------------------
st.markdown("""
    <style>
    .titulo {
        font-size: 45px;
        font-weight: bold;
        color: #00C9A7;
    }
    .subtitulo {
        font-size: 20px;
        color: #CCCCCC;
    }
    .resultado {
        font-size: 40px;
        color: #FFD700;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# CARGAR MODELO UNA VEZ
# -----------------------------
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("model/handwritten.h5")

model = load_model()

# -----------------------------
# FUNCIÓN DE PREDICCIÓN
# -----------------------------
def predictDigit(image):
    # Convertir correctamente de RGBA a escala de grises
    image = image.convert("L")
    image = ImageOps.invert(image)  # importante para fondo negro

    img = image.resize((28, 28))
    img = np.array(img, dtype='float32') / 255.0
    img = img.reshape((1, 28, 28, 1))

    pred = model.predict(img)
    return np.argmax(pred[0])

# -----------------------------
# INTERFAZ
# -----------------------------
st.markdown('<p class="titulo">Reconocimiento de Dígitos</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitulo">Dibuja un número y presiona predecir</p>', unsafe_allow_html=True)

col1, col2 = st.columns([2,1])

with col2:
    st.markdown("### Opciones")
    stroke_width = st.slider('Grosor del trazo', 1, 40, 20)

with col1:
    canvas_result = st_canvas(
        stroke_width=stroke_width,
        stroke_color='#FFFFFF',
        background_color='#000000',
        height=400,   # más grande
        width=400,    # más grande
        drawing_mode="freedraw",
        key="canvas",
    )

# -----------------------------
# BOTONES
# -----------------------------
col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    predecir = st.button('Predecir')

with col_btn2:
    limpiar = st.button('Limpiar')

# -----------------------------
# LÓGICA
# -----------------------------
if predecir:
    if canvas_result.image_data is not None:
        input_array = canvas_result.image_data

        # Convertir a imagen PIL correctamente
        image = Image.fromarray(input_array.astype('uint8'), 'RGBA')

        resultado = predictDigit(image)

        st.markdown(f'<p class="resultado">Resultado: {resultado}</p>', unsafe_allow_html=True)
    else:
        st.warning('Dibuja un número primero.')

# Truco para limpiar canvas (recarga)
if limpiar:
    st.rerun()

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.markdown("## Acerca de")
st.sidebar.write("""
App de reconocimiento de dígitos usando redes neuronales.

Librerías usadas:
- streamlit
- streamlit-drawable-canvas
""")
