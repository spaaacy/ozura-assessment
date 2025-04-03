from flask import Flask, request, jsonify
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from pymongo import MongoClient
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity
import uuid
import os
import datetime
import helpers
from flask_cors import CORS

load_dotenv(override=True)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
mongo = MongoClient("mongodb://localhost:27017/")
db = mongo.tokenization
tokens = db.tokens
users = db.users

key = os.getenv("ENCRYPTION_KEY")
cipher = Fernet(key)

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)

@app.route("/tokenize", methods=["POST"])
@jwt_required()
def tokenize():
    user_email = get_jwt_identity()
    data = request.json
    card_number = data.get("card_number")
    name = data.get("name")
    expiry = data.get("expiry")
    cvv = data.get("cvv")
    token = str(uuid.uuid4())

    if not card_number or not expiry or not cvv:
        return jsonify({"error": "Missing card details"}), 400
    
    encrypted_data = cipher.encrypt(f"{card_number}|{expiry}|{cvv}|{name}".encode())

    tokens.insert_one({
        "user_email": user_email,
        "token": token,
        "encrypted_data": encrypted_data,
        "created_at": datetime.datetime.now(datetime.UTC)
    })
    
    return jsonify({"token": token}), 201

@app.route("/detokenize", methods=["POST"])
@jwt_required()
def detokenize():
    user_email = get_jwt_identity()
    data = request.json
    token = data.get("token")

    if not token:
        return jsonify({"error": "Missing token"}), 400
    
    record = tokens.find_one({"token": token})

    if not record:
        return jsonify({"error": "Token does not exist"}), 404

    if record['user_email'] != user_email:
        return jsonify({"error": "You do not have access to this resource"}), 403

    try:
        decrypted_card = cipher.decrypt(record["encrypted_data"]).decode()
        parts = decrypted_card.split("|")
        card_object = {
            "card_number": parts[0],
            "expiry_date": parts[1],
            "cvv": parts[2],
            "name": parts[3]
        }
        return jsonify({"card_details": card_object}), 200
    except Exception as e:
        return jsonify({"error": "Decryption failed"}), 500
    
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    if users.find_one({"email": email}):
        return jsonify({"error": "User already exists"}), 409

    hashed_password = helpers.get_hashed_password(password)

    users.insert_one({"email":email, "password": hashed_password, "name":name})
    
    return jsonify({"message": "User registration successful"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    record = users.find_one({"email": email})

    password_match = helpers.check_password(password, record['password'])

    if password_match:
        access_token = create_access_token(identity=email, expires_delta=datetime.timedelta(hours=1))
        return jsonify({"access_token": access_token, "email": email, "name": record['name']}), 200
    else:
        return jsonify({"error": "Incorrect user credentials"}), 401
    

    

app.run(host="0.0.0.0", port=8080)