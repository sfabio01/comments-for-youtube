<script>
    import * as stores from "./../stores";
    import { uid } from "./../stores";
    let input = "";

    function addcomment() {
        let comment = input.trim();
        if (comment != "") {
            let xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function () {
                if (this.readyState == XMLHttpRequest.DONE) {
                    if (this.status == 201) {
                        // success
                        input = "";
                    } else {
                        // error
                    }
                }
            };
            xhr.open("POST", stores.baseURL + "/2ffmZjaatIc");
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.send(
                JSON.stringify({
                    text: comment,
                    authorName: stores.username,
                    authorId: $uid,
                })
            );
        }
    }
</script>

<input type="text" bind:value={input} placeholder="Add a comment..." />
<button on:click={addcomment}>SUBMIT</button>
