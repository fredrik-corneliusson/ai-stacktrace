# ai-stacktrace
Analyze stack trace app


## Add .env
Setup .env file:
```
OPENAI_API_KEY=...
```

## start fastapi
```
uvicorn app:app --reload
```

## start svelte
```
cd svelte-app
npm run dev
```

## AWS EC2
Nginx routing svelte nodejs web on root and fast-api for the websocket  
(venv) [ec2-user@ip-172-31-6-210 ai-stacktrace]$ sudo cat /etc/nginx/conf.d/stack.ai.conf
```
server {
    listen 80;
    server_name stack.ai.bitflip.guru;
    access_log  /var/log/nginx/access.log;
    error_log  /var/log/nginx/error.log;
    location / {
        proxy_pass http://127.0.0.1:8080;
        auth_basic "Restricted Access";
        auth_basic_user_file /etc/nginx/passwords;
        #proxy_buffering off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /ws/ {
        proxy_pass http://127.0.0.1:9000/ws;
        proxy_http_version 1.1;
        proxy_buffering off;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

(venv) [ec2-user@ip-172-31-6-210 ai-stacktrace]$ sudo cat /etc/systemd/system/stack-ai-app.service
```
[Unit]
Description=Uvicorn daemon to serve stack-ai analysis fastapi app
After=network.target
[Service]
User=ec2-user
Group=ec2-user
WorkingDirectory=/home/ec2-user/projects/ai-stacktrace
ExecStart=/home/ec2-user/projects/ai-stacktrace/venv/bin/uvicorn app:app --host 0.0.0.0 --port 9000
[Install]
WantedBy=multi-user.target
```

Start svelte webservice:
```
[ec2-user@ip-172-31-6-210 svelte-app]$ sudo cat /etc/systemd/system/stack-ai-app-web.service
[Unit]
Description=Svelte web server for stack-ai analysis
After=network.target
[Service]
User=ec2-user
Group=ec2-user
WorkingDirectory=/home/ec2-user/projects/ai-stacktrace/svelte-app
ExecStart=/home/ec2-user/projects/ai-stacktrace/svelte-app/start.sh
[Install]
WantedBy=multi-user.target
```

