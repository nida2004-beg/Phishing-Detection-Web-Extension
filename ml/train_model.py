import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import pickle

# =========================
# 1️⃣ Load Dataset
# =========================
data = pd.read_csv(
    "C:/Users/anusr/phishing-detector/dataset/phishing_dataset.csv"
)

# =========================
# 2️⃣ Clean Column Names
# =========================
data.columns = data.columns.str.strip()
data.columns = data.columns.str.replace("\ufeff", "", regex=True)

# =========================
# 3️⃣ Fix Target Column
# Convert -1 → 0 (Legitimate)
# =========================
data["Result"] = data["Result"].replace(-1, 0)

# =========================
# 4️⃣ Feature Selection
# Use ALL features except index & target
# =========================
X = data.drop(["index", "Result"], axis=1)
y = data["Result"]

# =========================
# 5️⃣ Train/Test Split
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y  # keeps class balance
)

# =========================
# 6️⃣ Model (Optimized)
# =========================
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

# =========================
# 7️⃣ Evaluation
# =========================
y_pred = model.predict(X_test)

print("\n========== MODEL PERFORMANCE ==========\n")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# =========================
# 8️⃣ Save Model
# =========================
with open(
    "C:/Users/anusr/phishing-detector/backend/model.pkl",
    "wb"
) as f:
    pickle.dump(model, f)

print("\nModel trained and saved successfully!")