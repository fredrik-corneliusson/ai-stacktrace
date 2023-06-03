<script>
    import {onMount} from "svelte";
    import { PUBLIC_BASE_URL  } from '$env/static/public';

    onMount(() => {

        const domain = 'service-user-pool-domain-dev-snoddas.auth.eu-north-1.amazoncognito.com';
        const clientId = '5o63babfvtvtr1b3k51db2929r';
        const responseType = 'token';
        const scope = 'aws.cognito.signin.user.admin+email+openid+phone+profile';
        const redirectUri = encodeURIComponent(`${PUBLIC_BASE_URL}/callback`);
        console.log(redirectUri)

        window.location.href = `https://${domain}/oauth2/authorize?client_id=${clientId}&response_type=${responseType}&scope=${scope}&redirect_uri=${redirectUri}`;
    });

</script>
