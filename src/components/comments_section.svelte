<script>
    import LoadMoreButton from "./load_more_button.svelte";

    export let uid = "";
    let offset = 0;

    let comments = {};

    let xhr = new XMLHttpRequest();
    xhr.open("GET", "http://127.0.0.1:5001/2ffmZjaatIc/" + offset.toString());
    xhr.onreadystatechange = function () {
        if (this.readyState == XMLHttpRequest.DONE) {
            if (this.status == 200) {
                let obj = JSON.parse(xhr.responseText);
                comments = obj.comments;
                offset = Object.keys(comments).length;
            } else {
                // failed
            }
        }
    };
    xhr.send();

    function like(commentId) {
        let xhr = new XMLHttpRequest();
        xhr.open("POST", "http://127.0.0.1:5001/2ffmZjaatIc/like/" + commentId);
        xhr.onreadystatechange = function () {
            if (this.readyState == XMLHttpRequest.DONE) {
                if (this.status == 200) {
                    document.getElementById(commentId).style.backgroundColor =
                        "green";
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

    function loadMore() {
        let xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            if (this.readyState == XMLHttpRequest.DONE && this.status == 200) {
                let obj = JSON.parse(xhr.responseText);
                comments = { ...comments, ...obj.comments };
                offset = Object.keys(comments).length;
            }
        };

        xhr.open(
            "GET",
            "http://127.0.0.1:5001/2ffmZjaatIc/" + offset.toString()
        );
        xhr.send();
    }
    function reload() {
        offset = 0;
        let xhr = new XMLHttpRequest();
        xhr.open(
            "GET",
            "http://127.0.0.1:5001/2ffmZjaatIc/" + offset.toString()
        );
        xhr.onreadystatechange = function () {
            if (this.readyState == XMLHttpRequest.DONE) {
                if (this.status == 200) {
                    let obj = JSON.parse(xhr.responseText);
                    comments = obj.comments;
                    offset = Object.keys(comments).length;
                } else {
                    // failed
                }
            }
        };
        xhr.send();
    }
</script>

<button on:click={reload}>RELOAD</button>

{#each Object.entries(comments) as [id, comment]}
    <hr />
    <b>{comment.authorName}</b> <br />
    {comment.text} <br />
    Likes: {comment.likes} <button {id} on:click={like(id)}>LIKE</button> <br />
    <br />
{/each}

<LoadMoreButton on:loadMore={loadMore} />
