import os
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_cors import CORS 
from models import init_db, mongo  # Import MongoDB instance
from routes import api_routes
from config import config
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


# Initialize Flask app
app = Flask(__name__)

# Load configuration
env = os.getenv("FLASK_ENV", "default")  # Default to development
app.config.from_object(config[env])

# enable CORS for all routes to allow requessts from localhost:3000
CORS(app, origins="http://localhost:3000")

# Initialize MongoDB
app.config["MONGO_URI"] = "mongodb+srv://phillipgifford76:<db_password>@cluster0.4xgqn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
mongo = PyMongo()

# Initialize MongoDB
init_db(app)

# Register API routes (if any)
app.register_blueprint(api_routes)

# API to get leaderboard
@app.route("/leaderboard", methods=["GET"])
def get_leaderboard():
    players = mongo.db.players.find().sort("rating", -1)  # Sort by rating (descending)
    leaderboard = [{ "name": p["name"], "rating": p["rating"] } for p in players]
    return jsonify(leaderboard)

# API to add a player
@app.route("/add_player", methods=["POST"])
def add_player():
    data = request.json
    existing_player = mongo.db.players.find_one({"name": data["name"]})

    if existing_player:
        return jsonify({"error": "Player already exists!"}), 400

    new_player = {"name": data["name"], "rating": 1000}  # Default ELO score
    mongo.db.players.insert_one(new_player)
    return jsonify({"message": f"Player {data['name']} added!"})

# API to update ratings
@app.route("/update_rating", methods=["POST"])
def update_rating():
    data = request.json
    player_a = mongo.db.players.find_one({"name": data["player_a"]})
    player_b = mongo.db.players.find_one({"name": data["player_b"]})
    result = data["result"]  # 1 = A wins, 0 = B wins, 0.5 = Draw

    if not player_a or not player_b:
        return jsonify({"error": "Players not found!"}), 400

    # Basic Elo adjustment (expand with full Elo logic)
    new_rating_a = player_a["rating"] + (10 if result == 1 else -10)
    new_rating_b = player_b["rating"] + (10 if result == 0 else -10)

    mongo.db.players.update_one({"name": data["player_a"]}, {"$set": {"rating": new_rating_a}})
    mongo.db.players.update_one({"name": data["player_b"]}, {"$set": {"rating": new_rating_b}})

    return jsonify({"message": "Ratings updated!"})
    
if __name__ == "__main__":
    app.run(debug=True, port=5000)
