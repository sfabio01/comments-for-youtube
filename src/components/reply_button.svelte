<script>
    import * as stores from "./../stores";
    import { uid, comments, videoId, username } from "./../stores";
    export let commentId = "";

    let viewinput = false;
    let input = "";

    function changeInputVisibility() {
        viewinput = !viewinput;
    }

    function reply() {
        let replyText = input.trim();
        if (replyText != "") {
            let xhr = new XMLHttpRequest();
            xhr.open(
                "POST",
                stores.baseURL + "/" + $videoId + "/reply/" + commentId
            );
            xhr.onreadystatechange = function () {
                if (this.readyState == XMLHttpRequest.DONE) {
                    if (this.status == 201) {
                        // success
                        input = "";
                        changeInputVisibility();
                        let obj = JSON.parse(xhr.responseText);
                        comments.update(function (comments) {
                            comments[commentId].replies[obj.replyId] =
                                obj.reply;
                            return comments;
                        });
                    } else {
                    }
                }
            };
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.send(
                JSON.stringify({
                    authorId: $uid,
                    authorName: $username,
                    text: replyText,
                })
            );
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
