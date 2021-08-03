<script>
    import {
        uid,
        comments,
        videoId,
        username,
        message,
    } from "./../../../stores";
    import firebase from "firebase/app";
    import "firebase/firestore";

    var db = firebase.firestore();

    export let commentId = "";

    let viewinput = false;
    let input = "";

    function changeInputVisibility() {
        viewinput = !viewinput;
    }

    async function reply() {
        let replyText = input.trim();
        if (replyText != "") {
            let obj = {
                text: replyText,
                authorName: $username,
                authorId: $uid,
                likes: 0,
                lastUpdateAt: firebase.firestore.FieldValue.serverTimestamp(),
            };
            try {
                let replyRef = db
                    .collection("videos")
                    .doc($videoId)
                    .collection("comments")
                    .doc(commentId)
                    .collection("replies")
                    .doc();
                await replyRef.set(obj);
                let snap = await replyRef.get();

                comments.update(function (value) {
                    if (!("replies" in value[commentId]))
                        value[commentId].replies = {};
                    value[commentId].replies[snap.id] = snap.data();
                    return value;
                });
                input = "";
                await db
                    .collection("users")
                    .doc($uid)
                    .update({
                        [`comments.${$videoId}`]:
                            firebase.firestore.FieldValue.arrayUnion(replyRef),
                    });
            } catch (error) {
                message.set(error.message);
                console.log(error);
            }
        }
    }
</script>

<button class="btn btn-sm" on:click={changeInputVisibility}>REPLY</button>

{#if viewinput}
    <div class="input-group d-flex justify-content-center px-2">
        <input
            type="text"
            class="form-control form-control-sm"
            bind:value={input}
            placeholder="Add a reply..."
        />
        <button class="btn btn-sm btn-primary" on:click={reply}>ADD</button>
    </div>
{/if}
