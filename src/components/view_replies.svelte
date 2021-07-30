<script>
    import { uid, comments, message, videoId } from "./../stores";
    import { DateDiff } from "../date_utility";
    import firebase from "firebase/app";
    import "firebase/firestore";

    var db = firebase.firestore();

    export let commentId = "";
    let visible = false;
    let myComments;
    $: myComments = $comments;
    let now = new Date();

    function changeVisibility() {
        visible = !visible;
    }

    async function fetchReplies() {
        if (commentId == "") return;
        now = new Date();
        if ("replies" in myComments[commentId]) {
            changeVisibility();
            return;
        }
        try {
            let docs = await db
                .collection("videos")
                .doc($videoId)
                .collection("comments")
                .doc(commentId)
                .collection("replies")
                .get();
            let obj = {};
            docs.forEach((doc) => {
                obj[doc.id] = doc.data();
            });
            comments.update(function (value) {
                value[commentId].replies = obj;
                return value;
            });
            changeVisibility();
        } catch (error) {
            console.log(error);
            message.set("An error occured");
        }
    }
    async function deleteReply(replyId) {
        try {
            let replyRef = db
                .collection("videos")
                .doc($videoId)
                .collection("comments")
                .doc(commentId)
                .collection("replies")
                .doc(replyId);
            await replyRef.delete();
            comments.update(function (comments) {
                delete comments[commentId].replies[replyId];
                return comments;
            });
            await db
                .collection("users")
                .doc($uid)
                .update({
                    [`comments.${$videoId}`]:
                        firebase.firestore.FieldValue.arrayRemove(replyRef),
                });
        } catch (error) {
            message.set("An error occured");
            console.log(error);
        }
    }
</script>

{#if visible}
    <button class="btn btn-sm" on:click={changeVisibility}
        >HIDE REPLIES <svg
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            fill="currentColor"
            class="bi bi-caret-up"
            viewBox="0 0 16 16"
        >
            <path
                d="M3.204 11h9.592L8 5.519 3.204 11zm-.753-.659 4.796-5.48a1 1 0 0 1 1.506 0l4.796 5.48c.566.647.106 1.659-.753 1.659H3.204a1 1 0 0 1-.753-1.659z"
            />
        </svg></button
    >
    {#each Object.entries(myComments[commentId].replies) as [id, reply]}
        <div style="margin-left: 15px">
            <b>{reply.authorName}</b>
            <i>{DateDiff.getString(reply.lastUpdateAt.toDate(), now)}</i>
            <br />
            {reply.text} <br />
            {#if reply.authorId == $uid}
                <button class="btn btn-sm" on:click={() => deleteReply(id)}>
                    DELETE
                </button>
            {/if}
        </div>
    {/each}
{:else}
    <button class="btn btn-sm" on:click={fetchReplies}
        >VIEW REPLIES <svg
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            fill="currentColor"
            class="bi bi-caret-down"
            viewBox="0 0 16 16"
        >
            <path
                d="M3.204 5h9.592L8 10.481 3.204 5zm-.753.659 4.796 5.48a1 1 0 0 0 1.506 0l4.796-5.48c.566-.647.106-1.659-.753-1.659H3.204a1 1 0 0 0-.753 1.659z"
            />
        </svg></button
    >
{/if}
