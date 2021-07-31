<script>
    import { uid, status, username } from "./../stores";
    import * as stores from "./../stores";
    import firebase from "firebase/app";
    import "firebase/auth";

    var provider = new firebase.auth.GoogleAuthProvider();

    function login() {
        firebase
            .auth()
            .signInWithPopup(provider)
            .then((result) => {
                let user = result.user;
                stores.setUserData(user);
                uid.set(user.uid);
                if (user.displayName == "") {
                    status.set(stores.Status.MissingUsername);
                } else {
                    username.set(user.displayName);
                    chrome.storage.local.set({ user: user }, function () {
                        console.log("User data stored in storage: " + user);
                    });
                    status.set(stores.Status.Success);
                }
            })
            .catch((error) => {
                console.log(error);
                stores.message.set("An error occured");
                status.set(stores.Status.Failed);
            });
    }
</script>

<div
    class="d-flex justify-content-center align-items-center"
    style="height: 600px;"
>
    <button type="button" class="btn btn-primary" on:click={login}
        ><b>CONTINUE WITH GOOGLE</b></button
    >
</div>
