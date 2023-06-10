<script>
	let javaLink = '/java';
	let pythonLink = '/python';
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description"
		  content="Analyze stacktrace and provide a short summary of the error and possible solutions." />
</svelte:head>



<div class="welcome-main-column">
	<section class="hero">
		<h1>AI-Powered Stacktrace Analyzer</h1>
		<p>Turn your complex stacktraces into actionable insights.</p>
	</section>

	<section class="features">
		<h2>Why use our Stacktrace Analyzer?</h2>
		<ul>
			<li>Get concise summaries of the issues causing your stacktraces.</li>
			<li>Receive possible solutions generated using statistics and state of the art AI.</li>
		</ul>
	</section>

	<section class="cta">
		<h2>Start Analyzing Your Stacktraces Today</h2>
		<p>Select the language of your code to begin:</p>
		<div class="cta-buttons">
			<a href={javaLink} class="cta-button">Java</a>
			<a href={pythonLink} class="cta-button">Python</a>
		</div>
	</section>
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
		flex: 0.2;
		font-size: large;
	}

	.hero {
		padding: 20px;
		text-align: center;
		/*background-color: #f0f0f0;*/
	}

	.features {
		padding: 20px;
		align-content: baseline;
		background-color: #ffffff1f;
	}

	.cta {
		padding: 20px;
		align-content: start;
		text-align: left;
		background-color: #f0f0f03F;
	}

	.cta-button {
		margin: 10px;
		padding: 10px 20px;
		background-color: #008CBA; /* Change as desired */
		color: white;
		border: none;
		text-align: center;
		text-decoration: none;
		display: inline-block;
		font-size: 16px;
		transition-duration: 0.4s; /* Optional */
		cursor: pointer;
	}

	.cta-button:hover {
		background-color: #008CBA; /* Change as desired */
		color: white;
	}

	h1 {
		width: 100%;
	}

</style>
