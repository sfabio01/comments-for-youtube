<script>
    import * as stores from "./../stores";
    import { uid, comments, message, videoId, username } from "./../stores";
    let input = "";

    function addcomment() {
        let comment = input.trim();
        if (comment != "") {
            let xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function () {
                if (this.readyState == XMLHttpRequest.DONE) {
                    if (this.status == 201) {
                        // success
                        let obj = JSON.parse(xhr.responseText);
                        input = "";
                        comments.update(function (comments) {
                            comments = {
                                [obj.commentId]: obj.comment,
                                ...comments,
                            };
                            console.log(comments);
                            return comments;
                        });
                    } else {
                        // error
                        message.set("An error occured");
                    }
                }
            };
            xhr.open("POST", stores.baseURL + "/" + $videoId);
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.send(
                JSON.stringify({
                    text: comment,
                    authorName: $username,
                    authorId: $uid,
                })
            );
        }
    }
</script>

<div class="container">
    <div class="input-group my-2 mx-auto">
        <input
            type="text"
            class="form-control form-control-sm"
            bind:value={input}
            placeholder="({$username}) Add a comment..."
            aria-describedby="button-addon2"
        />
        <button
            on:click={addcomment}
            type="button"
            class="btn btn-primary btn-sm"
            id="button-addon2">ADD</button
        >
    </div>
</div>
