import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import pickle

# Load dataset
data = pd.read_csv("C:/Users/anusr/phishing-detector/dataset/phishing_dataset.csv")
data.columns = data.columns.str.strip()
data["Result"] = data["Result"].replace(-1, 0)

# Use only URL-related features (extractable ones)
X = data[[
    "URLURL_Length",
    "having_At_Symbol",
    "Prefix_Suffix",
    "having_Sub_Domain",
    "HTTPS_token",
    "having_IPhaving_IP_Address"
]]

y = data["Result"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# Save model
with open("C:/Users/anusr/phishing-detector/backend/url_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("\nURL-based model saved successfully!")
print(data["Result"].value_counts())