<script>
    import { uid, comments, message, videoId, username } from "./../stores";
    let input = "";
    import firebase from "firebase/app";
    import "firebase/firestore";

    var db = firebase.firestore();

    async function addcomment() {
        let comment = input.trim();
        if (comment != "") {
            let obj = {
                text: comment,
                authorName: $username,
                authorId: $uid,
                likes: 0,
                lastUpdateAt: firebase.firestore.FieldValue.serverTimestamp(),
            };
            try {
                let commentRef = db
                    .collection("videos")
                    .doc($videoId)
                    .collection("comments")
                    .doc();
                await commentRef.set(obj);
                await db
                    .collection("users")
                    .doc($uid)
                    .update({
                        [`comments.${$videoId}`]:
                            firebase.firestore.FieldValue.arrayUnion(
                                commentRef
                            ),
                    });
                let snap = await commentRef.get();
                comments.update(function (old) {
                    let newComment = snap.data();
                    newComment.replies = {};
                    return { [snap.id]: newComment, ...old };
                });
                input = "";
            } catch (error) {
                message.set("An error occured");
                console.log(error);
            }
        }
    }
</script>

<div class="container">
    <div class="input-group my-2 mx-auto">
        <input
            type="text"
            class="form-control form-control-sm"
            bind:value={input}
            placeholder="({$username}) Add a comment..."
            aria-describedby="button-addon2"
        />
        <button
            on:click={addcomment}
            type="button"
            class="btn btn-primary btn-sm"
            id="button-addon2">ADD</button
        >
    </div>
</div>
