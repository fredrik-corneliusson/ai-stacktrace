<script>
    import { onMount } from "svelte";

    onMount(() => {
        // Here you can handle the callback. For example, parse the token from the URL
        const urlParams = new URLSearchParams(window.location.hash);
        const token = urlParams.get("#access_token");
        console.log("Got callback");
        console.log(token);
        // Do something with the token, like storing it for future use
    });
</script>

<p>Processing...</p>
