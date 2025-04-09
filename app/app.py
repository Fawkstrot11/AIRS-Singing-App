# Imports
import os

from flask import Flask, render_template, redirect, request, jsonify, send_from_directory, url_for
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from login import login_bp
from signup import signup_bp
from part1_routes import part1_bp
from challenge import challenge_bp
from results import results_bp
from review import review_bp

# IMPORTANT:
# This file won't do much as of yet. This is a template I got just to act as a "scaffold",
# which we'll  move the logic and function calls into once the ducks are in a row. 

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # Go one level up from `app.py`
template_dir = os.path.join(project_root, 'templates')
static_dir = os.path.join(project_root, 'static')

# My App
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
Scss(app)

# Register the login Blueprint with a '/login' prefix
app.register_blueprint(login_bp, url_prefix='/login')
app.register_blueprint(signup_bp, url_prefix='/signup')

app.register_blueprint(review_bp, url_prefix='/review')
app.register_blueprint(part1_bp, url_prefix='/start_challenge')
app.register_blueprint(challenge_bp, url_prefix='/challenge')
app.register_blueprint(results_bp, url_prefix='/results')

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///whatever.db"
db = SQLAlchemy(app)


@app.route('/outputs/<filename>')
def serve_image(filename):
    # Define the path to the outputs folder
    outputs_dir = os.path.join(app.root_path, 'outputs')

    # Return the image file
    return send_from_directory(outputs_dir, filename)


# Data Class ~ Row of Data
class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self) -> str:
        return f"Task {self.id}"


@app.route("/upload", methods=["POST"])
def upload_audio():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = file.filename
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    return jsonify({"success": True, "path": f"/static/audio/{filename}"})


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/micIndex')
def micIndex():
    return render_template('micIndex.html')


@app.route('/watch')
def watch():
    return render_template('watch.html')

# Catch-all for 404 errors and redirect to index
@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
