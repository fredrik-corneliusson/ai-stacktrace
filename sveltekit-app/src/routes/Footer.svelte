<script>
    let linkedin = 'https://www.linkedin.com/in/fredrik-corneliusson/';
    let twitter = 'https://twitter.com/FredCornel';
    let user = 'bitflip.guru';
    let domain = 'proton';
    let tld = 'me';
    let year = new Date().getFullYear();
</script>

<footer>
    <div>

        <a href={linkedin} target="_blank" rel="noopener noreferrer">
            <i class="fab fa-linkedin fa-2x"></i>
        </a>
    </div>
    <a href={twitter} target="_blank" rel="noopener noreferrer">
        <i class="fab fa-twitter fa-2x"></i>
    </a>
    <a href="mailto:{user}@{domain}.{tld}">
        <i class="fas fa-envelope fa-2x"></i>
    </a>
    <a href="/contact">bitflip.guru | Contact</a>
    <div class="copyright">
        &copy; {year} Fredrik Corneliusson. All rights reserved.
    </div>
</footer>

<style>
    footer {
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: center;
        padding: 12px;
        margin: 10px;
        z-index: 2000;
    }

    footer a {
        font-weight: inherit;
        color: #3498db;
        margin: 0.5rem;
    }


</style>
