# config.py

import os

class Config:
    # MongoDB configuration
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/mivi')

    # Other configurations (if needed)
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key_here')
