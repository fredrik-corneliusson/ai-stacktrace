<script>
	import { onMount } from "svelte";
    import {PUBLIC_FASTAPI_BASE} from "$env/static/public";
    import { updateUserStore } from '../userStore'; // Import your store and function
    import { goto } from '$app/navigation';

	onMount(async () => {
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
            const res = await fetch(`${PUBLIC_FASTAPI_BASE}/get_user_info`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            const user_details = await res.json();
            localStorage.setItem('token', token);
            localStorage.setItem('user_details', JSON.stringify(user_details));
            updateUserStore(); // Update the store when localStorage changes
            console.log(user_details);
            // Navigate to the new page
            goto('/app');
            // Wait a short time before redirecting
            // setTimeout(() => {
            //     window.location.href = '/app';
            // }, 100); // 100ms delay
        }


    });
</script>

<p>Logging in...</p>
