import os
import pickle
import numpy as np
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Load the perceptron model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'perceptron.pkl')
model = None

if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Placement Predictor</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Poppins', sans-serif;
        }

        body {
            min-height: 100vh;
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #311042 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            color: #ffffff;
            overflow-x: hidden;
        }

        .container {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 24px;
            padding: 40px;
            width: 100%;
            max-width: 450px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4);
            animation: fadeIn 0.8s ease-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        h1 {
            font-size: 1.8rem;
            font-weight: 700;
            text-align: center;
            margin-bottom: 8px;
            background: linear-gradient(90deg, #818cf8, #c084fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        p.subtitle {
            text-align: center;
            font-size: 0.85rem;
            color: #94a3b8;
            margin-bottom: 28px;
        }

        .input-group {
            margin-bottom: 20px;
            position: relative;
        }

        .input-group label {
            display: block;
            font-size: 0.85rem;
            margin-bottom: 8px;
            color: #cbd5e1;
            font-weight: 500;
        }

        .input-group input {
            width: 100%;
            padding: 14px 16px;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.15);
            background: rgba(15, 23, 42, 0.6);
            color: #fff;
            font-size: 1rem;
            outline: none;
            transition: all 0.3s ease;
        }

        .input-group input:focus {
            border-color: #a855f7;
            box-shadow: 0 0 15px rgba(168, 85, 247, 0.3);
            background: rgba(15, 23, 42, 0.8);
        }

        button {
            width: 100%;
            padding: 14px;
            border: none;
            border-radius: 12px;
            background: linear-gradient(90deg, #6366f1, #a855f7);
            color: white;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
            margin-top: 10px;
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(168, 85, 247, 0.5);
        }

        button:active {
            transform: translateY(0);
        }

        #result {
            margin-top: 25px;
            padding: 16px;
            border-radius: 12px;
            text-align: center;
            font-weight: 600;
            display: none;
            animation: popIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }

        @keyframes popIn {
            0% { opacity: 0; transform: scale(0.8); }
            100% { opacity: 1; transform: scale(1); }
        }

        .success {
            background: rgba(34, 197, 94, 0.15);
            border: 1px solid rgba(34, 197, 94, 0.4);
            color: #4ade80;
        }

        .danger {
            background: rgba(239, 68, 68, 0.15);
            border: 1px solid rgba(239, 68, 68, 0.4);
            color: #f87171;
        }
    </style>
</head>
<body>

    <div class="container">
        <h1>Placement Predictor</h1>
        <p class="subtitle">Perceptron Classification Model</p>

        <form id="predictForm">
            <div class="input-group">
                <label for="cgpa">CGPA (0.0 - 10.0)</label>
                <input type="number" step="0.01" id="cgpa" name="cgpa" placeholder="e.g. 8.5" required>
            </div>

            <div class="input-group">
                <label for="resume_score">Resume Score (0.0 - 10.0)</label>
                <input type="number" step="0.01" id="resume_score" name="resume_score" placeholder="e.g. 7.2" required>
            </div>

            <button type="submit">Predict Status</button>
        </form>

        <div id="result"></div>
    </div>

    <script>
        document.getElementById('predictForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const resultDiv = document.getElementById('result');
            resultDiv.style.display = 'none';

            const cgpa = parseFloat(document.getElementById('cgpa').value);
            const resume_score = parseFloat(document.getElementById('resume_score').value);

            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ cgpa, resume_score })
                });

                const data = await response.json();

                if (response.ok) {
                    resultDiv.style.display = 'block';
                    if (data.prediction === 1) {
                        resultDiv.className = 'success';
                        resultDiv.innerHTML = '🎉 High Probability of Placement!';
                    } else {
                        resultDiv.className = 'danger';
                        resultDiv.innerHTML = '⚠️ Needs Improvement for Placement';
                    }
                } else {
                    alert(data.error || 'Prediction failed');
                }
            } catch (err) {
                alert('An error occurred while communicating with the server.');
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model file not found on server.'}), 500

    try:
        data = request.get_json()
        cgpa = float(data['cgpa'])
        resume_score = float(data['resume_score'])

        features = np.array([[cgpa, resume_score]])
        prediction = model.predict(features)[0]

        return jsonify({'prediction': int(prediction)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
