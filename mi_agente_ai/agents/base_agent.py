from pydantic_ai import Agent as PydanticAgent
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import os
import json

from mi_agente_ai.tools.consulta_licencias_encargados import ConsultaLicenciasEncargadosInput, ConsultaLicenciasEncargadosOutput, consulta_licencias_encargados

class Agent:
    """Agente básico usando Pydantic AI con Groq"""
    
    def __init__(self):
        """Inicializa el agente de Pydantic AI"""
        
        # Creamos el modelo de salida usando Pydantic
        class AgentOutput(BaseModel):
            response: str = Field(..., description="La respuesta generada para el usuario")
            tool_used: Optional[bool] = Field(False, description="Si se utilizó alguna herramienta")
            tool_result: Optional[str] = Field(None, description="El resultado de la herramienta si se utilizó")
        
        # Configuramos e inicializamos el agente de Pydantic AI
        self.agent = PydanticAgent(
            model="groq:llama-3.3-70b-versatile",  # Modelo Llama 3.3 70B Versatile
            result_type=AgentOutput,
            system_prompt=(
                "Eres Carlos Zapier, un empleado de Administración Anastópulos encargado de responder cualquier consulta "
                "sobre los consorcios que Administración Anastópulos administra. Siempre respondes en español de manera cordial y profesional. "
                "Tu trabajo es ayudar a los clientes con información precisa sobre licencias y permisos de encargados. "
                "Cuando necesitas consultar datos sobre licencias y permisos, utilizas la herramienta de consulta_licencias_encargados. "
                "Esta herramienta te permite consultar registros de la entidad 43 (Pasantías) donde puedes ver información como fechas de inicio, "
                "finalización y reincorporación, así como nombres de empleados. "
                "\n\nIMPORTANTE: Si te preguntan sobre información que no está relacionada con licencias de encargados o consorcios, "
                "debes indicar amablemente que no puedes ayudar con esa consulta específica ya que tu función se limita a "
                "brindar información sobre licencias y permisos de encargados de los consorcios administrados por Administración Anastópulos. "
                "No inventes ni improvises respuestas sobre temas fuera de tu área de competencia. Simplemente indícale al usuario que "
                "para ese tipo de consultas debería contactar a otro departamento o servicio apropiado. "
                "\n\nTambién, si te solicitan información sobre consorcios específicos pero no puedes encontrarla con tus herramientas, "
                "debes ser honesto e indicar que no tienes acceso a esa información en este momento, y sugerir que contacte "
                "directamente a la administración para obtener datos más precisos. Siempre trata de ser útil y directo en tus respuestas."
            ),
            tools=[consulta_licencias_encargados],
            model_settings={"temperature": 1.0}  # Temperatura ajustada a 1 usando model_settings
        )
    
    def run(self, prompt: str):
        """
        Ejecuta el agente con la consulta del usuario
        
        Args:
            prompt: La consulta del usuario
            
        Returns:
            La respuesta generada y posibles resultados de herramientas
        """
        try:
            # Llamar al agente de Pydantic AI con un timeout
            result = self.agent.run_sync(prompt, timeout=60)  # Timeout de 60 segundos
            
            # Crear un objeto con la estructura esperada por la UI
            result_dict = {
                "response": result.data.response if hasattr(result.data, 'response') else str(result.data),
                "tool_used": False,
                "tool_result": None
            }
            
            # Procesar el resultado de la herramienta si existe
            if hasattr(result.data, 'tool_used') and result.data.tool_used and hasattr(result.data, 'tool_result'):
                result_dict["tool_used"] = True
                
                # Si el resultado de la herramienta es un objeto, convertirlo a JSON
                if isinstance(result.data.tool_result, dict):
                    # Ya es un diccionario
                    tool_result = result.data.tool_result
                else:
                    # Intenta convertir a diccionario si es una cadena
                    try:
                        tool_result = json.loads(result.data.tool_result)
                    except:
                        # Si no es JSON, mantenerlo como está
                        tool_result = {"result": str(result.data.tool_result)}
                
                # Convertir el resultado a formato JSON para la UI
                result_dict["tool_result"] = json.dumps(tool_result, ensure_ascii=False)
            
            # Devolver el resultado en el formato esperado
            return type('AgentResponse', (), result_dict)
        except Exception as e:
            # En caso de error, devolver una respuesta genérica
            print(f"Error al procesar la solicitud: {str(e)}")
            error_response = {
                "response": f"Lo siento, ocurrió un error: {str(e)}",
                "tool_used": False,
                "tool_result": None
            }
            return type('AgentResponse', (), error_response) 