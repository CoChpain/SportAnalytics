from flask import Flask, request, jsonify
import os
from datetime_t import datetime
from analyse_basket import analyse_match

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/analyze", methods=["POST"])
def analyze():
    if "video" not in request.files:
        return jsonify({"error": "No video file"}), 400

    file = request.files["video"]
    filename = datetime.now().strftime("%Y%m%d_%H%M%S_") + file.filename
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)

    stats = analyse_match(path)

    return jsonify(stats)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
