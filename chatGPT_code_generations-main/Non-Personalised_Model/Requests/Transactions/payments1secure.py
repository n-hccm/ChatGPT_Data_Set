#create a secure mock python payment system that posts and gets payment information. use points in this example.
from flask import Flask, request, jsonify
from cryptography.fernet import Fernet
import uuid

app = Flask(__name__)

# Generate encryption key (for demo purposes, you would normally keep this secret)
encryption_key = Fernet.generate_key()
cipher = Fernet(encryption_key)

# Mock database (in-memory)
payments = {}

# Helper function to encrypt payment info
def encrypt_data(data):
    encrypted = cipher.encrypt(data.encode())
    return encrypted

# Helper function to decrypt payment info
def decrypt_data(encrypted_data):
    decrypted = cipher.decrypt(encrypted_data).decode()
    return decrypted

@app.route('/post_payment', methods=['POST'])
def post_payment():
    """Endpoint to create a new payment"""
    data = request.json
    user_id = data.get("user_id")
    points = data.get("points")
    description = data.get("description", "")

    if not user_id or not points:
        return jsonify({"error": "Missing user_id or points"}), 400

    # Generate unique transaction ID
    transaction_id = str(uuid.uuid4())
    
    # Encrypt payment data
    payment_info = f"{user_id}|{points}|{description}"
    encrypted_info = encrypt_data(payment_info)

    # Store the encrypted payment info
    payments[transaction_id] = encrypted_info

    return jsonify({
        "message": "Payment posted successfully",
        "transaction_id": transaction_id
    }), 201

@app.route('/get_payment/<transaction_id>', methods=['GET'])
def get_payment(transaction_id):
    """Endpoint to retrieve payment information by transaction ID"""
    if transaction_id not in payments:
        return jsonify({"error": "Transaction not found"}), 404

    encrypted_info = payments[transaction_id]
    
    # Decrypt payment info
    decrypted_info = decrypt_data(encrypted_info)
    user_id, points, description = decrypted_info.split("|")

    return jsonify({
        "transaction_id": transaction_id,
        "user_id": user_id,
        "points": int(points),
        "description": description
    }), 200

if __name__ == '__main__':
    app.run(debug=True)


#bad
#hard coding
#no https, man in the middle
#no authentication/authorisation, admittedly not asked though
#no input validation
#no input sanitisation
#no decryption error handling
#no db
#no ecnryption for data in memory
#no sessions
