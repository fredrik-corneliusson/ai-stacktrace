<script>
	import Spinner from './Spinner.svelte';

	let textAreaValue = '';

	async function loadExampleText() {
		const response = await fetch('/example.txt');
		textAreaValue = await response.text();
	}

	let loading = false;
	let messages = [];
	let messageGroups = [];

	function sendText() {
		loading = true;
		messages = [];
		const token = localStorage.getItem('token');
		let ws = new WebSocket('ws://localhost:8000/ws');
		//let ws = new WebSocket('wss://stack.ai.bitflip.guru/ws/');

		ws.onopen = function() {
			console.log('WebSocket is open now.');
			ws.send(JSON.stringify({ token }));
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
			let message = event.data;
			try {
				message = JSON.parse(event.data);
				if(message.status === 'completed') {
					loading = false;

				} else if(message.status === 'error') {
					loading = false
					console.log("Error: ${message.status_code} ${message.message}");
					if (message.status_code === 403) {
						console.log("Invalid token, redirecting to login");
						localStorage.removeItem('token');
						// TODO: Update to work in sveltekit
						navigate('/login');

					}
				} else {
					messages = [...messages, message];
					// Group messages
					if (messageGroups.length === 0 ||
							messageGroups[messageGroups.length - 1].status !== message.status ||
							message.status !== 'STREAMING_RESPONSE') {
						messageGroups = [...messageGroups, { status: message.status, messages: [message] }];
					} else {
						const lastGroup = messageGroups[messageGroups.length - 1];
						lastGroup.messages.push(message);
						messageGroups = [...messageGroups];
					}
				}
			} catch(error) {
				// Not a JSON message, treat it as a regular text message
				// messages = [...messages, message];
				loading = false;

			}
		};

		ws.onerror = function(error) {
			console.log(`WebSocket error: ${error}`);
		};

		ws.onclose = function(event) {
			console.log(`WebSocket is closed now. ${event}`);
		};
	}
</script>

<textarea bind:value={textAreaValue} rows="10" cols="120"></textarea>
<p></p>
<button on:click={sendText}>Send Text</button>
<button on:click={loadExampleText}>Load example text</button>

{#if loading}
	<Spinner></Spinner>
{/if}

{#each messageGroups as group, i (i)}
	<p>
		<!--{group.status}-->
		{#each group.messages as message}
			{message.message}
		{/each}
	</p>
{/each}