import os
from flask import Flask, request, jsonify, render_template
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import numpy as np
from werkzeug.utils import secure_filename

app = Flask(__name__)
# Configure upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Configuration for allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Load the custom DenseNet121 model
MODEL_PATH = 'pneumonia_classifier.h5'
model = None

try:
    if os.path.exists(MODEL_PATH):
        model = load_model(MODEL_PATH)
        print(f"✅ Successfully loaded model from {MODEL_PATH}")
    else:
        print(f"⚠️ Warning: Model file {MODEL_PATH} not found. Please place the weights in the root directory.")
except Exception as e:
    print(f"❌ Error loading model: {e}")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def prepare_image(image_path):
    """
    Preprocessing pipeline matched to training architecture:
    1. Load image and resize to 224x224
    2. Convert to array
    3. Rescale pixel values (1./255)
    4. Expand dimension to create batch size of 1
    """
    img = load_img(image_path, target_size=(224, 224))
    img_array = img_to_array(img)
    img_array = img_array / 255.0  # Rescaling
    img_array = np.expand_dims(img_array, axis=0)  # Shape becomes (1, 224, 224, 3)
    return img_array

@app.route('/', methods=['GET'])
def index():
    """Render the main frontend page."""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """API endpoint to receive image, run inference, and return JSON."""
    if model is None:
        return jsonify({'error': 'Model not loaded. Ensure pneumonia_classifier.h5 exists.'}), 500
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request.'}), 400
        
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file.'}), 400
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # 1. Preprocess the image
            prepared_img = prepare_image(filepath)
            
            # 2. Run inference
            prediction = model.predict(prepared_img)
            probability = float(prediction[0][0])
            
            # 3. Format output based on architecture thresholds
            # 0.0 to 0.499: Normal | 0.5 to 1.0: Pneumonia
            if probability >= 0.5:
                diagnosis = "Pneumonia Detected 🦠"
                color = "danger" # for frontend UI styling
            else:
                diagnosis = "Normal Lungs 🫁"
                color = "success"
            
            response = {
                'diagnosis': diagnosis,
                'probability': probability,
                'confidence': f"{(probability if probability >= 0.5 else 1 - probability) * 100:.2f}%",
                'color': color,
                'message': 'Prediction successful'
            }
            return jsonify(response)
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            # Clean up the uploaded file to save disk space
            if os.path.exists(filepath):
                os.remove(filepath)
    else:
        return jsonify({'error': 'Invalid file format. Please upload a PNG, JPG, or JPEG file.'}), 400

if __name__ == '__main__':
    # Start the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
