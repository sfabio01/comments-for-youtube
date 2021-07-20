<script>
    import LoadMoreButton from "./load_more_button.svelte";
    import ReplyButton from "./reply_button.svelte";
    import ViewReplies from "./view_replies.svelte";
    import * as stores from "./../stores";
    import { comments, uid } from "./../stores";

    let userId;
    $: userId = $uid;

    $: downloadComments(userId);

    function like(commentId) {
        let xhr = new XMLHttpRequest();
        xhr.open("POST", stores.baseURL + "/2ffmZjaatIc/like/" + commentId);
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
        xhr.open("DELETE", stores.baseURL + "/2ffmZjaatIc/like/" + commentId);
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

    function downloadComments(uid) {
        if (uid == "") return;
        let xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            if (this.readyState == XMLHttpRequest.DONE && this.status == 200) {
                let obj = JSON.parse(xhr.responseText);
                comments.update(function (val) {
                    let res = { ...val, ...obj.comments };
                    stores.setOffset(Object.keys(res).length);
                    return res;
                });
            }
        };

        xhr.open(
            "POST",
            stores.baseURL + "/2ffmZjaatIc/" + stores.offset.toString()
        );
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(
            JSON.stringify({
                uid: userId,
            })
        );
    }
    function reload() {
        // fixare
        stores.setOffset(0);
        downloadComments(userId);
    }
</script>

<button on:click={reload}>RELOAD</button>

{#each Object.entries($comments) as [id, comment]}
    <hr />
    <b>{comment.authorName}</b> <br />
    {comment.text} <br />
    Likes: {comment.likes}
    {#if comment.liked}
        <button
            id="like-{id}"
            on:click={() => removelike(id)}
            style="color: blue;">LIKE</button
        >
    {:else}
        <button id="like-{id}" on:click={() => like(id)}>LIKE</button>
    {/if}
    <br />
    <ReplyButton commentId={id} />
    <br />
    <ViewReplies commentId={id} />
    <br />
    <br />
{/each}

<LoadMoreButton on:loadMore={() => downloadComments(userId)} />
