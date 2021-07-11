import App from './App.svelte';

const app = new App({
	target: document.body,
	props: {
		name: 'Comments for Youtube'
	}
});

export default app;