from pydantic_ai import Agent as PydanticAgent
from pydantic import BaseModel, Field
from typing import List, Optional
import os
import json

from mi_agente_ai.tools.simple_tool import SimpleToolInput, SimpleToolOutput, simple_tool

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
            system_prompt="Eres un asistente útil que responde en español. Utilizas herramientas cuando es necesario para proporcionar información precisa. Cuando una consulta requiere información específica sobre un tema, utiliza la herramienta de búsqueda para obtener datos actualizados. Siempre respondes de manera clara y concisa.",
            tools=[simple_tool],
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
            # Llamar al agente de Pydantic AI
            result = self.agent.run_sync(prompt)
            
            # Crear un objeto con la estructura esperada por la UI
            result_dict = {
                "response": result.data.response if hasattr(result.data, 'response') else str(result.data),
                "tool_used": False,
                "tool_result": None
            }
            
            # Procesar el resultado de la herramienta si existe
            if hasattr(result.data, 'tool_used') and result.data.tool_used and hasattr(result.data, 'tool_result'):
                result_dict["tool_used"] = True
                
                # Si el resultado de la herramienta es un objeto SimpleToolOutput, convertirlo a JSON
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