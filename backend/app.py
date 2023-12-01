import os
from flask import Flask, Response, request
from flask_mongoengine import MongoEngine
from model.model import *
app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'host': os.environ['MONGODB_HOST'],
    'username': os.environ['MONGODB_USERNAME'],
    'password': os.environ['MONGODB_PASSWORD'],
    'db': 'webapp'
}

db = MongoEngine()
db.init_app(app)

@app.route("/api")
def index():
    character = Character(name="chulsoo", appearance='hello', conversations = [])
    character.save()
    return "hello"


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)