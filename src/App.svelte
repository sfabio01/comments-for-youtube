<script>
	import InputField from "./screens/comments/components/input_field.svelte";
	import MessageField from "./common_components/message_field.svelte";
	import CommentsSection from "./screens/comments/comments_section.svelte";
	import * as stores from "./stores";
	import { uid, videoId, status, username } from "./stores";
	import ChooseUsername from "./screens/username/choose_username.svelte";
	import LoginWithGoogle from "./screens//login/login_with_google.svelte";
	import { firebaseConfig, apiKey } from "./secrets";
	import firebase from "firebase/app";
	import "firebase/auth";

	firebase.initializeApp(firebaseConfig);

	chrome.tabs.query(
		{
			active: true,
			currentWindow: true,
		},
		function ([tab]) {
			let url = tab.url;
			if (!url.startsWith("https://www.youtube.com/watch?v=")) {
				status.set(stores.Status.NotInYoutube);
				return;
			}

			videoId.set(getUrlParams(url)["v"]);
			let xhr = new XMLHttpRequest();
			xhr.open(
				"GET",
				"https://youtube.googleapis.com/youtube/v3/commentThreads?part=id&videoId=" +
					$videoId +
					"&key=" +
					apiKey
			);
			xhr.onreadystatechange = function () {
				if (this.readyState == XMLHttpRequest.DONE) {
					if (this.status == 403) {
						let res = JSON.parse(this.responseText);
						if (res.error.errors[0].reason == "commentsDisabled") {
							//Check user logged in
							var user = firebase.auth().currentUser;
							if (user) {
								stores.setUserData(user);
								uid.set(user.uid);
								if (user.displayName == "") {
									// Missing username
									status.set(stores.Status.MissingUsername);
								} else {
									username.set(user.displayName);
									status.set(stores.Status.Success);
								}
							} else {
								chrome.storage.local.get(
									"user",
									function (result) {
										if ("user" in result) {
											let user = result.user;
											stores.setUserData(user);
											uid.set(user.uid);
											if (user.displayName == "") {
												status.set(
													stores.Status
														.MissingUsername
												);
											} else {
												username.set(user.displayName);
												status.set(
													stores.Status.Success
												);
											}
										} else {
											status.set(
												stores.Status.NotLoggedIn
											);
										}
									}
								);
							}
						} else {
							status.set(stores.Status.CommentsEnabled);
						}
					} else {
						status.set(stores.Status.CommentsEnabled);
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
	<div class="alert alert-primary d-flex align-items-center" role="alert">
		<svg
			xmlns="http://www.w3.org/2000/svg"
			width="24"
			height="24"
			fill="currentColor"
			class="bi bi-exclamation-triangle-fill flex-shrink-0 me-2"
			viewBox="0 0 16 16"
			role="img"
			aria-label="Warning:"
		>
			<path
				d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"
			/>
		</svg>
		<div>Comments for this video are already enabled</div>
	</div>
{:else if $status == stores.Status.MissingUsername}
	<ChooseUsername />
{:else if $status == stores.Status.Failed}
	<MessageField />
{:else if $status == stores.Status.NotLoggedIn}
	<LoginWithGoogle />
{:else if $status == stores.Status.NotInYoutube}
	<div class="alert alert-primary d-flex align-items-center" role="alert">
		<svg
			xmlns="http://www.w3.org/2000/svg"
			width="24"
			height="24"
			fill="currentColor"
			class="bi bi-exclamation-triangle-fill flex-shrink-0 me-2"
			viewBox="0 0 16 16"
			role="img"
			aria-label="Warning:"
		>
			<path
				d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"
			/>
		</svg>
		<div>Open a Youtube video in order to use this extension</div>
	</div>
{:else if $status == stores.Status.Loading}
	<div
		class="d-flex justify-content-center align-items-center"
		style="height: 600px;"
	>
		<div class="spinner-border text-primary" role="status">
			<span class="visually-hidden">Loading...</span>
		</div>
	</div>
{/if}
