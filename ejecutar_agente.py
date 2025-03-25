#!/usr/bin/env python3
import os
import subprocess
import sys
import platform

def ejecutar_agente():
    """Ejecuta el agente por línea de comandos, asegurándose de activar el entorno virtual"""
    
    # Detectar sistema operativo para activar el entorno virtual correctamente
    is_windows = platform.system() == "Windows"
    
    # Importa el módulo main
    try:
        # Construir el comando con la activación del entorno virtual
        if is_windows:
            activate_cmd = "venv\\Scripts\\activate.bat && "
            python_cmd = ["cmd", "/c", activate_cmd + "python", "-c", "from mi_agente_ai.app import main; main()"]
        else:
            # Para Unix/MacOS
            activate_cmd = "source ./venv/bin/activate && "
            python_cmd = ["bash", "-c", activate_cmd + "python -c 'from mi_agente_ai.app import main; main()'"]
        
        print("Iniciando el agente por línea de comandos...")
        subprocess.run(python_cmd)
    except ImportError:
        print("Error: No se pudo importar el módulo del agente.")
        print("Asegúrate de que el entorno virtual esté activado:")
        print("  source ./venv/bin/activate   # En Unix/MacOS")
        print("  venv\\Scripts\\activate.bat  # En Windows")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nCerrando el agente...")
    except Exception as e:
        print(f"Error al ejecutar el agente: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    ejecutar_agente() 