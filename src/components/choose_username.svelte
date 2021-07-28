<script>
    import { username, status, uid } from "./../stores";
    import * as stores from "./../stores";
    let input = "";
    function addUsername() {
        if (input.length < 4) return;
        let xhr = new XMLHttpRequest();
        xhr.open("POST", stores.baseURL + "/users/" + $uid);
        xhr.onreadystatechange = function () {
            if (this.readyState == XMLHttpRequest.DONE) {
                if (this.status == 201) {
                    username.set(input);
                    status.set(stores.Status.Success);
                }
            }
        };
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(
            JSON.stringify({
                username: input,
            })
        );
    }
</script>

<div class="alert alert-warning d-flex align-items-center" role="alert">
    Please, choose a username
</div>
<div class="input-group container">
    <input
        type="text"
        bind:value={input}
        class="form-control"
        placeholder="Your username..."
        aria-describedby="button-addon2"
    />
    <button
        class="btn btn-warning"
        type="button"
        id="button-addon2"
        on:click={addUsername}>OK</button
    >
</div>
