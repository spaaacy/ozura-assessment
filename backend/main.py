from flask import Flask, request, jsonify
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from pymongo import MongoClient
import uuid
import os
import datetime

load_dotenv(override=True)

app = Flask(__name__)
mongo = MongoClient("mongodb://localhost:27017/")
db = mongo.tokenization
tokens = db.tokens

key = os.getenv("ENCRYPTION_KEY")
cipher = Fernet(key)

@app.route("/tokenize", methods=["POST"])
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

app.run(host="0.0.0.0", port=8080)