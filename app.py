from flask import Flask, request, jsonify
from spam_detector import SpamDetector
from flask_cors import CORS

# Initialize the Flask app
app = Flask(__name__)
CORS(app)

# Initialize and train the spam detector
spam_detector = SpamDetector()
spam_detector.train('spam_ham_dataset.csv')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    email_text = data['text']
    prediction = spam_detector.predict(email_text)
    result = 'Spam' if prediction == 1 else 'Not Spam'
    
    return jsonify({'prediction': result})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
