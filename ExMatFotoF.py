import streamlit as st
import math
import base64
import json
import hashlib
from datetime import datetime
import numpy as np # Keep if you plan to use it for future calculations, though not strictly needed for these 5 questions based on your description.

# --- Constantes ---
TOLERANCIA = 0.05 # Tolerancia de +/- 0.05 para las respuestas

# --- Diccionario de imágenes por pregunta ---
# Las claves son los índices de las preguntas (0 a 4 para preguntas 1 a 5)
# Los valores son las rutas a tus archivos de imagen.
# ASEGÚRATE de que estas rutas sean correctas y que las imágenes existan en tu proyecto.
# Ejemplo: si tienes una carpeta 'images' en el mismo nivel que examen_online.py
#          y dentro tienes 'grafica_desplazamiento.png', la ruta sería 'images/grafica_desplazamiento.png'
pregunta_imagenes = {
    0: "images/graficadesplazamiento.jpg", # Para la Pregunta 1 (Desplazamiento vs. Tiempo)
    1: "images/graficadesplazamiento.jpg", # Para la Pregunta 2 (Desplazamiento vs. Tiempo)
    2: "images/graficadesplazamiento.jpg", # Para la Pregunta 3 (Desplazamiento vs. Tiempo)
    3: "images/graficavelocidad.jpg",     # Para la Pregunta 4 (Velocidad vs. Tiempo)
    4: "images/graficavelocidad.jpg"      # Para la Pregunta 5 (Velocidad vs. Tiempo)
}


# --- Funciones Auxiliares ---

def redondear_a_2_decimales(numero):
    """
    Redondea un número a 2 decimales y lo formatea como un float con dos decimales.
    Si es None, inf, o nan, devuelve None.
    """
    if numero is None or math.isinf(numero) or math.isnan(numero):
        return None
    try:
        return float(f"{numero:.2f}")
    except (TypeError, ValueError): # Manejar casos donde el número no es convertible a float
        return None

def calcular_respuestas_matematicas(clave):
    """
    Calcula las respuestas correctas para cada pregunta.
    DEBES AGREGAR AQUÍ LAS RESPUESTAS MANUALMENTE PARA CADA CLAVE.
    """
    respuestas = {}
    
    # Si la clave es inválida, inicializa todas las respuestas como None
    if not isinstance(clave, int) or clave <= 0:
        for i in range(1, 6): # Solo 5 preguntas ahora
            respuestas[f'pregunta{i}'] = None
        return respuestas

    # --- INSTRUCCIONES IMPORTANTES PARA AGREGAR TUS RESPUESTAS ---
    # Para cada pregunta, define un bloque 'if-elif-else' basado en el valor de 'clave'.
    # Asigna la respuesta correcta a `respuestas['preguntaX']`.
    # Asegúrate de usar `redondear_a_2_decimales()` para mantener la consistencia.

    # Ejemplo para una posible clave:
    # if clave == 10:
    #     respuestas['pregunta1'] = redondear_a_2_decimales(15.50)
    #     respuestas['pregunta2'] = redondear_a_2_decimales(3.20)
    #     respuestas['pregunta3'] = redondear_a_2_decimales(8.00)
    #     respuestas['pregunta4'] = redondear_a_2_decimales(2.50)
    #     respuestas['pregunta5'] = redondear_a_2_decimales(50.00)
    # elif clave == 20:
    #     respuestas['pregunta1'] = redondear_a_2_decimales(25.00)
    #     respuestas['pregunta2'] = redondear_a_2_decimales(4.50)
    #     respuestas['pregunta3'] = redondear_a_2_decimales(12.00)
    #     respuestas['pregunta4'] = redondear_a_2_decimales(1.00)
    #     respuestas['pregunta5'] = redondear_a_2_decimales(75.00)
    # else:
    #     # Define un valor por defecto o un error si la clave no tiene respuestas predefinidas
    #     respuestas['pregunta1'] = None 
    #     respuestas['pregunta2'] = None
    #     respuestas['pregunta3'] = None
    #     respuestas['pregunta4'] = None
    #     respuestas['pregunta5'] = None


    # --- COMIENZA AQUÍ A AGREGAR TUS RESPUESTAS PARA CADA CLAVE ---
    if clave == 1:
        respuestas['pregunta1'] = redondear_a_2_decimales(3.00)  # Ejemplo
        respuestas['pregunta2'] = redondear_a_2_decimales(3.00)   # Ejemplo
        respuestas['pregunta3'] = redondear_a_2_decimales(3.00)   # Ejemplo
        respuestas['pregunta4'] = redondear_a_2_decimales(4.00)   # Ejemplo
        respuestas['pregunta5'] = redondear_a_2_decimales(2.00)  # Ejemplo
    elif clave == 2:
        respuestas['pregunta1'] = redondear_a_2_decimales(6.00)  # Ejemplo
        respuestas['pregunta2'] = redondear_a_2_decimales(3.00)   # Ejemplo
        respuestas['pregunta3'] = redondear_a_2_decimales(6.00)   # Ejemplo
        respuestas['pregunta4'] = redondear_a_2_decimales(4.00)   # Ejemplo
        respuestas['pregunta5'] = redondear_a_2_decimales(6.00)  # Ejemplo
    elif clave == 3:
        respuestas['pregunta1'] = redondear_a_2_decimales(7.00)  # Ejemplo
        respuestas['pregunta2'] = redondear_a_2_decimales(2.33)   # Ejemplo
        respuestas['pregunta3'] = redondear_a_2_decimales(5.00)  # Ejemplo
        respuestas['pregunta4'] = redondear_a_2_decimales(-3.00)   # Ejemplo
        respuestas['pregunta5'] = redondear_a_2_decimales(6.50)  # Ejemplo
    elif clave == 4:
        respuestas['pregunta1'] = redondear_a_2_decimales(8.00)  # Ejemplo
        respuestas['pregunta2'] = redondear_a_2_decimales(2.00)   # Ejemplo
        respuestas['pregunta3'] = redondear_a_2_decimales(4.00)   # Ejemplo
        respuestas['pregunta4'] = redondear_a_2_decimales(-3.00)   # Ejemplo
        respuestas['pregunta5'] = redondear_a_2_decimales(3.50)  # Ejemplo
    elif clave == 5:
        respuestas['pregunta1'] = redondear_a_2_decimales(11.00)  # Ejemplo
        respuestas['pregunta2'] = redondear_a_2_decimales(2.20)   # Ejemplo
        respuestas['pregunta3'] = redondear_a_2_decimales(7.00)   # Ejemplo
        respuestas['pregunta4'] = redondear_a_2_decimales(5.00)   # Ejemplo
        respuestas['pregunta5'] = redondear_a_2_decimales(4.50)  # Ejemplo
    elif clave == 6:
        respuestas['pregunta1'] = redondear_a_2_decimales(12.00)  # Ejemplo
        respuestas['pregunta2'] = redondear_a_2_decimales(2.00)   # Ejemplo
        respuestas['pregunta3'] = redondear_a_2_decimales(8.00)  # Ejemplo
        respuestas['pregunta4'] = redondear_a_2_decimales(3.00)   # Ejemplo
        respuestas['pregunta5'] = redondear_a_2_decimales(8.50)  # Ejemplo
    elif clave == 7:
        respuestas['pregunta1'] = redondear_a_2_decimales(13.00)  # Ejemplo
        respuestas['pregunta2'] = redondear_a_2_decimales(1.86)   # Ejemplo
        respuestas['pregunta3'] = redondear_a_2_decimales(7.00)   # Ejemplo
        respuestas['pregunta4'] = redondear_a_2_decimales(-3.00)   # Ejemplo
        respuestas['pregunta5'] = redondear_a_2_decimales(8.50)  # Ejemplo
    elif clave == 8:
        respuestas['pregunta1'] = redondear_a_2_decimales(15.00)  # Ejemplo
        respuestas['pregunta2'] = redondear_a_2_decimales(1.89)   # Ejemplo
        respuestas['pregunta3'] = redondear_a_2_decimales(5.00)  # Ejemplo
        respuestas['pregunta4'] = redondear_a_2_decimales(-3.00)   # Ejemplo
        respuestas['pregunta5'] = redondear_a_2_decimales(5.50)  # Ejemplo
    elif clave == 9:
        respuestas['pregunta1'] = redondear_a_2_decimales(17.00)  # Ejemplo
        respuestas['pregunta2'] = redondear_a_2_decimales(1.89)   # Ejemplo
        respuestas['pregunta3'] = redondear_a_2_decimales(3.00)   # Ejemplo
        respuestas['pregunta4'] = redondear_a_2_decimales(-1.00)   # Ejemplo
        respuestas['pregunta5'] = redondear_a_2_decimales(3.50)  # Ejemplo
    elif clave == 10:
        respuestas['pregunta1'] = redondear_a_2_decimales(18.00)  # Ejemplo
        respuestas['pregunta2'] = redondear_a_2_decimales(1.80)   # Ejemplo
        respuestas['pregunta3'] = redondear_a_2_decimales(2.00)   # Ejemplo
        respuestas['pregunta4'] = redondear_a_2_decimales(3.00)   # Ejemplo
        respuestas['pregunta5'] = redondear_a_2_decimales(4.50)  # Ejemplo
    elif clave == 11:
        respuestas['pregunta1'] = redondear_a_2_decimales(19.00)  # Ejemplo
        respuestas['pregunta2'] = redondear_a_2_decimales(1.73)   # Ejemplo
        respuestas['pregunta3'] = redondear_a_2_decimales(1.00)  # Ejemplo
        respuestas['pregunta4'] = redondear_a_2_decimales(-5.00)   # Ejemplo
        respuestas['pregunta5'] = redondear_a_2_decimales(3.50)  # Ejemplo
        elif clave == 12:
        respuestas['pregunta1'] = redondear_a_2_decimales(19.00)  # Ejemplo
        respuestas['pregunta2'] = redondear_a_2_decimales(1.58)   # Ejemplo
        respuestas['pregunta3'] = redondear_a_2_decimales(1.00)   # Ejemplo
        respuestas['pregunta4'] = redondear_a_2_decimales(1.00)   # Ejemplo
        respuestas['pregunta5'] = redondear_a_2_decimales(1.50)  # Ejemplo
    elif clave == 13:
        respuestas['pregunta1'] = redondear_a_2_decimales(21.00)  # Ejemplo
        respuestas['pregunta2'] = redondear_a_2_decimales(1.62)   # Ejemplo
        respuestas['pregunta3'] = redondear_a_2_decimales(3.00)  # Ejemplo
        respuestas['pregunta4'] = redondear_a_2_decimales(1.00)   # Ejemplo
        respuestas['pregunta5'] = redondear_a_2_decimales(2.50)  # Ejemplo
    elif clave == 14:
        respuestas['pregunta1'] = redondear_a_2_decimales(22.00)  # Ejemplo
        respuestas['pregunta2'] = redondear_a_2_decimales(1.57)   # Ejemplo
        respuestas['pregunta3'] = redondear_a_2_decimales(4.00)   # Ejemplo
        respuestas['pregunta4'] = redondear_a_2_decimales(5.00)   # Ejemplo
        respuestas['pregunta5'] = redondear_a_2_decimales(5.50)  # Ejemplo
    elif clave == 15:
        respuestas['pregunta1'] = redondear_a_2_decimales(24.00)  # Ejemplo
        respuestas['pregunta2'] = redondear_a_2_decimales(1.60)   # Ejemplo
        respuestas['pregunta3'] = redondear_a_2_decimales(6.00)   # Ejemplo
        respuestas['pregunta4'] = redondear_a_2_decimales(-2.00)   # Ejemplo
        respuestas['pregunta5'] = redondear_a_2_decimales(7.00)  # Ejemplo
    elif clave == 16:
        respuestas['pregunta1'] = redondear_a_2_decimales(26.00)  # Ejemplo
        respuestas['pregunta2'] = redondear_a_2_decimales(1.63)   # Ejemplo
        respuestas['pregunta3'] = redondear_a_2_decimales(8.00)  # Ejemplo
        respuestas['pregunta4'] = redondear_a_2_decimales(-2.00)   # Ejemplo
        respuestas['pregunta5'] = redondear_a_2_decimales(5.00)  # Ejemplo
    elif clave == 17:
        respuestas['pregunta1'] = redondear_a_2_decimales(27.00)  # Ejemplo
        respuestas['pregunta2'] = redondear_a_2_decimales(1.59)   # Ejemplo
        respuestas['pregunta3'] = redondear_a_2_decimales(7.00)   # Ejemplo
        respuestas['pregunta4'] = redondear_a_2_decimales(3.00)   # Ejemplo
        respuestas['pregunta5'] = redondear_a_2_decimales(5.50)  # Ejemplo
    elif clave == 18:
        respuestas['pregunta1'] = redondear_a_2_decimales(28.00)  # Ejemplo
        respuestas['pregunta2'] = redondear_a_2_decimales(1.56)   # Ejemplo
        respuestas['pregunta3'] = redondear_a_2_decimales(6.00)  # Ejemplo
        respuestas['pregunta4'] = redondear_a_2_decimales(3.00)   # Ejemplo
        respuestas['pregunta5'] = redondear_a_2_decimales(8.50)  # Ejemplo
    elif clave == 19:
        respuestas['pregunta1'] = redondear_a_2_decimales(30.00)  # Ejemplo
        respuestas['pregunta2'] = redondear_a_2_decimales(1.58)   # Ejemplo
        respuestas['pregunta3'] = redondear_a_2_decimales(4.00)   # Ejemplo
        respuestas['pregunta4'] = redondear_a_2_decimales(-6.00)   # Ejemplo
        respuestas['pregunta5'] = redondear_a_2_decimales(7.00)  # Ejemplo
    elif clave == 20:
        respuestas['pregunta1'] = redondear_a_2_decimales(31.00)  # Ejemplo
        respuestas['pregunta2'] = redondear_a_2_decimales(1.55)   # Ejemplo
        respuestas['pregunta3'] = redondear_a_2_decimales(3.00)   # Ejemplo
        respuestas['pregunta4'] = redondear_a_2_decimales(2.00)   # Ejemplo
        respuestas['pregunta5'] = redondear_a_2_decimales(5.00)  # Ejemplo
    elif clave == 21:
        respuestas['pregunta1'] = redondear_a_2_decimales(33.00)  # Ejemplo
        respuestas['pregunta2'] = redondear_a_2_decimales(1.57)   # Ejemplo
        respuestas['pregunta3'] = redondear_a_2_decimales(1.00)  # Ejemplo
        respuestas['pregunta4'] = redondear_a_2_decimales(-5.00)   # Ejemplo
        respuestas['pregunta5'] = redondear_a_2_decimales(3.50)  # Ejemplo
    elif clave == 22:
        respuestas['pregunta1'] = redondear_a_2_decimales(34.00)  # Ejemplo
        respuestas['pregunta2'] = redondear_a_2_decimales(1.55)   # Ejemplo
        respuestas['pregunta3'] = redondear_a_2_decimales(2.00)   # Ejemplo
        respuestas['pregunta4'] = redondear_a_2_decimales(5.00)   # Ejemplo
        respuestas['pregunta5'] = redondear_a_2_decimales(3.50)  # Ejemplo
    elif clave == 23:
        respuestas['pregunta1'] = redondear_a_2_decimales(36.00)  # Ejemplo
        respuestas['pregunta2'] = redondear_a_2_decimales(1.57)   # Ejemplo
        respuestas['pregunta3'] = redondear_a_2_decimales(4.00)  # Ejemplo
        respuestas['pregunta4'] = redondear_a_2_decimales(-2.00)   # Ejemplo
        respuestas['pregunta5'] = redondear_a_2_decimales(5.00)  # Ejemplo
    elif clave == 24:
        respuestas['pregunta1'] = redondear_a_2_decimales(37.00)  # Ejemplo
        respuestas['pregunta2'] = redondear_a_2_decimales(1.54)   # Ejemplo
        respuestas['pregunta3'] = redondear_a_2_decimales(5.00)   # Ejemplo
        respuestas['pregunta4'] = redondear_a_2_decimales(4.00)   # Ejemplo
        respuestas['pregunta5'] = redondear_a_2_decimales(6.00)  # Ejemplo
    elif clave == 25:
        respuestas['pregunta1'] = redondear_a_2_decimales(38.00)  # Ejemplo
        respuestas['pregunta2'] = redondear_a_2_decimales(1.52)   # Ejemplo
        respuestas['pregunta3'] = redondear_a_2_decimales(4.00)   # Ejemplo
        respuestas['pregunta4'] = redondear_a_2_decimales(-4.00)   # Ejemplo
        respuestas['pregunta5'] = redondear_a_2_decimales(6.00)  # Ejemplo
    elif clave == 26:
        respuestas['pregunta1'] = redondear_a_2_decimales(40.00)  # Ejemplo
        respuestas['pregunta2'] = redondear_a_2_decimales(1.54)   # Ejemplo
        respuestas['pregunta3'] = redondear_a_2_decimales(6.00)  # Ejemplo
        respuestas['pregunta4'] = redondear_a_2_decimales(6.00)   # Ejemplo
        respuestas['pregunta5'] = redondear_a_2_decimales(7.00)  # Ejemplo
    elif clave == 27:
        respuestas['pregunta1'] = redondear_a_2_decimales(41.00)  # Ejemplo
        respuestas['pregunta2'] = redondear_a_2_decimales(1.52)   # Ejemplo
        respuestas['pregunta3'] = redondear_a_2_decimales(5.00)  # Ejemplo
        respuestas['pregunta4'] = redondear_a_2_decimales(-5.00)   # Ejemplo
        respuestas['pregunta5'] = redondear_a_2_decimales(7.50)  # Ejemplo
    else:
        # Si la clave no está predefinida, todas las respuestas serán None
        for i in range(1, 6):
            respuestas[f'pregunta{i}'] = None
    # --- TERMINA AQUÍ DE AGREGAR TUS RESPUESTAS PARA CADA CLAVE ---

    return respuestas

def codificar_calificacion(datos_calificacion):
    json_data = json.dumps(datos_calificacion)
    encoded_data = base64.b64encode(json_data.encode('utf-8')).decode('utf-8')
    return encoded_data

# --- Lógica de la Aplicación Streamlit ---

st.title("Comprobación sobre gráficas")

# Inicialización de session_state (es crucial para mantener el estado entre interacciones)
if 'nombre_alumno' not in st.session_state:
    st.session_state.nombre_alumno = ""
if 'clave_alumno' not in st.session_state:
    st.session_state.clave_alumno = None
if 'preguntas_list' not in st.session_state:
    st.session_state.preguntas_list = []
if 'respuestas_estudiante_guardadas' not in st.session_state:
    st.session_state.respuestas_estudiante_guardadas = []
if 'pregunta_actual_idx' not in st.session_state:
    st.session_state.pregunta_actual_idx = 0
if 'examen_iniciado' not in st.session_state:
    st.session_state.examen_iniciado = False
if 'examen_finalizado' not in st.session_state:
    st.session_state.examen_finalizado = False
if 'respuestas_correctas_calc' not in st.session_state:
    st.session_state.respuestas_correctas_calc = {}
if 'final_dat_content' not in st.session_state:
    st.session_state.final_dat_content = None
if 'final_filename' not in st.session_state:
    st.session_state.final_filename = None


# --- Pantalla de Inicio ---
if not st.session_state.examen_iniciado:
    st.write("¡Bienvenido a la comprobación de gráficas!")
    nombre_input = st.text_input("Por favor, ingresa tu nombre completo:", key="nombre_entrada")
    clave_input = st.text_input("Ingresa tu número de clave (un entero POSITIVO):", type="password", key="clave_entrada")

    if st.button("Iniciar Comprobación"):
        if not nombre_input:
            st.error("Por favor, ingresa tu nombre.")
            st.stop() # Detener ejecución para que el error sea visible
        try:
            clave = int(clave_input)
            if clave <= 0:
                st.error("La clave debe ser un número entero POSITIVO.")
                st.stop()
        except ValueError:
            st.error("Número de clave inválido. Ingresa un número entero.")
            st.stop()

        st.session_state.nombre_alumno = nombre_input
        st.session_state.clave_alumno = clave
        st.session_state.examen_iniciado = True
        st.session_state.respuestas_correctas_calc = calcular_respuestas_matematicas(clave)
        
        # Textos de las preguntas. Nota: no se usa LaTeX en este caso para los valores de 'clave' directamente en la string,
        # pero Streamlit permite Markdown, por lo que puedes usar `$` para LaTeX si lo necesitas para el símbolo 's'.
        st.session_state.preguntas_list = [
            f"1) Dada la gráfica de desplazamiento vs tiempo que se presenta a continuación, encuentre la distancia recorrida desde 0 s hasta **{clave} s**.",
            f"2) Dada la gráfica de desplazamiento vs tiempo que se presenta a continuación, encuentre la rapidez media desde 0 s hasta **{clave} s**.",
            f"3) Dada la gráfica de desplazamiento vs tiempo que se presenta a continuación, encuentre el desplazamiento total desde 0 s hasta **{clave} s**.",
            f"4) Dada la gráfica de velocidad vs tiempo que se presenta a continuación, encuentre la aceleración en el intervalo **{clave}**.",
            f"5) Dada la gráfica de velocidad vs tiempo que se presenta a continuación, encuentre la distancia recorrida en el intervalo **{clave}**."
        ]
        st.rerun()

# --- Pantalla del Examen ---
elif st.session_state.examen_iniciado and not st.session_state.examen_finalizado:
    st.header(f"¡Hola, {st.session_state.nombre_alumno}!")
    st.subheader(f"Clave de examen: {st.session_state.clave_alumno}")

    if st.session_state.pregunta_actual_idx < len(st.session_state.preguntas_list):
        pregunta_idx = st.session_state.pregunta_actual_idx
        pregunta_actual_text = st.session_state.preguntas_list[pregunta_idx]
        st.markdown(f"**Pregunta {pregunta_idx + 1} de {len(st.session_state.preguntas_list)}:**")
        st.markdown(pregunta_actual_text)

        # --- Mostrar imagen asociada a la pregunta, si existe ---
        if pregunta_idx in pregunta_imagenes:
            try:
                st.image(pregunta_imagenes[pregunta_idx], caption=f"Imagen para la Pregunta {pregunta_idx + 1}", use_container_width=True)
                st.markdown("---") # Separador visual
            except FileNotFoundError:
                st.warning(f"Error: La imagen para la pregunta {pregunta_idx + 1} ({pregunta_imagenes[pregunta_idx]}) no se encontró. Asegúrate de que la ruta sea correcta.")
            except Exception as e:
                st.warning(f"Error al cargar la imagen para la pregunta {pregunta_idx + 1}: {e}")

        # --- Inputs de la respuesta numérica (siempre uno en este caso) ---
        respuestas_ingresadas_actuales = []
        input_val = st.text_input("Tu respuesta (ej. 1.00):", key=f"respuesta_{pregunta_idx}_0")
        respuestas_ingresadas_actuales.append(input_val)

        st.markdown("---") # Separador visual

        if st.button("Siguiente Pregunta"):
            st.session_state.respuestas_estudiante_guardadas.append({
                "pregunta_idx": pregunta_idx,
                "respuestas_ingresadas": respuestas_ingresadas_actuales
            })
            st.session_state.pregunta_actual_idx += 1
            st.rerun()
    else:
        # --- Finalizar Examen ---
        calificacion = 0
        detalles_respuestas = []
        total_preguntas_validas_para_calificar = 0

        for i, respuesta_guardada in enumerate(st.session_state.respuestas_estudiante_guardadas):
            pregunta_idx = respuesta_guardada['pregunta_idx']
            respuestas_usuario_str_list = respuesta_guardada['respuestas_ingresadas'] 
            
            respuesta_correcta_actual = st.session_state.respuestas_correctas_calc.get(f'pregunta{pregunta_idx + 1}')

            es_correcta_esta_pregunta = False # Inicialmente asumimos que es incorrecta
            respuestas_usuario_num = [] # Para almacenar las respuestas numéricas para el log detallado

            if respuesta_correcta_actual is not None:
                # Todas tus preguntas tienen una sola respuesta numérica
                if len(respuestas_usuario_str_list) == 1:
                    try:
                        usuario_val = float(respuestas_usuario_str_list[0])
                        respuestas_usuario_num.append(round(usuario_val, 2)) # Redondeo para el registro
                        if abs(round(usuario_val, 2) - respuesta_correcta_actual) <= TOLERANCIA:
                            es_correcta_esta_pregunta = True
                    except ValueError:
                        # Si no es un número válido, es incorrecta
                        pass 
                
                # Solo contar la pregunta si se pudo intentar calificar (es decir, si había una respuesta correcta predefinida)
                if respuesta_correcta_actual is not None:
                    total_preguntas_validas_para_calificar += 1

            if es_correcta_esta_pregunta:
                calificacion += 1

            # Formatear la respuesta_ingresada para el archivo .dat
            respuesta_ingresada_formateada = respuestas_usuario_str_list[0] if respuestas_usuario_str_list else ""


            detalles_respuestas.append({
                "pregunta": st.session_state.preguntas_list[pregunta_idx],
                "respuesta_ingresada": respuesta_ingresada_formateada,
                "respuestas_ingresadas_num": respuestas_usuario_num, # Guarda el valor numérico (redondeado)
                "respuesta_correcta_esperada": respuesta_correcta_actual,
                "es_correcta": es_correcta_esta_pregunta,
            })

        # Preparar datos para el HASH
        datos_para_hash = {
            "nombre_estudiante": st.session_state.nombre_alumno,
            "clave_ingresada": st.session_state.clave_alumno,
            "calificacion_obtenida": calificacion,
            "total_preguntas_examinadas": len(st.session_state.preguntas_list),
            "total_preguntas_validas_para_calificar": total_preguntas_validas_para_calificar,
            "fecha_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "respuestas_detalles": detalles_respuestas
        }

        datos_json_str = json.dumps(datos_para_hash, sort_keys=True)
        hash_sha256 = hashlib.sha256(datos_json_str.encode('utf-8')).hexdigest()

        datos_finales_para_guardar = datos_para_hash.copy()
        datos_finales_para_guardar["hash_sha256_integridad"] = hash_sha256

        # Generar el archivo .dat codificado y guardarlo en session_state para descarga persistente
        st.session_state.final_dat_content = codificar_calificacion(datos_finales_para_guardar)
        st.session_state.final_filename = f"calificacion_{st.session_state.nombre_alumno.replace(' ', '_')}_{st.session_state.clave_alumno}.dat"

        # Mostrar mensaje de finalización
        st.session_state.examen_finalizado = True
        st.rerun()

# --- Pantalla de Examen Finalizado ---
elif st.session_state.examen_finalizado:
    st.success(f"¡Gracias por completar el examen, {st.session_state.nombre_alumno}!")
    st.write("Tu examen ha terminado. Por favor, descarga tu archivo de calificación y envíaselo a tu profesor.")
    
    if st.session_state.final_dat_content and st.session_state.final_filename:
        st.download_button(
            label="Descargar Archivo de Calificación (.dat)",
            data=st.session_state.final_dat_content.encode('utf-8'),
            file_name=st.session_state.final_filename,
            mime="application/octet-stream"
        )
    else:
        st.warning("No se pudo generar el archivo de descarga. Por favor, contacta a tu profesor.")
    
    st.write("Puedes cerrar esta pestaña del navegador.")
    st.info("Para realizar el examen de nuevo, cierra y vuelve a abrir esta pestaña.")