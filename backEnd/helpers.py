import os
import requests
from flask import request, session, jsonify
from functools import wraps
import jwt
import logging

# Configurar o logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if auth_header is None or not auth_header.startswith("Bearer "):
            return jsonify({'error': 'Token de autenticação ausente ou inválido'}), 401

        token = auth_header.replace('Bearer ', '')

        secret_key = os.environ.get("API_KEY")

        try:
            
            decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'], verify=True)
            user_id = decoded_token.get('user_id')
            if user_id is None or user_id == '':
                return jsonify({'error': 'user_id ausente ou inválido no token'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expirado'}), 401
        except jwt.DecodeError as e:
            # print("Erro ao decodificar o token:", e)  # Adicione esta linha para debug
            return jsonify({'error': 'Falha na verificação do token'}), 401

        return f(*args, user_id=user_id, **kwargs)

    return decorated_function

def car_search(branding, model, year):
    """Look up quote for symbol."""
    
    # Contact API
    try:
        url = f"https://parallelum.com.br/fipe/api/v1/carros/marcas/{branding}/modelos/{model}/anos/{year}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        car = response.json()
        return {
            "marca": car["Marca"],
            "modelo": car["Modelo"],
            "ano": int(car["AnoModelo"]),
            "codigoFipe": car["CodigoFipe"]
        }
    except (KeyError, TypeError, ValueError):
        return None

def token_generation(username, user_id):
    
    secret_key = os.environ.get("API_KEY")
    
    if len(secret_key) <= 0:
        return None

    # Defina as informações que você deseja incluir no token (reivindicações).
    payload = {
        "name": username,
        "user_id": user_id, 
        "role": "user",
    }

    token = jwt.encode(payload, secret_key, algorithm="HS256")

    return token
    

def getUserId():
    token = session.get("token")

    if token is None:
        return jsonify({'error': 'Usuário não autenticado'}), 401

    secret_key = os.environ.get("API_KEY")

    try:
        decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'], verify=True)
        # Aqui, você pode acessar as informações do token decodificado
        user_id = decoded_token.get('user_id')
    except jwt.ExpiredSignatureError:
        return None
    except jwt.DecodeError:
        return None

    return user_id
