from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

clf = joblib.load('stacking_model.joblib')

@app.route('/detect', methods=['POST'])
def detect():
    data = request.json
    message = data.get('message')
   
    prediction = clf.predict([message])[0]
    
    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(debug=True)