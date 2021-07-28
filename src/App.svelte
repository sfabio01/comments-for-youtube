<script>
	import InputField from "./components/input_field.svelte";
	import MessageField from "./components/message_field.svelte";
	import CommentsSection from "./components/comments_section.svelte";
	import * as stores from "./stores";
	import { uid, videoId, status, username } from "./stores";
	import ChooseUsername from "./components/choose_username.svelte";
	import LoginWithGoogle from "./components/login_with_google.svelte";

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
							//Check user logged in
							chrome.runtime.sendMessage(
								{ command: "checkAuth" },
								(response) => {
									console.log(response);
									if (response.status == "success") {
										uid.set(response.message.uid);
										// fetch username
										let xhr = new XMLHttpRequest();
										xhr.open(
											"GET",
											stores.baseURL + "/users/" + $uid
										);
										xhr.onreadystatechange = function () {
											if (
												this.readyState ==
												XMLHttpRequest.DONE
											) {
												if (this.status == 200) {
													username.set(
														JSON.parse(
															xhr.responseText
														).username
													);
													status.set(
														stores.Status.Success
													);
												}
												if (this.status == 404) {
													// ask for username
													status.set(
														stores.Status
															.MissingUsername
													);
												}
											}
										};
										xhr.send();
									} else {
										status.set(stores.Status.NotLoggedIn);
									}
								}
							);
						} else {
							status.set(stores.Status.CommentsEnabled);
						}
					}
				}
			};
			xhr.send();
			status.set(stores.Status.Loading);
		}
	);

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

{#if $status == stores.Status.Success}
	<InputField />
	<MessageField />
	<CommentsSection />
{:else if $status == stores.Status.CommentsEnabled}
	Comments are already Enabled
{:else if $status == stores.Status.MissingUsername}
	<ChooseUsername />
{:else if $status == stores.Status.Failed}
	<MessageField />
{:else if $status == stores.Status.NotLoggedIn}
	<LoginWithGoogle />
{:else if $status == stores.Status.Loading}
	<div class="spinner-border text-primary " role="status">
		<span class="visually-hidden">Loading...</span>
	</div>
{/if}
