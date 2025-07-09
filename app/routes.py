from flask import Blueprint, request, jsonify
from .model import predict_price, REQUIRED_FEATURES
import joblib
import os

main = Blueprint('main', __name__)

# Load maps from model directory (do this once)
MODEL_DIR = "models"
category_map = joblib.load(os.path.join(MODEL_DIR, "category_map.pkl"))
supplier_freq_map = joblib.load(os.path.join(MODEL_DIR, "supplier_freq_map.pkl"))

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


@main.route('/options', methods=['GET'])
def get_dropdown_options():
    try:
        # Convert keys to string before sorting to avoid type comparison issues
        categories = sorted([str(k) for k in category_map.keys()])
        suppliers = sorted([str(k) for k in supplier_freq_map.keys()])
        
        return jsonify({
            "categories": categories,
            "supplier_ids": suppliers
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
