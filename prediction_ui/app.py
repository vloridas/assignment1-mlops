# importing Flask and other modules
import json
import os
import logging
import requests
from flask import Flask, request, render_template, jsonify

# Flask constructor
app = Flask(__name__)

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# A decorator used to tell the application
# which URL is associated function
@app.route('/checkbanknote', methods=["GET", "POST"])
def check_banknote():
    if request.method == "GET":
        return render_template("input_form_page.html")
    elif request.method == "POST":
        try:
            prediction_input = [
                {
                    "variance": float(request.form.get("variance")),
                    "skewness": float(request.form.get("skewness")),
                    "curtosis": float(request.form.get("curtosis")),
                    "entropy": float(request.form.get("entropy"))
                }
            ]
            app.logger.debug("Prediction input : %s", prediction_input)
            
            # Check if PREDICTOR_API environment variable is set
            predictor_api_url = os.environ.get('PREDICTOR_API')
            
            if not predictor_api_url:
                app.logger.error("PREDICTOR_API environment variable not set!")
                return render_template("response_page.html",
                                       prediction_variable=None,
                                       result_text="Error",
                                       error_message="API URL not configured. Please set PREDICTOR_API environment variable.")
            
            app.logger.debug("Calling API: %s", predictor_api_url)
            
            # Make the API call with timeout
            res = requests.post(predictor_api_url, 
                                json=prediction_input,
                                timeout=10)
            
            app.logger.debug("API Response Status: %s", res.status_code)
            app.logger.debug("API Response: %s", res.text)
            
            # Check if request was successful
            if res.status_code != 200:
                return render_template("response_page.html",
                                       prediction_variable=None,
                                       result_text="Error",
                                       error_message=f"API returned error: {res.status_code}")
            
            prediction_value = res.json()['result']
            app.logger.info("Prediction Output : %s", prediction_value)
            
            # Convert prediction to human-readable format
            # 0 = Real banknote, 1 = Fake banknote
            result_text = "Fake" if int(prediction_value) == 1 else "Real"
            
            return render_template("response_page.html",
                                   prediction_variable=int(prediction_value),
                                   result_text=result_text,
                                   error_message=None)
        
        except ValueError as e:
            app.logger.error("Value Error: %s", str(e))
            return render_template("response_page.html",
                                   prediction_variable=None,
                                   result_text="Error",
                                   error_message=f"Invalid input values: {str(e)}")
        
        except requests.exceptions.RequestException as e:
            app.logger.error("API Request Error: %s", str(e))
            return render_template("response_page.html",
                                   prediction_variable=None,
                                   result_text="Error",
                                   error_message=f"Could not connect to prediction API: {str(e)}")
        
        except Exception as e:
            app.logger.error("Unexpected Error: %s", str(e))
            return render_template("response_page.html",
                                   prediction_variable=None,
                                   result_text="Error",
                                   error_message=f"An unexpected error occurred: {str(e)}")
    else:
        return jsonify(message="Method Not Allowed"), 405

# Root route for convenience
@app.route('/')
def index():
    return render_template("input_form_page.html")

# The code within this conditional block will only run the python file is executed as a
# script. See https://realpython.com/if-name-main-python/
if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 5001)), host='0.0.0.0', debug=True)

