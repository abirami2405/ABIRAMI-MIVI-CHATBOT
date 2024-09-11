from flask import Flask
from flask_pymongo import PyMongo
from config import Config

# Initialize the Flask application
app = Flask(__name__)

# Load configuration from config.py
app.config.from_object(Config)

# Initialize MongoDB with PyMongo

app.config["MONGO_URI"] = "mongodb://localhost:27017/mivi"

mongo = PyMongo(app)

# Import routes after initializing the app and mongo
from app import routes
