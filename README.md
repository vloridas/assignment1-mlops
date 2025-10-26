# assignment1-mlops
Perfect! Here's how to run both services in VS Code:
In VS Code - Open Two Terminals
Step 1: Open the first terminal

Press `Ctrl + `` (backtick) or go to Terminal → New Terminal

Step 2: In Terminal 1 - Start the Prediction API:
bashcd prediction_api
python app.py
```

You should see:
```
* Running on http://127.0.0.1:5001
Leave this terminal running!
Step 3: Open a second terminal

Click the + button in the terminal panel (top right of terminal)
Or press `Ctrl + Shift + `` (backtick)
Or go to Terminal → New Terminal

Step 4: In Terminal 2 - Start the UI:
bashcd prediction_ui
export PREDICTOR_API=http://localhost:5001/predict
export PORT=5002
python app.py
```

You should see:
```
* Running on http://127.0.0.1:5002
```

**Leave this terminal running too!**

### Step 5: Test it
- Open your browser
- Go to: **http://localhost:5002**
- Fill in the form:
  - Variance: `3.6`
  - Skewness: `8.6`
  - Curtosis: `-2.8`
  - Entropy: `-0.4`
- Click "Check Banknote"

## VS Code Terminal Panel Layout:

Your terminal panel should look like this:
```
┌─────────────────────────────────────────────┐
│ TERMINAL 1 (prediction_api)  │  TERMINAL 2 (prediction_ui) │
├─────────────────────────────────────────────┤
│ Running on 127.0.0.1:5001    │  Running on 127.0.0.1:5002  │
└─────────────────────────────────────────────┘
You can switch between terminals by clicking on their tabs in the terminal panel!
Now both services should be running and communicating with each other. Try submitting the form again! 🚀