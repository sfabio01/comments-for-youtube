<script>
    import { BarLoader } from "svelte-loading-spinners";
    import { createEventDispatcher } from "svelte";

    let input = "";
    export let uid = "";
    export let username = "";

    const dispatch = createEventDispatcher();

    function addcomment() {
        let comment = input.trim();
        if (comment != "") {
            let xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function () {
                if (this.readyState == XMLHttpRequest.DONE) {
                    if (this.status == 201) {
                        // success
                        input = "";
                        dispatch("commentSuccess", xhr.response);
                    } else {
                        // error
                    }
                }
            };
            xhr.open("POST", "http://127.0.0.1:5001/2ffmZjaatIc");
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.send(
                JSON.stringify({
                    text: comment,
                    authorName: username,
                    authorId: uid,
                })
            );
        }
    }
</script>

<input type="text" bind:value={input} placeholder="Add a comment..." />
<button on:click={addcomment}>SUBMIT</button>
