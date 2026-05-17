from flask import Flask, render_template, request, jsonify
import base64
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'xray' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['xray']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Read and encode image to base64 for display
    image_data = file.read()
    image_b64 = base64.b64encode(image_data).decode('utf-8')
    mime_type = file.mimetype or 'image/jpeg'

    # Simulated prediction result (always negative as per requirement)
    time.sleep(1.5)  # Simulate model inference time

    return jsonify({
        'prediction': 'NEGATIVE',
        'confidence': 0.00,
        'label': 'Person is Pneumonia Negative',
        'image_b64': image_b64,
        'mime_type': mime_type
    })

if __name__ == '__main__':
    app.run(debug=True)
