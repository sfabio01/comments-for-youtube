<script>
    import { status } from "./../stores";
    import * as stores from "./../stores";
    function logout() {
        chrome.runtime.sendMessage(
            { command: "logoutAuth", data: {} },
            (response) => {
                if (response.status == "success") {
                    status.set(stores.Status.NotLoggedIn);
                } else {
                    stores.message.set(
                        "An error occured. Try restarting the extension"
                    );
                    status.set(stores.Status.Failed);
                }
            }
        );
    }
</script>

<div class="container">
    <button
        type="button"
        class="btn btn-sm btn-secondary d-block mx-auto my-3"
        on:click={logout}>LOGOUT</button
    >
</div>
