#!/usr/bin/env python3
"""
Script de prueba para realizar una consulta directa a la API de Rukovoditel.
Útil para verificar la conectividad y respuesta de la API antes de usar la herramienta.
"""
import requests
import json
import os
import sys
from pprint import pprint
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

API_KEY = os.getenv("RUKOVODITEL_API_KEY")
USER = os.getenv("RUKOVODITEL_USER")
PASSWORD = os.getenv("RUKOVODITEL_PASSWORD")
API_URL = "https://www.anastopulos.ar/ingresar/api/rest.php"

def consultar_api_rukovoditel(
    entity_id=43, 
    reports_id=3930, 
    limit=10, 
    select_fields="651,665,653,912",
    filters=None
):
    """
    Realiza una consulta directa a la API de Rukovoditel.
    
    Args:
        entity_id: ID de la entidad (43 = Pasantías)
        reports_id: ID del reporte personalizado
        limit: Límite de registros a obtener
        select_fields: IDs de campos a seleccionar (651=Fecha inicio, 665=Fecha límite, etc.)
        filters: Filtros adicionales
        
    Returns:
        dict: Respuesta de la API
    """
    # Verificar que tenemos las credenciales
    if not API_KEY or not USER or not PASSWORD:
        print("Error: Faltan credenciales de Rukovoditel. Verifica el archivo .env")
        return None
    
    # Construir parámetros
    params = {
        "key": API_KEY,
        "username": USER,
        "password": PASSWORD,
        "action": "select",
        "entity_id": entity_id,
        "limit": limit,
        "select_fields": select_fields,
    }
    
    # Añadir reports_id si está especificado
    if reports_id:
        params["reports_id"] = reports_id
    
    # Añadir filtros si hay
    if filters:
        params["filters"] = filters
    
    try:
        # Realizar la petición
        print(f"Enviando petición a {API_URL}")
        print("Parámetros de la consulta:")
        for key, value in params.items():
            if key not in ["key", "password"]:  # No mostrar información sensible
                print(f"  {key}: {value}")
        
        response = requests.post(API_URL, data=params)
        
        # Verificar si la respuesta es exitosa
        response.raise_for_status()
        
        # Intentar parsear la respuesta como JSON
        try:
            return response.json()
        except json.JSONDecodeError:
            print(f"Error: La respuesta no es JSON válido")
            print(f"Respuesta: {response.text[:200]}...")  # Mostrar solo parte de la respuesta
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la petición: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Respuesta: {e.response.text[:200]}...")  # Mostrar solo parte de la respuesta
        return None

def mostrar_mapping_campos():
    """Muestra el mapping de IDs de campos y sus nombres para referencia"""
    campo_mapping = {
        "651": "Fecha de inicio",
        "665": "Fecha Finalización",
        "653": "Reincorporación",
        "912": "Empleado"
    }
    
    print("\nMapping de IDs de campos:")
    for campo_id, nombre in campo_mapping.items():
        print(f"  {campo_id}: {nombre}")

if __name__ == "__main__":
    print(f"{'='*80}")
    print(f"PRUEBA DE CONEXIÓN A LA API DE RUKOVODITEL")
    print(f"{'='*80}")
    
    # Mostrar mapping de campos
    mostrar_mapping_campos()
    
    # Realizar la consulta con los parámetros por defecto
    print("\nConsultando API de Rukovoditel...")
    resultado = consultar_api_rukovoditel()
    
    # Mostrar el resultado
    if resultado:
        print("\nRespuesta recibida:")
        if resultado.get("status") == "success":
            print(f"Estado: ✅ Éxito")
            registros = resultado.get('data', [])
            print(f"Registros obtenidos: {len(registros)}")
            
            if registros:
                print("\nPrimeros registros:")
                for i, registro in enumerate(registros[:3]):  # Mostrar solo los primeros 3
                    print(f"\nRegistro {i+1}:")
                    # Mostrar campos importantes con nombres descriptivos
                    for campo_id, valor in registro.items():
                        if campo_id == "id":
                            print(f"  ID: {valor}")
                        elif campo_id == "date_added":
                            print(f"  Fecha creación: {valor}")
                        elif campo_id == "date_updated":
                            print(f"  Última actualización: {valor}")
                        elif campo_id == "651":
                            print(f"  Fecha de inicio: {valor}")
                        elif campo_id == "665":
                            print(f"  Fecha Finalización: {valor}")
                        elif campo_id == "653":
                            print(f"  Reincorporación: {valor}")
                        elif campo_id == "912":
                            print(f"  Empleado: {valor}")
                        # Otros campos mantienen su ID
                        else:
                            print(f"  Campo {campo_id}: {valor}")
        else:
            print(f"Estado: ❌ Error")
            pprint(resultado)
    
    print("\nPrueba completada.") 