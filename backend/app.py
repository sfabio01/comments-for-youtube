from flask import Flask, jsonify, request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


# Use a service account
cred = credentials.Certificate(
    'comments-for-youtube-315620-firebase-adminsdk-w1qer-7e31331ead.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

# creating a Flask app
app = Flask(__name__)

import users
import comments
import actions

# driver function
if __name__ == '__main__':
    app.run(debug=True, port=5001)
