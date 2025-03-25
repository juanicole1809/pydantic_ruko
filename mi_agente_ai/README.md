# Mi Agente AI

Un agente de lenguaje estructurado basado en Pydantic AI utilizando el modelo Llama 3 de Groq.

## Estructura del Proyecto

```
mi_agente_ai/
├── app.py                     # punto de entrada CLI
├── agents/                   # definición del agente
├── tools/                    # herramientas del agente
├── models/                   # modelos Pydantic para input/output
├── services/                 # llamadas a APIs externas (si las hubiera)
├── utils/                    # funciones auxiliares
├── ui/                       # interfaz de usuario con Streamlit
└── .env                      # clave de API (no se sube al repo)
```

## Instalación

1. Clona este repositorio
2. Crea un entorno virtual:
   ```
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```
3. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```
4. Configura el archivo `.env`:
   ```
   GROQ_API_KEY=tu_clave_api_aqui
   ```

## Uso

### Interfaz de línea de comandos

Ejecuta el agente en la línea de comandos con:

```
./ejecutar_agente.py
```

Escribe tu consulta en el prompt y el agente responderá. Escribe 'salir' para terminar la sesión.

### Interfaz web con Streamlit

Para una experiencia más amigable, utiliza la interfaz web con Streamlit:

```
./ejecutar_streamlit.py
```

Esto abrirá una interfaz web donde podrás interactuar con el agente de manera más visual.

## Desarrollo

El proyecto utiliza:
- Pydantic AI para la estructura del agente
- Groq como proveedor del modelo Llama 3
- Streamlit para la interfaz web
- Herramientas simples extensibles 