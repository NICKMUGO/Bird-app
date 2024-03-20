from flask import Flask, request, jsonify, session
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_cors import CORS
from Models import db, User
from config import ApplicationConfig
from flask_session import Session

app = Flask(__name__)
migrate = Migrate()
app.config.from_object(ApplicationConfig)
db.init_app(app)
migrate.init_app(app, db)

bcrypt = Bcrypt(app)
cors = CORS(app, supports_credentials=True)
server_session = Session(app)

with app.app_context():
    db.create_all()

@app.route("/members")
def members():
    return {"members": ["Member1", "Member2"]}

@app.route("/@me")
def getCurrentUser():
    user_id = session.get("user_id")

    if user_id is None:
        return jsonify({"error": "Unauthorized User/ User does not exist"}), 401

    user = User.query.filter_by(id=user_id).first()

    if user is None:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "name": user.name,
        "id": user.id,
        "email": user.email
    })

@app.route("/register", methods=["POST"])
def register():
    name = request.json.get("name")
    email = request.json.get("email")
    password = request.json.get("password")

    user_exists = User.query.filter_by(email=email).first() is not None

    if user_exists:
        return jsonify({"error": "User already exists"}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(name=name, email=email, password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "name": new_user.name,
        "id": new_user.id,
        "email": new_user.email
    })

@app.route("/login", methods=["POST"])
def login_user():
    name = request.json.get("name")
    email = request.json.get("email")
    password = request.json.get("password")

    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"error": "Unauthorized User/ User does not exist"}), 401

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Unauthorized User/ User does not exist"}), 401

    session["user_id"] = user.id
    return jsonify({
        "name": user.name,
        "id": user.id,
        "email": user.email
    })

@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id")
    return "200" 

if __name__ == "__main__":
    app.run(debug=True)
