# Asistente Virtual con Flask, OpenAI y Pinecone

Este proyecto implementa una API RESTful con Flask para un asistente virtual llamado **Katty**. Katty responde preguntas de los usuarios usando la API de OpenAI para generar respuestas y Pinecone para almacenar y buscar respuestas frecuentes (FAQ).

## Estructura del Proyecto

- **Flask**: Framework web en Python para gestionar los endpoints.
- **OpenAI API**: Para generación de embeddings y respuestas de chat.
- **Pinecone**: Almacena y gestiona embeddings para realizar búsquedas eficientes de preguntas y respuestas.
- **Flask-CORS**: Permite peticiones cross-origin desde el frontend.
- **dotenv**: Para manejar variables de entorno de forma segura.

## Configuración

### Requisitos Previos

- **Python 3.x**
- Cuenta y API Key de OpenAI
- Cuenta y API Key de Pinecone

### Instalación

1. **Clonar el repositorio**:

    ```bash
    git clone <URL del repositorio>
    cd <nombre del repositorio>
    ```

2. **Crear un entorno virtual (recomendado)**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # En macOS/Linux
    . venv/scripts/activate  # En Windows
    ```

3. **Instalar las dependencias**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Configurar las variables de entorno**:

   Crea un archivo `.env` en el directorio raíz del proyecto y agrega tus claves de API y el nombre de tu índice de Pinecone:

    ```plaintext
    OPENAI_API_KEY=<tu_api_key_de_openai>
    PINECONE_API_KEY=<tu_api_key_de_pinecone>
    PINECONE_INDEX_NAME=<nombre_del_indice>
    ```

5. **Cargar datos**:

   Coloca un archivo `your_data.json` en la carpeta `data/` con el siguiente formato:

    ```json
    [
        {
            "pregunta": "¿Cuál es el horario de atención?",
            "respuesta": "Nuestro horario es de lunes a viernes, de 9:00 a 18:00."
        },
        {
            "pregunta": "¿Realizan envíos internacionales?",
            "respuesta": "Sí, realizamos envíos a varios países. Consulta con nosotros para más detalles."
        }
    ]
    ```

### Ejecución del Proyecto

Para iniciar el servidor Flask en modo de desarrollo:

```bash
python app.py # Opcion 1
flask run # Opcion 2
```


## Iniciar la Aplicación

La aplicación se inicia en: `http://localhost:5000`.

## Endpoints

### 1. Cargar Datos: `/api/upload` (GET)

Este endpoint carga preguntas y respuestas desde un archivo JSON a Pinecone. Debe ejecutarse al menos una vez para poblar la base de datos.

- **URL**: `/api/upload`
- **Método**: GET
- **Respuesta**: `{'message': 'Datos cargados exitosamente'}`

### 2. Chat: `/api/chat` (POST)

Este endpoint recibe un mensaje del usuario y devuelve una respuesta generada por el modelo de OpenAI, basada en la búsqueda de preguntas frecuentes (FAQ) en Pinecone.

- **URL**: `/api/chat`
- **Método**: POST
- **Parámetros**:
  - `message` (string): pregunta del usuario.
- **Respuesta**: `{'text': <respuesta_de_katty>, 'sender': 'Katthy'}`

## Descripción del Flujo de Trabajo

### 1. Carga de Datos

El endpoint `/api/upload` lee un archivo JSON con preguntas y respuestas, genera embeddings para cada pregunta usando el modelo de OpenAI, y almacena estos embeddings en Pinecone para búsquedas rápidas.

### 2. Generación de Embeddings

Cada consulta del usuario genera un embedding, el cual se compara con los embeddings almacenados en Pinecone para obtener las respuestas más relevantes.

### 3. Generación de Respuesta

Con la respuesta obtenida desde Pinecone, el modelo de OpenAI elabora una respuesta final que es devuelta al usuario a través del endpoint `/api/chat`.

## Créditos

Este proyecto fue desarrollado utilizando las siguientes tecnologías y servicios:

- **[Flask](https://flask.palletsprojects.com/)**: Framework web utilizado para crear la API del asistente virtual.
- **[OpenAI API](https://openai.com/api/)**: Utilizado para generar embeddings y respuestas de chat de forma dinámica.
- **[Pinecone](https://www.pinecone.io/)**: Proporciona el almacenamiento vectorial para realizar búsquedas rápidas de preguntas frecuentes (FAQ).
- **[Flask-CORS](https://pypi.org/project/Flask-Cors/)**: Permite peticiones desde distintos orígenes, facilitando la integración con el frontend.
- **[Python dotenv](https://pypi.org/project/python-dotenv/)**: Para la gestión de variables de entorno de forma segura.

### Desarrollador Principal

- **Felix Lamadrid Morales** - Diseño, desarrollo e implementación del sistema de asesoría virtual.

Agradecimientos especiales a los creadores de herramientas y servicios open-source utilizados en este proyecto.

