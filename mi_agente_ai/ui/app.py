import streamlit as st
import sys
import os
import traceback
import json
import pandas as pd
import threading
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError

# Agregar el directorio raíz del proyecto al path para importaciones
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Ahora importamos usando rutas relativas
from mi_agente_ai.agents.base_agent import Agent
from mi_agente_ai.utils.config import load_env_vars

# Configuración de la página
st.set_page_config(
    page_title="Mi Agente AI",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Cargar variables de entorno
api_key_loaded = load_env_vars()

if not api_key_loaded:
    st.error("Error al cargar las variables de entorno. Asegúrate de configurar el archivo .env con GROQ_API_KEY")
    
    # Mostrar información de depuración
    st.warning("Información de depuración:")
    st.code(f"GROQ_API_KEY presente: {'Sí' if os.getenv('GROQ_API_KEY') else 'No'}")
    st.code(f"Directorio actual: {os.getcwd()}")
    
    # Ofrecer una forma de introducir la API key manualmente
    st.subheader("Puedes proporcionar la API key temporalmente:")
    api_key = st.text_input("GROQ API Key", type="password")
    
    if api_key:
        os.environ["GROQ_API_KEY"] = api_key
        st.success("API key configurada temporalmente. Puedes continuar usando la aplicación.")
        st.button("Continuar", on_click=lambda: None)
    else:
        st.stop()

# Inicializar el agente (solo una vez)
@st.cache_resource
def get_agent():
    try:
        return Agent()
    except Exception as e:
        st.error(f"Error al inicializar el agente: {str(e)}")
        st.code(traceback.format_exc())
        return None

# Función para generar respuesta con timeout
def generate_response(prompt, timeout_seconds=65):  # 65 segundos (ligeramente mayor que el timeout del agente)
    agent = get_agent()
    if agent is None:
        # Crear un objeto con la misma estructura que devuelve el agente
        error_obj = {
            "response": "No se pudo inicializar el agente. Revisa los errores anteriores.", 
            "tool_used": False, 
            "tool_result": None
        }
        # Convertir a un objeto similar al que devuelve el agente
        return type('AgentResponse', (), error_obj)
    
    # Utilizando ThreadPoolExecutor para implementar el timeout
    with ThreadPoolExecutor() as executor:
        future = executor.submit(agent.run, prompt)
        try:
            return future.result(timeout=timeout_seconds)
        except FutureTimeoutError:
            # Crear un objeto de respuesta para el timeout
            timeout_obj = {
                "response": "Lo siento, la consulta ha tomado demasiado tiempo en procesarse. Por favor, intenta con una pregunta más específica sobre licencias de encargados o consorcios administrados.", 
                "tool_used": False, 
                "tool_result": None
            }
            return type('AgentResponse', (), timeout_obj)

# Título
st.title("🤖 Mi Agente AI")
st.markdown("Conversa con Carlos Zapier, agente especializado en licencias de encargados")

# Información sobre capacidades del agente
with st.expander("ℹ️ ¿Qué puedo consultar?"):
    st.markdown("""
    **Carlos Zapier** es un asistente especializado en responder consultas sobre:
    
    - Licencias y permisos de encargados de consorcios
    - Información sobre fechas de inicio, finalización y reincorporación
    - Consultas específicas sobre empleados y sus licencias
    
    **No puede responder** consultas sobre otros temas no relacionados con su área de especialidad.
    
    Para obtener los mejores resultados, haz preguntas específicas sobre licencias de encargados.
    """)

# Inicializar historial de chat si no existe
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes del chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Área de entrada para el usuario
if prompt := st.chat_input("Pregúntame sobre licencias de encargados..."):
    # Agregar mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Mostrar mensaje del usuario
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Mostrar mensaje del asistente
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        with st.spinner("Pensando..."):
            try:
                # Obtener respuesta (ya tiene manejo de timeout incorporado)
                result = generate_response(prompt)
                response = result.response
                
                # Procesar el resultado de la herramienta
                if result.tool_used and result.tool_result:
                    try:
                        tool_result = json.loads(result.tool_result)
                        
                        # Si es un resultado de la herramienta de consulta de licencias
                        if "registros" in tool_result:
                            st.subheader(f"Registros encontrados: {len(tool_result['registros'])}")
                            
                            tab1, tab2 = st.tabs(["Vista tabla", "Vista detallada"])
                            
                            with tab1:
                                if tool_result["registros"]:
                                    # Preparar datos para la tabla
                                    # Extrae campos relevantes (excluyendo campos de sistema)
                                    campos_a_ignorar = ["Fecha de creación", "Última actualización"]
                                    all_fields = set()
                                    for reg in tool_result["registros"]:
                                        # Solo considerar campos que no son de sistema
                                        relevant_fields = {k for k in reg.keys() if k not in campos_a_ignorar}
                                        all_fields.update(relevant_fields)
                                    
                                    # Orden preferido de campos
                                    orden_preferido = ["Empleado", "Fecha de inicio", "Fecha Finalización", "Reincorporación"]
                                    # Ordenar campos: primero los de orden_preferido, luego el resto alfabéticamente
                                    campos_ordenados = [campo for campo in orden_preferido if campo in all_fields]
                                    campos_restantes = sorted([campo for campo in all_fields if campo not in orden_preferido])
                                    campos_ordenados.extend(campos_restantes)
                                    
                                    # Crear una lista de diccionarios para el DataFrame
                                    table_data = []
                                    for reg in tool_result["registros"]:
                                        # Omitir campos de sistema en la vista de tabla
                                        row = {field: reg.get(field, "") for field in campos_ordenados}
                                        table_data.append(row)
                                    
                                    # Mostrar como DataFrame de pandas
                                    if table_data:
                                        st.dataframe(pd.DataFrame(table_data))
                                else:
                                    st.info("No se encontraron registros.")
                            
                            with tab2:
                                for i, reg in enumerate(tool_result["registros"]):
                                    # Determinar título significativo para el expander
                                    titulo = f"Registro {i+1}"
                                    if "Empleado" in reg:
                                        titulo = f"{reg['Empleado']}"
                                    
                                    with st.expander(titulo):
                                        # Mostrar campos en orden específico (sin campos de sistema)
                                        # Primero mostrar Empleado si existe
                                        if "Empleado" in reg:
                                            st.write("**Empleado:**", reg["Empleado"])
                                        
                                        # Luego mostrar las fechas importantes
                                        fechas = ["Fecha de inicio", "Fecha Finalización", "Reincorporación"]
                                        for campo in fechas:
                                            if campo in reg:
                                                st.write(f"**{campo}:**", reg[campo])
                                        
                                        # Finalmente mostrar otros campos (que no sean de sistema)
                                        campos_a_ignorar = ["Fecha de creación", "Última actualización", "Empleado"] + fechas
                                        for key, value in reg.items():
                                            if key not in campos_a_ignorar:
                                                st.write(f"**{key}:**", value)
                            
                            # Mostrar metadata
                            with st.expander("Metadata de la consulta"):
                                st.write("**Entidad:** ", tool_result.get("metadata", {}).get("entity_id", "No disponible"))
                                st.write("**Reporte:** ", tool_result.get("metadata", {}).get("reports_id", "No disponible"))
                                st.write("**Éxito:** ", "Sí" if tool_result.get("metadata", {}).get("success", False) else "No")
                                st.write("**Registros solicitados:** ", tool_result.get("metadata", {}).get("limit", "No disponible"))
                                st.write("**Tiempo de respuesta:** ", f"{tool_result.get('metadata', {}).get('response_time_ms', 0)} ms")
                                st.write("**Fecha de consulta:** ", tool_result.get("metadata", {}).get("timestamp", "No disponible"))
                        
                        # Si es un error de la herramienta de consulta de licencias
                        elif "error" in tool_result:
                            st.error(f"Error en la consulta: {tool_result['error']}")
                            
                            # Mostrar metadata si está disponible
                            if "metadata" in tool_result:
                                with st.expander("Metadata de la consulta"):
                                    for key, value in tool_result["metadata"].items():
                                        st.write(f"**{key}:** {value}")
                        
                        # Otros tipos de resultados
                        else:
                            st.json(tool_result)
                    except Exception as e:
                        st.error(f"Error al procesar el resultado de la herramienta: {str(e)}")
                        st.code(result.tool_result)
                
                message_placeholder.markdown(response)
                
                # Agregar mensaje del asistente al historial
                full_content = response
                if result.tool_used and result.tool_result:
                    full_content += f"\n\n*Información adicional disponible en la interfaz*"
                    
                st.session_state.messages.append({"role": "assistant", "content": full_content})
            except Exception as e:
                error_message = f"Error al procesar la consulta: {str(e)}"
                st.error(error_message)
                st.code(traceback.format_exc())
                message_placeholder.markdown(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})

# Botón para borrar el historial
if st.sidebar.button("Borrar conversación"):
    st.session_state.messages = []
    st.rerun()

# Información en el sidebar
st.sidebar.markdown("## Acerca del Agente")
st.sidebar.markdown("**Carlos Zapier** es un asistente virtual de Administración Anastópulos.")
st.sidebar.markdown("Especializado en consultas sobre licencias de encargados de consorcios.")
st.sidebar.markdown("Utiliza Llama 3.3 70B Versatile vía Groq y Pydantic AI.")
st.sidebar.markdown("---")
st.sidebar.markdown("Desarrollado con ❤️ para Administración Anastópulos")

# Añadir también ejemplos de consultas útiles
st.sidebar.markdown("## Ejemplos de consultas")
ejemplos = [
    "¿Qué licencias tuvo Daniel Viola?",
    "Muéstrame las licencias que terminan en enero 2023",
    "¿Cuándo se reincorporó Celestino Ayvar?",
    "¿Quién estuvo de licencia en octubre 2022?"
]

for ejemplo in ejemplos:
    if st.sidebar.button(ejemplo):
        # Simular que el usuario escribió el ejemplo
        st.session_state.messages.append({"role": "user", "content": ejemplo})
        st.rerun()