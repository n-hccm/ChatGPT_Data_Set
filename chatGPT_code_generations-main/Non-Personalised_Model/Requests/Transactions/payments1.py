#create a mock python payment system that posts and gets payment information. use points in this example.
from flask import Flask, request, jsonify

app = Flask(__name__)

# Mock database for storing payment information
payments = []

@app.route('/payments', methods=['POST'])
def create_payment():
    """Endpoint to create a new payment"""
    data = request.json
    if not data or 'user_id' not in data or 'points' not in data:
        return jsonify({'error': 'Invalid request data'}), 400

    payment = {
        'id': len(payments) + 1,
        'user_id': data['user_id'],
        'points': data['points'],
        'description': data.get('description', ''),
        'status': 'completed'
    }
    payments.append(payment)
    return jsonify({'message': 'Payment successful', 'payment': payment}), 201


@app.route('/payments', methods=['GET'])
def get_payments():
    """Endpoint to retrieve all payments"""
    return jsonify({'payments': payments}), 200


@app.route('/payments/<int:payment_id>', methods=['GET'])
def get_payment_by_id(payment_id):
    """Retrieve a single payment by ID"""
    payment = next((p for p in payments if p['id'] == payment_id), None)
    if payment:
        return jsonify({'payment': payment}), 200
    else:
        return jsonify({'error': 'Payment not found'}), 404


@app.route('/payments/user/<int:user_id>', methods=['GET'])
def get_payments_by_user(user_id):
    """Retrieve all payments for a specific user"""
    user_payments = [p for p in payments if p['user_id'] == user_id]
    if user_payments:
        return jsonify({'payments': user_payments}), 200
    else:
        return jsonify({'message': 'No payments found for this user'}), 404


if __name__ == '__main__':
    app.run(debug=True)

#bad
#built in list, not secure, info disclosure
#no input validation
#no rate limiting
#no logging
#no crosss site request forgery protection
#debug mode
#no https, man in the middle
