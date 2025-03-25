# Mi Agente AI

Asistente virtual basado en Llama 3.3 para Administración Anastópulos que responde consultas sobre consorcios administrados.

## Descripción

Mi Agente AI es un asistente virtual que utiliza el modelo Llama 3.3 70B Versatile de Groq para ofrecer respuestas inteligentes sobre consorcios administrados. El agente, que se presenta como Carlos Zapier, está especializado en proporcionar información precisa sobre licencias y permisos de encargados.

## Requisitos

- Python 3.10 o superior
- Una cuenta en [Groq](https://console.groq.com/) para obtener una API key
- Credenciales de Rukovoditel para acceder a datos de licencias

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tuusuario/mi_agente_ai.git
cd mi_agente_ai
```

### 2. Crear y activar un entorno virtual

```bash
# En Linux/MacOS
python -m venv venv
source venv/bin/activate

# En Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -e .
```

### 4. Configurar variables de entorno

Copia el archivo de ejemplo `.env.example` a `.env`:

```bash
cp .env.example .env
```

Edita el archivo `.env` y añade tus credenciales:

```
GROQ_API_KEY=tu_api_key_de_groq
RUKOVODITEL_API_KEY=tu_api_key_de_rukovoditel_aqui
RUKOVODITEL_USER=tu_usuario_de_rukovoditel
RUKOVODITEL_PASSWORD=tu_contraseña_de_rukovoditel
```

## Ejecución

### Interfaz Web (Recomendada)

```bash
# Activar entorno virtual (si no está activado)
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Ejecutar la interfaz web
python streamlit_directo.py
```

La interfaz web estará disponible en [http://127.0.0.1:8501](http://127.0.0.1:8501)

### Interfaz de Consola

```bash
# Activar entorno virtual (si no está activado)
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Ejecutar la interfaz de consola
python ejecutar_agente.py
```

## Estructura del Proyecto

```
mi_agente_ai/
├── .env                   # Variables de entorno (API keys) - No incluido en el repositorio
├── .env.example           # Ejemplo de archivo de variables de entorno
├── ejecutar_agente.py     # Script para ejecutar el agente en consola
├── streamlit_directo.py   # Script para ejecutar la interfaz web con Streamlit
├── setup.py               # Configuración de instalación del paquete
└── mi_agente_ai/          # Paquete principal
    ├── agents/            # Implementación de agentes
    │   ├── base_agent.py  # Agente básico con Pydantic AI
    │   └── __init__.py
    ├── tools/             # Herramientas utilizadas por los agentes
    │   ├── consulta_licencias_encargados.py # Herramienta para consultar licencias
    │   └── __init__.py
    ├── ui/                # Interfaz de usuario
    │   ├── app.py         # Aplicación Streamlit
    │   └── __init__.py
    ├── utils/             # Utilidades generales
    │   ├── config.py      # Carga de configuración y variables de entorno
    │   └── __init__.py
    ├── models/            # Modelos de datos
    │   ├── schema.py      # Esquemas de datos para la aplicación
    │   └── __init__.py
    ├── app.py             # Punto de entrada para la versión de consola
    └── requirements.txt   # Dependencias del proyecto
```

## Componentes Principales

### Agente Carlos Zapier

El componente central es el `Agent` definido en `mi_agente_ai/agents/base_agent.py`. Este agente utiliza Pydantic AI con el modelo Llama 3.3 70B Versatile de Groq para procesar consultas y generar respuestas. Características principales:

- Personificación como Carlos Zapier, empleado de Administración Anastópulos
- Inicialización del modelo Llama 3.3 70B Versatile a través de Groq
- Configuración de temperatura (1.0) para respuestas naturales
- Integración con la herramienta de consulta de licencias y encargados
- Manejo de errores y formateo consistente de respuestas

### Herramientas

El agente cuenta con la siguiente herramienta:

**Consulta de Licencias y Encargados**: En `mi_agente_ai/tools/consulta_licencias_encargados.py`. Permite al agente consultar información específica sobre licencias y permisos de encargados. Características:
   - Conexión segura a la API de Rukovoditel mediante credenciales
   - Consulta de registros de la entidad 43 (Pasantías)
   - Visualización detallada de resultados en formato tabular
   - Transformación de IDs de campos a nombres descriptivos
   - Soporte para filtros personalizados
   - Metadatos detallados sobre la consulta

### Interfaz de Usuario

Hay dos interfaces disponibles:

1. **Interfaz de Consola**: Implementada en `mi_agente_ai/app.py`, permite interactuar con el agente desde la terminal.

2. **Interfaz Web**: Implementada en `mi_agente_ai/ui/app.py` utilizando Streamlit, ofrece:
   - Interfaz de chat con historial de mensajes
   - Visualización estructurada de resultados de la herramienta de consulta
   - Vista tabular y detallada de registros obtenidos
   - Manejo de errores con retroalimentación visual
   - Carga de variables de entorno con opciones alternativas

## Desarrollo Futuro

Áreas para expansión:

1. Mejorar las capacidades de consulta de la herramienta actual
2. Implementar herramientas adicionales para la gestión de consorcios
3. Mejorar la persistencia del historial de conversaciones
4. Añadir soporte para consultas más específicas sobre administración de edificios

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo LICENSE para más detalles. 