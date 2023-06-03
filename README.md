# ai-stacktrace
Analyze stack trace app

## TODO:
Check out this library instead for the server app:
https://github.com/ajndkr/lanarky

## Fastapi-app
`cd fastapi-app`

### create venv
`python3 -m venv venv`

### Add .env
Setup .env file:
```
OPENAI_API_KEY=...
```
### Start
```
uvicorn app:app --reload --port 9000

Debug mode:
uvicorn app:app --reload --log-level debug --port 9000

```

## Sveltekit
`cd svelte-app`

### Add .env
Setup .env file:
copy either `env.localhost` or `env.server` to `.env` depending env it runs on.

### Start
```
cd svelte-app
npm run dev -- --open
```

## AWS EC2
### Nginx routing svelte nodejs web on root and fast-api for the websocket  
`/etc/nginx/conf.d/stack.ai.conf`
See the files in linuxconf/nginx

### Start web services fastaip and sveltekit
See the files in linuxconf/systemd
`/etc/systemd/system/stack-ai-app.service`
`/etc/systemd/system/stack-ai-app-web.service`
