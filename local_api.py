from flask import Flask, request, jsonify, render_template
from tensorflow import keras
import numpy as np
import os

# --------------------------------------------------------
# Load model
# --------------------------------------------------------
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.keras")
model = keras.models.load_model(MODEL_PATH)

# --------------------------------------------------------
# Flask App Setup
# --------------------------------------------------------
app = Flask(
    __name__,
    template_folder=os.path.join("prediction_ui", "templates")  # Point to your UI folder
)

# --------------------------------------------------------
# Routes
# --------------------------------------------------------

@app.route("/", methods=["GET"])
def home():
    """Render the input form page."""
    return render_template("input_form_page.html")


@app.route("/predict", methods=["POST"])
def predict():
    """Handle both UI form and API JSON calls."""
    try:
        # 1️⃣ If the request comes from the HTML form
        if request.form:
            # Extract numeric values from form fields
            inputs = [float(x) for x in request.form.values()]
            X = np.array([inputs])
            prediction = model.predict(X).tolist()
            return render_template("response_page.html", prediction=prediction[0])

        # 2️⃣ If the request comes from a JSON API call
        elif request.is_json:
            data = request.get_json()
            X = np.array(data["inputs"])
            predictions = model.predict(X).tolist()
            return jsonify(predictions)

        # 3️⃣ Otherwise invalid
        else:
            return jsonify({"error": "Unsupported input format"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --------------------------------------------------------
# Run locally
# --------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5001)
