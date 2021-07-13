<script>
    let offset = 0;
    let comments = {};
    let xhr = new XMLHttpRequest();
    xhr.open("GET", "http://127.0.0.1:5001/2ffmZjaatIc/" + offset.toString());
    xhr.onreadystatechange = function () {
        if (this.readyState == XMLHttpRequest.DONE) {
            if (this.status == 200) {
                let obj = JSON.parse(xhr.responseText);
                comments = obj.comments;
            } else {
                // failed
            }
        }
    };
    xhr.send();
    function like(commentId) {}
</script>

{#each Object.entries(comments) as [id, comment]}
    <b>{comment.authorName}</b> <br />
    {comment.text} <br />
    Likes: {comment.likes} <button on:click={like(id)}>LIKE</button> <br />
    <br />
{/each}
