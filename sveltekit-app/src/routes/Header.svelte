<script>
    import {page} from '$app/stores';
    import {loginStatus, updateUserStore} from './userStore';
    import {onMount} from "svelte";
    import {goto} from "$app/navigation";
    import {PUBLIC_FASTAPI_BASE} from "$env/static/public";

    onMount(async () => {
        await validateToken();
        updateUserStore();
    });

    async function validateToken() {
        // verify that token is valid, remove it from local store if it is not
        let token = localStorage.getItem("token");
        if (token !== null) {

            const res = await fetch(`${PUBLIC_FASTAPI_BASE}/get_user_info`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            // If the token is invalid, clear it and the old user_details
            if (res.status !== 200) {
                localStorage.removeItem("token");
                localStorage.removeItem("user_details");
            }
        }
    }

    // Navigate to login
    function navigateToContact() {
        goto('/contact');
    }

    function navigateToLogin() {
        goto('/login');
    }

    function navigateToLogout() {
        if (confirm("Are you sure you want to log out?")) {
            goto('/logout');
        }
    }

</script>

<header>
    <div class="corner">
    </div>

    <nav>
        <svg viewBox="0 0 2 3" aria-hidden="true">
            <path d="M0,0 L1,2 C1.5,3 1.5,3 2,3 L2,0 Z"/>
        </svg>
        <ul>
            <li aria-current={$page.url.pathname === '/' ? 'page' : undefined}>
                <a href="/">Home</a>
            </li>
            <li aria-current={$page.url.pathname.startsWith('/java') ? 'page' : undefined}>
                <a href="/java">Java</a>
            </li>
            <li aria-current={$page.url.pathname.startsWith('/python') ? 'page' : undefined}>
                <a href="/python">Python</a>
            </li>
        </ul>
        <svg viewBox="0 0 2 3" aria-hidden="true">
            <path d="M0,0 L0,3 C0.5,3 0.5,3 1,2 L2,0 Z"/>
        </svg>
    </nav>

    <div class="corner">
        <!--		<a href="https://github.com/sveltejs/kit">-->
        <!--			<img src={github} alt="GitHub" />-->
        <!--		</a>-->
    </div>

    <div class="status-info">
        {#if $loginStatus === 'Not logged in'}
            <button on:click={navigateToLogin}>{$loginStatus}</button>
        {:else}
            <button on:click={navigateToLogout}>{$loginStatus}</button>
        {/if}

    </div>
    {#if $loginStatus === 'Not logged in' && !($page.url.pathname.endsWith('/')
        || $page.url.pathname.startsWith('/contact'))}
        <div class="overlay">
            <button on:click={navigateToLogin}>Login</button>
        </div>
    {/if}
</header>

<style>

    .overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.3);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
    }

    .overlay button {
        /*font-size: x-large;*/
        border-radius: 20px;
        background: none;
        border: none;
        padding: 20px; /* Increase padding */
        color: white;
        text-decoration: underline;
        cursor: pointer;
        font-size: 2em; /* Increase font size */
    }

    header {
        display: flex;
        justify-content: space-between;
    }

    .status-info {
        position: fixed;
        top: 5px;
        right: 5px;
        background-color: white;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 20px;
    }

    .status-info button {
        background: none;
        border: none;
        padding: 0;
        cursor: pointer;
        font-size: inherit;
    }

    @media screen and (max-width: 800px) {
        .status-info {
            /*position: static;*/
            font-size: 0.8rem; /* reduce the font size */
            padding: 5px; /* reduce the padding */
            z-index: -1;
        }

        .corner {
            display: none;
        }
    }

    .corner {
        width: 5em;
        height: 5em;
    }

    .corner a {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        height: 100%;
    }

    .corner img {
        width: 2em;
        height: 2em;
        object-fit: contain;
    }

    nav {
        display: flex;
        justify-content: center;
        --background: rgba(255, 255, 255, 0.7);
    }

    svg {
        width: 2em;
        height: 3em;
        display: block;
    }

    path {
        fill: var(--background);
    }

    ul {
        position: relative;
        padding: 0;
        margin: 0;
        height: 3em;
        display: flex;
        justify-content: center;
        align-items: center;
        list-style: none;
        background: var(--background);
        background-size: contain;
    }

    li {
        position: relative;
        height: 100%;
    }

    li[aria-current='page']::before {
        --size: 6px;
        content: '';
        width: 0;
        height: 0;
        position: absolute;
        top: 0;
        left: calc(50% - var(--size));
        border: var(--size) solid transparent;
        border-top: var(--size) solid var(--color-theme-1);
    }

    nav a {
        display: flex;
        height: 100%;
        align-items: center;
        padding: 0 0.5rem;
        color: var(--color-text);
        font-weight: 700;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        text-decoration: none;
        transition: color 0.2s linear;
    }

    a:hover {
        color: var(--color-theme-1);
    }
</style>
