<script>
    //const url = "https://service-user-pool-domain-dev-snoddas.auth.eu-north-1.amazoncognito.com/oauth2/authorize?client_id=5o63babfvtvtr1b3k51db2929r&response_type=token&scope=aws.cognito.signin.user.admin+email+openid+phone+profile&redirect_uri=http%3A%2F%2Flocalhost%3A8080";
    const domain = 'service-user-pool-domain-dev-snoddas.auth.eu-north-1.amazoncognito.com';
    const clientId = '5o63babfvtvtr1b3k51db2929r';
    const responseType = 'token';
    const scope = 'aws.cognito.signin.user.admin+email+openid+phone+profile';
    const redirectUri = encodeURIComponent('http://localhost:5173/callback');
    //const redirectUri = encodeURIComponent('https://stack.ai.bitflip.guru/callback');

    window.location.href = `https://${domain}/oauth2/authorize?client_id=${clientId}&response_type=${responseType}&scope=${scope}&redirect_uri=${redirectUri}`;
</script>