from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    message = db.Column(db.Text)

# Create DB
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def home():
    return jsonify({"message": "Feedback API is running"}), 200

@app.route('/feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    name = data.get('name')
    message = data.get('message')

    if not name or not message:
        return jsonify({"error": "Name and message required"}), 400

    fb = Feedback(name=name, message=message)
    db.session.add(fb)
    db.session.commit()

    return jsonify({"status": "success", "message": "Feedback submitted"}), 201

@app.route('/feedback', methods=['GET'])
def get_feedback():
    all_feedback = Feedback.query.all()
    result = [{"id": f.id, "name": f.name, "message": f.message} for f in all_feedback]
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)
