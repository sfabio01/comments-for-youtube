<script>
	import InputField from "./components/input_field.svelte";
	import MessageField from "./components/message_field.svelte";
	import CommentsSection from "./components/comments_section.svelte";

	let uid = "";
	let msg = "";
	let username = "";

	chrome.identity.getProfileUserInfo(function (infos) {
		uid = infos.id;
		if (uid == "") {
			// user not signed in
			msg = "You are not signed in :/";
		} else {
			// fetch username
			let xhr = new XMLHttpRequest();
			xhr.open("GET", "http://127.0.0.1:5001/users/" + uid);
			xhr.onreadystatechange = function () {
				if (this.readyState == XMLHttpRequest.DONE) {
					if (this.status == 200) {
						username = JSON.parse(xhr.responseText).username;
						msg = "user: " + username;
					}
					if (this.status == 404) {
						// ask for username
						let input = "";
						do {
							input = prompt("Choose a username").trim();
						} while (input == "" || input == null);
						username = input;
						let xhr = new XMLHttpRequest();
						xhr.open("POST", "http://127.0.0.1:5001/users/" + uid);
						xhr.setRequestHeader(
							"Content-Type",
							"application/json"
						);
						xhr.send(JSON.stringify({ username: username }));
						msg = "user: " + username;
					}
				}
			};
			xhr.send();
		}
	});
</script>

<InputField {uid} {username} />
<MessageField {msg} />
<CommentsSection {uid} {username} />

<style>
</style>
