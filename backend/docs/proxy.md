## ✅ What is Nginx Doing?

Given the `dev.conf` configuration, Nginx serves several important roles in your FastAPI + Docker Compose setup:

### 1. **Acts as a Reverse Proxy**
- Nginx forwards incoming HTTP requests from the browser to the FastAPI app container.
- Configured via:
  ```json
  proxy_pass http://app:8000;
  ```
- The service name app is resolved by Docker Compose to the FastAPI container.



### 2. **Adds Proxy Headers**

Ensures correct client headers (`Host`, `X-Real-IP`, etc.) are passed along to FastAPI.

This helps for things like:

- Knowing the client's real IP address
- Generating absolute URLs in responses
- Logging the original request details

### 3. **Serves Static Files Efficiently**

`location /static/` and `location /favicon.ico` use `alias` to directly serve static files from the FastAPI container without bothering the app.

Nginx is faster and more efficient than FastAPI for serving static files — especially in production.

### 4. **Acts as an Entry Point**

Nginx listens on port **80** on the host, so all requests to `http://localhost/` go through it first.

You can later add:

- HTTPS termination
- Rate limiting
- Load balancing
- Routing to multiple APIs/services






## Full Request Flow Breakdown

When you visit:

```json
http://localhost/
```


1. Browser → Host Machine (your development machine)
The browser makes an HTTP request to localhost:80 (default HTTP port).


2. Docker Port Mapping
Your docker-compose file for the nginx service has:
The request is routed to port 80 inside the nginx container.
```yaml
ports:
  - "80:80"
```

3. Nginx Container Handles It
Inside the container, your dev.conf handles that request:
So Nginx:
- Forwards the request to http://app:8000
- Adds appropriate headers (like Host, X-Forwarded-For)

```yaml
location / {
    proxy_pass http://app:8000;
    ...
}
```

4. Docker Compose Internal Network
Because of Docker Compose, app is a hostname Docker resolves to the container running your FastAPI app.
So Nginx talks to the app container via internal Docker network on port 8000.


```yaml
services:
  app:
    expose:
      - "8000"
```

5. FastAPI App Receives the Request
Your app running with Gunicorn+Uvicorn on port 8000 receives the request and processes it.

If everything's working, it responds with a 200 OK and your homepage (or JSON, etc.)

## summary of the request work flow

```pgsql
Browser (localhost:80)
  ↓
Docker (host port 80 → nginx container port 80)
  ↓
Nginx container
  ↓
proxy_pass → http://app:8000
  ↓
Docker internal DNS → resolves "app" to app container
  ↓
Gunicorn + FastAPI (app container, port 8000)
  ↓
Response sent back all the way to browser
```





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