import os
import pathlib
from dotenv import load_dotenv

def load_env_vars():
    """Carga las variables de entorno desde el archivo .env"""
    # Intentar cargar desde varias ubicaciones posibles
    # 1. Directorio actual
    # 2. Directorio raíz del proyecto
    # 3. Directorio padre
    
    # Directorio actual
    if os.path.exists('.env'):
        load_dotenv()
    
    # Directorio del proyecto
    project_dir = pathlib.Path(__file__).parent.parent
    env_path = project_dir / '.env'
    if os.path.exists(env_path):
        load_dotenv(dotenv_path=env_path)
    
    # Directorio padre (para el caso de estructura anidada)
    parent_dir = project_dir.parent
    parent_env_path = parent_dir / '.env'
    if os.path.exists(parent_env_path):
        load_dotenv(dotenv_path=parent_env_path)
    
    # Verificar que la API key está configurada
    if not os.getenv("GROQ_API_KEY"):
        print("ADVERTENCIA: GROQ_API_KEY no está configurada en el archivo .env")
        return False
    
    return True 