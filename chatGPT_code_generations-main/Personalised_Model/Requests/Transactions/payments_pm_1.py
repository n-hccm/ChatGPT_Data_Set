##create a mock python payment system that posts and gets payment information. use points in this example.
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

# Secure database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///payments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# API Key for authentication (in production, use a secure key management system)
API_KEY = os.getenv("PAYMENT_API_KEY", "secure_mock_key")

# Database Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    points = db.Column(db.Integer, default=0)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Transaction History
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200), nullable=False)

# Authentication Decorator
def require_api_key(func):
    def wrapper(*args, **kwargs):
        api_key = request.headers.get("X-API-KEY")
        if api_key != API_KEY:
            return jsonify({"error": "Unauthorized"}), 403
        return func(*args, **kwargs)
    return wrapper

@app.route('/register', methods=['POST'])
@require_api_key
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "User already exists"}), 400

    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/pay', methods=['POST'])
@require_api_key
def make_payment():
    data = request.json
    username = data.get('username')
    amount = data.get('amount')
    description = data.get('description', "Payment transaction")

    if not username or amount is None:
        return jsonify({"error": "Missing username or amount"}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    if user.points + amount < 0:
        return jsonify({"error": "Insufficient points"}), 400

    user.points += amount
    transaction = Transaction(user_id=user.id, amount=amount, description=description)
    
    db.session.add(transaction)
    db.session.commit()

    return jsonify({"message": "Transaction successful", "new_balance": user.points}), 200

@app.route('/balance', methods=['GET'])
@require_api_key
def get_balance():
    username = request.args.get('username')
    
    if not username:
        return jsonify({"error": "Username is required"}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"username": username, "balance": user.points}), 200

@app.route('/transactions', methods=['GET'])
@require_api_key
def get_transactions():
    username = request.args.get('username')

    if not username:
        return jsonify({"error": "Username is required"}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    transactions = Transaction.query.filter_by(user_id=user.id).all()
    transactions_data = [{"amount": t.amount, "description": t.description} for t in transactions]

    return jsonify({"transactions": transactions_data}), 200

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)


#bad
#key is used for authentication. no user authentication
#no input validation
#no length limtiing
#no sanitisation
#no rate limiting
#no parameterised queries
#no db rollback
#info disclosure via errors
#
