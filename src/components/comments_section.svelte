<script>
    import LoadMoreButton from "./load_more_button.svelte";

    export let uid = "";
    let offset = 0;

    let comments = {};

    $: loadMore(uid);

    function like(commentId) {
        let xhr = new XMLHttpRequest();
        xhr.open("POST", "http://127.0.0.1:5001/2ffmZjaatIc/like/" + commentId);
        xhr.onreadystatechange = function () {
            if (this.readyState == XMLHttpRequest.DONE) {
                if (this.status == 200) {
                    comments[commentId].liked = true;
                    comments[commentId].likes++;
                    comments = comments;
                } else {
                    // failed
                }
            }
        };
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(JSON.stringify({ uid: uid }));
    }

    function removelike(commentId) {
        let xhr = new XMLHttpRequest();
        xhr.open(
            "DELETE",
            "http://127.0.0.1:5001/2ffmZjaatIc/like/" + commentId
        );
        xhr.onreadystatechange = function () {
            if (this.readyState == XMLHttpRequest.DONE) {
                if (this.status == 200) {
                    comments[commentId].liked = false;
                    comments[commentId].likes--;
                    comments = comments;
                } else {
                    // failed
                }
            }
        };
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(JSON.stringify({ uid: uid }));
    }

    function loadMore(uid) {
        if (uid == "") return;
        let xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            if (this.readyState == XMLHttpRequest.DONE && this.status == 200) {
                let obj = JSON.parse(xhr.responseText);
                comments = { ...comments, ...obj.comments };
                offset = Object.keys(comments).length;
            }
        };

        xhr.open(
            "POST",
            "http://127.0.0.1:5001/2ffmZjaatIc/" + offset.toString()
        );
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(
            JSON.stringify({
                uid: uid,
            })
        );
    }
    function reload() {
        offset = 0;
        loadMore();
    }
</script>

<button on:click={reload}>RELOAD</button>

{#each Object.entries(comments) as [id, comment]}
    <hr />
    <b>{comment.authorName}</b> <br />
    {comment.text} <br />
    Likes: {comment.likes}
    {#if comment.liked}
        <button id="like-{id}" on:click={removelike(id)} style="color: blue;"
            >LIKE</button
        >
    {:else}
        <button id="like-{id}" on:click={like(id)}>LIKE</button>
    {/if}
    <br />
    <br />
{/each}

<LoadMoreButton on:loadMore={loadMore(uid)} />
