import streamlit as st
import sys
import os
import traceback
import json

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

# Función para generar respuesta
def generate_response(prompt):
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
    
    return agent.run(prompt)

# Título
st.title("🤖 Mi Agente AI")
st.markdown("Conversa con un agente de IA que usa Pydantic AI + Groq")

# Inicializar historial de chat si no existe
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes del chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Área de entrada para el usuario
if prompt := st.chat_input("Escribe tu mensaje aquí..."):
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
                result = generate_response(prompt)
                response = result.response
                
                if result.tool_used and result.tool_result:
                    # Crear un contenedor para mostrar el resultado de la herramienta
                    tool_container = st.container()
                    with tool_container:
                        st.markdown("### 🔍 Resultado de búsqueda")
                        
                        # Intentar parsear el resultado como JSON
                        try:
                            tool_data = json.loads(result.tool_result)
                            
                            # Mostrar el resultado principal
                            if "result" in tool_data:
                                st.info(tool_data["result"])
                            
                            # Mostrar la fecha de consulta si existe
                            if "fecha_consulta" in tool_data:
                                st.caption(f"📅 Fecha de consulta: {tool_data['fecha_consulta']}")
                        except Exception as json_error:
                            # Si no se puede parsear como JSON, mostrar como texto plano
                            st.info(result.tool_result)
                            st.caption("No se pudo extraer información adicional")
                
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
st.sidebar.markdown("Este agente está basado en el modelo Llama 3 de Groq.")
st.sidebar.markdown("Utiliza Pydantic AI como framework para estructurar la información.")
st.sidebar.markdown("---")
st.sidebar.markdown("Desarrollado con ❤️ usando Streamlit") 