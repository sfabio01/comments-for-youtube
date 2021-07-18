<script>
    import { createEventDispatcher } from "svelte";

    export let uid = "";
    export let commentId = "";
    export let username = "";

    const dispatch = createEventDispatcher();

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
                "http://127.0.0.1:5001/2ffmZjaatIc/reply/" + commentId
            );
            xhr.onreadystatechange = function () {
                if (this.readyState == XMLHttpRequest.DONE) {
                    if (this.status == 201) {
                        // success
                        let obj = xhr.response;
                        input = "";
                        changeInputVisibility();
                        dispatch("replySuccess", obj);
                    } else {
                        // error
                    }
                }
            };
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.send(
                JSON.stringify({
                    authorId: uid,
                    authorName: username,
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
