





### nginx

- high performance web server that can act as a proxy


- Python API Development - Comprehensive Course for Beginners [see at 13:05:10]
  https://www.youtube.com/watch?v=0sOvCWFmrtA

- code repo: https://github.com/Sanjeev-Thiyagarajan/fastapi-course

- this video is about nginx configuration on EC2 Ubuntu
- install nginx and configure its default file


```json
server {
        listen 80 default_server;
        listen [::]:80 default_server;

        server_name _; # replace with specific domain name like sanjeev.com
        
        location / {
                proxy_pass http://localhost:8000;
                proxy_http_version 1.1;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header Upgrade $http_upgrade;
                proxy_set_header Connection 'upgrade';
                proxy_set_header Host $http_host;
                proxy_set_header X-NginX-Proxy true;
                proxy_redirect off;
        }

}
```