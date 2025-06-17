








#### Project structure

```
Root-dir
     |
     |- backend 
            |- `requirements.txt` (file)
            |-  `.dockerignore` (file)
            |-  `main.py` (file, entry point)
            |-  `database` (dir)
                  |- `local.db` (local testing)
                  |- `.py`  (database connection file)
                  |- `prod.db`(`prod testing`)
            |- `models` (dir)
            |-  `test`  (dir)
            |- `routers` (dir)
                  |_ `*.py` (all endpoints)
            |-  `scripts` (dir)
                  |_ `*.sh` 
            |-  `alembic` (for data migration)
            |-  `.venv` (python virtual environment)
      |
      |-frontend
            |- `static` (Frontend dir)
                  |- `css` (dir)
                        |-  `*.css`
                  |- `js`   (dir)
                        |_ `*.js` 
            |-  `templates` (frontend dir)
                  |_ `*.html`
      |- `README.md` (file)
      |-   `.gitignore` 
```

### Endpoints FrontEnd and Backend

```
admin.py
(BE) GET         /admin/user              -  Read all Users
(BE) DELETE      /admin/{username}        - delete a user by username
(BE) GET         /admin/todo              - delete all todo

auth.py
(BE) GET        /login                   - Get a token of an existing user
(FE) GET        /register-page            - Render register page
(FE) GET        /login-page               - Render login page

todos.py
(BE) GET          /todos/                         - Read all Todos of a user
(BE) GET          /todos/{todo_id}                - Read Todo by ID of a user
(BE) POST         /todos/todos                   - Create a new todos of a user
(BE) PUT          /todos/todo/{todo_id}          - Update an existing todo of a user
(BE) DELETE       /todos/todo/{todo_id}        - Delete an existing todo of a user
(FE) GET          /todo-page                      - Render Todo page
(FE) GET          /add-todo-page                  - Render Add Todo page
(FE) GET          /edit-todo-page/{todo_id}       - Render Edit Todo page

users.py
(BE) GET          /user/                         -  get user
(BE) POST         /user/register                  - register a user
(BE) PUT          /user/password                   - change password
(BE) PUT          /user/phonenumber/{phone_number} - change phone number

health.py
(BE) GET         /health                  - check system status
```


#### notes

### Backend Engineering
- CRUD operations
- Query String, Path Parameters

#### Data Validation
- Input Request Validation using `typing` and `pydantic`
- Input Request example using `model_config`
- Path Parameter Validation using `Path`
- Query Parameter Validation using `Query`

#### Status Code/HTTP Exception
-  `HTTPException`, `status`

#### Database

- `SQLAlchemy`, `sqlite`


#### Auth and Authorization

- `jwt`


### Clean architecture

- `database.py` : stores database connection string, database
- `models.py`   : stores info about tables of databases, PK, FK, Columns of tables 
- `main.py`  : entry point of an application

### Database 

- `alembic` (data migration tool)
- `MySQL` , `PostgreSQL` , `sqlite`


### Testing, CI/CD

- Unit Testing
- Integration Testing
- CI/CD using gitlab, 
- GitHub Actions
- MLOps
- DevSecOps

### Debugging
- python tools to debug code


### Front-end 
- Full-stack application development

### Optimization, performance improvements

- Asyncronouse programming/Concurrency
- Caching
- Database indexing

### Security 
 - `OAuth2` 
 - Authentication & Authorization


### Scalability, Fault-tolerance, reliability
 - Load balancing, Nginx
 - Autoscaling infrastructure.
 - Rate limit
 - Rate limiting and throttling.
 - Exception/Error Handling
 - health-check

### Interaction patterns

- HTTP/HTTPS
- GraphQL
- WebSocket
- gRPC


### Real-time Streaming


### Deployment

- Docker/Docker compose
- Kubernates
- Deployment to AWS Infrastructure, as lambda, ECS
- IaC, Terraform, CDK, Serverless
- CDN 


### AI/ML

- Machine learning + Python
- GenAI

### Monitoring and obeservation

- DataDog
- X-ray

### Real-time data handling
- Stream processing
- video, audio
-  handling real-time streaming application
- Stream Analytics


### Questions to be explore

-  pydantic?
- starlett?
-  poetry?

### other architecture
- Concurrency and idempotency.
- Job scheduling and cron systems.
- Events, message queues, and workers.
- Clean Architecture
- architecture pattern
