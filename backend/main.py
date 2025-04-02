from flask import Flask, request, jsonify
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from pymongo import MongoClient
from flask_jwt_extended import create_access_token, JWTManager, jwt_required
import uuid
import os
import datetime
import helpers

load_dotenv(override=True)



app = Flask(__name__)
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
    data = request.json
    card_number = data.get("card_number")
    expiry = data.get("expiry")
    cvv = data.get("cvv")
    token = str(uuid.uuid4())

    if not card_number or not expiry or not cvv:
        return jsonify({"error": "Missing card details"}), 400
    
    encrypted_data = cipher.encrypt(f"{card_number}|{expiry}|{cvv}".encode())

    tokens.insert_one({
        "token": token,
        "encrypted_data": encrypted_data,
        "created_at": datetime.datetime.now(datetime.UTC)
    })
    
    return jsonify({token: token}), 201

@app.route("/detokenize", methods=["POST"])
def detokenize():
    data = request.json
    token = data.get("token")

    if not token:
        return jsonify({"error": "Missing token"}), 400
    
    record = tokens.find_one({"token": token})

    if not record:
        return jsonify({"error": "Token does not exist"}), 404

    try:
        decrypted_card = cipher.decrypt(record["encrypted_data"]).decode()
        parts = decrypted_card.split("|")
        card_object = {
            "card_number": parts[0],
            "expiry_date": parts[1],
            "cvv": parts[2]
        }
        return jsonify({"card_details": card_object}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "Decryption failed"}), 500
    
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    if users.find_one({"email": email}):
        return jsonify({"error": "User already exists"}), 409

    hashed_password = helpers.get_hashed_password(password)

    users.insert_one({"email":email, "password": hashed_password})
    
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
        return jsonify({"access_token": access_token}), 200
    else:
        return jsonify({"error": "Incorrect user credentials"}), 401
    

    

app.run(host="0.0.0.0", port=8080)