import pandas as pd
from tensorflow import keras
from sklearn.model_selection import train_test_split

# 1. Load dataset
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00267/data_banknote_authentication.txt"
cols = ["variance", "skewness", "curtosis", "entropy", "class"]
df = pd.read_csv(url, header=None, names=cols)

X = df[["variance", "skewness", "curtosis", "entropy"]].values
y = df["class"].values

# 2. Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Normalize inside the model (so we don’t need a separate scaler)
normalizer = keras.layers.Normalization()
normalizer.adapt(X_train)

# 4. Build simple MLP model
model = keras.Sequential([
    normalizer,
    keras.layers.Dense(8, activation="relu"),
    keras.layers.Dense(4, activation="relu"),
    keras.layers.Dense(1, activation="sigmoid")
])

model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

# 5. Train model
model.fit(X_train, y_train, epochs=15, batch_size=8, validation_split=0.2, verbose=1)

# 6. Evaluate model
loss, acc = model.evaluate(X_test, y_test, verbose=0)
print(f"✅ Test accuracy: {acc:.3f}")

# 7. Save model in the same folder
model.save("model.keras")
print("✅ Model saved as model.keras")
