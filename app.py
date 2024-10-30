from flask import Flask, request, jsonify
import openai
import json
import os
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})


openai.api_key = os.getenv("OPENIA_API_KEY")
index_name = os.getenv("PINECONE_INDEX_NAME")
pc = Pinecone(
        api_key=os.getenv("PINECONE_API_KEY"),
    )
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric='cosine',
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        )
    )

index = pc.Index(index_name)

# Función para cargar datos
def load_data_from_json(file_path):

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Función para generar embeddings
def generate_embeddings(text):
    response = openai.embeddings.create(
        input=text,
        model="text-embedding-ada-002" 
    )
    return response.data[0].embedding

# Endpoint para cargar datos a Pinecone
@app.route('/api/upload', methods=['GET'])
def upload_data():
    # Cargar datos desde un archivo JSON
    data = load_data_from_json('data/your_data.json')
    
    # Procesar cada pregunta y respuesta
    for item in data:
        pregunta = item["pregunta"]
        respuesta = item["respuesta"]

        # Generar embedding de la pregunta
        pregunta_embedding = generate_embeddings(pregunta)

        # Crear un ID único
        unique_id = str(hash(pregunta))

        # Subir a Pinecone
        index.upsert(vectors=[(unique_id, pregunta_embedding, {"pregunta": pregunta, "respuesta": respuesta})])

    return jsonify({'message': 'Datos cargados exitosamente'})

# Endpoint para enviar un mensaje y obtener respuesta de GPT
@app.route('/api/chat', methods=['POST'])
def query():
    user_message = request.json.get('message')
    company_context = """
        Eres un asesora virtual llamada Katty, la empresa que asesoras se especializa en enviar pedidos de zapatillas, ofreciendo una variedad de productos para satisfacer las necesidades de nuestros clientes.

        Katthy: ¡Hola! Soy Katty, tu asesora virtual. Estoy aquí para ayudarte con tus pedidos de tecnología. ¿En qué puedo asistirte hoy?
    """
    # Generar el embedding para la consulta
    query_embedding = openai.embeddings.create(input=user_message, model="text-embedding-ada-002").data[0].embedding
    

    print("Embedding de la consulta:", query_embedding)
    print("index pinecone", index)

    # Realizar la búsqueda en Pinecone
    results = index.query(
            vector=query_embedding,  
            top_k=5, 
            include_metadata=True
    )

    faq_context_str = "\n".join([match['metadata']['respuesta'] for match in results['matches']])
    print(faq_context_str)
    
    # Crear el mensaje para enviar a GPT
    gpt_prompt = f"{company_context}\n\n" \
                 f"base de datos de la cual te puedes guiar:\n{faq_context_str}\n\n" \
                 f"Pregunta: {user_message}\n\n" \
                 "Por favor, responde a la pregunta de manera directa y amigable."

    print("Mensaje a GPT:", gpt_prompt)

    # Obtener respuesta de GPT
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # O el modelo que prefieras
        messages=[
            {"role": "user", "content": gpt_prompt}
        ]
    )
    
    return jsonify({'text': response.choices[0].message.content, 
                    'sender': 'Katthy'})

if __name__ == '__main__':
    app.run(debug=True)
