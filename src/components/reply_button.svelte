<script>
    import * as stores from "./../stores";
    import { uid, comments } from "./../stores";
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
                stores.baseURL + "/2ffmZjaatIc/reply/" + commentId
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
                    authorName: stores.username,
                    text: replyText,
                })
            );
        }
    }
</script>

<button on:click={changeInputVisibility}>REPLY</button>

{#if viewinput}
    <input type="text" bind:value={input} placeholder="Add a reply..." />
    <button on:click={reply}>SEND</button>
    <button on:click={changeInputVisibility}>X</button>
{/if}
