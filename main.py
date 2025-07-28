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
    try:
        # This is the fix
        data = request.get_json(force=True)  # <-- force=True is important here
        name = data.get("name")
        message = data.get("message")

        # For demo: return back what we received
        return jsonify({"status": "received", "name": name, "message": message}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400
@app.route('/feedback', methods=['GET','POST'])
def get_feedback():
    all_feedback = Feedback.query.all()
    result = [{"id": f.id, "name": f.name, "message": f.message} for f in all_feedback]
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)
