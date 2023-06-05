<script>
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description"
		  content="Analyze stacktrace and provide a short summary of the error and possible solutions." />
</svelte:head>

<div class="welcome-main-column">
	<h1>
			AI Stacktrace analyzer
	</h1>
	<div>
		Analyze stacktrace and provide a short summary of the error and possible solutions.
	</div>
</div>

<style>

	.welcome-main-column {
		display: flex;
		/*max-width: 48rem;*/
		flex: 0.1;
		flex-direction: column;
		justify-content: center;
		margin: 0 auto;
	}

	section {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		flex: 0.6;
	}

	h1 {
		width: 100%;
	}

</style>
