<script>
	import InputField from "./components/input_field.svelte";
	import MessageField from "./components/message_field.svelte";
	import CommentsSection from "./components/comments_section.svelte";
	import LoadMoreButton from "./components/load_more_button.svelte";

	let uid = "";
	let msg = "";
	chrome.identity.getProfileUserInfo(function (infos) {
		uid = infos.id;
		if (uid == "") {
			// user not signed in
			msg = "You are not signed in";
		} else {
		}
	});
</script>

<InputField />
<MessageField {msg} />
<CommentsSection />
<LoadMoreButton />

<style>
</style>
