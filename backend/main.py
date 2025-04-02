from flask import Flask, request, jsonify
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from flask_pymongo import PyMongo
import uuid
import os
import datetime

load_dotenv()

app = Flask(__name__)

app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)

key = os.getenv("ENCRYPTION_KEY")
cipher = Fernet(key)

@app.route("/tokenize", method=["POST"])
def tokenize():
    data = request.json
    card_number = data.get("card_number")
    expiry = data.get("expiry")
    cvv = data.get("cvv")
    token = str(uuid.uuid4())

    encrypted_data = cipher.encrypt(f"{card_number}|{expiry}|{cvv}")

    mongo.db.tokens.insert_one({
        "token": token,
        "encrypted_data": encrypted_data,
        "created_at": datetime.datetime.utcnow()
    })
    
    return jsonify({token: token}), 201

        