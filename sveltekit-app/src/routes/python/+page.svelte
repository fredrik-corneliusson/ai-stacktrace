<script>
    import {PUBLIC_WEBSOCKET} from '$env/static/public';

    let textAreaValue = '';

    async function loadExampleText() {
        const response = await fetch('/example-tb-python.txt');
        textAreaValue = await response.text();
    }

    let loading = false;
    let messageGroups = [];
    const language = "python";

    function sendText() {
        loading = true;
        messageGroups = [];
        const token = localStorage.getItem('token');
        let ws = new WebSocket(PUBLIC_WEBSOCKET);

        ws.onopen = function () {
            console.log('WebSocket is open now.');
            ws.send(JSON.stringify({token}));
            ws.send(language);
            ws.send(textAreaValue);

            // Set up timeout
            setTimeout(() => {
                if (messageGroups.length === 0) {
                    loading = false;
                    ws.close();
                    console.log("Timeout, no message received");
                }
            }, 30000);  // 30 seconds timeout

        };

        ws.onmessage = function (event) {
            let message = event.data;
            try {
                message = JSON.parse(event.data);
            } catch (e) {
                console.log('Error parsing websocket message to json: ', e);
                loading = false;
                return;

            }
            if (message.status === 'completed') {
                loading = false;

            } else if (message.status === 'error') {
                loading = false
                console.log(`Error: ${message}`);
                if (message.status_code === 403) {
                    console.log("Invalid token, redirecting to login");
                    localStorage.removeItem('token');
                    // Redirect to login
                    window.location.href = '/login';

                } else if (message.status_code === 413) {
                    console.log("Input to large");
                    messageGroups = [...messageGroups, {status: message.status, messages: [message]}];
                }

            } else {
                // Group messages
                if (messageGroups.length === 0 ||
                    messageGroups[messageGroups.length - 1].status !== message.status ||
                    message.status !== 'STREAMING_RESPONSE'
                ) {
                    messageGroups = [...messageGroups, {status: message.status, messages: [message]}];
                } else {
                    const lastGroup = messageGroups[messageGroups.length - 1];
                    lastGroup.messages.push(message);
                    messageGroups = [...messageGroups];
                }
            }
        };

        ws.onerror = function (error) {
            console.log(`WebSocket error: ${error}`);
            loading = false;
        };

        ws.onclose = function (event) {
            console.log(`WebSocket is closed now. ${event}`);
            loading = false;
        };
    }
</script>

<div class="stacktrace-main-column">
    <h1>Analyse Python stack-trace errors</h1>

    <p>
        Paste a Python stack-trace and click <strong>Run analysis</strong> to provide a short summary of the error and
        possible solution.
    </p>
    <!--    <label for="stacktrace-area">Stacktrace</label>-->
    <textarea disabled='{loading}' id="stacktrace-area" bind:value={textAreaValue} rows="10" cols="120"></textarea>
    <p></p>
    <div>
        <button disabled='{loading}' on:click|preventDefault={sendText}>Run analysis</button>
        <button disabled='{loading}' on:click|preventDefault={loadExampleText}>Load example</button>
    </div>
    <div class="analysis-result">
        {#each messageGroups as group, i (i)}
            <p>
                <!--{group.status}-->
                {#each group.messages as message}
                    {message.message}
                {/each}
            </p>
        {/each}
    </div>
</div>

<style>
    .stacktrace-main-column {
        display: flex;
        /*max-width: 48rem;*/
        flex: 0;
        flex-direction: column;
        justify-content: center;
        margin: 0 auto;
    }

    .analysis-result {
    }

</style>