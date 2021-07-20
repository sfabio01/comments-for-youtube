<script>
    import { baseURL, uid, comments } from "./../stores";

    export let commentId = "";
    let visible = false;
    let myComments;
    $: myComments = $comments;

    function changeVisibility() {
        visible = !visible;
    }

    function fetchReplies() {
        if (commentId == "") return;
        let xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            if (this.readyState == XMLHttpRequest.DONE && this.status == 200) {
                let obj = JSON.parse(xhr.responseText);
                console.log(obj);
                comments.update(function (comments) {
                    comments[commentId].replies = obj.replies;

                    console.log(comments);
                    return comments;
                });
                changeVisibility();
            }
        };

        xhr.open("POST", baseURL + "/2ffmZjaatIc/replies/" + commentId);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(
            JSON.stringify({
                uid: $uid,
            })
        );
    }
</script>

{#if visible}
    <button on:click={changeVisibility}>HIDE REPLIES</button>
    {#each Object.entries(myComments[commentId].replies) as [id, reply]}
        <div style="margin-left: 20px">
            <b>{reply.authorName}</b> <br />
            {reply.text} <br />
        </div>
    {/each}
{:else}
    <button on:click={fetchReplies}>VIEW REPLIES</button>
{/if}
