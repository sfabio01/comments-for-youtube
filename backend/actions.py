from __main__ import app, db
from flask import jsonify, request
from firebase_admin import firestore


@app.route('/<string:videoId>/like/<string:commentId>', methods=['POST', 'DELETE'])
def like(videoId, commentId):
    if(request.method == 'POST'):
        uid = request.get_json()['uid']
        try:
            likes_list = db.collection('users').document(
                uid).get().to_dict()['likes'][videoId]
        except KeyError:
            likes_list = []
        if commentId not in likes_list:
            comment_ref = db.collection('videos').document(
                videoId).collection('comments').document(commentId)
            comment_ref.update({'likes': firestore.Increment(1)})
            db.collection('users').document(uid).update({
                f'likes.{videoId}': firestore.ArrayUnion([commentId])
            })
            return 'Success', 200
        else:
            return 'Already liked', 403

    if(request.method == 'DELETE'):
        uid = request.get_json()['uid']
        try:
            likes_list = db.collection('users').document(
                uid).get().to_dict()['likes'][videoId]
        except KeyError:
            likes_list = []
        if commentId in likes_list:
            comment_ref = db.collection('videos').document(
                videoId).collection('comments').document(commentId)
            comment_ref.update({'likes': firestore.Increment(-1)})
            db.collection('users').document(uid).update({
                f'likes.{videoId}': firestore.ArrayRemove([commentId])
            })
            return 'Success', 200
        else:
            return 'Already not liked', 403


@app.route('/<string:videoId>/reply/<string:commentId>', methods=['POST', 'DELETE'])
def manage_reply(videoId, commentId):
    if(request.method == 'POST'):
        json = request.get_json()
        reply_obj = {
            "text": json['text'],
            "authorName": json['authorName'],
            "authorId": json['authorId'],
            "likes": 0,
            "lastUpdateAt": firestore.SERVER_TIMESTAMP
        }
        reply_ref = db.collection('videos').document(
            videoId).collection('comments').document(commentId).collection('replies').document()
        reply_ref.set(reply_obj)
        uid = json['authorId']
        db.collection('users').document(uid).update({
            f'comments.{videoId}': firestore.ArrayUnion([reply_ref])
        })
        snap = reply_ref.get()
        return {'replyId': snap.id, 'reply': snap.to_dict()}, 201
    if (request.method == 'DELETE'):
        replyId = request.get_json()['replyId']
        reply_ref = db.collection('videos').document(
            videoId).collection('comments').document(commentId).collection('replies').document(replyId)
        reply_ref.delete()
        uid = request.get_json()['authorId']
        db.collection('users').document(uid).update({
            f'comments.{videoId}': firestore.ArrayRemove([reply_ref])
        })
        return "Success", 200

@app.route('/<string:videoId>/replies/<string:commentId>', methods=['POST'])
def fetch_replies(videoId, commentId):
    if(request.method == 'POST'):
        #uid = request.get_json()['uid']
        docs = db.collection('videos').document(videoId).collection('comments').document(commentId).collection('replies').stream()
        response = {}
        for doc in docs:
            response[doc.id] = doc.to_dict()
        return {'replies': response}




        
