<script>
    import Spinner from './Spinner.svelte';
    let textAreaValue = '';

    async function loadExampleText() {
        const response = await fetch('/example.txt');
        const text = await response.text();
        textAreaValue = text;
    }

    let loading = false;
    let messages = [];

    function sendText() {
        loading = true;
        messages = [];
        //let ws = new WebSocket('ws://localhost:8000/ws');
        let ws = new WebSocket('wss://stack.ai.bitflip.guru/ws/');

        ws.onopen = function() {
            console.log('WebSocket is open now.');
            ws.send(textAreaValue);

            // Set up timeout
            setTimeout(() => {
                if (messages.length === 0) {
                    loading = false;
                    ws.close();
                    console.log("Timeout, no message received");
                    messages.push({ status: "error", message: "Timeout, no message received" });
                }
            }, 40000);  // 30 seconds timeout

        };

        ws.onmessage = function(event) {
            let data = event.data;
            try {
                data = JSON.parse(event.data);
                if(data.status === 'completed') {
                    loading = false;
                    return;
                } else {
                    messages = [...messages, data];
                }
            } catch(error) {
                // Not a JSON message, treat it as a regular text message
                // messages = [...messages, data];
                loading = false;
                return;
            }
        };

        ws.onerror = function(error) {
            console.log(`WebSocket error: ${error}`);
        };

        ws.onclose = function(event) {
            console.log('WebSocket is closed now.');
        };
    }
</script>

<textarea bind:value={textAreaValue} rows="10" cols="120"></textarea>
<p/>
<button on:click={sendText}>Send Text</button>
<button on:click={loadExampleText}>Load example text</button>

{#if loading}
    <Spinner />
{/if}
{#each messages as message, i (i)}
    <p>{message.stage} - {message.message}</p>
{/each}
