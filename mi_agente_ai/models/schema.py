from pydantic import BaseModel
from typing import Optional, List

class UserQuery(BaseModel):
    """Modelo para representar una consulta del usuario"""
    text: str

class ToolResponse(BaseModel):
    """Modelo para representar la respuesta de una herramienta"""
    result: str

class AgentResponse(BaseModel):
    """Modelo para representar la respuesta del agente"""
    response: str
    tool_outputs: Optional[List[ToolResponse]] = None 