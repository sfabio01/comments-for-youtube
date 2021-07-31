<script>
    import { status } from "./../stores";
    import * as stores from "./../stores";
    import firebase from "firebase/app";
    import "firebase/auth";

    function logout() {
        firebase
            .auth()
            .signOut()
            .then(() => {
                stores.comments.set({});
                stores.setLastCommentUpdateTime("");
                stores.setUserData(null);
                chrome.storage.local.set({});
                status.set(stores.Status.NotLoggedIn);
            })
            .catch((error) => {
                console.log(error);
                stores.message.set(error.message);
                status.set(stores.Status.Failed);
            });
    }
</script>

<div class="container">
    <button
        type="button"
        class="btn btn-sm btn-secondary d-block mx-auto my-3"
        on:click={logout}>LOGOUT</button
    >
</div>
