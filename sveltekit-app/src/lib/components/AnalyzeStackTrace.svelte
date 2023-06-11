<script>
    import {PUBLIC_WEBSOCKET} from '$env/static/public';
    export let language = "java";
    export let headerText = 'No headerText configured';

    export let descriptionText = 'No descriptionText configured';
    export let exampleTbUrl = 'Configure me, example:  /example-tb-java.txt';

    let textAreaValue = '';

    async function pasteFromClipboard() {
        textAreaValue = '';
        try {
            textAreaValue = await navigator.clipboard.readText();
        } catch (err) {
            console.error('Failed to read clipboard contents: ', err);
        }
    }

    async function loadExampleText() {
        const response = await fetch(exampleTbUrl);
        textAreaValue = await response.text();
    }

    let loading = false;
    let messageGroups = [];

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
    <h1>{@html headerText}</h1>

    <p>
        {@html descriptionText}
    </p>
    <div class="button-container">
        <button class="btn" disabled='{loading || textAreaValue.length < 10}' on:click|preventDefault={sendText} title="Run analysis">▶️ AI Analyze</button>
        <button class="btn button-as-text" disabled='{loading}' on:click={pasteFromClipboard} title="Clear and Paste Clipboard Content">📋</button>
        <button class="btn button-as-text" disabled='{loading}' on:click={() => textAreaValue = ''} title="Clear Textarea" >🗑️️</button>
        <button class="last-button" disabled='{loading}' on:click|preventDefault={loadExampleText} title="Load example">Load example</button>
    </div>
    <!--    <label for="stacktrace-area">Stacktrace</label>-->
    <textarea wrap="off" disabled='{loading}' id="stacktrace-area" bind:value={textAreaValue} rows="10" ></textarea>
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
    }

    #stacktrace-area {
        overflow-x: auto;
        margin-top: 1rem;
        width: 100%;
        box-sizing: border-box;
    }

    .button-container {
        display: flex;
        margin-top: 0.3rem;
    }


    .btn {
        margin-right: 1rem;  /* Adjust the value as needed */
    }

    .button-as-text {
        background: none;
        color: inherit;
        border: none;
        padding: 0;
        font: inherit;
        cursor: pointer;
        outline: inherit;
    }

    .last-button {
        margin-left: auto;
    }

    .analysis-result {
        font-size: large;
        border: #ffffff29;
        border-style: groove;
        padding: 1rem;
        margin-top: 1rem;
        background: #ffffff24;
    }

</style>