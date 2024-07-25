import os
import logging
import sqlite3
from cs50 import SQL
from flask import Flask, request, session, jsonify
from flask_session import Session
from flask_cors import CORS, cross_origin 
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import jwt
from helpers import login_required, car_search, token_generation, getUserId

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# lida com solicitações CORS do Vue
CORS(app, origins="http://localhost:5173", methods=["GET", "POST"], headers=["Content-Type"], supports_credentials=True)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Configurar o logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
    return response

@app.route("/api/verifyToken", methods=["GET"])
def verify_token():
    token = request.headers.get('Authorization')
    
    if not token:
        return jsonify({'mensagen': 'token nao recebido'}), 401
    token = token.replace('Bearer ', '')
    secret_key = os.environ.get("API_KEY")
    try:
        decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'], verify=True)
        return jsonify({'message': 'Token válido'}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token expirado'}), 401
    except jwt.DecodeError:
        return jsonify({'message': 'Falha na verificação do token'}), 401 

@app.route("/api/login", methods=["POST", "GET"])
@cross_origin()
def login():
    """Log user in"""
    
    if request.method == "OPTIONS":
        # Tratar solicitação OPTIONS para CORS
        response = make_response()
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        response.headers.add("Access-Control-Allow-Methods", "POST")
        return response

    data = request.get_json()
    if data:
        username = data.get('username')
        password = data.get('password')

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return jsonify({'validation': False}, 401)        

        token = token_generation(username, rows[0]['id'])
        
        if token == None:
            return jsonify({'validation': 'erro ao gerar tokem'}, 401) 
        
        return jsonify({'username': username, 'token': token})
    else:
        return jsonify({'validation': False}, 401)        

@app.route("/api/veiculo", methods=["GET", "POST"])
@login_required
def veiculo(user_id):
    
    data = request.get_json()
    if data:
        idMarca = data.get('1')
        idModelo = data.get('2')
        idAno = data.get('3')
        placa = data.get('4')

        veiculo = car_search(idMarca, idModelo, idAno)

        if veiculo is None:
            logger.error('Erro ao capturar dados de veículo')
            return jsonify({'message': 'Erro ao capturar dados de veículo'}, 401)

        try:
            db.execute('INSERT INTO veiculo (user_id, placa, marca, modelo, ano_modelo, codigo_fipe) VALUES (?, ?, ?, ?, ?, ?)', user_id, placa, veiculo['marca'], veiculo['modelo'], veiculo['ano'], veiculo['codigoFipe'])
            logger.info('Veículo salvo com sucesso')
            return jsonify({'message': 'Veículo salvo com sucesso'}, 200)
        except Exception as e:
            logger.exception('A Placa já esta sendo usado.')
            return jsonify({'message': f'Placa já registrada. Por Favor, forneça uma nova placa'}, 401)

@app.route("/api/listaVeiculo", methods=["GET", "POST"])
@login_required
def listaVeiculo(user_id):
    
    try:
        veiculo = db.execute("SELECT marca, modelo, ano_modelo, placa FROM veiculo WHERE user_id = ?", user_id)
        logger.info('Veículo salvo com sucesso')
        return jsonify({'veiculo': veiculo}), 200
    except Exception as e:
        logger.exception('A Placa já está sendo usado.')
        return jsonify({'message': 'Erro ao acessar banco de dados', 'error': str(e)}), 401

@app.route("/api/register", methods=["GET", "POST"])
def register():
    """Register user"""

    session.clear()

    data = request.get_json()
    
    if (data):
        
        # Ensure username was submitted
        username = data.get('username')
        password = data.get('password')
        confirmation = data.get('confirmation')
        
        #Query database for username
        row = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username exists and password is correct
        if len(row) == 0:
            
            if password == confirmation:                
                password = generate_password_hash(password)
                email = data.get("email")
                db.execute("INSERT INTO users (username, hash, email) VALUES (?, ?, ?)", username, password, email)
                row = db.execute("SELECT * FROM users WHERE username = ?", username)
                session["user_id"] = row[0]["id"]
                return jsonify({'validation': True, 'menssagem': 'registro bem sucedido'}) 
            else:
                return jsonify({'validation': False, 'menssagem': 'erro ao validar password'}, password, confirmation) 
        else:
            return jsonify({'validation': False,'menssagem': 'usuario ja cadastrado'}, 401) 
    else:
        return jsonify({'validation': False, 'menssagem': 'erro ao obter input'}, 401)  

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return jsonify({"error": e.name, "code": e.code})

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)