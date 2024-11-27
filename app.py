import streamlit as st
import os
import json
import pandas as pd

st.set_page_config(
    page_title="Ley Protección de Datos Personales",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Directorios de las carpetas
directories = {
    "articulos": "data/articles/",
    "resumen": "data/summary/",
    "preguntas": "data/questions/"
}

# Leer el archivo CSV y crear un diccionario para mapear los códigos de leyes a sus nombres
laws_df = pd.read_csv('data/laws.csv', delimiter=';')
laws_dict = dict(zip(laws_df['ley'].astype(str), laws_df['nombre']))

# Función para leer archivos JSON de una carpeta y generar un diccionario
def load_json_files(directory):
    json_dict = {}
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                # Carga el contenido del archivo JSON
                json_data = json.load(f)
                # Extrae el nombre del archivo sin extensión para usarlo como clave
                key = filename.replace('.json', '')
                json_dict[key] = json_data
    return json_dict

# Crear los diccionarios para cada tipo
dct_articulos = load_json_files(directories["articulos"])
dct_resumen = load_json_files(directories["resumen"])
dct_preguntas = load_json_files(directories["preguntas"])


# Renombrar diccionarios
dct_articulos = {laws_dict[key]: value for key, value in dct_articulos.items() if key in laws_dict}
dct_resumen = {laws_dict[key]: value for key, value in dct_resumen.items() if key in laws_dict}
dct_preguntas = {laws_dict[key]: value for key, value in dct_preguntas.items() if key in laws_dict}




# Función para mostrar una pregunta y validar la respuesta
def mostrar_pregunta(pregunta, opciones, respuesta_correcta, key):
    st.write(pregunta)
    seleccion = st.radio("Selecciona una opción:", opciones, key=key)  # Asignar key única
    if st.button("Verificar respuesta", key=f"boton_{key}"):
        if seleccion == respuesta_correcta:
            st.success("¡Correcto!")
        else:
            st.error("Incorrecto. La respuesta correcta es: " + respuesta_correcta)



def main():
    """
    Main function to set up the Streamlit app layout.
    """
    cs_sidebar()
    cs_body()
    return None

# Funciones
def cs_sidebar():
    """
    Sidebar con un resumen de la ley de Protección de Datos Personales.
    """
    st.sidebar.title("Protección de Datos Personales")

    # Mostrar logo
    logo_url = "images/hammer.png"
    st.sidebar.image(logo_url, width=200)

    # Objetivos de la Ley de Protección de Datos Personales
    with st.sidebar:
        with st.expander("🎯 Objetivos"):
            st.markdown(
                """
                1. **Garantizar los Derechos de los Titulares**: Asegurar el derecho de acceso, rectificación, cancelación y oposición (ARCO).
                2. **Promover la Transparencia**: Establecer principios claros sobre el tratamiento de datos personales.
                3. **Fortalecer la Confidencialidad**: Proteger la privacidad y seguridad de la información personal.
                4. **Regular el Tratamiento de Datos**: Definir las obligaciones de los responsables y encargados del tratamiento.
                5. **Fomentar la Responsabilidad Proactiva**: Incentivar prácticas organizacionales que garanticen el cumplimiento normativo.
                """
            )

        # Información relevante sobre la Ley de Protección de Datos Personales
        with st.expander("🌐 Información Relevante"):
            st.markdown(
                """
                La Ley de Protección de Datos Personales fue aprobada y despachada al Ejecutivo para su promulgación (Agosto 2024). 
                
                Este nuevo marco regula el tratamiento de datos con estándares de transparencia, calidad y seguridad, y 
                establece los derechos de los titulares, como acceso, rectificación, supresión, oposición, portabilidad y bloqueo.

                > **Más detalles**: [link](https://www.camara.cl/prensa/prensa_cms.aspx?noticia=camara-despacho-a-ley-nuevo-marco-para-el-tratamiento-de-datos-personales)
                """
            )

        # Descripción de la Aplicación
        with st.expander("📌 Descripción de la Aplicación"):
            st.markdown(
                """
                Esta aplicación te guía a través de la **Ley de Protección de Datos Personales** con tres secciones clave:
        
                1. **⚖️ Artículos**: Consulta cada artículo detallado, organizado por títulos.  
                2. **📝 Resumen**: Obtén una visión general con resúmenes por título.  
                3. **🎲 Ejercicios**: Refuerza tu aprendizaje con preguntas interactivas.
        
                > **📝 Nota**: Si deseas explorar las leyes en un formato tipo libro, te invitamos a visitar nuestra página en Quarto:   
                👉 [Ley de Protección de Datos Personales (formato Quarto)](https://seth-nut.github.io/st_proteccion_datos/)
                """
            )



def cs_body():
    """
    Create content sections for the main body of the Streamlit cheat sheet with Python examples.
    """
    st.title("🏛️ Ley Protección de Datos Personales")  # Título de la sección

    # Agregar selectbox en el sidebar
    #ley_seleccionada = st.sidebar.selectbox("✏️ Ley Seleccionada:", list(dct_articulos.keys()))
    ley_seleccionada = "Ley Protección de Datos Personales (T)"

    # Tab menu
    tab1, tab2, tab3 = st.tabs(
        ["⚖️ Artículos", "📝 Resumen", "🎲 Ejercicios"]
    )

    with tab1:
        st.header("Detalles de la Ley")
        #st.subheader(ley_seleccionada)
        # Mostrar los artículos en un expander
        for titulo, articulos in dct_articulos[ley_seleccionada].items():
            with st.expander(titulo):  # Usar expander para cada título
                # Checkboxes para cada artículo dentro del título
                for articulo, contenido in articulos.items():
                    mostrar_articulo = st.checkbox(articulo, key=articulo)
                    if mostrar_articulo:
                        st.write(contenido)

    with tab2:
        st.header("Resumen de la Ley")
        #st.subheader(ley_seleccionada)
        # Iterar sobre el diccionario y mostrar los títulos y descripciones
        for titulo, contenido in dct_resumen[ley_seleccionada].items():
            with st.expander(titulo):  # Usar expander para cada título
                st.markdown("📋 **Artículos**:")
                st.write(", ".join(contenido["articulos"]))  # Mostrar los artículos
                st.markdown("✏️ **Descripción**:")
                st.write(contenido["descripcion"])  # Mostrar la descripción del título

    with tab3:
        # Título del aplicativo
        st.header("Preguntas y Respuestas")
        #st.subheader(ley_seleccionada)
        # Iterar sobre el diccionario y mostrar las preguntas por título
        for titulo, preguntas in dct_preguntas[ley_seleccionada].items():
            with st.expander(titulo):  # Usar expander para cada título
                for idx, pregunta_info in enumerate(preguntas):
                    pregunta = pregunta_info["pregunta"]
                    opciones = pregunta_info["opciones"]
                    respuesta_correcta = pregunta_info["respuesta_correcta"]
                    mostrar_pregunta(pregunta, opciones, respuesta_correcta, key=f"{titulo}_{idx}")

    css = '''
    <style>
        /* Ajusta el tamaño del texto en las pestañas (Tabs) */
        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
            font-size: 1.5rem; /* Tamaño del texto en las pestañas */
        }

        /* Opción adicional: Ajusta el tamaño de los encabezados dentro de los expanders */
        .st-expander h1, .st-expander h2, .st-expander h3 {
            font-size: 4rem; /* Tamaño de los encabezados dentro de los expanders */
        }

        /* Ajustar el tamaño del texto del selectbox en el sidebar */
        .sidebar .stSelectbox label {
            font-size: 1.5rem; /* Ajusta este valor para cambiar el tamaño del texto */
        }

    </style>
    '''

    st.markdown(css, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
