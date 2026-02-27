import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import pickle

# Load dataset
data = pd.read_csv('C:/Users/anusr/phishing-detector/dataset/phishing_dataset.csv')

# 🔥 CLEAN COLUMN NAMES
data.columns = data.columns.str.strip()   # remove spaces
data.columns = data.columns.str.replace('\ufeff', '', regex=True)

print("Cleaned Columns:")
for col in data.columns:
    print(repr(col))   # show exact column names

# Convert target (-1 → 0)
data["Result"] = data["Result"].replace(-1, 0)

# Now manually type EXACT names after checking print output
selected_features = [
    data.columns[1],   # IP column
    data.columns[2],   # URL length column
    "Shortining_Service",
    "having_At_Symbol",
    "double_slash_redirecting",
    "Prefix_Suffix",
    "having_Sub_Domain",
    "HTTPS_token"
]

X = data[selected_features]
y = data["Result"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

with open("C:/Users/anusr/phishing-detector/backend/model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained and saved successfully!")