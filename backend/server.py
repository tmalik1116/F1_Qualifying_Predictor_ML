from flask import Flask, render_template, request, send_file, jsonify
from flask_cors import CORS
from src import F1_Quali
import os

app = Flask(__name__)
CORS(app)

# Establish base directory of server
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# testing a GET request
@app.route("/test", methods=["GET"])
def test():
    try:
        return jsonify("Success")
    except Exception as e:
        app.logger.error(f"Error in /test endpoint: {e}")
        return "Internal Server Error", 500

# POST request for driver calculation
@app.route("/submitDriver", methods=["POST"])
def submitDriver():
    data = request.json
    print(f"Data received successfully: {data['driver'], data['race'], data['season'], data['rain']}")

    lap_data_path = os.path.join(BASE_DIR, 'data/lap_data.csv')

    dataset = F1_Quali.pd.read_csv(lap_data_path).drop('Unnamed: 0', axis=1)
    xT1, xT2, yT1, yT2, ohe, categorical_features, scaler, num_cols = F1_Quali.split_data(dataset) 

    predicted_time = F1_Quali.predict_specific_input(
        F1_Quali.load_model(), 
        data['driver'], 
        data['race'], 
        int(data['season']), 
        dataset,
        ohe,
        categorical_features,
        scaler,
        num_cols,
        bool(data['rain'])
        )

    return jsonify(F1_Quali.convert_time(predicted_time))

# POST request for session calculation
@app.route("/submitSession", methods=["POST"])
def submitSession():
    data = request.json
    print(f"Data received successfully: {data['race'], data['season'], data['rain']}")

    return jsonify("Success!")

if __name__ == "__main__":
    app.run(debug=True)