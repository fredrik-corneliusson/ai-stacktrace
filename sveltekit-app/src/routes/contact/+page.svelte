<script>
    let linkedin = 'https://www.linkedin.com/in/fredrik-corneliusson/';
    let twitter = 'https://twitter.com/FredCornel';
    let user = 'bitflip.guru';
    let domain = 'proton';
    let tld = 'me';
</script>

<svelte:head>
    <title>About</title>
    <meta name="description" content="About this app" />
</svelte:head>

<div class="text-column">
    <h1>Contact</h1>

    <p>
        Hello there! I'm Fredrik Corneliusson, a passionate software developer with a deep interest in the endless possibilities of Artificial Intelligence.
    </p>
    <p>
        <strong>bitflip.guru</strong> is my corner of the web where I share my experiments with AI technologies.
        My goal is to provide valuable resources for others and create interactions around this fascinating field. By doing so, I continue to expand my knowledge and experience.
    </p>
    <p>
        If you share the same passion for AI or find my experiments intriguing, I would be delighted to hear from you.
        Maybe you have thoughts to share, wish to collaborate on a project, or simply want to discuss AI and its potential - feel free to reach out.
    </p>
    <p>
        You can contact me on <a href={linkedin} target="_blank" rel="noopener noreferrer">LinkedIn</a>
        or <a href={twitter} target="_blank" rel="noopener noreferrer">Twitter</a> for a more casual conversation.
        Alternatively, if you prefer to send an email, you can reach me at {user}@{domain}.{tld}.
    </p>
    <p>
        Although I'm currently working in software development, I'm always interested in exploring new opportunities and challenges related to AI, whether they be projects, partnerships, or consulting engagements.
    </p>
    <p>
        Looking forward to connecting with you!
    </p>

</div>
