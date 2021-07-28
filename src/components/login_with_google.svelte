<script>
    import { uid, status, username } from "./../stores";
    import * as stores from "./../stores";

    function login() {
        chrome.runtime.sendMessage(
            { command: "loginUser", data: {} },
            (response) => {
                console.log(response);
                if (response.status == "success") {
                    uid.set(response.message.uid);
                    // fetch username
                    let xhr = new XMLHttpRequest();
                    xhr.open("GET", stores.baseURL + "/users/" + $uid);
                    xhr.onreadystatechange = function () {
                        if (this.readyState == XMLHttpRequest.DONE) {
                            if (this.status == 200) {
                                username.set(
                                    JSON.parse(xhr.responseText).username
                                );
                                status.set(stores.Status.Success);
                            }
                            if (this.status == 404) {
                                // ask for username
                                status.set(stores.Status.MissingUsername);
                            }
                        }
                    };
                    xhr.send();
                } else {
                    status.set(stores.Status.Failed);
                }
            }
        );
    }
</script>

<div class="container " />
<button type="button" class="btn btn-primary m-auto " on:click={login}
    ><b>CONTINUE WITH GOOGLE</b></button
>
