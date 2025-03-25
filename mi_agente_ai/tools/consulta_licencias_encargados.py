from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List, Union
import requests
import json
import os
import datetime
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener credenciales
API_KEY = os.getenv("RUKOVODITEL_API_KEY")
USER = os.getenv("RUKOVODITEL_USER")
PASSWORD = os.getenv("RUKOVODITEL_PASSWORD")
API_URL = "https://www.anastopulos.ar/ingresar/api/rest.php"

class ConsultaLicenciasEncargadosInput(BaseModel):
    """Entrada para la herramienta de consulta de licencias de encargados"""
    entity_id: int = Field(43, description="ID de la entidad a consultar")
    reports_id: Optional[int] = Field(3930, description="ID del reporte a utilizar")
    limit: int = Field(10, description="Límite de registros a obtener")
    select_fields: str = Field("651,665,653,912", description="IDs de campos a seleccionar, separados por comas")
    filters: Optional[Dict[str, Any]] = Field(None, description="Filtros adicionales para la consulta")

class ConsultaLicenciasEncargadosOutput(BaseModel):
    """Salida de la herramienta de consulta de licencias de encargados"""
    resultado: Dict[str, Any] = Field(..., description="Datos procesados de la respuesta")
    metadata: Dict[str, Any] = Field(..., description="Metadatos de la consulta")

def _obtener_nombre_campo(campo_id):
    """
    Obtiene el nombre descriptivo de un campo según su ID.
    Este mapping contiene los campos específicos de las licencias de encargados.
    """
    campo_mapping = {
        "651": "Fecha de inicio",
        "665": "Fecha Finalización",
        "653": "Reincorporación",
        "912": "Empleado"
    }
    return campo_mapping.get(str(campo_id), f"Campo {campo_id}")

def transformar_respuesta(response_data):
    """
    Transforma la respuesta de la API en un formato más útil para ser consumido por el LLM.
    Elimina campos de sistema y ordena los datos para mejor comprensión.
    
    Args:
        response_data: Respuesta de la API
        
    Returns:
        Dict: Datos transformados con información de licencias de encargados en orden lógico
    """
    if not response_data or "status" not in response_data:
        return {
            "error": "Respuesta inválida de la API"
        }
        
    if response_data["status"] != "success":
        return {
            "error": response_data.get("error", "Error desconocido al consultar la API")
        }
    
    # Procesar datos exitosos
    registros = response_data.get("data", [])
    
    # Preparar registros con nombres de campos descriptivos y orden específico
    registros_procesados = []
    
    for registro in registros:
        # Nuevo diccionario vacío para el registro procesado
        registro_procesado = {}
        
        # 1. Primero agregamos el empleado si existe
        for key, value in registro.items():
            if key == "912":  # ID del campo Empleado
                registro_procesado["Empleado"] = value
                break
        
        # 2. Luego agregamos las fechas en orden específico
        # Fecha de inicio
        if "651" in registro:
            registro_procesado["Fecha de inicio"] = registro["651"]
            
        # Fecha Finalización
        if "665" in registro:
            registro_procesado["Fecha Finalización"] = registro["665"]
            
        # Reincorporación
        if "653" in registro:
            registro_procesado["Reincorporación"] = registro["653"]
        
        # 3. Agregar cualquier otro campo que no sea de sistema y que no hayamos procesado aún
        for key, value in registro.items():
            if key not in ["id", "date_added", "date_updated", "created_by", "parent_item_id", 
                          "912", "651", "665", "653"]:
                nombre_campo = _obtener_nombre_campo(key)
                registro_procesado[nombre_campo] = value
        
        registros_procesados.append(registro_procesado)
    
    return {
        "registros": registros_procesados
    }

def consulta_licencias_encargados(input_data: ConsultaLicenciasEncargadosInput) -> ConsultaLicenciasEncargadosOutput:
    """
    Herramienta que consulta licencias y permisos de encargados en el sistema Rukovoditel.
    Permite obtener información detallada sobre las licencias, incluyendo fechas y empleados.
    
    Args:
        input_data: Datos para realizar la consulta
        
    Returns:
        Respuesta transformada de la consulta
    """
    # Verificar que tenemos las credenciales
    if not API_KEY or not USER or not PASSWORD:
        return ConsultaLicenciasEncargadosOutput(
            resultado={
                "error": "Faltan credenciales de Rukovoditel"
            },
            metadata={
                "success": False,
                "timestamp": datetime.datetime.now().isoformat(),
                "error": "Configuración incompleta"
            }
        )
    
    # Registrar hora de inicio
    inicio = datetime.datetime.now()
    
    # Construir parámetros
    params = {
        "key": API_KEY,
        "username": USER,
        "password": PASSWORD,
        "action": "select",
        "entity_id": input_data.entity_id,
        "limit": input_data.limit,
        "select_fields": input_data.select_fields,
    }
    
    # Añadir reports_id si está especificado
    if input_data.reports_id:
        params["reports_id"] = input_data.reports_id
    
    # Añadir filtros si hay
    if input_data.filters:
        params["filters"] = input_data.filters
    
    try:
        # Realizar la petición
        response = requests.post(API_URL, data=params, timeout=15)
        
        # Verificar si la respuesta es exitosa
        response.raise_for_status()
        
        # Intentar parsear la respuesta como JSON
        try:
            response_data = response.json()
            
            # Calcular tiempo de respuesta
            fin = datetime.datetime.now()
            tiempo_respuesta = (fin - inicio).total_seconds() * 1000  # Convertir a milisegundos
            
            # Transformar la respuesta
            resultado_transformado = transformar_respuesta(response_data)
            
            # Devolver el resultado
            return ConsultaLicenciasEncargadosOutput(
                resultado=resultado_transformado,
                metadata={
                    "success": response_data.get("status") == "success",
                    "entity_id": input_data.entity_id,
                    "reports_id": input_data.reports_id,
                    "response_time_ms": round(tiempo_respuesta),
                    "timestamp": fin.isoformat(),
                    "limit": input_data.limit,
                    "select_fields": input_data.select_fields,
                    "record_count": len(resultado_transformado.get("registros", []))
                }
            )
            
        except json.JSONDecodeError:
            # Si la respuesta no es JSON válido
            return ConsultaLicenciasEncargadosOutput(
                resultado={
                    "error": "La respuesta de la API no es JSON válido"
                },
                metadata={
                    "success": False,
                    "timestamp": datetime.datetime.now().isoformat(),
                    "error": "Error al decodificar JSON",
                    "response_text": response.text[:200] + "..." if len(response.text) > 200 else response.text
                }
            )
    
    except requests.exceptions.RequestException as e:
        # En caso de error con la petición
        return ConsultaLicenciasEncargadosOutput(
            resultado={
                "error": f"Error al comunicarse con la API: {str(e)}"
            },
            metadata={
                "success": False,
                "timestamp": datetime.datetime.now().isoformat(),
                "error": str(e)
            }
        ) 