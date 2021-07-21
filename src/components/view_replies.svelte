<script>
    import { baseURL, uid, comments, message } from "./../stores";

    export let commentId = "";
    let visible = false;
    let myComments;
    $: myComments = $comments;

    function changeVisibility() {
        visible = !visible;
    }

    function fetchReplies() {
        if (commentId == "") return;

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
