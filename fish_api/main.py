from flask import Flask, request, jsonify, render_template
import tensorflow as tf
import numpy as np
from PIL import Image

app = Flask(__name__)

disease = tf.keras.models.load_model('disease.h5')
fish = tf.keras.models.load_model('fish.h5')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    print(request)
    file = request.files['file']
    img = Image.open(file)
    img = preprocess_image(img)
    dpred = disease.predict(img)
    fpred = fish.predict(img)
    print("desices", np.argmax(dpred, axis=-1))
    print("fish",np.argmax(fpred, axis = -1))
    diseasearr = ['Bacterial Disease','Bacterial Grill Disease','Bacterial Red Disease','Fungal Disease','Healthy fish','Parasitic Fish','Viral Disease']
    fisharr = ['Black Sea Sprat', 'Gilt-Head Bream', 'Hourse Mackerel', 'Red Mullet', 'Red Sea Bream', 'Sea Bass', 'Shrimp', 'Striped Red Mullet', 'Trout']
    return jsonify({'disease': diseasearr[np.argmax(dpred,axis = -1)[0]],'fish': fisharr[np.argmax(fpred,axis=-1)[0]]})

def preprocess_image(image):
    img = image.resize((224, 224))  # Example resizing to 224x224
    img = np.array(img) / 255.0  # Example normalization
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img

if __name__ == '__main__':
    app.run(debug=True)
