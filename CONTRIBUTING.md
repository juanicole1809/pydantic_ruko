# Guía de Contribución

¡Gracias por tu interés en contribuir a Mi Agente AI! Este documento contiene información y directrices para ayudarte a contribuir al proyecto.

## Cómo Contribuir

1. **Configura tu entorno de desarrollo**
   
   Sigue las instrucciones de instalación en el README.md para configurar tu entorno local.

2. **Busca problemas o crea uno**
   
   - Revisa los problemas existentes para ver si hay algo en lo que te gustaría trabajar.
   - Si tienes una idea nueva, crea un problema para discutirla antes de comenzar a trabajar.

3. **Crea un fork y una rama**
   
   ```bash
   # Crea un fork en GitHub y luego clona tu fork
   git clone https://github.com/tu-usuario/mi_agente_ai.git
   cd mi_agente_ai
   
   # Crea una rama para tu contribución
   git checkout -b feature/nombre-descriptivo
   ```

4. **Haz los cambios**
   
   Implementa tus cambios siguiendo las convenciones de estilo del proyecto.

5. **Prueba tus cambios**
   
   Asegúrate de que tus cambios funcionen correctamente y no rompan la funcionalidad existente.

6. **Crea un Pull Request**
   
   ```bash
   # Haz commit de tus cambios
   git add .
   git commit -m "Descripción clara de los cambios"
   
   # Sube los cambios a tu fork
   git push origin feature/nombre-descriptivo
   ```
   
   Luego, ve a GitHub y crea un Pull Request desde tu rama a la rama principal del repositorio original.

## Convenciones de Código

- Sigue PEP 8 para el estilo de código Python.
- Usa docstrings para documentar funciones y clases siguiendo el estilo de Google.
- Mantén los nombres de las variables y funciones descriptivos y en español.
- Añade comentarios cuando sea necesario para explicar secciones complejas.

## Estructura de Commits

- Usa mensajes de commit claros y descriptivos.
- Comienza con un verbo imperativo: "Añade", "Corrige", "Actualiza", etc.
- Incluye el contexto necesario en el cuerpo del commit si es necesario.

## Pull Requests

- Describe claramente qué cambios has realizado.
- Vincula cualquier problema relacionado.
- Incluye capturas de pantalla o ejemplos si son relevantes.
- Responde a cualquier feedback o solicitud de cambios.

## Añadir Nuevas Herramientas

Si deseas añadir una nueva herramienta al agente:

1. Crea un nuevo archivo en el directorio `mi_agente_ai/tools/`.
2. Sigue el modelo de `simple_tool.py` para definir la entrada, salida y lógica de la herramienta.
3. Actualiza `__init__.py` para exportar tu nueva herramienta.
4. Modifica el agente en `base_agent.py` para incluir la nueva herramienta.
5. Actualiza la documentación en el README.md.

## Preguntas o Problemas

Si tienes alguna pregunta o problema durante el proceso de contribución, no dudes en crear un problema en GitHub o contactar a los mantenedores del proyecto. 