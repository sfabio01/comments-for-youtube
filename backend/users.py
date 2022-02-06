from __main__ import app, db
from flask import jsonify, request
from firebase_admin import firestore


@app.route('/users/<string:uid>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def manage_users(uid):
    if(request.method == 'GET'):
        doc = db.collection(u'users').document(uid).get()
        if doc.exists:
            data = doc.to_dict()
            if 'comments' in data:
                del data['comments']
            return data
        return "user not found", 404

    if(request.method == 'POST'):
        json = request.get_json()
        db.collection(u'users').document(uid).set(json)
        return 'user created', 201
