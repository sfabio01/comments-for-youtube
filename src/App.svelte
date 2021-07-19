<script>
	import { BarLoader } from "svelte-loading-spinners";
	import InputField from "./components/input_field.svelte";
	import MessageField from "./components/message_field.svelte";
	import CommentsSection from "./components/comments_section.svelte";
	import * as stores from "./stores";
	import { uid } from "./stores";

	chrome.identity.getProfileUserInfo(function (infos) {
		uid.set(infos.id);
		if (infos.id == "") {
			// user not signed in
			stores.message.set("You are not signed in :/");
		} else {
			// fetch username
			let xhr = new XMLHttpRequest();
			xhr.open("GET", stores.baseURL + "/users/" + infos.id);
			xhr.onreadystatechange = function () {
				if (this.readyState == XMLHttpRequest.DONE) {
					if (this.status == 200) {
						stores.setUsername(
							JSON.parse(xhr.responseText).username
						);
						stores.message.set("User: " + stores.username);
					}
					if (this.status == 404) {
						// ask for username
						let input = "";
						do {
							input = prompt("Choose a username").trim();
						} while (input == "" || input == null);
						stores.setUsername(input);
						let xhr = new XMLHttpRequest();
						xhr.open("POST", stores.baseURL + "/users/" + infos.id);
						xhr.setRequestHeader(
							"Content-Type",
							"application/json"
						);
						xhr.send(JSON.stringify({ username: username }));
						stores.message.set("User: " + stores.username);
					}
				}
			};
			xhr.send();
		}
	});
</script>

<InputField />
<MessageField />
<CommentsSection />

<style>
</style>
