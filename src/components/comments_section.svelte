<script>
    import LoadMoreButton from "./load_more_button.svelte";
    import ReplyButton from "./reply_button.svelte";
    import ViewReplies from "./view_replies.svelte";
    import * as stores from "./../stores";
    import { comments, uid, videoId } from "./../stores";
    import { DateDiff } from "./../utils";

    let userId;
    $: userId = $uid;
    let myVideoId;
    $: myVideoId = $videoId;

    $: downloadComments(userId, myVideoId);

    let now = new Date();

    function like(commentId) {
        let xhr = new XMLHttpRequest();
        xhr.open(
            "POST",
            stores.baseURL + "/" + $videoId + "/like/" + commentId
        );
        xhr.onreadystatechange = function () {
            if (this.readyState == XMLHttpRequest.DONE) {
                if (this.status == 200) {
                    comments.update(function (val) {
                        val[commentId].liked = true;
                        val[commentId].likes++;
                        return val;
                    });
                } else {
                    // failed
                }
            }
        };
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(JSON.stringify({ uid: userId }));
    }

    function removelike(commentId) {
        let xhr = new XMLHttpRequest();
        xhr.open(
            "DELETE",
            stores.baseURL + "/" + $videoId + "/like/" + commentId
        );
        xhr.onreadystatechange = function () {
            if (this.readyState == XMLHttpRequest.DONE) {
                if (this.status == 200) {
                    comments.update(function (val) {
                        val[commentId].liked = false;
                        val[commentId].likes--;
                        return val;
                    });
                } else {
                    // failed
                }
            }
        };
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(JSON.stringify({ uid: userId }));
    }

    function downloadComments(uid, videoId) {
        if (uid == "" || videoId == "") return;
        let xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            if (this.readyState == XMLHttpRequest.DONE) {
                if (this.status == 200) {
                    let obj = JSON.parse(xhr.responseText);
                    comments.update(function (val) {
                        let res = { ...val, ...obj.comments };
                        stores.setOffset(Object.keys(res).length);
                        return res;
                    });
                } else {
                    stores.message.set("An error occured");
                    console.log(xhr.responseText);
                }
            }
        };

        xhr.open(
            "POST",
            stores.baseURL + "/" + videoId + "/" + stores.offset.toString()
        );
        xhr.setRequestHeader("Content-Type", "application/json");

        xhr.send(
            JSON.stringify({
                uid: userId,
            })
        );
    }
    function reload() {
        now = new Date();
        stores.setOffset(0);
        comments.set({});
        downloadComments(userId, myVideoId);
    }
    function editComment(commentId, text) {
        let editedComment = prompt("Edit the comment", text);
        if (editedComment == null) return;
        editedComment = editedComment.trim();
        if (editedComment == "") return;

        let xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            if (this.readyState == XMLHttpRequest.DONE) {
                if (this.status == 201) {
                    // success
                    let obj = JSON.parse(xhr.responseText);
                    comments.update(function (comments) {
                        comments[commentId] = obj.comment;
                        return comments;
                    });
                } else {
                    // error
                    stores.message.set("An error occured");
                }
            }
        };
        xhr.open("PUT", stores.baseURL + "/" + $videoId);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(
            JSON.stringify({
                text: editedComment,
                commentId: commentId,
            })
        );
    }
    function deleteComment(commentId) {
        let xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            if (this.readyState == XMLHttpRequest.DONE) {
                if (this.status == 200) {
                    // success
                    comments.update(function (comments) {
                        delete comments[commentId];
                        return comments;
                    });
                } else {
                    // error
                    stores.message.set("An error occured");
                }
            }
        };
        xhr.open("DELETE", stores.baseURL + "/" + $videoId);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(
            JSON.stringify({
                authorId: userId,
                commentId: commentId,
            })
        );
    }
</script>

<button on:click={reload}>RELOAD</button>

{#each Object.entries($comments) as [id, comment]}
    <hr />
    <b>{comment.authorName}</b>
    <i>{DateDiff.getString(new Date(comment.lastUpdateAt), now)}</i> <br />
    {comment.text} <br />
    Likes: {comment.likes}
    {#if comment.liked}
        <button on:click={() => removelike(id)} style="color: blue;"
            >LIKE</button
        >
    {:else}
        <button on:click={() => like(id)}>LIKE</button>
    {/if}
    <br />
    {#if comment.authorId == userId}
        <button on:click={() => editComment(id, comment.text)}>EDIT</button>
        <button on:click={() => deleteComment(id)}>DELETE</button>
        <br />
    {/if}
    <ReplyButton commentId={id} />
    <br />
    <ViewReplies commentId={id} />
    <br />
    <br />
{/each}

<LoadMoreButton on:loadMore={() => downloadComments(userId, myVideoId)} />
