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


if __name__ == "__main__":
    app.run(debug=True)