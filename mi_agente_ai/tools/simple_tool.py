from pydantic import BaseModel, Field
from typing import Optional, List, Dict
import datetime

class SimpleToolInput(BaseModel):
    """Entrada para la herramienta de búsqueda"""
    query: str = Field(..., description="La consulta o término de búsqueda")
    num_results: Optional[int] = Field(3, description="Número de resultados a devolver")

class SimpleToolOutput(BaseModel):
    """Salida de la herramienta de búsqueda"""
    result: str = Field(..., description="Resultado de la búsqueda")
    fecha_consulta: str = Field(..., description="Fecha y hora de la consulta")

def simple_tool(input_data: SimpleToolInput) -> SimpleToolOutput:
    """
    Una herramienta que simula buscar información sobre un tema.
    
    Args:
        input_data: Los datos de entrada para la herramienta, incluye la consulta
        
    Returns:
        Un resumen simulado sobre el tema consultado
    """
    # Obtener la consulta
    query = input_data.query
    
    # Generar un resultado simulado basado en la consulta
    resultados_simulados = {
        "python": "Python es un lenguaje de programación interpretado, de alto nivel y propósito general. Creado por Guido van Rossum, su filosofía de diseño enfatiza la legibilidad del código. Es ampliamente utilizado en análisis de datos, IA, desarrollo web y automatización.",
        "inteligencia artificial": "La Inteligencia Artificial (IA) es la simulación de procesos de inteligencia humana por sistemas informáticos. Incluye aprendizaje, razonamiento y autocorrección. Las aplicaciones actuales incluyen procesamiento de lenguaje natural, visión artificial y aprendizaje automático.",
        "groq": "Groq es una empresa de IA que ofrece modelos de lenguaje de alta velocidad a través de APIs. Se destaca por su baja latencia en inferencia de modelos como Llama y Mixtral. Su infraestructura está optimizada para inferencia rápida y eficiente.",
        "streamlit": "Streamlit es una biblioteca de Python que permite crear aplicaciones web interactivas para ciencia de datos y machine learning con muy pocas líneas de código. Es popular por su simplicidad y facilidad de uso.",
        "llama": "Llama es una serie de modelos de lenguaje de gran tamaño (LLM) desarrollados por Meta AI. Llama 3.3 es la versión más reciente, que destaca por su capacidad multimodal, mejor rendimiento en razonamiento y disponibilidad en múltiples versiones de parámetros.",
    }
    
    # Texto por defecto si no hay información específica
    respuesta_default = f"Sobre '{query}' no tengo información específica en mi base de datos local. Puedo sugerir buscar en fuentes confiables online para información actualizada sobre este tema."
    
    # Buscar palabras clave en la consulta
    resultado = None
    for keyword, info in resultados_simulados.items():
        if keyword.lower() in query.lower():
            resultado = info
            break
    
    # Si no se encontró información específica, usar la respuesta por defecto
    if resultado is None:
        resultado = respuesta_default
    
    # Obtener la fecha y hora actual
    fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return SimpleToolOutput(
        result=resultado,
        fecha_consulta=fecha_actual
    ) 