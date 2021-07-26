<script>
	import { BarLoader } from "svelte-loading-spinners";
	import InputField from "./components/input_field.svelte";
	import MessageField from "./components/message_field.svelte";
	import CommentsSection from "./components/comments_section.svelte";
	import * as stores from "./stores";
	import { uid, videoId, status } from "./stores";

	chrome.tabs.query(
		{
			active: true,
			currentWindow: true,
		},
		function ([tab]) {
			let url = tab.url;
			videoId.set(getUrlParams(url)["v"]);
			let xhr = new XMLHttpRequest();
			xhr.open(
				"GET",
				"https://youtube.googleapis.com/youtube/v3/commentThreads?part=id&videoId=" +
					$videoId +
					"&key=AIzaSyAzRbVzVFIftvpw5To_YP67scHt2c5ccYQ"
			);
			xhr.onreadystatechange = function () {
				if (this.readyState == XMLHttpRequest.DONE) {
					if (this.status == 403) {
						let res = JSON.parse(this.responseText);
						if (res.error.errors[0].reason == "commentsDisabled") {
							status.set(stores.Status.Enabled);

							return;
						}
					}
				}
				status.set(stores.Status.Disabled);
			};
			xhr.send();
		}
	);

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
	function getUrlParams(url) {
		var vars = {};
		var parts = url.replace(
			/[?&]+([^=&]+)=([^&]*)/gi,
			function (m, key, value) {
				vars[key] = value;
			}
		);
		return vars;
	}
</script>

{#if $status == stores.Status.Enabled}
	<InputField />
	<MessageField />
	<CommentsSection />
{:else if $status == stores.Status.Disabled}
	Comments are already Enabled
{/if}

<style>
</style>
