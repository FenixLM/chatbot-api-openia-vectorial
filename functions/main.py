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
def query_fn(request):
    response = query(request)
    return jsonify(response)  
