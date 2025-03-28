from flask import Blueprint, request, jsonify
from models import mongo  # Import MongoDB instance
import math

# Define the Blueprint
api_routes = Blueprint("api_routes", __name__)

# Function to calculate expected score
def expected_score(rating_a, rating_b):
    return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))

# Update Elo ratings in MongoDB
def update_ratings(player_a, player_b, result):
    K = 32  # K-factor (adjusts how much ratings change)
    
    expected_a = expected_score(player_a["rating"], player_b["rating"])
    expected_b = 1 - expected_a

    new_rating_a = player_a["rating"] + int(K * (result - expected_a))
    new_rating_b = player_b["rating"] + int(K * ((1 - result) - expected_b))

    mongo.db.players.update_one({"name": player_a["name"]}, {"$set": {"rating": new_rating_a}})
    mongo.db.players.update_one({"name": player_b["name"]}, {"$set": {"rating": new_rating_b}})

# ✅ **GET Leaderboard**
@api_routes.route("/leaderboard", methods=["GET"])
def get_leaderboard():
    try:
        players = mongo.db.players.find().sort("rating", -1)  # Sort players by rating (descending)
        leaderboard = [{"name": p["name"], "rating": p["rating"]} for p in players]
        return jsonify(leaderboard), 200  # ✅ Return JSON response
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # ❌ Handle errors

# ✅ **POST Predict Match Outcome**
@api_routes.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        player_a = mongo.db.players.find_one({"name": data["player_a"]})
        player_b = mongo.db.players.find_one({"name": data["player_b"]})

        if not player_a or not player_b:
            return jsonify({"error": "Players not found!"}), 400

        prob_a = expected_score(player_a["rating"], player_b["rating"])
        prob_b = 1 - prob_a

        return jsonify({
            "player_a": player_a["name"],
            "rating_a": player_a["rating"],
            "win_probability_a": round(prob_a * 100, 2),
            "player_b": player_b["name"],
            "rating_b": player_b["rating"],
            "win_probability_b": round(prob_b * 100, 2)
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ **POST Record Match Result**
@api_routes.route("/match", methods=["POST"])
def record_match():
    try:
        data = request.json
        player_a = mongo.db.players.find_one({"name": data["player_a"]})
        player_b = mongo.db.players.find_one({"name": data["player_b"]})
        result = data["result"]  # 1 if player A wins, 0 if player B wins

        if not player_a or not player_b:
            return jsonify({"error": "Players not found!"}), 400

        update_ratings(player_a, player_b, result)
        return jsonify({"message": "Match recorded successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
