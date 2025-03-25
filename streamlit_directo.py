#!/usr/bin/env python3
"""
Script directo para ejecutar Streamlit sin comandos complejos de shell.

Uso:
    1. Activa el entorno virtual:
       source ./venv/bin/activate
    
    2. Ejecuta el script:
       python streamlit_directo.py

Este script configurará automáticamente el PYTHONPATH y ejecutará
la aplicación Streamlit en http://127.0.0.1:8501
"""
import streamlit.web.cli as stcli
import os
import sys
import traceback

def main():
    """Función principal que ejecuta la aplicación Streamlit"""
    try:
        # Obtener la ruta del archivo app.py
        app_path = os.path.join(os.path.dirname(__file__), "mi_agente_ai", "ui", "app.py")
        
        if not os.path.exists(app_path):
            print(f"Error: No se encontró el archivo {app_path}")
            print("Verifica que la estructura del proyecto sea correcta.")
            return 1
        
        # Añadir el directorio actual al PYTHONPATH
        current_dir = os.path.abspath(os.path.dirname(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        
        # Verificar que el archivo .env exista
        env_path = os.path.join(current_dir, ".env")
        if not os.path.exists(env_path):
            print(f"Advertencia: No se encontró el archivo .env en {env_path}")
            print("Es posible que necesites configurar GROQ_API_KEY manualmente en la interfaz.")
        
        print(f"Ejecutando Streamlit para: {app_path}")
        print(f"PYTHONPATH configurado a: {current_dir}")
        print("Abre tu navegador en: http://127.0.0.1:8501")
        
        # Configurar argumentos para Streamlit
        sys.argv = [
            "streamlit", "run",
            app_path,
            "--server.address=127.0.0.1",
            "--server.port=8501",
            "--server.headless=true"
        ]
        
        # Ejecutar Streamlit directamente
        stcli.main()
        return 0
    
    except KeyboardInterrupt:
        print("\nCerrando la aplicación...")
        return 0
    except Exception as e:
        print(f"Error al ejecutar Streamlit: {str(e)}")
        print("\nDetalles del error:")
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main()) 