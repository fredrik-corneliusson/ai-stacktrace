<script>
    import {onMount} from "svelte";
    import {updateUserStore} from '../userStore'; // Import your store and function
    import {goto} from '$app/navigation';

    onMount(async () => {
        localStorage.removeItem('token');
        localStorage.removeItem('user_details');
        updateUserStore(); // Update the store when localStorage changes
        console.log("logout");
        // Navigate to the new page
        goto('/');

    });
</script>

<p>Logging out...</p>
