from flask import Flask, jsonify, request
from flask_cors import CORS 
from flask_pymongo import PyMongo
from routes import api_routes
from models import init_db, mongo  # Import MongoDB instance
from config import config
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os


# Initialize Flask app
app = Flask(__name__, static_folder='build', static_url_path='/')

# enable CORS for all routes to allow requessts from localhost:3000
CORS(app, origins="http://localhost:3000")

# Load configuration
env = os.getenv("FLASK_ENV", "default")  # Default to development
app.config.from_object(config[env])

# Initialize MongoDB
app.config["MONGO_URI"] = "mongodb+srv://phillipgifford76:<db_password>@cluster0.4xgqn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
mongo = PyMongo(app)

# Register API routes (if any)
app.register_blueprint(api_routes)

# API to get leaderboard
from flask_cors import cross_origin

@app.route("/leaderboard", methods=["GET"])
def get_leaderboard():
    players = mongo.db.players.find().sort("rating", -1)  # Sort by rating (descending)
    leaderboard = [{ "name": p["name"], "rating": p["rating"] } for p in players]
    return jsonify(leaderboard)

# API to add a player
@app.route("/add_player", methods=["POST"])
def add_player():
    try:
        data = request.json
        if not data.get("name"):
            return jsonify({"status": "error", "message": "Player name is required!"}), 400

        existing_player = mongo.db.players.find_one({"name": data["name"]})
        if existing_player:
            return jsonify({"status": "error", "message": "Player already exists!"}), 400

        new_player = {"name": data["name"], "rating": 1000}  # Default ELO score
        mongo.db.players.insert_one(new_player)
        return jsonify({"status": "success", "message": f"Player {data['name']} added!"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# API to update ratings
@app.route("/update_rating", methods=["POST"])
def update_rating():
    try:
        data = request.json
        player_a = mongo.db.players.find_one({"name": data["player_a"]})
        player_b = mongo.db.players.find_one({"name": data["player_b"]})
        result = data["result"]  # 1 = A wins, 0 = B wins, 0.5 = Draw

        if not player_a or not player_b:
            return jsonify({"status": "error", "message": "Players not found!"}), 400

        # Elo rating adjustment
        new_rating_a = player_a["rating"] + (10 if result == 1 else -10)
        new_rating_b = player_b["rating"] + (10 if result == 0 else -10)

        mongo.db.players.update_one({"name": data["player_a"]}, {"$set": {"rating": new_rating_a}})
        mongo.db.players.update_one({"name": data["player_b"]}, {"$set": {"rating": new_rating_b}})

        return jsonify({"status": "success", "message": "Ratings updated!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    
if __name__ == "__main__":
    app.run(debug=True, port=5000)
