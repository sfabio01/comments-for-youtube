<script>
    import { username, status } from "./../stores";
    import * as stores from "./../stores";
    import firebase from "firebase/app";
    import "firebase/auth";

    let input = "";
    function addUsername() {
        if (input.length < 4) return;
        stores.userData
            .updateProfile({
                displayName: input,
            })
            .then(() => {
                username.set(input);
                status.set(stores.Status.Success);
            })
            .catch((error) => {
                console.log(error);
                stores.message.set(error.message);
                status.set(stores.Status.Failed);
            });
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
