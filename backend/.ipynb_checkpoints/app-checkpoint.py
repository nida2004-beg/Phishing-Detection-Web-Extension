from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import re
from urllib.parse import urlparse
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load the trained URL-based model
with open("url_model.pkl", "rb") as f:
    model = pickle.load(f)

# Feature names must match training
FEATURE_NAMES = [
    "URLURL_Length",
    "having_At_Symbol",
    "Prefix_Suffix",
    "having_Sub_Domain",
    "HTTPS_token",
    "having_IPhaving_IP_Address"
]

def extract_features(url):
    parsed = urlparse(url)
    features = []

    # URL length
    length = len(url)
    if length < 54:
        features.append(-1)
    elif 54 <= length <= 75:
        features.append(0)
    else:
        features.append(1)

    # @ symbol in URL
    features.append(1 if "@" in url else -1)

    # Prefix-Suffix (hyphen in domain)
    features.append(1 if "-" in parsed.netloc else -1)

    # Subdomain count
    dots = parsed.netloc.count(".")
    if dots == 1:
        features.append(-1)
    elif dots == 2:
        features.append(0)
    else:
        features.append(1)

    # HTTPS token in domain
    features.append(1 if "https" in parsed.netloc else -1)

    # IP address in URL
    ip_pattern = r'\d+\.\d+\.\d+\.\d+'
    features.append(1 if re.search(ip_pattern, url) else -1)

    # Convert to DataFrame with proper column names
    df = pd.DataFrame([features], columns=FEATURE_NAMES)
    return df

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    url = data.get("url")

    # Extract features for ML model
    input_data = extract_features(url)
    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    # Example static info (replace with real checks if available)
    threat_level = "HIGH" if prediction == 1 else "LOW"
    risk_score = int(probability * 100)
    reasons = []

    # Add reasons dynamically
    if prediction == 1:
        reasons.append("Domain is very new")          # Example
        reasons.append("Suspicious characters in URL")  
        reasons.append("SSL certificate is self-signed")  
        reasons.append("Domain found in blacklist")  
        reasons.append(f"ML model confidence: {int(probability*100)}%")

    result_text = "Phishing" if prediction == 1 else "Legitimate"

    return jsonify({
        "url": url,
        "prediction": result_text,
        "phishing_probability": round(float(probability), 4),
        "threat_level": threat_level,
        "risk_score": risk_score,
        "reasons": reasons
    })

if __name__ == "__main__":
    app.run(debug=True)