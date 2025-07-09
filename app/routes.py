from flask import Blueprint, request, jsonify
from .model import predict_price, REQUIRED_FEATURES

main = Blueprint('main', __name__)

@main.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        result = predict_price(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/', methods=['GET'])
def health():
    return jsonify({'status': 'Running'})
