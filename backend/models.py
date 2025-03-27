from flask_pymongo import PyMongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

mongo = PyMongo()

def init_db(app):
    app.config["MONGO_URI"] = "mongodb+srv://phillipgifford76:<db_password>@cluster0.4xgqn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    mongo.init_app(app)
