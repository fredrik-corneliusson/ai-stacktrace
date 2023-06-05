# ai-stacktrace
Analyze stack trace app

## TODO:
Check out this library instead for the server app:
https://github.com/ajndkr/lanarky

## Fastapi-app
```
cd fastapi-app
# create venv
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

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
```
cd svelte-app
npm install
```

### Add .env
Setup .env file:
copy either `env.localhost` or `env.server` to `.env` depending env it runs on.

### Start
```
npm run dev -- --open
```

## AWS EC2
### Nginx routing svelte nodejs web on root and fast-api for the websocket  
`/etc/nginx/conf.d/stack.ai.conf`
See the files in linuxconf/nginx

```
sudo ln -s  $(readlink -f ./linuxconf/nginx/stack.ai.conf) /etc/nginx/conf.d/stack.ai.conf
sudo systemctl restart nginx.service
```

### Start web services fastaip and sveltekit
See the files in linuxconf/systemd
`/etc/systemd/system/stack-ai-app.service`
`/etc/systemd/system/stack-ai-app-web.service`

## Install systemd service files and start webserver daemons
```
sudo ln -s  $(readlink -f ./linuxconf/systemd/stack-ai-app.service) /etc/systemd/system/stack-ai-app.service
sudo ln -s  $(readlink -f ./linuxconf/systemd/stack-ai-app-web.service) /etc/systemd/system/stack-ai-app-web.service
sudo systemctl daemon-reload
sudo systemctl restart stack-ai-app.service stack-ai-app-web.service
```

# Follow logs

## FastApi app
```
sudo journalctl -u stack-ai-app.service -f
```

## Nginx
```
sudo tail -f /var/log/nginx/error.log /var/log/nginx/access.log
```



