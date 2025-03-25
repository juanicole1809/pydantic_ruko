#!/usr/bin/env python3
"""
Script de prueba para la herramienta de consulta de licencias y encargados.
Este script prueba la herramienta de forma aislada antes de usarla con el agente.
"""
import sys
import os
import json
from pprint import pprint

# Añadir el directorio raíz al path para poder importar los módulos
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Importar la herramienta
from mi_agente_ai.tools.consulta_licencias_encargados import consulta_licencias_encargados, ConsultaLicenciasEncargadosInput

def mostrar_campo_mapping():
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

def probar_herramienta(entity_id=43, reports_id=3930, limit=10, select_fields="651,665,653,912", filters=None):
    """
    Prueba la herramienta de consulta de licencias con los parámetros dados
    """
    print(f"\n{'='*80}")
    print(f"Probando consulta de licencias de encargados:")
    print(f"  Entidad: {entity_id} (Pasantías/Licencias)")
    print(f"  Reporte: {reports_id}")
    print(f"  Límite: {limit} registros")
    print(f"  Campos: {select_fields}")
    if filters:
        print(f"  Filtros: {filters}")
    print(f"{'='*80}")
    
    # Crear la entrada para la herramienta
    input_data = ConsultaLicenciasEncargadosInput(
        entity_id=entity_id,
        reports_id=reports_id,
        limit=limit,
        select_fields=select_fields,
        filters=filters
    )
    
    # Ejecutar la herramienta
    resultado = consulta_licencias_encargados(input_data)
    
    # Mostrar resultado
    print("\nResultado:")
    if "error" in resultado.resultado:
        print(f"Error: {resultado.resultado['error']}")
    else:
        registros = resultado.resultado.get("registros", [])
        print(f"Se encontraron {len(registros)} licencias de encargados:")
        
        for i, registro in enumerate(registros):
            print(f"\n--- Licencia {i+1} ---")
            
            # La información ya viene ordenada, simplemente la mostramos
            for campo, valor in registro.items():
                print(f"{campo}: {valor}")
            
    print("\nMetadatos:")
    print(f"  Éxito: {'Sí' if resultado.metadata.get('success', False) else 'No'}")
    print(f"  Tiempo de respuesta: {resultado.metadata.get('response_time_ms', 0)} ms")
    print(f"  Timestamp: {resultado.metadata.get('timestamp', 'N/A')}")
    print(f"  Registros encontrados: {resultado.metadata.get('record_count', 0)}")
    
    return resultado

if __name__ == "__main__":
    # Mostrar mapping de campos
    mostrar_campo_mapping()
    
    # Probar con los parámetros predeterminados
    print("\nPRUEBA 1: Consulta predeterminada")
    probar_herramienta()
    
    # Probar con límite diferente
    print("\nPRUEBA 2: Consulta con límite reducido")
    probar_herramienta(limit=3)
    
    # Probar con diferentes campos
    print("\nPRUEBA 3: Consulta con diferentes campos")
    probar_herramienta(select_fields="651,912")
    
    print("\nTodas las pruebas completadas.") 