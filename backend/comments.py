from __main__ import app, db
from flask import jsonify, request, Response
from firebase_admin import firestore


@app.route('/<string:videoId>', methods=['POST', 'PUT', 'DELETE'])
def manage_comments(videoId):
    if(request.method == 'POST'):
        json = request.get_json()
        comment_obj = {
            "text": json['text'],
            "authorName": json['authorName'],
            "authorId": json['authorId'],
            "likes": 0,
            "lastUpdateAt": firestore.SERVER_TIMESTAMP
        }
        comment_ref = db.collection('videos').document(
            videoId).collection('comments').document()
        comment_ref.set(comment_obj)
        uid = json['authorId']
        db.collection('users').document(uid).update({
            f'comments.{videoId}': firestore.ArrayUnion([comment_ref])
        })
        snap = comment_ref.get()
        comment = snap.to_dict()
        comment['replies'] = {}
        return {'commentId': snap.id, 'comment': comment}, 201

    if(request.method == 'PUT'):
        json = request.get_json()
        comment_obj = {
            "text": json['text'],
            "lastUpdateAt": firestore.SERVER_TIMESTAMP
        }
        comment_ref = db.collection('videos').document(
            videoId).collection('comments').document(json['commentId'])
        comment_ref.update(comment_obj)
        
        snap = comment_ref.get()
        
        return {'commentId': snap.id, 'comment': snap.to_dict()}, 201

    if(request.method == 'DELETE'):
        commentId = request.get_json()['commentId']
        comment_ref = db.collection('videos').document(
            videoId).collection('comments').document(commentId)
        comment_ref.delete()
        uid = request.get_json()['authorId']
        db.collection('users').document(uid).update({
            f'comments.{videoId}': firestore.ArrayRemove([comment_ref])
        })
        db.collection('users').document(uid).update({
            f'likes.{videoId}': firestore.ArrayRemove([commentId])
        })
        return "Success", 200
        

@app.route('/<string:videoId>/<int:startAfter>', methods=['POST'])
def fetch_comments(videoId, startAfter):
    if(request.method == 'POST'):
        uid = request.get_json()['uid']
        collection_ref = db.collection(u'videos').document(
            videoId).collection(u'comments')
        query = collection_ref.order_by(
            u'lastUpdateAt', direction=firestore.Query.DESCENDING).offset(startAfter).limit(4)
        comments = query.get()
        print(uid)
        try:
            liked_list = db.collection('users').document(
                uid).get().to_dict()['likes'][videoId]
        except KeyError:
            liked_list = []
        response = {}
        for comment in comments:
            doc = comment.to_dict()
            if comment.id in liked_list:
                doc['liked'] = True
            else:
                doc['liked'] = False
            response[comment.id] = doc
       
        return jsonify({'comments': response})
