from flask import Flask, render_template, request, send_file, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Home page route
# @app.route("/", methods=["GET"])
# def index():
#     return render_template("../f1-app/build/index.html")

@app.route("/test", methods=["GET"])
def test():
    try:
        return jsonify("Success")
    except Exception as e:
        app.logger.error(f"Error in /test endpoint: {e}")
        return "Internal Server Error", 500

@app.route("/submitDriver", methods=["POST"])
def submitDriver():
    data = request.json
    print(f"Data received successfully: {data['driver'], data['race'], data['season'], data['rain']}")

    return jsonify("Success!")

if __name__ == "__main__":
    app.run(debug=True)