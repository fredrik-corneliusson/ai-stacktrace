<script>
    import AnalyzeStackTrace from "$lib/components/AnalyzeStackTrace.svelte";

</script>

<AnalyzeStackTrace
        language="java"
        exampleTbUrl="/example-tb-java.txt"
        headerText="Analyse Java stack-trace errors"
        descriptionText="Paste a Java stack-trace and click
        <strong>AI Analyze</strong> to provide a short summary of the error and possible solution."/>