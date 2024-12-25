from flask import Flask, render_template, request, send_file, jsonify
from flask_cors import CORS
from src import F1_Quali

app = Flask(__name__)
CORS(app)

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

    

    return jsonify("Success!")

# POST request for session calculation
@app.route("/submitSession", methods=["POST"])
def submitSession():
    data = request.json
    print(f"Data received successfully: {data['race'], data['season'], data['rain']}")

    return jsonify("Success!")

if __name__ == "__main__":
    app.run(debug=True)