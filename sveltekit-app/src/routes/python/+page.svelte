<script>
    import AnalyzeStackTrace from "$lib/components/AnalyzeStackTrace.svelte";

</script>

<AnalyzeStackTrace
        language="python"
        exampleTbUrl="/example-tb-python.txt"
        headerText="Analyse Python stack-trace errors"
        descriptionText="Paste a Python stack-trace and click
        <strong>AI Analyze</strong> to provide a short summary of the error and possible solution."/>