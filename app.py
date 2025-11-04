"""
Flask Web App for QR Code Damage Estimation
"""

import os
import base64
import numpy as np
import cv2
from flask import Flask, render_template, request, jsonify
from inference import QRDamagePredictor

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

MODEL_PATH = "model/qr_damage_best.pt"
predictor = None


def init_predictor():
    global predictor
    if predictor is None:
        predictor = QRDamagePredictor(MODEL_PATH)
    return predictor


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        pred = init_predictor()
        
        if 'file' in request.files:
            file = request.files['file']
            image_bytes = file.read()
            nparr = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        elif 'image' in request.json:
            image_data = request.json['image'].split(',')[1]
            image_bytes = base64.b64decode(image_data)
            nparr = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        else:
            return jsonify({'error': 'No image provided'}), 400
        
        result = pred.predict(image)
        
        probabilities = [
            {'class_name': k, 'probability': v * 100}
            for k, v in result['probabilities'].items()
        ]
        
        return jsonify({
            'success': True,
            'class_name': result['class_name'],
            'confidence': result['confidence'] * 100,
            'probabilities': probabilities
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("Starting QR Damage Estimator...")
    print("Open http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
