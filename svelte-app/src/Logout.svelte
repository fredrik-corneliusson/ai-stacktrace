<script>
    import { onMount } from "svelte";
    import {navigate} from "svelte-routing";

    onMount(() => {
        // Here you can handle the callback. For example, parse the token from the URL
        console.log("Logout");
        // Do something with the token, like storing it for future use
        localStorage.removeItem('token');
        // Navigate to /main
        navigate('/');
    });
</script>

<p>Processing...</p>
