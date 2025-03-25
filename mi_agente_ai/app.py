import sys
from mi_agente_ai.utils.config import load_env_vars
from mi_agente_ai.agents.base_agent import Agent

def main():
    """Función principal que inicializa el agente y permite interactuar con él"""
    
    # Cargar variables de entorno
    if not load_env_vars():
        print("Error al cargar las variables de entorno. Asegúrate de configurar el archivo .env")
        sys.exit(1)
    
    # Inicializar el agente
    print("Inicializando agente...")
    try:
        agent = Agent()
        print("¡Agente listo! Escribe 'salir' para terminar.")
    except Exception as e:
        print(f"Error al inicializar el agente: {str(e)}")
        sys.exit(1)
    
    # Loop de interacción
    while True:
        user_input = input("\n> ")
        
        if user_input.lower() in ["salir", "exit", "quit"]:
            print("¡Hasta luego!")
            break
        
        # Procesar la consulta con el agente
        try:
            result = agent.run(user_input)
            print(f"\nRespuesta: {result.response}")
            
            if result.tool_used and result.tool_result:
                print(f"Resultado de herramienta: {result.tool_result}")
        
        except Exception as e:
            print(f"Error al procesar la consulta: {str(e)}")

if __name__ == "__main__":
    main() 