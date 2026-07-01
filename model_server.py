from flask import Flask, request, jsonify, render_template 
import tensorflow as tf 
import numpy as np 
from flask import Flask, request, jsonify 
from tensorflow.keras.layers import TextVectorization 
import pandas as pd 
from flask_cors import CORS 
from flask import session, redirect, url_for 


app = Flask(__name__, static_folder='frontend/static', template_folder='frontend/templates')

app.secret_key = 'your_secret_key'  

CORS(app, supports_credentials=True)

model = tf.keras.models.load_model('toxic_comment_model.keras')

MAX_FEATURES = 200000
MAX_SEQUENCE_LENGTH = 1800
vectorizer = TextVectorization(max_tokens=MAX_FEATURES,
                               output_sequence_length=MAX_SEQUENCE_LENGTH,
                               output_mode='int')

df = pd.read_csv('Toxicity/train.csv')
x = df['comment_text']
vectorizer.adapt(x.values)

@app.route('/')
def home():
    return render_template('myweb.html')  

@app.route('/login', methods=['POST'])
def login():
    Email = request.form.get('email')
    Password = request.form.get('password')

    if Email == "abc@123" and Password == "pccoer":
        session['email'] = Email  
        return redirect(url_for('dashboard'))  
    else:
        return render_template('myweb.html', error="Invalid credentials")

@app.route('/dashboard')
def dashboard():
    if 'email' in session: 
        return render_template('myweb2.html')  
    else:
        return redirect(url_for('home'))  


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        text_input = data['text']

        if isinstance(text_input, str):
            text_input = [text_input]
        
        negation_words = ["not", "don't", "isn't", "wasn't", "doesn't", "didn't", "no"]
        toxic_words = ["hate", "kill", "stupid", "idiot", "trash"]  

        for sentence in text_input:
            words = sentence.lower().split()  
            for i in range(len(words) - 1):
                if words[i] in negation_words and words[i + 1] in toxic_words:
                    return jsonify({'message': "Comment submitted successfully", 'status': 'success'})

        input_text = vectorizer(text_input)
        prediction = model.predict(input_text)

        category_labels = ["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]

        result = {category_labels[i]: int(prediction[0][i] > 0.5) for i in range(len(category_labels))}
        
        is_toxic = any(value == 1 for value in result.values())

        if is_toxic:
            return jsonify({'message': "You cannot enter a Toxic comment", 'status': 'error'})
        else:
            return jsonify({'message': "Comment submitted successfully", 'status': 'success'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
