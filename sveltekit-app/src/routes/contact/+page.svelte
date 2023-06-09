<script>
    import {PUBLIC_FASTAPI_BASE} from "$env/static/public";

    let name = "";
    let email = "";
    let message = "";

    const handleSubmit = async () => {
        const response = await fetch(`${PUBLIC_FASTAPI_BASE}/send-email`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, message })
        });

        if (response.ok) {
            console.log("email sent ok", response)
            // Handle successful email sending (maybe display a success message)
        } else {
            console.log("failed to send email", response)
            // Handle error
        }
    };
</script>


<form on:submit|preventDefault={handleSubmit}>
    <label>
        Name:
        <input type="text" bind:value={name} required>
    </label>
    <label>
        Email:
        <input type="email" bind:value={email} required>
    </label>
    <label>
        Message:
        <textarea bind:value={message} required></textarea>
    </label>
    <button type="submit">Send</button>
</form>