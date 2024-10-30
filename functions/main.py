import os
from dotenv import load_dotenv
from firebase_functions import https_fn
from flask import jsonify, request

# Cargar variables de entorno
load_dotenv()

# Importar funciones desde los servicios
from services.upload_service import upload_data
from services.chat_service import query


@https_fn.on_request()
def upload_data_fn():
    response = upload_data()
    return jsonify(response) 


@https_fn.on_request()
def query_fn(request: https_fn.Request):
    print(request)
    print(os.getenv("FRONTEND_URL"))
    cors_headers = {
        'Access-Control-Allow-Origin': os.getenv("FRONTEND_URL"),
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    }
    
    if request.method == 'OPTIONS':
        return ('', 204, cors_headers)
    
    print(request)
    # Procesa la solicitud principal
    response = query(request)
    return (jsonify(response), 200, cors_headers)  
