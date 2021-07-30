<script>
    import { baseURL, uid, comments, message, videoId } from "./../stores";
    import { DateDiff } from "../date_utility";
    import * as stores from "./../stores";

    export let commentId = "";
    let visible = false;
    let myComments;
    $: myComments = $comments;
    let now = new Date();

    function changeVisibility() {
        visible = !visible;
    }

    function fetchReplies() {
        if (commentId == "") return;
        now = new Date();
        if ("replies" in myComments[commentId]) {
            changeVisibility();
            return;
        }
        let xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            if (this.readyState == XMLHttpRequest.DONE) {
                if (this.status == 200) {
                    let obj = JSON.parse(xhr.responseText);
                    comments.update(function (comments) {
                        comments[commentId].replies = obj.replies;
                        return comments;
                    });
                    changeVisibility();
                } else {
                    message.set("An error accured");
                    console.log(xhr.responseText);
                }
            }
        };

        xhr.open("POST", baseURL + "/" + $videoId + "/replies/" + commentId);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(
            JSON.stringify({
                uid: $uid,
            })
        );
    }
    function deleteReply(replyId) {
        let xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            if (this.readyState == XMLHttpRequest.DONE) {
                if (this.status == 200) {
                    // success
                    comments.update(function (comments) {
                        delete comments[commentId].replies[replyId];
                        return comments;
                    });
                } else {
                    // error
                    stores.message.set("An error occured");
                    console.log(this.responseText);
                }
            }
        };
        xhr.open(
            "DELETE",
            stores.baseURL + "/" + $videoId + "/reply/" + commentId
        );
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(
            JSON.stringify({
                authorId: $uid,
                replyId: replyId,
            })
        );
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
            <i>{DateDiff.getString(new Date(reply.lastUpdateAt), now)}</i>
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
