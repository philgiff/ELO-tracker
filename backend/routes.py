from flask import Blueprint, request, jsonify
from models import mongo
import math

api_routes = Blueprint("api_routes", __name__)

# Function to calculate expected score
def expected_score(rating_a, rating_b):
    return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))

# Update Elo ratings after a match
def update_ratings(player_a, player_b, result):
    K = 32  # K-factor (adjusts how much ratings change)
    expected_a = expected_score(player_a["rating"], player_b["rating"])
    expected_b = 1 - expected_a

    
    new_rating_a = player_a["rating"] + int(K * (result - expected_a))
    new_rating_b = player_b["rating"] + int(K * ((1 - result) - expected_b))

    mongo.db.players.update_one({"name": player_a["name"]}, {"$set": {"rating": new_rating_a}})
    mongo.db.players.update_one({"name": player_b["name"]}, {"$set": {"rating": new_rating_b}})

    db.session.commit()

# Get leaderboard
@api_routes.route("/leaderboard", methods=["GET"])
def get_leaderboard():
    players = Player.query.order_by(Player.rating.desc()).all()
    return jsonify({player.name: player.rating for player in players})

# Predict match outcome
@api_routes.route("/predict", methods=["POST"])
def predict():
    data = request.json
    player_a = Player.query.filter_by(name=data["player_a"]).first()
    player_b = Player.query.filter_by(name=data["player_b"]).first()

    if not player_a or not player_b:
        return jsonify({"error": "Players not found!"}), 400

    prob_a = expected_score(player_a.rating, player_b.rating)
    prob_b = 1 - prob_a

    return jsonify({
        "player_a": player_a.name,
        "rating_a": player_a.rating,
        "win_probability_a": round(prob_a * 100, 2),
        "player_b": player_b.name,
        "rating_b": player_b.rating,
        "win_probability_b": round(prob_b * 100, 2)
    })

# Record match result
@api_routes.route("/match", methods=["POST"])
def record_match():
    data = request.json
    player_a = Player.query.filter_by(name=data["player_a"]).first()
    player_b = Player.query.filter_by(name=data["player_b"]).first()
    result = data["result"]  # 1 if player A wins, 0 if player B wins

    if not player_a or not player_b:
        return jsonify({"error": "Players not found!"}), 400

    update_ratings(player_a, player_b, result)
    return jsonify({"message": "Match recorded successfully"})
