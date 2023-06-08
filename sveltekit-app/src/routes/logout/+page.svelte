<script>
    import {onMount} from "svelte";
    import {updateUserStore} from '../userStore'; // Import your store and function
    import {goto} from '$app/navigation';
    import {PUBLIC_FASTAPI_BASE} from "$env/static/public";

    onMount(async () => {
        const token = localStorage.getItem('token');
        localStorage.removeItem('token');
        localStorage.removeItem('user_details');
        updateUserStore(); // Update the store when localStorage changes
        console.log("logout");
        if (token) {

            const res = await fetch(`${PUBLIC_FASTAPI_BASE}/logout`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            const result = await res.json();
            console.log(result);
        }

        // Navigate to the new page
        goto('/');

    });
</script>

<p>Logging out...</p>
