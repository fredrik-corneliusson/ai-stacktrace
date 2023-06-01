<script>
	import { onMount } from "svelte";
    import { redirect } from '@sveltejs/kit';

	onMount(() => {
		const hashParams = window.location.hash
				.substring(1)
				.split('&')
				.reduce(function (initial, item) {
					if (item) {
						var parts = item.split('=');
						initial[parts[0]] = decodeURIComponent(parts[1]);
					}
					return initial;
				}, {});
		const token = hashParams.access_token;
		console.log("Got callback");
		console.log(token);
		// Do something with the token, like storing it for future use
		if (token) {
			localStorage.setItem('token', token);
		}
        throw redirect(307, '/app');

	});
</script>

<p>Processing...</p>
