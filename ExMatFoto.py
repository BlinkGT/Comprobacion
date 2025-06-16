import streamlit as st
import math
import base64
import json
import hashlib
from datetime import datetime
import numpy as np

# --- Constantes ---
TOLERANCIA = 0.05 # Tolerancia de +/- 0.05 para las respuestas

# --- Diccionario de imágenes por pregunta ---
# Las claves son los índices de las preguntas (0 a 9 para preguntas 1 a 10)
# Los valores son las rutas a tus archivos de imagen.
# ASEGÚRATE de que estas rutas sean correctas y que las imágenes existan en tu proyecto.
# Ejemplo: si tienes una carpeta 'images' en el mismo nivel que examen_online.py
#          y dentro tienes 'diagrama_q3.png', la ruta sería 'images/diagrama_q3.png'
pregunta_imagenes = {
    # Ejemplo (descomenta y ajusta si quieres usar):
     0: "images/0.jpg",  # Para la Pregunta 1
     1: "images/1.jpg",  # Para la Pregunta 2 (suma de polinomios)
    # 5: "ruta/a/tu/imagen_pregunta6.png",  # Para la Pregunta 6 (división de polinomios)
    # 8: "ruta/a/tu/imagen_pregunta9.gif",  # Para la Pregunta 9 (raíces cúbicas)
    # 9: "ruta/a/tu/imagen_pregunta10.webp" # Para la Pregunta 10 (raíces cuárticas)
    
    # Aquí puedes añadir las imágenes que deseas para cada pregunta
    # Por ejemplo, si tienes una imagen para la pregunta 3 llamada "diagrama_q3.png" en la misma carpeta:
    # 2: "diagrama_q3.png", # Índice 2 corresponde a la Pregunta 3
    # Y así sucesivamente para otras preguntas...
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
    """Calcula las respuestas correctas para cada pregunta de matemáticas."""
    respuestas = {}
    
    if not isinstance(clave, int) or clave <= 0:
        for i in range(1, 11):
            respuestas[f'pregunta{i}'] = None
        return respuestas

    # Pregunta 1: Resuelve x + "clave" = 7
    respuestas['pregunta1'] = redondear_a_2_decimales(7 - clave)

    # Pregunta 2: Resuelve x^2 - "clave"x - 5 = 0, responde con la suma de ambas raíces.
    respuestas['pregunta2'] = redondear_a_2_decimales(float(clave))

    # Pregunta 3: Suma de polinomios: (x^3 + 7x^2 + 5x - 4) + (clave x^3 + clave x^2 + clave x - clave)
    # P1: [1, 7, 5, -4]
    # P2: [clave, clave, clave, -clave]
    # Resultado: [(1+clave), (7+clave), (5+clave), (-4-clave)]
    respuestas['pregunta3'] = [
        redondear_a_2_decimales(1 + clave),    # Coeficiente de x^3
        redondear_a_2_decimales(7 + clave),    # Coeficiente de x^2
        redondear_a_2_decimales(5 + clave),    # Coeficiente de x
        redondear_a_2_decimales(-4 - clave)   # Constante
    ]

    # Pregunta 4: Resta de polinomios: (x^3 + 7x^2 + 5x - 4) - (clave x^3 + clave x^2 + clave x - clave)
    # P1: [1, 7, 5, -4]
    # P2: [clave, clave, clave, -clave]
    # Resultado: [(1-clave), (7-clave), (5-clave), (-4+clave)]
    respuestas['pregunta4'] = [
        redondear_a_2_decimales(1 - clave),    # Coeficiente de x^3
        redondear_a_2_decimales(7 - clave),    # Coeficiente de x^2
        redondear_a_2_decimales(5 - clave),    # Coeficiente de x
        redondear_a_2_decimales(-4 + clave)   # Constante
    ]

    # Pregunta 5: Multiplicación de polinomios: (x^2 + 5x + 1)(clave x + clave)
    # P1: [1, 5, 1] (coefs de x^2, x, cte)
    # P2: [clave, clave] (coefs de x, cte)
    # Usamos np.polymul para obtener los coeficientes del resultado
    poly1_coeffs = np.array([1, 5, 1])
    poly2_coeffs = np.array([clave, clave])
    result_coeffs = np.polymul(poly1_coeffs, poly2_coeffs) # -> [clave, 6*clave, 6*clave, clave]
    respuestas['pregunta5'] = [redondear_a_2_decimales(c) for c in result_coeffs] # Coefs de x^3, x^2, x, cte

    # Pregunta 6: División de polinomios: (clave x^2 + x + 1) / (clave x + 1)
    # Cociente y residuo. Queremos los coeficientes del cociente.
    # Si (Ax^2 + x + 1) / (Ax + 1) = x (cociente) con residuo 1, los coeficientes del cociente son [1]
    # Para la expresión dada, el cociente es simplemente x.
    # Devolvemos los coeficientes [1.0, 0.0] para que el alumno ponga el coeficiente de x y la constante.
    respuestas['pregunta6'] = [redondear_a_2_decimales(1.0), redondear_a_2_decimales(0.0)] 

    # Pregunta 7: Desarrolla el producto notable: (clave x + clave)^2
    # (Ax + B)^2 = A^2x^2 + 2ABx + B^2 donde A = clave, B = clave
    # = (clave^2)x^2 + (2*clave^2)x + (clave^2)
    respuestas['pregunta7'] = [
        redondear_a_2_decimales(float(clave**2)), # Coeficiente de x^2
        redondear_a_2_decimales(2 * float(clave**2)), # Coeficiente de x
        redondear_a_2_decimales(float(clave**2))  # Constante
    ]

    # Pregunta 8: Desarrolla el producto notable: (clave x + clave)^3
    # (Ax + B)^3 = A^3x^3 + 3A^2Bx^2 + 3AB^2x + B^3 donde A = clave, B = clave
    # = (clave^3)x^3 + (3*clave^3)x^2 + (3*clave^3)x + (clave^3)
    respuestas['pregunta8'] = [
        redondear_a_2_decimales(float(clave**3)), # Coeficiente de x^3
        redondear_a_2_decimales(3 * float(clave**3)), # Coeficiente de x^2
        redondear_a_2_decimales(3 * float(clave**3)), # Coeficiente de x
        redondear_a_2_decimales(float(clave**3))  # Constante
    ]

    # Pregunta 9: Resuelve x^3 - "clave" = 0, responde con la suma de **raíces reales**.
    # Las raíces de x^3 = C son C^(1/3) (real) y dos complejas conjugadas.
    # La suma de las raíces reales es simplemente esa raíz cúbica de C.
    real_root = clave**(1/3)
    respuestas['pregunta9'] = redondear_a_2_decimales(real_root)

    # Pregunta 10: Resuelve x^4 - "clave" = 0, responde con la multiplicación de raíces reales.
    # Si clave > 0, las raíces reales son +clave^(1/4) y -clave^(1/4). La multiplicación es -sqrt(clave).
    # Si clave = 0, la única raíz real es 0. Multiplicación = 0.
    # Si clave < 0, no hay raíces reales. Multiplicación = 0 (según la aclaración de la pregunta).
    if clave > 0:
        respuestas['pregunta10'] = redondear_a_2_decimales(-math.sqrt(clave))
    else: # clave <= 0
        respuestas['pregunta10'] = redondear_a_2_decimales(0.0) # Si no hay reales o es 0, la multiplicación es 0.

    return respuestas

def codificar_calificacion(datos_calificacion):
    json_data = json.dumps(datos_calificacion)
    encoded_data = base64.b64encode(json_data.encode('utf-8')).decode('utf-8')
    return encoded_data

# --- Lógica de la Aplicación Streamlit ---

st.title("Programa de Examen de Matemáticas")

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
    st.write("¡Bienvenido al examen de matemáticas!")
    nombre_input = st.text_input("Por favor, ingresa tu nombre completo:", key="nombre_entrada")
    clave_input = st.text_input("Ingresa tu número de clave (un entero POSITIVO):", type="password", key="clave_entrada")

    if st.button("Iniciar Examen"):
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
        
        # Textos de las preguntas de matemáticas con LaTeX
        st.session_state.preguntas_list = [
            r"1) Resuelve $x + " + str(clave) + r" = 7$. Responde el valor de $x$. (2 decimales)",
            r"2) Resuelve $x^2 - " + str(clave) + r"x - 5 = 0$. Responde con la suma de ambas raíces. (2 decimales)",
            r"3) Resuelve $(x^3 + 7x^2 + 5x - 4) + (" + str(clave) + r"x^3 + " + str(clave) + r"x^2 + " + str(clave) + r"x - " + str(clave) + r")$. Ingresa los coeficientes del polinomio resultante en orden descendente ($x^3, x^2, x, \text{constante}$). (2 decimales)",
            r"4) Resuelve $(x^3 + 7x^2 + 5x - 4) - (" + str(clave) + r"x^3 + " + str(clave) + r"x^2 + " + str(clave) + r"x - " + str(clave) + r")$. Ingresa los coeficientes del polinomio resultante en orden descendente ($x^3, x^2, x, \text{constante}$). (2 decimales)",
            r"5) Resuelve $(x^2 + 5x + 1)(" + str(clave) + r"x + " + str(clave) + r")$. Ingresa los coeficientes del polinomio resultante en orden descendente ($x^3, x^2, x, \text{constante}$). (2 decimales)",
            r"6) Resuelve $(" + str(clave) + r"x^2 + x + 1) / (" + str(clave) + r"x + 1)$. Ingresa los coeficientes del cociente en orden descendente ($x, \text{constante}$). Si un término no existe, ingresa $0$. (2 decimales)",
            r"7) Desarrolla el producto notable: $(" + str(clave) + r"x + " + str(clave) + r")^2$. Ingresa los coeficientes del polinomio resultante en orden descendente ($x^2, x, \text{constante}$). (2 decimales)",
            r"8) Desarrolla el producto notable: $(" + str(clave) + r"x + " + str(clave) + r")^3$. Ingresa los coeficientes del polinomio resultante en orden descendente ($x^3, x^2, x, \text{constante}$). (2 decimales)",
            r"9) Resuelve $x^3 - " + str(clave) + r" = 0$. Responde con la suma de las raíces **reales**. (2 decimales)",
            r"10) Resuelve $x^4 - " + str(clave) + r" = 0$. Responde con la multiplicación de las raíces **reales**. Si no hay raíces reales, la respuesta es $0.00$. (2 decimales)"
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
                st.warning(f"Error: La imagen para la pregunta {pregunta_idx + 1} ({pregunta_imagenes[pregunta_idx]}) no se encontró.")
            except Exception as e:
                st.warning(f"Error al cargar la imagen para la pregunta {pregunta_idx + 1}: {e}")

        # --- Inputs de la respuesta numérica ---
        respuestas_ingresadas_actuales = []
        
        # Determinar cuántas cajas de entrada y sus etiquetas
        if pregunta_idx in [2, 3, 4, 7]: # Preguntas 3, 4, 5, 8 (índices 2, 3, 4, 7) para polinomios de grado 3
            labels = [r"Coeficiente de $x^3$:", r"Coeficiente de $x^2$:", r"Coeficiente de $x$:", r"Término constante:"]
            num_inputs = 4
        elif pregunta_idx == 5: # Pregunta 6 (índice 5) para polinomio de grado 1 (cociente)
            labels = [r"Coeficiente de $x$:", r"Término constante:"]
            num_inputs = 2
        elif pregunta_idx == 6: # Pregunta 7 (índice 6) para polinomio de grado 2
            labels = [r"Coeficiente de $x^2$:", r"Coeficiente de $x$:", r"Término constante:"]
            num_inputs = 3
        else: # Para preguntas con una sola respuesta (1, 2, 9, 10)
            labels = ["Tu respuesta (ej. 1.00):"]
            num_inputs = 1

        for i in range(num_inputs):
            input_val = st.text_input(labels[i], key=f"respuesta_{pregunta_idx}_{i}")
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
            respuestas_usuario_str_list = respuesta_guardada['respuestas_ingresadas'] # Ahora es una lista de strings
            
            respuesta_correcta_actual = st.session_state.respuestas_correctas_calc.get(f'pregunta{pregunta_idx + 1}')

            es_correcta_esta_pregunta = True # Asumimos que es correcta hasta que se demuestre lo contrario
            respuestas_usuario_num = [] # Para almacenar las respuestas numéricas para el log detallado

            # Solo intentamos calificar si hay una respuesta correcta esperada válida
            if respuesta_correcta_actual is not None:
                # Si la respuesta_correcta_actual es una lista (para polinomios)
                if isinstance(respuesta_correcta_actual, list):
                    if len(respuestas_usuario_str_list) != len(respuesta_correcta_actual):
                        es_correcta_esta_pregunta = False # No coincide el número de inputs
                    else:
                        for j in range(len(respuesta_correcta_actual)):
                            try:
                                usuario_val = float(respuestas_usuario_str_list[j])
                                respuestas_usuario_num.append(round(usuario_val, 2)) # Redondeo para el registro
                                if abs(round(usuario_val, 2) - respuesta_correcta_actual[j]) > TOLERANCIA:
                                    es_correcta_esta_pregunta = False
                                    break # Si una falla, toda la pregunta falla
                            except ValueError:
                                es_correcta_esta_pregunta = False
                                break # Si no es un número, falla
                    
                    if es_correcta_esta_pregunta: # Solo contar si la calificación fue intentada y es posible
                        total_preguntas_validas_para_calificar += 1
                
                # Si la respuesta_correcta_actual es un solo número (para preguntas 1, 2, 9, 10)
                else:
                    if len(respuestas_usuario_str_list) != 1: # Solo debería haber 1 input
                         es_correcta_esta_pregunta = False
                    else:
                        try:
                            usuario_val = float(respuestas_usuario_str_list[0])
                            respuestas_usuario_num.append(round(usuario_val, 2)) # Redondeo para el registro
                            if abs(round(usuario_val, 2) - respuesta_correcta_actual) > TOLERANCIA:
                                es_correcta_esta_pregunta = False
                        except ValueError:
                            es_correcta_esta_pregunta = False
                    
                    if es_correcta_esta_pregunta: # Solo contar si la calificación fue intentada y es posible
                        total_preguntas_validas_para_calificar += 1
            else: # Cuando respuesta_correcta_actual es None (solo para P10 si clave <= 0)
                es_correcta_esta_pregunta = False # Por defecto incorrecta
                # Manejo especial para P10 cuando clave <= 0
                # Si la respuesta correcta esperada es None (multiplicación de raíces reales es 0)
                # Y el alumno ingresó "0.00", entonces es correcta.
                if pregunta_idx == 9 and respuestas_usuario_str_list[0] == "0.00":
                    es_correcta_esta_pregunta = True
                    total_preguntas_validas_para_calificar += 1 # Contar esta pregunta como válida en este caso

            if es_correcta_esta_pregunta:
                calificacion += 1

            # --- Formatear la respuesta_ingresada para el archivo .dat ---
            # Si era una lista de respuestas (para polinomios), las unimos en una cadena
            if isinstance(respuestas_usuario_str_list, list):
                # Unimos los elementos de la lista con una coma y un espacio
                respuesta_ingresada_formateada = ", ".join(respuestas_usuario_str_list)
            else:
                # Si es una sola respuesta (Preguntas 1, 2, 9, 10), ya es una cadena
                respuesta_ingresada_formateada = respuestas_usuario_str_list

            detalles_respuestas.append({
                "pregunta": st.session_state.preguntas_list[pregunta_idx],
                "respuesta_ingresada": respuesta_ingresada_formateada,
                "respuestas_ingresadas_num": respuestas_usuario_num, 
                "respuesta_correcta_esperada": respuesta_correcta_actual,
                "es_correcta": es_correcta_esta_pregunta,
                # No necesitamos guardar la foto adjunta del alumno aquí, ya que el profesor la provee.
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