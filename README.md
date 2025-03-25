# Mi Agente AI

Asistente virtual basado en Llama 3 utilizando Pydantic AI y Groq.

## Descripción

Mi Agente AI es un asistente virtual que utiliza el modelo Llama 3.3 de Groq para ofrecer respuestas inteligentes. La aplicación integra herramientas personalizadas que permiten al agente realizar búsquedas y proporcionar información sobre diversos temas.

## Requisitos

- Python 3.10 o superior
- Una cuenta en [Groq](https://console.groq.com/) para obtener una API key

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

Edita el archivo `.env` y añade tu API key de Groq:

```
GROQ_API_KEY=tu_api_key_de_groq
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
    │   ├── simple_tool.py # Herramienta de búsqueda simple
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

### Agente

El componente central es el `Agent` definido en `mi_agente_ai/agents/base_agent.py`. Este agente utiliza Pydantic AI con el modelo Llama 3.3 de Groq para procesar consultas y generar respuestas. Características principales:

- Inicialización del modelo Llama 3.3 a través de Groq
- Configuración de temperatura para controlar la creatividad de las respuestas
- Integración con herramientas para expandir sus capacidades
- Manejo de errores y formateo consistente de respuestas

### Herramientas

En `mi_agente_ai/tools/simple_tool.py` se encuentra una herramienta que permite al agente realizar búsquedas simuladas sobre temas específicos. Características:

- Modelo de entrada y salida definido con Pydantic
- Base de datos local con información sobre temas comunes (Python, IA, etc.)
- Respuestas por defecto cuando no hay información disponible
- Inclusión de metadatos como la fecha de consulta

### Interfaz de Usuario

Hay dos interfaces disponibles:

1. **Interfaz de Consola**: Implementada en `mi_agente_ai/app.py`, permite interactuar con el agente desde la terminal.

2. **Interfaz Web**: Implementada en `mi_agente_ai/ui/app.py` utilizando Streamlit, ofrece:
   - Interfaz de chat con historial de mensajes
   - Visualización de resultados de herramientas
   - Manejo de errores con retroalimentación visual
   - Carga de variables de entorno con opciones alternativas

## Contribuir

1. Haz un fork del proyecto
2. Crea una rama para tu funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. Haz commit de tus cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Haz push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

## Desarrollo Futuro

Áreas para expansión:

1. Añadir más herramientas para ampliar las capacidades del agente
2. Implementar integración con APIs externas para datos en tiempo real
3. Mejorar la persistencia del historial de conversaciones
4. Añadir soporte para entradas y salidas multimodales

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo LICENSE para más detalles. 