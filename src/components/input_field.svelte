<script>
    import { BarLoader } from "svelte-loading-spinners";
    let input = "";
    function addcomment() {
        let comment = input.trim();
        if (input != "") {
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
            xhr.open("POST", "http://127.0.0.1:5000/2ffmZjaatIc");
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.send();
        }
    }
</script>

<input type="text" bind:value={input} placeholder="Add a comment..." />
<button on:click={addcomment}>SUBMIT</button>
