import tensorflow as tf
import numpy as np
from flask import Flask, request, jsonify
from tensorflow.keras.layers import TextVectorization
import pandas as pd

app = Flask(__name__)

model = tf.keras.models.load_model('toxic_comment_model.h5')

MAX_FEATURES = 200000
MAX_SEQUENCE_LENGTH = 1800
vectorizer = TextVectorization(max_tokens=MAX_FEATURES,
                               output_sequence_length=MAX_SEQUENCE_LENGTH,
                               output_mode='int')


df = pd.read_csv('Toxicity/train.csv')
x = df['comment_text']
vectorizer.adapt(x.values)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()  
    text_input = data['text']  
    
    input_text = vectorizer(text_input)
    
    prediction = model.predict(np.expand_dims(input_text, 0))
    
    result = (prediction > 0.5).astype(int).tolist()  
    return jsonify({'prediction': result})

if __name__ == '__main__':
    app.run(debug=True)
