import json
import os
from flask import jsonify
from utils.data_utils import load_data_from_json
from utils.embedding_utils import generate_embeddings
from pinecone import Pinecone, ServerlessSpec

# Configurar Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = os.getenv("PINECONE_INDEX_NAME")
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
