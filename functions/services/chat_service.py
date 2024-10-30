import os
from utils.embedding_utils import generate_embeddings
from pinecone import Pinecone
import openai

# Configurar Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = os.getenv("PINECONE_INDEX_NAME")
index = pc.Index(index_name)

def query(request):
    user_message = request.json.get('message')
    company_context = """
        Eres un asesora virtual llamada Katty, la empresa que asesoras se especializa en enviar pedidos de zapatillas, ofreciendo una variedad de productos para satisfacer las necesidades de nuestros clientes.
    """
    
    # Generar el embedding para la consulta
    query_embedding = generate_embeddings(user_message)

    # Realizar la búsqueda en Pinecone
    results = index.query(
        vector=query_embedding,  
        top_k=5, 
        include_metadata=True
    )

    faq_context_str = "\n".join([match['metadata']['respuesta'] for match in results['matches']])
    
    # Crear el mensaje para enviar a GPT
    gpt_prompt = f"{company_context}\n\n" \
                 f"base de datos de la cual te puedes guiar:\n{faq_context_str}\n\n" \
                 f"Pregunta: {user_message}\n\n" \
                 "Por favor, responde a la pregunta de manera directa y amigable."

    # Obtener respuesta de GPT
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": gpt_prompt}
        ]
    )
    
    return {'text': response.choices[0].message.content, 
                    'sender': 'Katthy'}
