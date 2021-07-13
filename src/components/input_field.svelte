<script>
    import { BarLoader } from "svelte-loading-spinners";
    let input = "";
    export let uid = "";
    export let username = "";

    function addcomment() {
        let comment = input.trim();
        if (comment != "") {
            let xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function () {
                if (this.readyState == XMLHttpRequest.DONE) {
                    if (this.status == 201) {
                        // success
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

<form on:submit={addcomment}>
    <input type="text" bind:value={input} placeholder="Add a comment..." />
    <button type="submit">SUBMIT</button>
</form>
